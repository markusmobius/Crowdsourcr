import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime
import os
import uuid
import pymongo
import Settings
import models
import controllers
import json
 
from tornado.options import define, options
 
class BaseHandler(tornado.web.RequestHandler):
    __superusers__ = ['samgrondahl@gmail.com', 'kmill31415@gmail.com']
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
    @property
    def cdocument_controller(self):
        return controllers.CDocumentController(self.db)
    @property
    def xmltask_controller(self):
        return controllers.XMLTaskController(self.db)
    @property
    def cresponse_controller(self):
        return controllers.CResponseController(self.db)
    @property
    def mturkconnection_controller(self):
        return controllers.MTurkConnectionController(self.db)
    def is_super_admin(self):
        admin_email = self.get_secure_cookie('admin_email')
        return admin_email in self.__superusers__
    def get_current_admin(self):
        admin = self.admin_controller.get_by_email(self.get_secure_cookie("admin_email"))
    def return_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.finish(tornado.escape.json_encode(data))

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")

# Doesn't appear to be used (instead using GoogleLoginHandler)
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

class AdminRemoveHandler(BaseHandler) :
    def post(self):
        if self.is_super_admin():
            self.admin_controller.remove(json.loads(self.get_argument("data", "{}")))
            self.return_json({"success" : True})
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
               full_name = " ".join(u for u in [user['first_name'], user['last_name']]
                                    if u != None)
               self.set_secure_cookie('admin_email', user['email'])
               self.set_secure_cookie('admin_name', full_name)
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
        if not self.request.files :
            self.return_json({'error' : "Error: No file selected."});
            return
        try :
            with open(os.path.join(Settings.TMP_PATH, uuid.uuid4().hex + '.upload'), 'wb') as temp:
                temp.write(self.request.files['file'][0]['body'])
                temp.flush()
                xmltask = self.xmltask_controller.xml_upload(temp.name)
                for module in xmltask.get_modules():
                    self.ctype_controller.create(module)
                for task in xmltask.get_tasks():
                    self.ctask_controller.create(task)
                for hit in xmltask.get_hits():
                    self.chit_controller.create(hit)
                for name, doc in xmltask.docs.iteritems():
                    self.cdocument_controller.create(name, doc)
            self.return_json({'success' : True})
        except Exception as x :
            self.return_json({'error' : type(x).__name__ + ": " + str(x)})

class DocumentViewHandler(BaseHandler):
    def get(self, name):
        try :
            self.finish(self.cdocument_controller.get_document_by_name(name))
        except :
            raise tornado.web.HTTPError(404)

class RecruitingBeginHandler(BaseHandler):
    def post(self):
        admin_email = self.get_secure_cookie('admin_email')
        max_assignments = self.chit_controller.get_agg_hit_info()['num_total']
        if admin_email:
            self.mturkconnection_controller.begin_run(admin_email, max_assignments)
        self.finish()

class RecruitingEndHandler(BaseHandler):
    def post(self):
        admin_email = self.get_secure_cookie('admin_email')
        self.mturkconnection_controller.end_run(admin_email)
        self.finish()

class RecruitingInfoHandler(BaseHandler):
    def post(self):
        admin_email = self.get_secure_cookie('admin_email')
        if admin_email:
            recruiting_info = json.loads(self.get_argument('data', '{}'))
            recruiting_info['email'] = admin_email
            mtconn = self.mturkconnection_controller.create(recruiting_info)
        self.finish()

class AdminInfoHandler(BaseHandler):
    def get(self):
        admin_email = self.get_secure_cookie('admin_email')
        if not admin_email:
            self.return_json({'authed' : False, 'reason' : 'no_login'})
        if not self.admin_controller.get_by_email(admin_email):
            self.return_json({'authed' : False, 'reason' : 'not_admin'})
        else :
            turk_conn = self.mturkconnection_controller.get_by_email(admin_email)
            turk_info = False 
            turk_balance = False
            if turk_conn:
                turk_info = turk_conn.serialize()
                turk_balance = (turk_conn.get_balance() or [0])[0]
                ensure_automatic_make_payments(self.mturkconnection_controller,
                                               admin_email)
            
            self.return_json({'authed' : True,
                              'email' : self.get_secure_cookie('admin_email'),
                              'full_name' : self.get_secure_cookie('admin_name'),
                              'hitinfo' : self.chit_controller.get_agg_hit_info(),
                              'turkinfo' : turk_info,
                              'turkbalance' : str(turk_balance)})

class AdminHitInfoHandler(BaseHandler):
    def get(self, id=None) :
        admin_email = self.get_secure_cookie('admin_email')
        if admin_email and self.admin_controller.get_by_email(admin_email):
            if id == None :
                ids = self.chit_controller.get_chit_ids()
                self.return_json({'ids' : ids})
            else :
                chit = self.chit_controller.get_chit_by_id(id)
                self.return_json({'tasks' : chit.tasks})
        else :
            self.return_json({'authed' : False})

class AdminTaskInfoHandler(BaseHandler):
    def get(self, tid) :
        admin_email = self.get_secure_cookie('admin_email')
        if admin_email and self.admin_controller.get_by_email(admin_email):
            task = self.ctask_controller.get_task_by_id(tid)
            self.return_json(task.serialize())
        else :
            self.return_json(False)


PERIODIC_PAYERS = {} # admin_email -> payer
def ensure_automatic_make_payments(mturk_controller, admin_email) :
    """Adds an automatic payer to the ioloop if one does not already
    exist for the particular admin."""
    def _ensure() :
        if admin_email not in PERIODIC_PAYERS :
            Settings.logging.info("Adding periodic payer for " + admin_email)
            def callback() :
                try :
                    mturk_controller.make_payments(admin_email)
                except :
                    Settings.logging.exception("Error in automatic payer for " + admin_email)
                    pc.stop()
            callback_time = 1000 * 10 # 10 seconds
            pc = tornado.ioloop.PeriodicCallback(callback, callback_time)
            PERIODIC_PAYERS[admin_email] = pc
            pc.start()
    # run this from the main ioloop just in case we have multiple threads
    tornado.ioloop.IOLoop.instance().add_callback(_ensure)

class WorkerLoginHandler(BaseHandler):
    def post(self):
        self.set_secure_cookie('workerid', self.get_argument('workerid', ''))
        self.finish()

class CHITViewHandler(BaseHandler):
    def post(self):
        forced = False
        hitid = self.get_secure_cookie('hitid')
        workerid = self.get_secure_cookie('workerid')
        taskindex = self.get_secure_cookie('taskindex')
        if self.get_argument('force', False) :
            forced = True
            hitid = self.get_argument('hitid', None)
            self.set_secure_cookie('hitid', hitid)
            workerid = self.get_argument('workerid', None)
            self.set_secure_cookie('workerid', workerid)
            taskindex = '0'
            self.set_secure_cookie('taskindex', taskindex)
        if not workerid:
            if forced :
                self.return_json({'needs_login' : True, 'reforce' : True})
            elif self.chit_controller.get_next_chit_id() == None :
                self.return_json({'no_hits' : True})
            else:
                self.return_json({'needs_login' : True})
        elif not hitid or not taskindex:
            next = self.chit_controller.get_next_chit_id()
            if next == None :
                self.clear_all_cookies()
                self.return_json({'no_hits' : True})
            else :
                self.set_secure_cookie('hitid', self.chit_controller.get_next_chit_id())
                self.set_secure_cookie('taskindex', '0')
                self.return_json({'reload_for_first_task':True})
        else:
            taskindex = int(taskindex)
            chit = self.chit_controller.get_chit_by_id(hitid)
            if taskindex >= len(chit.tasks):
                self.clear_all_cookies()
                completed_chit_info = self.chit_controller.add_completed_hit(chit=chit, worker_id=workerid)
                self.return_json({'completed_hit':True,
                                  'verify_code' : completed_chit_info['turk_verify_code']})
            else:
                task = self.ctask_controller.get_task_by_id(chit.tasks[taskindex])
                self.return_json({"task" : task.serialize(),
                                  "task_num" : taskindex,
                                  "num_tasks" : len(chit.tasks)})

class CResponseHandler(BaseHandler):
    def post(self):
        worker_id = self.get_secure_cookie('workerid')
        task_index = int(self.get_secure_cookie('taskindex'))
        print "***",task_index
        chit = self.chit_controller.get_chit_by_id(self.get_secure_cookie('hitid'))
        taskid = chit.tasks[task_index]
        responses = json.loads(self.get_argument('data', '{}'))
        self.cresponse_controller.create({'submitted' : datetime.datetime.utcnow(),
                                          'response' : responses,
                                          'workerid' : worker_id,
                                          'hitid' : chit.hitid,
                                          'taskid' : taskid})
        self.set_secure_cookie('taskindex', str(task_index + 1))
        self.finish()

class CSVDownloadHandler(BaseHandler):
    def get(self):
        self.set_header ('Content-Type', 'text/csv')
        self.set_header ('Content-Disposition', 'attachment; filename=data.csv')
        for row in self.cresponse_controller.write_response_to_csv():
            self.write("%s\n" % row)
        self.finish()
