import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import models
import controllers
import json
 
from tornado.options import define, options
 
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self) :
        return self.application.db
    @property
    def ctype_controller(self):
        return controllers.CTypeController(self.db)
    @property
    def ctask_controller(self):
        return controllers.CTaskController(self.db)
    @property
    def admin_controller(self) :
        return controllers.AdminController(self.db)
    @property
    def chit_controller(self):
        return controllers.CHITController(self.db)
    def is_super_admin(self):
        return self.get_secure_cookie('admin_email') == 'samgrondahl@gmail.com'
    def get_current_admin(self):
        admin = self.admin_controller.get_by_email(self.get_secure_cookie("admin_email"))
    def return_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.finish(tornado.escape.json_encode(data))

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html", username='Sam')

class AuthLoginHandler(BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", errormessage = errormessage)
 
    def check_permission(self, password, username):
        if username == "admin" and password == "admin":
            return True
        return False
 
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
 
class CTypeViewHandler(BaseHandler):
    def get(self, type_name):
        ctype_info = self.ctype_controller.get_by_name(type_name).to_dict()
        self.return_json(ctype_info)

class CTypeAllHandler(BaseHandler):
    def get(self):
        self.return_json(self.ctype_controller.get_names())

class CTypeCreateHandler(BaseHandler):
    def post(self):
        ctype = self.ctype_controller.create(json.loads(self.get_argument("ctype", "{}")))

class CTaskViewHandler(BaseHandler):
    def get(self):
        self.return_json(self.ctask_controller.get_by_name('', ''))

class AdminCreateHandler(BaseHandler) :
    def post(self):
        if self.is_super_admin():
            admin = self.admin_controller.create(json.loads(self.get_argument("data", "{}")))
            self.return_json(admin.to_dict())
        else:
            self.write("error: unauthorized")

class AdminAllHandler(BaseHandler) :
    def get(self):
        if self.is_super_admin():
            self.return_json(self.admin_controller.get_emails())
        else:
            self.write("error")

class GoogleLoginHandler(BaseHandler,
                         tornado.auth.GoogleMixin):
   @tornado.web.asynchronous
   @tornado.gen.coroutine
   def get(self):
       if self.admin_controller.get_by_email(self.get_secure_cookie('admin_email', '')):
           self.redirect('/admin/')
       elif self.get_argument("openid.mode", None):
           try:
               user = yield self.get_authenticated_user()
               # {'first_name': u'Sam', 'claimed_id': u'https://www.google.com/accounts/o8/id?id=AItOawkwMPsQnRxJcwHuqpxj5CaCSZ9mhkKMkPQ', 'name': u'Sam Grondahl', 'locale': u'en', 'last_name': u'Grondahl', 'email': u'samgrondahl@gmail.com'}
               self.set_secure_cookie('admin_email', user['email'])
               self.redirect('/admin/')
           except tornado.auth.AuthError as e:
               self.write('you did not auth!')
           except Exception as e:
               print type(e)
               print 'Unexpected error: ' + e
       else:
           self.clear_cookie('admin_email')
           yield self.authenticate_redirect()

class XMLUploadHandler(BaseHandler):
    def post(self):
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile() as temp:
            temp.write(self.request.files['file'][0]['body'])
            temp.flush()
            xmltask = controllers.XMLTaskController.xml_upload(temp.name)
            for module in xmltask.get_modules():
                self.ctype_controller.create(module)
            for task in xmltask.get_tasks():
                self.ctask_controller.create(task)
            for hit in xmltask.get_hits():
                self.chit_controller.create(hit)
        self.return_json({'success' : True})

class AdminInfoHandler(BaseHandler):
    def get(self):
        if (self.admin_controller.get_by_email(self.get_secure_cookie('admin_email'))):
            self.finish('Logged in as ' + self.get_secure_cookie('admin_email'))
        else:
            self.finish('Not logged in, <a href="/admin/login/">login here</a>.')

class CHITViewHandler(BaseHandler):
    def get(self):
        if not self.get_secure_cookie('hitid') or not self.get_secure_cookie('taskindex'):
            self.set_secure_cookie('hitid', self.chit_controller.get_next_chit_id())
            self.set_secure_cookie('taskindex', '0')
            self.return_json({'reload_for_first_task':True})
        else:
            task_index = int(self.get_secure_cookie('taskindex'))
            chit = self.chit_controller.get_chit_by_id(self.get_secure_cookie('hitid'))
            if task_index >= len(chit.tasks):
                self.return_json({'completed_hit':True})
            else:
                task = self.ctask_controller.get_task_by_id(chit.tasks[task_index])
                self.return_json(task.serialize())

class CResponseHandler(BaseHandler):
    def post(self):
        task_index = int(self.get_secure_cookie('taskindex'))
        hitid = self.get_secure_cookie('hitid')
        responses = json.loads(self.get_argument('data', '{}'))
        print responses
        self.set_secure_cookie('taskindex', str(task_index + 1))
        self.return_json({'completed_hit' : False})
