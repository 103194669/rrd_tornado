#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os.path
import sys
import rrdtool
import time

from rrdutils import RRD_PATH, CreateRRD

def daemon():
	sys.stdout.flush()
	sys.stderr.flush()
	try:
		pid = os.fork()
		if pid >0:
			sys.exit(0)
	except OSError, e:
		sys.stderr.write("fork failed: (%d) %s\n" % (e.errno, e.strerror))
		sys.exit(1)
	os.chdir("/")
	os.umask(0)
	os.setsid()

def datacollect():
	while True:
		f = open("/proc/net/dev")
		for i in f:
			data = i
		input = data.split()[0][5:]
		rrdtool.update(RRD_PATH, "N:%s" % input)
		f.close()
		time.sleep(5)

def main():
	daemon()
	if os.path.exists(RRD_PATH):
		datacollect()
	else:
		CreateRRD().create()
		datacollect()

if __name__ == "__main__":
	main()
