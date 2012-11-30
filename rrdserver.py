#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import rrdtool
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options
from rrdutils import GraphRRD

define("port", default=80, help="run on the given port", type=int)
define("static_path", default=os.path.join(os.path.dirname(__file__), "static"))
class Application(tornado.web.Application):
	def __init__(self):
		settings = dict(
				static_path=options.static_path
				)
		handers = [
			(r"/",MainHander),
			(r"/static/", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
		]
		tornado.web.Application.__init__(self, handers, **settings)

class MainHander(tornado.web.RequestHandler):
	def get(self):
		GraphRRD().graph(options.static_path, 86400)
		self.write('<html><body><img src="static/test.png"/>'
				'<form action="/" method="post">'
				'<input type="text" name="time">'
				'<input type="submit" value="提交">'
				'</form></body></html>')

	def post(self):
		try:
			time = self.get_argument("time")
			int(time)
			GraphRRD().graph(options.static_path, str(time))
			self.write('<html><body><img src="static/test.png"/>'
					'<form action="/" method="post">'
					'<input type="text" name="time">'
					'<input type="submit" value="提交">'
					'</form></body></html>')
		#except ValueError, e:
		except :
			self.write('<center><h1>输入错误<h1></center>'
					'<center><input type="button" name="Submit" value="返回"'
					'onclick ="location.href=\'/\'"/></center>')

def main():
	if not os.path.exists(options.static_path):
		os.makedirs(options.static_path)
		
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
