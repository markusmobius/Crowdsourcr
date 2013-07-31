import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
import models
import json
 
from tornado.options import define, options
 
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self) :
        return self.application.db
    @property
    def ctype_controller(self):
        return models.CTypeController(self.db)
    @property
    def ctask_controller(self):
        return models.CTaskController(self.db)
    def get_current_user(self):
        return self.get_secure_cookie("user")
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
        ctasks = self.ctask_controller.get_names(type_name)
        ctype_info['tasks'] = ctasks
        self.return_json(ctype_info)
        
class AllTypeStaticHandler(BaseHandler):
    def get(self):
        self.render("types.html")

class TypeViewStaticHandler(BaseHandler):
    def get(self, *args):
        self.render("type_view.html")

class CTypeAllHandler(BaseHandler):
    def get(self):
        self.return_json(self.ctype_controller.get_names())

class CTypeCreateHandler(BaseHandler):
    def post(self):
        ctype = self.ctype_controller.create(json.loads(self.get_argument("ctype")))

class CTaskViewHandler(BaseHandler):
    def get(self):
        self.return_json(self.ctask_controller.get_by_name('', ''))
