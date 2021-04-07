# coding:utf-8
"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

import utils
import time
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from utils import *
import sys
import os
sys.path.append(os.getcwd())

if __name__ == '__main__':
    net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

    c0 = net.addController('c1', controller=RemoteController,
                           ip="192.168.40.2", port=6653)

    # 新增switch
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    #
    h1 = net.addHost('h1', mac="00:00:00:00:00:a1", ip='192.168.1.1/24')
    h2 = net.addHost('h2', mac="00:00:00:00:00:a2", ip='192.168.2.1/24')
    h3 = net.addHost('h3', mac="00:00:00:00:00:a3", ip='192.168.3.1/24')
    h4 = net.addHost('h4', mac="00:00:00:00:00:a4", ip='192.168.4.1/24')
    h5 = net.addHost('h5', mac="00:00:00:00:00:a5", ip='192.168.5.1/24')
    h6 = net.addHost('h6', mac="00:00:00:00:00:a6", ip='192.168.6.1/24')

    net.addLink(h1, s3, port1=1, port2=1)
    net.addLink(h2, s3, port1=1, port2=2)
    net.addLink(h3, s3, port1=1, port2=3)

    net.addLink(h4, s4, port1=1, port2=1)
    net.addLink(h5, s4, port1=1, port2=2)
    net.addLink(h6, s4, port1=1, port2=3)

    net.addLink(s1, s3, port1=1, port2=4)
    net.addLink(s2, s3, port1=1, port2=5)
    net.addLink(s1, s4, port1=2, port2=4)
    net.addLink(s2, s4, port1=2, port2=5)

    net.build()

    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    s4.start([c0])

    # h1.cmd("ifconfig h1-eth1 0")
    # h1.cmd("vconfig add h1-eth1 10")
    # h1.cmd("ifconfig h1-eth1.10 10.0.0.1/24")
    # h1.cmd("route add -net 192.168.0.0 netmask 255.255.255.0 gw 10.0.0.100 " +
    #        "h1-eth1.10")

    h1.cmd("route add -net 0.0.0.0 gw 192.168.1.254 " +
           "h1-eth1")
    h2.cmd("route add -net 0.0.0.0 gw 192.168.2.254 " +
           "h2-eth1")
    h3.cmd("route add -net 0.0.0.0 gw 192.168.3.254 " +
           "h3-eth1")
    h4.cmd("route add -net 0.0.0.0 gw 192.168.4.254 " +
           "h4-eth1")
    h5.cmd("route add -net 0.0.0.0 gw 192.168.5.254 " +
           "h5-eth1")
    h6.cmd("route add -net 0.0.0.0 gw 192.168.6.254 " +
           "h6-eth1")

    clear_all_host_vlans()
    clear_all_switch_vlans()

    host_vlan_cfg1 = {
        'deviceId': cfg.s3['id'],
        'vlanId': 10,
        'tagPorts': [],
        'untagPorts': [1]
    }

    host_vlan_cfg2 = {
        'deviceId': cfg.s3['id'],
        'vlanId': 20,
        'tagPorts': [],
        'untagPorts': [2]
    }

    host_vlan_cfg3 = {
        'deviceId': cfg.s3['id'],
        'vlanId': 30,
        'tagPorts': [],
        'untagPorts': [3]
    }

    host_vlan_cfg4 = {
        'deviceId': cfg.s4['id'],
        'vlanId': 40,
        'tagPorts': [],
        'untagPorts': [1]
    }

    host_vlan_cfg5 = {
        'deviceId': cfg.s4['id'],
        'vlanId': 50,
        'tagPorts': [],
        'untagPorts': [2]
    }

    host_vlan_cfg6 = {
        'deviceId': cfg.s4['id'],
        'vlanId': 60,
        'tagPorts': [],
        'untagPorts': [3]
    }

    sr1 = (
        StaticRouting()
        .add_switch_vlan(cfg.s1['id'], 10, ["192.168.1.254/24"])
        .add_switch_vlan(cfg.s1['id'], 20, ["192.168.2.254/24"])
        .add_switch_vlan(cfg.s1['id'], 30, ["192.168.3.254/24"])
        .add_switch_vlan(cfg.s1['id'], 40, ["192.168.4.254/24"])
        .add_switch_vlan(cfg.s1['id'], 50, ["192.168.5.254/24"])
        .add_switch_vlan(cfg.s1['id'], 60, ["192.168.6.254/24"])
        .add_host_vlan(host_vlan_cfg1)
        .add_host_vlan(host_vlan_cfg2)
        .add_host_vlan(host_vlan_cfg3)
        .add_host_vlan(host_vlan_cfg4)
        .add_host_vlan(host_vlan_cfg5)
        .add_host_vlan(host_vlan_cfg6)
        .build()
    )

    pingTest(h1, h2)
    pingTest(h2, h3)
    pingTest(h3, h4)
    pingTest(h4, h5)
    pingTest(h5, h6)
    pingTest(h6, h1)

    CLI(net)
    net.stop()
