import libvirt
import sys

class Libvirt:
    def __init__(self):
        # Either works:
        #conn = libvirt.openReadOnly('lxc:///')
        self.conn = libvirt.openReadOnly(None)

        if self.conn == None:
            print 'Failed to open connection to the hypervisor'

    def container(self, name):
        try:
            return self.conn.lookupByName(name)
        except Exception as ex:
            print 'Failed to find the domain for {}: {}'.format(name, ex)

if __name__ == '__main__':
    server = Libvirt()
    test = server.container('test')
    print "Test: id {} running {}".format(test.ID(), test.OSType())
    print test.info()

