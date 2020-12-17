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

if __name__ == '__main__':
    net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

    c0 = net.addController('c1', controller=RemoteController,
                           ip="192.168.3.1", port=6653)

    # 新增switch
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    #
    h1 = net.addHost('h1', mac="00:00:00:00:00:a1")
    h2 = net.addHost('h2', mac="00:00:00:00:00:a2")
    h3 = net.addHost('h3', mac="00:00:00:00:00:a3")
    h4 = net.addHost('h4', mac="00:00:00:00:00:a4")
    h5 = net.addHost('h5', mac="00:00:00:00:00:a5")
    h6 = net.addHost('h6', mac="00:00:00:00:00:a6", ip='192.168.0.1/24')

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

    h1.cmd("ifconfig h1-eth1 0")
    h1.cmd("vconfig add h1-eth1 10")
    h1.cmd("ifconfig h1-eth1.10 10.0.0.1/24")
    h1.cmd("route add -net 192.168.0.0 netmask 255.255.255.0 gw 10.0.0.100 " +
           "h1-eth1.10")

    # h1.cmd("route add -net 192.168.0.0 netmask 255.255.255.0 gw 10.0.0.100 " +
    #        "h1-eth1")

    h6.cmd("ifconfig h6-eth1 0")
    h6.cmd("vconfig add h6-eth1 20")
    h6.cmd("ifconfig h6-eth1.20 192.168.0.1/24")
    h6.cmd("route add -net 10.0.0.0 netmask 255.255.255.0 gw 192.168.0.100 " +
           "h6-eth1.20")

    # h6.cmd("route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.100 " +
    #        "h6-eth1")

    CLI(net)
    net.stop()
