#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os.path
import sys
import rrdtool
import time
import re

from rrdutils import RRD_PATH, CreateRRD
from daemon import Daemon

def datacollect():
    p = re.compile(r"^.*: *(\d+) *")
    while True:
        f = open("/proc/net/dev")
        for i in f:
            data = i
        input = p.search(data)
        if input:
           # print input.group(1)
            rrdtool.update(RRD_PATH, "N:%s" % input.group(1))
        f.close()
        time.sleep(5)

def main():
    Daemon(pidfile=os.path.join(os.path.dirname(RRD_PATH),"log/data.pid")).daemon()
    if os.path.exists(RRD_PATH):
        datacollect()
    else:
        CreateRRD().create()
        datacollect()

if __name__ == "__main__":
    main()
