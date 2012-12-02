#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import mimetypes
import rrdtool
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options
from rrdutils import GraphRRD

define("port", default=80, help="run on the given port", type=int)
define("png_buffer", default=os.path.join(os.path.dirname(__file__), "pngbuffer"))
class Application(tornado.web.Application):
    def __init__(self):
        handers = [
            (r"/",MainHander),
            (r"/pngbuffer/(.*)", PNGHandler),
        ]
        tornado.web.Application.__init__(self, handers)


class MainHander(tornado.web.RequestHandler):
    def get(self):
        GraphRRD().graph(options.png_buffer, 86400)
        self.render("templates/main.html")

    def post(self):
        try:
            time = self.get_argument("time")
            int(time)
            print time
            GraphRRD().graph(options.png_buffer, str(time))
            self.render("templates/main.html")
        #except ValueError, e:
        except :
            self.render("templates/error.html")

class PNGHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.filename = self.request.path.lstrip("/")

    def get(self, path):
        abspath = os.path.abspath(self.filename)
        if not os.path.exists(abspath):
            raise tornado.web.HTTPError(404)
        if not os.path.isfile(abspath):
            raise tornado.web.HTTPError(403, "%s is not a file", self.filename)
        mime_type, encoding = mimetypes.guess_type(abspath)
        if mime_type:
            self.set_header("Content-Type", mime_type)
        self.set_header("Cache-Control", "no-cache")
        self.set_header("Etag", "unknown")
        with open(abspath, "rb") as file:
            data = file.read()
            self.write(data)

def main():
    if not os.path.exists(options.png_buffer):
        os.makedirs(options.png_buffer)
    
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
