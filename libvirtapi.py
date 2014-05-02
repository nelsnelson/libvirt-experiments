#! /usr/bin/env python

import libvirt
from libvirt import virDomain
import inspect
import sys

functions = dir(libvirt)

#print "Module libvirt methods:"
#print functions

functions = dir(virDomain)

print "Module domain methods:"
for f in functions:
    print "  {}".format(f)

#conn = libvirt.openReadOnly(None)

#functions = dir(conn)

#print globals()



method = None

try:
    method = getattr(globals()['virDomain'], sys.argv[1])
except:
    try:
        method = getattr(globals()['libvirt'], sys.argv[1])
    except:
        pass

if method:
    help(method)

conn = libvirt.open('lxc:///')

#for f in functions:
#    print f.func_defaults

print "Connection methods:"
for m in inspect.getmembers(conn, predicate=inspect.ismethod):
    print "  {}".format(m)


