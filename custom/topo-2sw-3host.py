# coding:utf-8
import unittest
import time
import config as cfg
from mininet.examples.vlanhost import VLANHost
from mininet.node import Host
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from utils import *


class TestSameVlanCase(unittest.TestCase):

    def setUp(self):
        # clear_all_host_vlans()
        # clear_all_switch_vlans()
        time.sleep(1)
        # clear_mininet()

    def test_tag_host_ping_tag_host(self):
        net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

        c0 = net.addController('c1', controller=RemoteController,
                               ip=cfg.controller['ip'], port=cfg.controller['port'])

        s1 = net.addSwitch('s1')
        s3 = net.addSwitch('s3')

        #
        h1 = net.addHost('h1', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a1",
                         ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
        h2 = net.addHost('h2', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a2",
                         ip='192.168.1.2/24', defaultRoute='via 192.168.1.254')
        h3 = net.addHost('h3', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a3",
                         ip='192.168.1.3/24', defaultRoute='via 192.168.1.254')

        net.addLink(h1, s3, port1=1, port2=1)
        net.addLink(h2, s3, port1=1, port2=2)
        net.addLink(h3, s3, port1=1, port2=3)

        net.addLink(s1, s3, port1=1, port2=4)

        net.build()

        h1.setDefaultRoute('via 192.168.1.254')
        h2.setDefaultRoute('via 192.168.1.254')
        h3.setDefaultRoute('via 192.168.1.254')

        c0.start()
        s1.start([c0])
        s3.start([c0])

        host_vlan_cfg1 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 10,
            'tagPorts': ['1-3'],
            'untagPorts': []
        }

        # sr1 = (
        #     StaticRouting()
        #     .add_switch_vlan(cfg.s1['id'], 10, ["192.168.1.254/24"])
        #     .add_host_vlan(host_vlan_cfg1)
        #     .build()
        # )

        # self.assertEqual(pingTest(h1, h2), 'success')

        CLI(net)
        net.stop()

    def test_untag_host_ping_tag_host(self):
        net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

        c0 = net.addController('c1', controller=RemoteController,
                               ip=cfg.controller['ip'], port=cfg.controller['port'])

        s1 = net.addSwitch('s1')
        s3 = net.addSwitch('s3')

        #
        h1 = net.addHost('h1', mac="00:00:00:00:00:a1",
                         ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
        h2 = net.addHost('h2', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a2",
                         ip='192.168.1.2/24', defaultRoute='via 192.168.1.254')
        h3 = net.addHost('h3', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a3",
                         ip='192.168.1.3/24', defaultRoute='via 192.168.1.254')

        net.addLink(h1, s3, port1=1, port2=1)
        net.addLink(h2, s3, port1=1, port2=2)
        net.addLink(h3, s3, port1=1, port2=3)

        net.addLink(s1, s3, port1=1, port2=4)

        net.build()

        h2.setDefaultRoute('via 192.168.1.254')
        h3.setDefaultRoute('via 192.168.1.254')

        c0.start()
        s1.start([c0])
        s3.start([c0])

        host_vlan_cfg1 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 10,
            'tagPorts': [2, 3],
            'untagPorts': [1]
        }

        sr1 = (
            StaticRouting()
            .add_switch_vlan(cfg.s1['id'], 10, ["192.168.1.254/24"])
            .add_host_vlan(host_vlan_cfg1)
            .build()
        )

        self.assertEqual(pingTest(h1, h2), 'success')
        self.assertEqual(pingTest(h2, h3), 'success')
        self.assertEqual(pingTest(h3, h1), 'success')

        CLI(net)
        net.stop()

    def test_untag_host_ping_untag_host(self):
        net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

        c0 = net.addController('c1', controller=RemoteController,
                               ip=cfg.controller['ip'], port=cfg.controller['port'])

        s1 = net.addSwitch('s1')
        s3 = net.addSwitch('s3')

        #
        h1 = net.addHost('h1', mac="00:00:00:00:00:a1",
                         ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
        h2 = net.addHost('h2', mac="00:00:00:00:00:a2",
                         ip='192.168.1.2/24', defaultRoute='via 192.168.1.254')
        h3 = net.addHost('h3', mac="00:00:00:00:00:a3",
                         ip='192.168.1.3/24', defaultRoute='via 192.168.1.254')

        net.addLink(h1, s3, port1=1, port2=1)
        net.addLink(h2, s3, port1=1, port2=2)
        net.addLink(h3, s3, port1=1, port2=3)

        net.addLink(s1, s3, port1=1, port2=4)

        net.build()

        c0.start()
        s1.start([c0])
        s3.start([c0])

        host_vlan_cfg1 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 10,
            'tagPorts': [],
            'untagPorts': ['1-3']
        }

        # sr1 = (
        #     StaticRouting()
        #     .add_switch_vlan(cfg.s1['id'], 10, ["192.168.1.254/24"])
        #     .add_host_vlan(host_vlan_cfg1)
        #     .build()
        # )

        # self.assertEqual(pingTest(h1, h2), 'success')
        # self.assertEqual(pingTest(h2, h3), 'success')
        # self.assertEqual(pingTest(h3, h1), 'success')

        CLI(net)
        net.stop()


class TestDifferentVlanCase(unittest.TestCase):

    def setUp(self):
        clear_mininet()
        clear_all_host_vlans()
        clear_all_switch_vlans()

    def test_untag_host_ping_untag_host(self):
        net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

        c0 = net.addController('c1', controller=RemoteController,
                               ip=cfg.controller['ip'], port=cfg.controller['port'])

        s1 = net.addSwitch('s1')
        s3 = net.addSwitch('s3')

        #
        h1 = net.addHost('h1', mac="00:00:00:00:00:a1",
                         ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
        h2 = net.addHost('h2', mac="00:00:00:00:00:a2",
                         ip='192.168.2.2/24', defaultRoute='via 192.168.2.254')
        h3 = net.addHost('h3', mac="00:00:00:00:00:a3",
                         ip='192.168.2.3/24', defaultRoute='via 192.168.2.254')

        net.addLink(h1, s3, port1=1, port2=1)
        net.addLink(h2, s3, port1=1, port2=2)
        net.addLink(h3, s3, port1=1, port2=3)

        net.addLink(s1, s3, port1=1, port2=4)

        net.build()

        c0.start()
        s1.start([c0])
        s3.start([c0])

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
            'untagPorts': [2, 3]
        }

        sr1 = (
            StaticRouting()
            .add_switch_vlan(cfg.s1['id'], 10, ["192.168.1.254/24"])
            .add_switch_vlan(cfg.s1['id'], 20, ["192.168.2.254/24"])
            .add_host_vlan(host_vlan_cfg1)
            .add_host_vlan(host_vlan_cfg2)
            .build()
        )

        self.assertEqual(pingTest(h1, h2), 'success')
        self.assertEqual(pingTest(h2, h3), 'success')
        self.assertEqual(pingTest(h3, h1), 'success')

        # CLI(net)
        net.stop()

    def test_tag_host_ping_tag_host(self):
        net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

        c0 = net.addController('c1', controller=RemoteController,
                               ip=cfg.controller['ip'], port=cfg.controller['port'])

        s1 = net.addSwitch('s1')
        s3 = net.addSwitch('s3')

        #
        h1 = net.addHost('h1', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a1",
                         ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
        h2 = net.addHost('h2', cls=VLANHost, vlan=20, mac="00:00:00:00:00:a2",
                         ip='192.168.2.2/24', defaultRoute='via 192.168.2.254')
        h3 = net.addHost('h3', cls=VLANHost, vlan=20, mac="00:00:00:00:00:a3",
                         ip='192.168.2.3/24', defaultRoute='via 192.168.2.254')

        net.addLink(h1, s3, port1=1, port2=1)
        net.addLink(h2, s3, port1=1, port2=2)
        net.addLink(h3, s3, port1=1, port2=3)

        net.addLink(s1, s3, port1=1, port2=4)

        net.build()

        h1.setDefaultRoute('via 192.168.1.254')
        h2.setDefaultRoute('via 192.168.2.254')
        h3.setDefaultRoute('via 192.168.2.254')

        c0.start()
        s1.start([c0])
        s3.start([c0])

        host_vlan_cfg1 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 10,
            'tagPorts': [1],
            'untagPorts': []
        }

        host_vlan_cfg2 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 20,
            'tagPorts': [2, 3],
            'untagPorts': []
        }

        sr1 = (
            StaticRouting()
            .add_switch_vlan(cfg.s1['id'], 10, ["192.168.1.254/24"])
            .add_switch_vlan(cfg.s1['id'], 20, ["192.168.2.254/24"])
            .add_host_vlan(host_vlan_cfg1)
            .add_host_vlan(host_vlan_cfg2)
            .build()
        )

        self.assertEqual(pingTest(h1, h2), 'success')
        self.assertEqual(pingTest(h2, h3), 'success')
        self.assertEqual(pingTest(h3, h1), 'success')

        # CLI(net)
        net.stop()

    def test_untag_host_ping_tag_host(self):
        net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

        c0 = net.addController('c1', controller=RemoteController,
                               ip=cfg.controller['ip'], port=cfg.controller['port'])

        s1 = net.addSwitch('s1')
        s3 = net.addSwitch('s3')

        #
        h1 = net.addHost('h1', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a1",
                         ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
        h2 = net.addHost('h2', mac="00:00:00:00:00:a2",
                         ip='192.168.2.2/24', defaultRoute='via 192.168.2.254')
        h3 = net.addHost('h3', cls=VLANHost, vlan=20, mac="00:00:00:00:00:a3",
                         ip='192.168.2.3/24', defaultRoute='via 192.168.2.254')

        net.addLink(h1, s3, port1=1, port2=1)
        net.addLink(h2, s3, port1=1, port2=2)
        net.addLink(h3, s3, port1=1, port2=3)

        net.addLink(s1, s3, port1=1, port2=4)

        net.build()

        h1.setDefaultRoute('via 192.168.1.254')
        h3.setDefaultRoute('via 192.168.2.254')

        c0.start()
        s1.start([c0])
        s3.start([c0])

        host_vlan_cfg1 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 10,
            'tagPorts': [1],
            'untagPorts': []
        }

        host_vlan_cfg2 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 20,
            'tagPorts': [3],
            'untagPorts': [2]
        }

        sr1 = (
            StaticRouting()
            .add_switch_vlan(cfg.s1['id'], 10, ["192.168.1.254/24"])
            .add_switch_vlan(cfg.s1['id'], 20, ["192.168.2.254/24"])
            .add_host_vlan(host_vlan_cfg1)
            .add_host_vlan(host_vlan_cfg2)
            .build()
        )

        self.assertEqual(pingTest(h1, h2), 'success')
        self.assertEqual(pingTest(h2, h3), 'success')
        self.assertEqual(pingTest(h3, h1), 'success')

        # CLI(net)
        net.stop()

    def test_isolation_vlan(self):
        net = Mininet(switch=OVSKernelSwitch, controller=RemoteController)

        c0 = net.addController('c1', controller=RemoteController,
                               ip=cfg.controller['ip'], port=cfg.controller['port'])

        s1 = net.addSwitch('s1')
        s3 = net.addSwitch('s3')

        #
        h1 = net.addHost('h1', cls=VLANHost, vlan=10, mac="00:00:00:00:00:a1",
                         ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')
        h2 = net.addHost('h2', mac="00:00:00:00:00:a2",
                         ip='192.168.2.2/24', defaultRoute='via 192.168.2.254')
        h3 = net.addHost('h3', cls=VLANHost, vlan=20, mac="00:00:00:00:00:a3",
                         ip='192.168.2.3/24', defaultRoute='via 192.168.2.254')

        net.addLink(h1, s3, port1=1, port2=1)
        net.addLink(h2, s3, port1=1, port2=2)
        net.addLink(h3, s3, port1=1, port2=3)

        net.addLink(s1, s3, port1=1, port2=4)

        net.build()

        h1.setDefaultRoute('via 192.168.1.254')
        h3.setDefaultRoute('via 192.168.2.254')

        c0.start()
        s1.start([c0])
        s3.start([c0])

        host_vlan_cfg1 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 10,
            'tagPorts': [1],
            'untagPorts': []
        }

        host_vlan_cfg2 = {
            'deviceId': cfg.s3['id'],
            'vlanId': 20,
            'tagPorts': [3],
            'untagPorts': [2]
        }

        sr1 = (
            StaticRouting()
            .add_host_vlan(host_vlan_cfg1)
            .add_host_vlan(host_vlan_cfg2)
            .build()
        )

        self.assertEqual(pingTest(h1, h2), 'failure')
        self.assertEqual(pingTest(h2, h3), 'success')
        self.assertEqual(pingTest(h3, h1), 'failure')

        # CLI(net)
        net.stop()


if __name__ == '__main__':
    unittest.main()
