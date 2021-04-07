"""Custom topology example

   host --- switch  --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.util import dumpNodeConnections
from mininet.topo import Topo
from mininet.cli import CLI


class OneSwitchTopo(Topo):
    "One switch topology test."

    def build(self):
        "Create custom topo."

        # Add hosts and switches
        h1 = self.addHost('h1', mac="00:00:00:00:00:a1", ip='192.168.1.1/24')
        h2 = self.addHost('h2', mac="00:00:00:00:00:a2", ip='192.168.2.1/24')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add links
        self.addLink(h1, s2, port1=1, port2=1)
        self.addLink(h2, s2, port1=1, port2=2)
        self.addLink(s1, s2, port1=1, port2=3)


def OneSwitchTopoTest(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
    net.ping(hosts=[h1, h2])


topos = {'one_switch_topo': OneSwitchTopo}
tests = {'one_switch_topo_test': OneSwitchTopoTest}
