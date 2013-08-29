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
import sys

from tornado.options import define, options
 
define('port', default=8080, help="run on the given port", type=int)
define('environment', default="development", help="server environment", type=str)
define('drop', default="", help="pass REALLYREALLY to drop the db", type=str)

def random256() :
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
 
class Application(tornado.web.Application):
    def __init__(self, environment, drop):
        self.db = pymongo.Connection()['news_crowdsourcing']
        if drop == "REALLYREALLY" :
            clear_db(self.db)
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "cookie_secret": Settings.COOKIE_SECRET,
            "root_path": Settings.ROOT_PATH,
            "login_url": "/auth/login/",
            "environment" : environment
        }

        app_handlers = [
            (r'/', handlers.MainHandler),
            (r'/help/?()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='help.html')),
            (r'/help/(README.md)', tornado.web.StaticFileHandler, dict(path=settings['root_path'], default_filename='README.md')),
#            (r'/types/?()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='types.html')),
#            (r'/types/new/?', handlers.CTypeCreateHandler),
#            (r'/types/all/?', handlers.CTypeAllHandler),
            (r'/types/view/(.*)', handlers.CTypeViewHandler),
            (r'/admin/?()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='admin.html')),
            (r'/admin/login/?', handlers.GoogleLoginHandler),
            (r'/admin/download/?', handlers.CSVDownloadHandler),
            (r'/admin/recruit/?', handlers.RecruitingInfoHandler),
            (r'/admin/recruit/end/?', handlers.RecruitingEndHandler),
            (r'/admin/recruit/begin/?', handlers.RecruitingBeginHandler),
            (r'/admin/all/?', handlers.AdminAllHandler),
            (r'/admin/new/?', handlers.AdminCreateHandler),
            (r'/admin/remove/?', handlers.AdminRemoveHandler),
            (r'/admin/info/?', handlers.AdminInfoHandler),
            (r'/admin/hits/?', handlers.AdminHitInfoHandler),
            (r'/admin/hits/(.+)', handlers.AdminHitInfoHandler),
            (r'/admin/tasks/(.+)', handlers.AdminTaskInfoHandler),
            (r'/superadmin/?()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='superadmin.html')),
            (r'/admin/xmlupload/?', handlers.XMLUploadHandler),
            (r'/document/(.+)', handlers.DocumentViewHandler),
            (r'/HIT/?()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='hit.html')),
            (r'/HIT/view/?', handlers.CHITViewHandler),
            (r'/HIT/submit/?', handlers.CResponseHandler),
            (r'/worker/login/?', handlers.WorkerLoginHandler),
            (r'.*()', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='404.html'))
        ]
        tornado.web.Application.__init__(self, app_handlers, **settings)
 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(environment=options.environment, drop=options.drop))
    http_server.listen(options.port)
    Settings.logging.info("Started news_crowdsourcer in %s mode." % options.environment)
    tornado.ioloop.IOLoop.instance().start()
 

def clear_db(db):
    db.ctasks.drop()
    db.ctypes.drop()
    db.cresponses.drop()
    db.chits.drop()
    db.cdocs.drop()
    db.chitloads.drop()

if __name__ == "__main__":
    main()
