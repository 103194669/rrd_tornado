#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys

class Daemon(object):
    def __init__(self, pidfile=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', chroot='/'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.chroot = chroot

    def daemon(self):
        try:
            pid = os.fork()
            if pid >0: 
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork failed: (%d) %s\n" % (e.errno, e.strerror))
            sys.exit(1)
        
        os.chdir(self.chroot)
        os.umask(0)
        os.setsid()
        sys.stdout.flush()
        sys.stderr.flush()
        sin = file(self.stdin, 'r')
        sout = file(self.stdout, 'a+')
        serr = file(self.stderr, 'a+')
        os.dup2(sin.fileno(), sys.stdin.fileno())
        os.dup2(sout.fileno(), sys.stdout.fileno())
        os.dup2(serr.fileno(), sys.stderr.fileno())
        
        if self.pidfile:
            pid = os.getpid()
            file(self.pidfile,'w+').write(str(pid))        
