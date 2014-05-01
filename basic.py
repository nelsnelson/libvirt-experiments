#! /usr/bin/env python

import libvirt
import sys
import os

CONFIG = '''<domain type='lxc'>
  <name>{}</name>
  <memory>500000</memory>
  <os>
    <type>exe</type>
    <init>/bin/bash</init>
  </os>
  <vcpu>1</vcpu>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/lib/libvirt_lxc</emulator>
    <console type='pty' />
  </devices>
</domain>'''

class Container:
    def __init__(self, name='test'):
        self.name = name
        self.conn = libvirt.open('lxc:///')
        if self.conn == None:
            print 'Failed to open connection to the hypervisor'

    def create(self, name=None):
        if not name:
            name = self.name
        try:
            self.domain = self.conn.lookupByName(name)
        except Exception as ex:
            try:
                self.domain = self.conn.defineXML(CONFIG.format(name))
                if self.domain:
                    result = self.domain.createWithFiles()
                    print "Created domain: {}".format(result)
            except Exception as ex:
                print 'Exception creating domain {}: {}'.format(name, ex)

        print "  Domain is active: {}".format(self.domain.isActive())
        print "  Domain state: {}".format(self.domain.state())

        return self.domain

    def destroy(self, domain=None, name=None):
        if not name:
            name = self.name
        if not domain:
            domain = self.domain
        try:
            return self.domain.destroy()
        except Exception as ex:
            print 'Exception destroying domain {}: {}'.format(name, ex)

    def __enter__(self):
        self.create()
        return self.domain

    def __exit__(self, type, value, tb):
        self.destroy() 

if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'test'
    with Container(name) as c:
        print "Test: id {} running {}".format(c.ID(), c.OSType())
        print c.info()

