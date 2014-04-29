#!/bin/sh

path=/var/lib/lxc/$1/rootfs
if [ -d $path ]; then
	echo "$1 already exists:  do you want to convert it (y/n)?"
	read x
	if [ $x != "y" ]; then
		"Ok, exiting."
		exit 0
	fi
else
	echo "$1 does not yet exist, creating it"
	lxc-create -n $1 -f /etc/lxc-basic.conf -t ubuntu
fi

echo Converting $1

# libvirt gives console on /dev/pts/0
oldpath=`pwd`
cd $path
echo "pts/0" >> etc/securetty
mv etc/init etc/init.bak
mkdir etc/init

cat >> etc/init/lxc.conf << EOF
description "Container upstart"
start on startup

script
	rm -rf /var/run/*.pid
	rm -rf /var/run/network
        /sbin/initctl emit stopped JOB=udevtrigger --no-wait
end script
EOF

cat >> etc/init/console.conf << EOF
description "Console"
start on startup

respawn
exec /sbin/getty -8 38400 pts/0
EOF

cat >> etc/init/networking.conf << EOF
description "Network"
start on stopped udevtrigger

pre-start exec mkdir -p /var/run/network

exec ifup -a
EOF

cp etc/init.bak/network-interface.conf etc/init/

cp etc/init.bak/ssh.conf etc/init/
sed -i 's/^start on.*$/start on stopped udevtrigger/' etc/init/ssh.conf

cd $oldpath
cp base.xml $1.xml

sed -i "s/NAME/$1/" $1.xml
sed -i "s<ROOT<$path<" $1.xml
virsh -c lxc:// define $1.xml

echo "Conversion complete"
