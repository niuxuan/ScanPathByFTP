# -*- coding: utf-8 -*-
from CleanPathScan import app
#异步处理
from gevent import monkey
from gevent.pywsgi import WSGIServer

"""
@app.route('/')
def hello_world():
    return 'Hello World!'
"""

monkey.patch_all()

if __name__ == '__main__':
    #app.run(debug=True)
    http_server = WSGIServer(('192.168.1.76', 5000), app)
    http_server.serve_forever()