# -*- coding: utf-8 -*-
import logging
import os,time

class Logger():
    # 创建一个logger
    logger = logging.getLogger('mylogger')

    def getInstans(self):
        return self.logger;

    def __init__(self):
        # 创建一个logger
        #logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        filename =  time.strftime('%Y%m%d', time.localtime(time.time()))
        fh = logging.FileHandler(os.getcwd()+'/CleanPathScan/logs/'+filename+'.log')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
