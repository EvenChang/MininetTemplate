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
                           ip="192.168.3.1", port=6653)

    # 新增switch
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')
    s3 = net.addSwitch('s3', protocols='OpenFlow13')

    h1 = net.addHost('h1', mac="00:00:00:00:00:a1", ip='192.168.2.1/24')
    h2 = net.addHost('h2', mac="00:00:00:00:00:a2", ip='192.168.2.2/24')
    h3 = net.addHost('h3', mac="00:00:00:00:00:a3", ip='192.168.2.3/24')

    net.addLink(s2, s1, port1=4, port2=4)
    net.addLink(s1, s3, port1=5, port2=5)
    net.addLink(s2, s3, port1=6, port2=6)
    net.addLink(h1, s1, port1=1, port2=2)
    net.addLink(h2, s2, port1=1, port2=2)
    net.addLink(h3, s3, port1=1, port2=2)

    net.build()

    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])

    #h2.cmd("ifconfig h2-eth1 0")
    #h2.cmd("vconfig add h2-eth1.100")
    #h2.cmd("ifconfig h2-eth1.100 192.168.1.2/24")
    #h1.cmd("route add -net 192.168.1.0 netmask 255.255.255.0 gw 10.0.0.100 " +
    #        "h1-eth1.100")

#    h1.cmd("route add -net 192.168.1.0 netmask 255.255.255.0 gw 10.0.0.100 " +
#           "h1-eth1")
#    h2.cmd("route add -net 10.0.0.0 netmask 255.255.255.0 gw 192.168.1.100 " +
#           "h2-eth1")
#    h3.cmd("route add -net 0.0.0.0 netmask 255.255.255.0 gw 192.168.1.254 " +
#           "h3-eth1")

    CLI(net)
    net.stop()
