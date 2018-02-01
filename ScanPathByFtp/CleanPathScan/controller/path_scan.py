# -*- coding: utf-8 -*-
#from CleanPathScan.model.Tpath import Tpath
import os
import threading,multiprocessing
from CleanPathScan import app #,db
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from CleanPathScan.common.FtpScanner import FtpScanner
import json
import re
import time

@app.route('/')
def view_index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/doScan',methods=['POST'])
def doScan():
    try:
        ip = request.values.get('ip')
        port = request.values.get('port')
        email = request.values.get('email')

        result,msg = Vali(ip,port,email=email)

        if(not result):
            t = {'result': result, 'msg': msg}
            return json.dumps(t)
        #print("POST-"+ip + ":" + port)
        t = threading.Thread(target=StartScan, args=(ip,port,email))
        t.start()
        print("异步完成")
        t={ 'result':True, 'msg' : "后台已经开始扫描，可以关闭页面但不要断开WIFI或关闭手机FTP程序"}
    except Exception as ex:
        t = {'result': False, 'msg': str(ex)}

    return json.dumps(t)

@app.route('/doTest',methods=['POST'])
def doTest():
    try:
        ip = request.values.get('ip')
        port = request.values.get('port')
        email = request.values.get('email')

        result,msg = Vali(ip,port,email)
        if(not result):
            t = {'result': result, 'msg': msg}
            return json.dumps(t)

        time.sleep(1)
        ftp = FtpScanner(ip,port, None)
        result = ftp.test()
        t = {'result': result, 'msg': u"连接测试成功！"}
    except Exception as ex:
        t = {'result': False, 'msg': unicode(str(ex), errors='ignore')}
        #return json.dumps(t)
    return json.dumps(t)

"""
扫描的异步方法
"""
def StartScan(ip,port,email):
    ftp = FtpScanner(ip, port, email)
    ftp.sum_file("/")

"""
验证参数
"""
def Vali(ip,port,email=""):
    rip = r"^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$"
    if not re.match(rip, ip):
        return False, "IP验证错误！"

    rport = r"^([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$"
    if not re.match(rport, port):
        return False, "端口号验证错误！"

    if(email):
        if( not email.lower().endswith("30.net")):
            return False,"请使用@30.net邮箱"

    return  True,"验证成功"
