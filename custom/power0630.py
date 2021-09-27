#!/usr/bin/python
"""
                    Spine1(s1)        B--> Spine2(s2)
                        |    A        B          |
                        |    AAAAAAAAAAAAAAAA    |
                        |             B     A    |
                        |    BBBBBBBBBB     A    |
                        |    B              A    |
                    LeafLeft(s3)           LeafRight(s4)
                        |                        |
                        |                        |
                ----------------         ----------------
                |       |      |         |       |      |
                host1  host2  host3    host4   host5   host6"""
import re
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Host, Node
from mininet.cli import CLI
from mininet.link import Intf
from mininet.log import setLogLevel, info, error
from mininet.util import quietRun
from mininet.node import OVSController

class VLANHost( Host ):
    "Host connected to VLAN interface"

    def config( self, vlan=100, **params ):
        """Configure VLANHost according to (optional) parameters:
           vlan: VLAN ID for default interface"""

        r = super( VLANHost, self ).config( **params )

        intf = self.defaultIntf()
        # remove IP from default, "physical" interface
        self.cmd( 'ifconfig %s inet 0' % intf )
        # create VLAN interface
        self.cmd( 'vconfig add %s %d' % ( intf, vlan ) )
        # assign the host's IP to the VLAN interface
        self.cmd( 'ifconfig %s.%d inet %s' % ( intf, vlan, params['ip'] ) )
        # update the intf name and host's intf map
        newName = '%s.%d' % ( intf, vlan )
        # update the (Mininet) interface to refer to VLAN interface name
        intf.name = newName
        # add VLAN interface to host's name to intf map
        self.nameToIntf[ newName ] = intf
        return r

def r1Topo():
    net = Mininet(controller=RemoteController)
    net.addController('c0', controller=RemoteController, ip='192.168.3.1', port=6653)

    #host1 = net.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.100')
    host1 = net.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.100', cls=VLANHost, vlan=10)
    host2 = net.addHost('h2', ip='10.0.0.2/24', defaultRoute='via 10.0.0.100', cls=VLANHost, vlan=10)
    host3 = net.addHost('h3', ip='10.0.0.3/24', defaultRoute='via 10.0.0.100')
    host4 = net.addHost('h4', ip='10.0.0.4/24', defaultRoute='via 10.0.0.100', cls=VLANHost, vlan=10)
    host5 = net.addHost('h5', ip='10.0.0.5/24', defaultRoute='via 10.10.0.100')
    host6 = net.addHost('h6', ip='192.168.0.1/24', defaultRoute='via 192.168.0.100', cls=VLANHost, vlan=20)
    # host4 = net.addHost('h4', ip='192.168.0.1/24', defaultRoute='via 192.168.0.100')
    # host5 = net.addHost('h5', ip='192.168.0.2/24', defaultRoute='via 192.168.0.100')
    #host6 = net.addHost('h6', ip='192.168.0.3/24', defaultRoute='via 192.168.0.100')

    Spine1 = net.addSwitch('s1', mac='00:00:00:00:00:01', protocols='OpenFlow13')
    Spine2 = net.addSwitch('s2', mac='00:00:00:00:00:02', protocols='OpenFlow13')
    LeafLeft_s3 = net.addSwitch('s3', mac='00:00:00:00:00:03', protocols='OpenFlow13')
    LeafRight_s4 = net.addSwitch('s4', mac='00:00:00:00:00:04', protocols='OpenFlow13')

    #net.addLink(Spine, LeafRight)
    net.addLink(host1, LeafLeft_s3)
    net.addLink(host2, LeafLeft_s3)
    net.addLink(host3, LeafLeft_s3)
    net.addLink(host4, LeafRight_s4)
    net.addLink(host5, LeafRight_s4)
    net.addLink(host6, LeafRight_s4)

    net.addLink(Spine1, LeafLeft_s3)
    net.addLink(Spine1, LeafRight_s4)
    net.addLink(Spine2, LeafLeft_s3)
    net.addLink(Spine2, LeafRight_s4)

    # host1.cmd("route add -net 192.168.0.0 netmask 255.255.255.0 gw 10.0.0.100 h1-eth0.10")
    # host6.cmd("route add -net 10.0.0.0 netmask 255.255.255.0 gw 192.168.0.100 h6-eth0.20")
    net.start()
    host1.cmd("ip route add 192.168.0.0/24 via 10.0.0.100 dev h1-eth0.10")
    host6.cmd("ip route add 10.0.0.0/24 via 192.168.0.100 dev h6-eth0.20")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    r1Topo()
