import urllib2
import re

def GetOutSideIpAdd():
    url = urllib2.urlopen("http://txt.go.sohu.com/ip/soip")
    text = url.read()
    ip = re.findall(r'\d+.\d+.\d+.\d+',text)
    return ip