import base64

controller = {
    'ip': '192.168.3.1',
    'port': 6653
}

API_BASE_URL = "http://" + controller['ip'] + ":8181/mars/"

# admin username
ADMIN_USERNAME = 'karaf'
ADMIN_PASSWORD = 'karaf'

# admin login
LOGIN = base64.b64encode(bytes('{}:{}'.format(ADMIN_USERNAME, ADMIN_PASSWORD)))

s1 = {
    'id': 'of:0000000000000001'
}
s2 = {
    'id': 'of:0000000000000002'
}
s3 = {
    'id': 'of:0000000000000003'
}
s4 = {
    'id': 'of:0000000000000004'
}
