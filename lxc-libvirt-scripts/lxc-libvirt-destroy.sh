#!/bin/sh

virsh -c lxc:// undefine $1
lxc-destroy -n $1
