from argparse import ArgumentParser
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
from handlers import FileHandler

define("port", default=8888, help="run on the given port", type=int)
gl_port = None


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world: Port number %s" % gl_port)


def main():
    # Parse the argument
    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=8888, help='Select port for listening')
    args = parser.parse_args()
    global gl_port
    gl_port = args.port

    application = tornado.web.Application([
        (r"/status", MainHandler),
        (r"/test/file", FileHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(args.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
