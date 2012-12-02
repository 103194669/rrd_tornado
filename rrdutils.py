#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os.path
import rrdtool

RRD_PATH = os.path.join(os.path.dirname(__file__), "test.rrd")

class CreateRRD(object):
    def create(self):
        rrdtool.create(RRD_PATH,
            '-s', '5',
            'DS:eth0:COUNTER:10:U:U',
            'RRA:MAX:0.5:1:600',
            'RRA:MAX:0.5:5:600',
            'RRA:MAX:0.5:12:600'
            )

class GraphRRD(object):
    def graph(self, static_path, time):
        rrdtool.graph(static_path + "/test.png",
            "-s","NOW-%s" % time,
            "DEF:in=%s:eth0:MAX" % RRD_PATH,
            "AREA:in#00FF00:In traffic",
            "CDEF:inbits=in,8,*",
            "GPRINT:inbits:AVERAGE:Avg In traffic\: %6.2lf %Sbps",
            "GPRINT:inbits:MAX:Max In traffic\: %6.2lf %Sbps",
            "-S","20",
            "-t","网卡流量",
            "-v","Bytes/s",
            "-X","0",
            "-c","FONT#9400d3",
            "-w","400",
            "--slope-mode",
            "--no-gridfit",
            "-b","1024",
            "--lower-limit","1.5",
            "--zoom","2"
            )
