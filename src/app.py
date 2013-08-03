import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import handlers
import pymongo
import uuid
import base64
import hashlib
import Settings
import os
 
from tornado.options import define, options
 
define('port', default=8888, help="run on the given port", type=int)

def random256() :
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
 
class Application(tornado.web.Application):
    def __init__(self):
        self.db = pymongo.Connection()['news_crowdsourcing']
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "cookie_secret": Settings.COOKIE_SECRET,
            "login_url": "/auth/login/"
        }

        app_handlers = [
            (r'/', handlers.MainHandler),
            (r'/types/()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='types.html')),
            (r'/types/new', handlers.CTypeCreateHandler),
            (r'/types/all', handlers.CTypeAllHandler),
            (r'/types/view/(.*)', handlers.CTypeViewHandler),
            (r'/admin/', handlers.GoogleLoginHandler),
            (r'/admin/all', handlers.AdminAllHandler),
            (r'/admin/new', handlers.AdminCreateHandler),
            (r'/superadmin/()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='superadmin.html')),
        ]
        tornado.web.Application.__init__(self, app_handlers, **settings)
 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()
