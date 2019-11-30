import argparse
import os
import LogHelp
import AliHelper
import Syshelper
from AliHelper import *
from Syshelper import *
parser = argparse.ArgumentParser()
FuncDomainMap=[]
needMakeServer = False
intervaltime = ""
supplier = "aliyun"
apikey = ""
secretkey = ""
logC = ""
domainType = "A"
domainRR = ""
domain=""

def init(ar):
    global needMakeServer,intervaltime,supplier,apikey,secretkey,logC,domainType,domainRR,domain,FuncDomainMap
    if ar.service:
        needMakeServer = True
    if ar.intervaltime:
        intervaltime = ar.intervaltime
    if ar.S and ar.S in ["aliyun","huawei","aliyun","google","tencent","baidu"]:
        supplier = ar.S
    if ar.A:
        apikey = ar.A
    if ar.K:
        secretkey = ar.K
    if ar.log:
        atlastfilename = ""
        if not os.path.exists(ar.log):
            try:
                fd = open(ar.log, mode="w", encoding="utf-8")
                fd.close()
                atlastfilename = ar.log
            except:
                print("the dir input is not a file path string;")
                return False
        else:
            atlastfilename = ar.log
        if os.path.isdir(atlastfilename):
            print("file name will change to "+atlastfilename +"\\ddns_log.log")
            atlastfilename += "\\ddns_log.log"
        logC = LogHelp
        logC.__init__(atlastfilename)
    if apikey == "" or secretkey == "":
        return False
    if intervaltime == "":
        intervaltime = "* * 1 * *"
    if ar.DT:
        domainType = ar.DT
    if ar.RR:
        domainRR = ar.RR
    else:
        print("you need set a Domain RR")
        exit(-1)
    if ar.D:
        domain = ar.D
    else :
        print("you need set a Domain to Update")
        exit(-1)        
    FuncDomainMap["aliyun"] = AliHelper.Alilib
    return True

if __name__ == '__main__':
    parser.description="Version v0.0"
    parser.add_argument("-s","--service", help="Make this programe like a service to use,default is work per day")
    parser.add_argument("-l","--log", help="set a Log File ,default no log output")
    parser.add_argument("-it","--intervaltime",help="work interval time,use crontab,e.q. */2 * * * *")
    parser.add_argument("-S",help="Supplier,default is aliyun,you can choose in huawei,aliyun,google,tencent,baidu")
    parser.add_argument("-A",help="the api key to use")
    parser.add_argument("-K",help="the secret key to use")
    parser.add_argument("-RR",help="set RR to update domain")
    parser.add_argument("-DT","--domain-type",help="set update domain type,default is A type")
    parser.add_argument("-D","--domain",help="set update Domain Name")
    if not init(parser.parse_args()):
        exit(0)

    FuncDomainMap[supplier].__init__(apikey,secretkey,domain,domainRR,domainType,logC,"cn-hangzhou")
    FuncDomainMap[supplier].main()