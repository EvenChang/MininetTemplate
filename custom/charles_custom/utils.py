import time
import base64
import requests
import re
import os
import subprocess
import config as cfg

URL = cfg.API_BASE_URL
LOGIN = cfg.LOGIN
AUTH_TOKEN = 'BASIC ' + LOGIN
GET_HEADER = {'Authorization': AUTH_TOKEN}
POST_HEADER = {'Authorization': AUTH_TOKEN, 'Content-Type': 'application/json'}
DELETE_HEADER = {'Authorization': AUTH_TOKEN, 'Accept': 'application/json'}
PUT_HEADER = {'Authorization': AUTH_TOKEN, 'Accept': 'application/json'}
# GET_HEADER = {'Accept': 'application/json'}
# POST_HEADER = {'Content-Type': 'application/json'}
# DELETE_HEADER = {'Accept': 'application/json'}
# PUT_HEADER = {'Accept': 'application/json'}


def clear_mininet():
    # subprocess.call(['mn', '-c'])
    p = subprocess.Popen('mn -c 2> /dev/null', shell=True)
    os.waitpid(p.pid, 0)


def pingTest(src_host, dst_host, debug=False):
    if debug:
        print "Starting test: " + src_host.name + ' ping ' + dst_host.name

    src_host.cmd('ping ' + dst_host.IP() +
                 ' > /tmp/{}.out &'.format(src_host.name))
    time.sleep(10)

    if debug:
        print "Stopping test"

    src_host.cmd('kill %ping')

    f = open('/tmp/{}.out'.format(src_host.name))
    lineno = 1

    result = 'failure'
    for line in f.readlines():
        if debug == True:
            print "%d: %s" % (lineno, line.strip())

        expected_str = '64 bytes from ' + dst_host.IP()

        if re.search(expected_str, line.strip()):
            result = 'success'

        lineno += 1
        f.close()

    return result


def clear_all_host_vlans():
    response = requests.get(
        URL+'staticrouting/v1/hostvlans', headers=GET_HEADER)
    assert response.status_code == 200, 'Get host vlans fail! ' + response.text

    for device in response.json()['hostVlans']:
        response = requests.delete(
            URL+'staticrouting/v1/hostvlans/{}'.format(device['deviceId']), headers=DELETE_HEADER)
        assert response.status_code == 200, 'Delete host vlans fail! ' + response.text


def clear_all_switch_vlans():
    response = requests.get(
        URL+'staticrouting/v1/devices', headers=GET_HEADER)
    assert response.status_code == 200, 'Get switch vlans fail! ' + response.text

    for device in response.json()['routings']:
        response = requests.delete(
            URL+'staticrouting/v1/vlans/{}'.format(device['deviceId']), headers=DELETE_HEADER)
        assert response.status_code == 200, 'Delete switch vlans fail! ' + response.text


class StaticRouting():
    def __init__(self):
        self._host_vlan_cfg_list = []
        self._switch_vlan_cfg_list = []
        self._rest_switch_vlan_cfg_list = []

    def add_switch_vlan(self, device_id, vlan_id, subnets, tag_ports=[], untag_ports=[]):
        switch_vlan = {
            'deviceId': device_id,
            'vlanId': vlan_id,
            'subnets': subnets,
            "tagPorts": tag_ports,
            "untagPorts": untag_ports
        }

        self._switch_vlan_cfg_list.append(switch_vlan)

        return self

    def add_rest_switch_vlan(self, device_id, vlan_id, primary, subnets, tag_ports=[], untag_ports=[]):
        switch_vlan = {
            'deviceId': device_id,
            'vlanId': vlan_id,
            'primary': primary,
            'subnets': subnets,
            "tagPorts": tag_ports,
            "untagPorts": untag_ports
        }

        self._rest_switch_vlan_cfg_list.append(switch_vlan)

        return self

    def add_host_vlan(self, cfg):
        self._host_vlan_cfg_list.append(cfg)

        return self

    def del_host_vlan(self, device_id, vlan_id):
        response = requests.delete(
            URL+'staticrouting/v1/hostvlans/{}/{}'.format(device_id, vlan_id), headers=DELETE_HEADER)
        assert response.status_code == 200, 'Delete host vlans fail! ' + response.text

        return self

    def build_host_vlan(self, cfg):
        payload = {
            "deviceId": cfg['deviceId'],
            "vlanId": cfg['vlanId'],
            "tagPorts": cfg['tagPorts'],
            "untagPorts": cfg['untagPorts']
        }

        response = requests.post(
            URL+'staticrouting/v1/hostvlans', json=payload, headers=POST_HEADER)
        assert response.status_code == 200, 'Add host vlan fail! ' + response.text

        return self

    def build_switch_vlan(self, cfg):
        payload = {
            "deviceId": cfg['deviceId'],
            "vlanId": cfg['vlanId'],
            "subnets": cfg['subnets'],
            "tagPorts": cfg['tagPorts'],
            "untagPorts": cfg['untagPorts']
        }

        response = requests.post(
            URL+'staticrouting/v1/vlans', json=payload, headers=POST_HEADER)
        assert response.status_code == 200, 'Add switch vlan fail! ' + response.text

        return self

    def build_rest_switch_vlan(self, cfg):
        payload = {
            "deviceId": cfg['deviceId'],
            "vlanId": cfg['vlanId'],
            "primary": cfg['primary'],
            "subnets": cfg['subnets'],
            "tagPorts": cfg['tagPorts'],
            "untagPorts": cfg['untagPorts']
        }

        response = requests.post(
            URL+'staticrouting/v1/vlans', json=payload, headers=POST_HEADER)
        assert response.status_code == 200, 'Add rest switch vlan fail! ' + response.text

        return self

    def build(self):
        for cfg in self._switch_vlan_cfg_list:
            self.build_switch_vlan(cfg)
        for cfg in self._rest_switch_vlan_cfg_list:
            self.build_rest_switch_vlan(cfg)
        for cfg in self._host_vlan_cfg_list:
            self.build_host_vlan(cfg)

        return self
