# coding:utf-8
"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.examples.vlanhost import VLANHost

if __name__ == '__main__':
    net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

    c0 = net.addController('c1', controller=RemoteController,
                           ip="124.219.108.7", port=6653)

    # 新增switch
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')
    s3 = net.addSwitch('s3', protocols='OpenFlow13')
    s4 = net.addSwitch('s4', protocols='OpenFlow13')
    s5 = net.addSwitch('s5', protocols='OpenFlow13')
    s6 = net.addSwitch('s6', protocols='OpenFlow13')
    s7 = net.addSwitch('s7', protocols='OpenFlow13')
    s8 = net.addSwitch('s8', protocols='OpenFlow13')
    s9 = net.addSwitch('s9', protocols='OpenFlow13')
    s10 = net.addSwitch('s10', protocols='OpenFlow13')
    s11 = net.addSwitch('s11', protocols='OpenFlow13')
    s12 = net.addSwitch('s12', protocols='OpenFlow13')

    #
    h1 = net.addHost('h1', mac="00:00:00:00:00:a1", ip='192.168.1.1/24')
    h2 = net.addHost('h2', mac="00:00:00:00:00:a2", ip='192.168.1.2/24')

    # Host
    net.addLink(h1, s1, port1=1, port2=1)
    net.addLink(h2, s2, port1=1, port2=1)
    # Switch
    net.addLink(s1, s3, port1=2, port2=2)
    net.addLink(s3, s4, port1=3, port2=1)
    net.addLink(s3, s5, port1=1, port2=1)
    net.addLink(s4, s6, port1=2, port2=1)
    net.addLink(s5, s7, port1=2, port2=1)
    net.addLink(s6, s8, port1=2, port2=1)
    net.addLink(s8, s10, port1=2, port2=1)
    net.addLink(s7, s9, port1=2, port2=1)
    net.addLink(s9, s11, port1=2, port2=1)
    net.addLink(s10, s12, port1=2, port2=3)
    net.addLink(s11, s12, port1=2, port2=1)
    net.addLink(s12, s2, port1=2, port2=2)

    net.build()

    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    s4.start([c0])
    s5.start([c0])
    s6.start([c0])
    s7.start([c0])
    s8.start([c0])
    s9.start([c0])
    s10.start([c0])
    s11.start([c0])
    s12.start([c0])
   

    h1.cmd("route add -net 0.0.0.0 gw 192.168.1.254 " +
           "h1-eth1")
    h2.cmd("route add -net 0.0.0.0 gw 192.168.1.254 " +
           "h2-eth1")

    CLI(net)
    net.stop()
