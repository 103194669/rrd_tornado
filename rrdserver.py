#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import mimetypes
import rrdtool
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.autoreload

from tornado.options import define, options
from rrdutils import GraphRRD
from daemon import Daemon

define("port", default=80, help="run on the given port", type=int)
define("daemon", default=False, help="True or False")
define("reload", default=True, help="True or False")
define("png_buffer", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "pngbuffer")))
define("template_path", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "templates")))
define("log_file", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "log/access.log")))
define("pid_file", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "log/rrd.pid")))
define("root_dir", default=os.path.abspath(os.path.dirname(__file__)))

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=options.template_path,
            static_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
            )

        handers = [
            (r"/",MainHander),
            (r"/pngbuffer/(.*)", PNGHandler),
        ]
    
        tornado.web.Application.__init__(self, handers, **settings)


class MainHander(tornado.web.RequestHandler):
    def get(self):
        GraphRRD().graph(options.png_buffer, 86400)
        self.render("main.html")

    def post(self):
        try:
            time = self.get_argument("time")
            int(time)
            GraphRRD().graph(options.png_buffer, str(time))
            self.render("main.html")
        #except ValueError, e:
        except :
            self.render("error.html")

class PNGHandler(tornado.web.RequestHandler):
    def get(self, path):
        abspath = os.path.join(options.png_buffer, path)
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

def main_reload():
    if not os.path.exists(options.png_buffer):
        os.makedirs(options.png_buffer)

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()

if __name__ == "__main__":
    if options.daemon:
        if not os.path.exists(os.path.dirname(options.pid_file)):
            os.makedirs(os.path.dirname(options.pid_file))
        if not os.path.exists(os.path.dirname(options.log_file)):
            os.makedirs(so.path.dirname(options.log_file))

        d = Daemon(pidfile=options.pid_file, 
                stdout=options.log_file,
                stderr=options.log_file,
                chroot=options.root_dir)
        d.daemon()
    if options.reload:
        main_reload()
    else:
        main()
