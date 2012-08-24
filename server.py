import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

from tornado.options import options, define
CWD = os.path.dirname(__file__)
define('port', default=8000, type=int)

class BaseHandler(tornado.web.RequestHandler):
  pass

class MainHandler(BaseHandler):
  def get(self):
    self.render('main.html')

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
        (r'/', MainHandler),
        ]
    settings = {
        'debug': True,
        'static_path': os.path.join(CWD, 'static'),
        'template_path': os.path.join(CWD, 'templates'),
        }
    tornado.web.Application.__init__(self, handlers, **settings)

# run server
if __name__ == "__main__":
  tornado.options.parse_command_line()
  httpserver = tornado.httpserver.HTTPServer(Application())
  httpserver.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
