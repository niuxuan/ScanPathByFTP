# -*- coding: utf-8 -*-
import time
import re
import os
import uuid
from ftplib import FTP
#from MSSQL import MSSQL
from SqliteHelper import DataHelper
from SmtpMail import SmtpMail
from LogHelper import Logger
import sys;
sys.path;

class FtpScanner():
    ftp = FTP()
    ip = "172.26.115.151"
    port = 2121
    name = ""
    sum1 = 0
    sum2 = 0
    value = 0
    batch = ''
    phoneSign = ''
    db = DataHelper("../database/pathdata.db3")
    email = None
    logger = Logger().getInstans();

    #递归搜索文件
    def search_file(self, start_dir, tcode):
        try:
            innerSum = 0;
            innerValue = 0;
            self.ftp.cwd(start_dir)
            dir_res = []
            self.ftp.dir('.', dir_res.append)  # 对当前目录进行dir()，将结果放入列表
            start_dir = start_dir.replace("//", "/");
            itindex = 1;
            for i in dir_res:
                if i.startswith("d"):
                    self.sum1 += 1
                    # search_file(ftp.pwd() + "/" + i.split(" ")[-1])
                    rpath = r'tencent|nubia|huawei'
                    rm = re.search(rpath,start_dir.lower())
                    #if (not start_dir.lower().__contains__("tencent") and not start_dir.lower().__contains__("nubia")):
                    if rm is None:
                        innerValue += self.search_file(
                            start_dir + "/" + re.split("\d+\s[A-Za-z]+\s\d{2}\s(\d{2}):(\d{2})\s", i)[-1],
                            '{0}-{1}'.format(tcode, itindex))
                        itindex += 1
                        self.ftp.cwd('..')
                else:
                    self.sum2 += 1
                    innerSum += 1;
                    itindex += 1
                    # val = i.split(" ")[-1]
                    val = re.split("\d+\s[A-Za-z]+\s\d{2}\s(\d{2}):(\d{2})\s", i)[-1]
                    self.value += self.ftp.size(val)
                    innerValue += self.ftp.size(val)
                    if start_dir.endswith('/'):
                        # print("父级："+tcode + "   自级：" + '{0}-{1}'.format(tcode,itindex)+ "   " + ftp.pwd()+val+"     "+str(ftp.size(val))+" B")   #打印出每个文件路径和大小

                        self.addPath('{0}-{1}'.format(tcode, itindex), tcode, start_dir + val, 0, self.ftp.size(val))
                        pass
                    else:
                        # print("父级："+tcode + "   自级：" + '{0}-{1}'.format(tcode,itindex)+ "   " + ftp.pwd()+"/"+val+"     "+str(ftp.size(val))+" B")
                        self.addPath('{0}-{1}'.format(tcode, itindex), tcode, start_dir + "/" + val, 0, self.ftp.size(val))
                        pass
            # print("父级："+"-".join(tcode.split('-')[0:len(tcode.split('-'))-1]) + "   自级：" + tcode+"  folder [" + ftp.pwd() +"] file number is " + str(innerSum) + ", Totle size is " + str(innerValue) + " B")
            self.addPath(tcode, "-".join(tcode.split('-')[0:len(tcode.split('-')) - 1]), start_dir, 1, innerValue)
            return innerValue;
        except Exception as ex:
            self.logger.error("{2} {3} 扫描出现异常：{0}  {1}".format(start_dir, '{0}-{1}'.format(tcode, itindex),self.ip, self.phoneSign));
            self.logger.error(ex);
        finally:
            return innerValue;

    #扫描文件
    def sum_file(self,file_path):
        start = time.time()
        self.GetPhoneSign();
        self.createDataBase();

        self.logger.info("{0}:{1},{2} 开始扫描：".format(self.ip,self.port,self.phoneSign))
        self.search_file(file_path, '0')
        self.logger.info( "folder number is " + str(self.sum1) + ", file number is " + str(self.sum2) + ", Totle size is " + str(self.value) + " B")
        end = time.time()
        if(self.email != None and self.email != ""):
            s = SmtpMail(self.email)
            s.SendEmail(str(self.sum1),str(self.sum2),self.value, round(end - start,2),self.ip);

    #添加路径到数据库
    def addPath(self,scode, pcode, path, isFolder, size):
        try:
            #print("父级：" + pcode + "   自级：" + scode + "   " + path + "      " + str(size) + " B")
            """
            self.ms.ExecNonQuery(
                r"insert into Tpath values('{0}','{1}','{2}',{3},{4},'{5}','{6}')".format(scode, pcode, path,
                                                                                                 isFolder, size, self.batch,
                                                                                                 self.phoneSign));
            """
            self.db.table("TPath").insert(scode=scode, pcode=pcode, path=path, isFolder=isFolder, size=size, batch=self.batch, phoneSign=self.phoneSign);
            self.db.execute();

        except Exception as ex:
            self.logger.error(
            "{0} {1} 数据录入异常： 父级：{2}  自级：{3}  路径：{4} 大小：{5}".format(self.ip, self.phoneSign, pcode,scode,path,str(size)));
            self.logger.error(ex);
            pass

    #创建数据库
    def createDataBase(self):
        self.batch = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        filename = self.batch.replace("-","").replace(" ","").replace(":","")
        dir = os.getcwd()+"\\CleanPathScan\\database\\"+self.ip+"\\"+self.phoneSign+"\\"
        self.logger.info(dir)
        if not os.path.exists(dir):
            os.makedirs(dir);

        self.logger.info(dir + "\\"+filename+".db3")
        self.db = DataHelper(dir + "\\"+filename+".db3")
        self.db.open()  # 打开数据库
        try:
            self.db.execute(
                "create table TPath (id INTEGER PRIMARY KEY AUTOINCREMENT, scode varchar(50),pcode varchar(50),path nvarchar(500),isFolder int, size double, batch varchar(20), phoneSign varchar(50))"
            )
        except:
            self.logger.error("Create table failed")
            self.db.table("TPath").delete("1=1")
            self.db.execute();
            self.db.execute("update sqlite_sequence set seq=0 where name='TPath'; ");

    #制造手机标识
    def GetPhoneSign(self):
        currenPath = "/";
        try:
            self.ftp.cwd(".FTPcleanScan");
            currenPath = ".FTPcleanScan"
            dir_res = []
            self.ftp.dir('.', dir_res.append)  # 对当前目录进行dir()，将结果放入列表

            if (len(dir_res) > 0):  # 存在目录时
                self.phoneSign = re.split("\d+\s[A-Za-z]+\s\d{2}\s(\d{2}):(\d{2})\s", dir_res[-1])[-1]
                self.logger.info("获取标识成功：" + ".FTPcleanScan/" + self.phoneSign)
            else:  # 不存在目录时创建
                self.phoneSign = str(uuid.uuid1())
                self.ftp.mkd(self.phoneSign)
                self.logger.info("创建标识成功1：" +".FTPcleanScan/"+ self.phoneSign)
        except Exception as ex:
            if (str(ex) == "250 Directory created"):
                self.logger.info("创建标识成功2：" + ".FTPcleanScan/" + self.phoneSign)
            else:
                # phoneSign = uuid.uuid1()
                self.NoPermissionGetPhoneSign(currenPath)

    #无权限时造出手机标识
    def NoPermissionGetPhoneSign(self,currenPath):
        noRootPath = True
        try:
            self.phoneSign = str(uuid.uuid1())
            if(currenPath=="/"):
                self.ftp.mkd(".FTPcleanScan")
                noRootPath = False
                self.ftp.mkd(".FTPcleanScan/" + self.phoneSign)
            else:
                noRootPath = False
                self.ftp.mkd(self.phoneSign)
            self.logger.info("创建标识成功3：" + ".FTPcleanScan/" + self.phoneSign)
        except Exception as ex:
            if (str(ex) == "250 Directory created"):
                if(noRootPath):
                    try:
                        self.ftp.mkd(".FTPcleanScan/" + self.phoneSign)
                    except:
                        pass
                    self.logger.info("创建标识成功4：" + ".FTPcleanScan/" + self.phoneSign)
                self.logger.info("创建标识成功5：" + ".FTPcleanScan/" + self.phoneSign)
            else:
                self.phoneSign = "{0},{1}".format(self.ip, self.name)
                self.logger.info("创建标识成功6：" + ".FTPcleanScan/" + self.phoneSign)

    #测试连接
    def test(self):
        try:
            self.logger.info("{0}:{1},{2} 连接测试：".format(self.ip, self.port, self.phoneSign))
            self.ftp.cwd("/");
            self.logger.info("{0}:{1},{2} 连接测试成功：".format(self.ip, self.port, self.phoneSign))
            return True
        except:
            return False

    def __init__(self,ip,port,email):
        self.ip  = str(ip)
        self.port = intern(str(port))
        self.ftp = FTP()
        self.email = email
        self.ftp.connect(self.ip, self.port);  # 连接的ftp sever和端口
        self.ftp.login("", "");  # 连接的用户名，密码
        self.ftp.encoding = "utf-8";


