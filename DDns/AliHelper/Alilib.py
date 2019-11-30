# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import Syshelper
from Syshelper import *
from datetime import datetime
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

_id=""
_secret=""
_region=""
_DomainName=""
_RR=""
_DomainType=""
_UpdateDomain=""
_client = ""
_FuncLog = ""
def __init__(accessKey,accessKeySecret,domain,rr,domaintype,FuncLog,region="cn-hangzhou"):
    global _id,_secret,_region,_DomainName,_RR,_DomainType,_client,_FuncLog
    _id = accessKey
    _secret=accessKeySecret
    _DomainName=domain
    _RR = rr
    _DomainType=domaintype
    _region = region
    _FuncLog = FuncLog
    try:
        _client = AliAccessKey()
    except Exception as e:
        FuncLog.WriteLog(e,2)
        exit(0)

def AliAccessKey():
    global _id,_secret,_region
    try:
        client = AcsClient(_id, _secret, _region)
        return client
    except Exception as e:
        print("验证aliyun key失败")
        print(e)
        _FuncLog.WriteLog(e,2)

def GetDNSRecordId(rr,client,DomainName):
    global _FuncLog
    try:
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))

        for RecordId in json_data['DomainRecords']['Record']:
            if rr == RecordId['RR']:
                return RecordId['RecordId']

    except Exception as e:
        print("Fail to get RecorId")
        print(e)
        _FuncLog.WriteLog(e,2)
        sys.exit(-1)

def UpdateDomainRecord(client,RecordId):
    global _RR,_DomainType,_client,_DomainName,_FuncLog
    try:
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')
        DomainValue = Syshelper.syslib.GetOutSideIpAdd()
        request.set_Value(DomainValue)
        request.set_Type(_DomainType)
        request.set_RR(_RR)
        request.set_RecordId(RecordId)
        response = _client.do_action_with_exception(request)
        msg = "Success update Domain value \r\nDomain:" + _DomainName + " Host:" + _RR + " DomainType:" + _DomainType + " Value:" +  DomainValue
        print(msg)
        _FuncLog.WriteLog(msg,0)
    except Exception as e:
        print("Update Domain Error:")
        print(e)
        _FuncLog.WriteLog(e,2)

def main():
    global _id,_secret,_region,_DomainName,_RR,_DomainType,_client
    RecordId = GetDNSRecordId(_RR,_client,_DomainName)
    UpdateDomainRecord(client,RecordId)