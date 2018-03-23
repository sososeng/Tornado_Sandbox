import tornado.ioloop
import tornado.web
import tornado.log
from jinja2 import Environment, PackageLoader, select_autoescape
ENV = Environment(
    loader=PackageLoader('myapp', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)




# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.set_header("Content-Type", 'text/plain')
#         self.write("Hello, world")
#
# class YouTooHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.set_header("Content-Type", 'text/plain')
#         name = self.get_query_argument("name", "NoBody")
#         self.write("Hello, {}".format(name))
#
# class YouHandler(tornado.web.RequestHandler):
#     def get(self, name):
#         self.set_header("Content-Type", 'text/plain')
#         self.write("Hello, {}".format(name))
#
#
# class YouThreeHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.set_header("Content-Type", 'text/plain')
#         names = self.get_query_arguments('name')
#         for name in names:
#             self.write("Hello, {}\n".format(name))



class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))


class MainHandler(TemplateHandler):
    def get(self):
        self.set_header(
          'Cache-Control',
          'no-store, no-cache, must-revalidate, max-age=0')

        name = self.get_query_argument("name","Anon")
        self.render_template("index.html", {'name': name})


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (
            r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {'path': 'static'}
        ),
        # (r"/hello2", YouTooHandler),
        # (r"/hello/(.*)", YouHandler),
        # (r"/hello3", YouThreeHandler),
    ], autoreload=True)


if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()