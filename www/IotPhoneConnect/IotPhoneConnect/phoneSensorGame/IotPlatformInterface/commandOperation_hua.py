
import urllib,urllib2,copy,time,json,httplib,pycurl


DeviceJsonObjNormal={}
DeviceJsonObjNormal["aid"]=""
DeviceJsonObjNormal["cid"]=""
DeviceJsonObjNormal["did"]=""
DeviceJsonObjNormal["typename"]=""
DeviceJsonObjNormal["command"]="shakeSpeed"
DeviceJsonObjNormal["paramsType"]=""
DeviceJsonObjNormal["params"]=0

__carAURL__="https://crl.ptopenlab.com:8800/iotdm/api/A5ADC758-D2E7-3330-96C52E3B267B/context/820b41ce-152e-4341-9bea-7ccfb75e3beb/executecommand"
__carBURL__="https://crl.ptopenlab.com:8800/iotdm/api/A5ADC758-D2E7-3330-96C52E3B267B/context/5b6b5a91-9b70-4801-a00a-0e6b975d61be/executecommand"

__header__ = ['Accept:*/*', 'Content-Type:application/json']

def selectURL(deviceID):
    if "lucy" in  deviceID:
	return __carAURL__
    else:
	return __carBURL__ 

def generateJson(value):
    DeviceJsonObjNormal["params"]=value
    return json.dumps(DeviceJsonObjNormal)

def commandOperation_old(deviceID, scoreValue):
    try:
        dataSend=json.dumps(generateJson(scoreValue))
        req=urllib2.Request(selectURL(deviceID),dataSend,headers={'Content-type':'application/json'})
        responseText= urllib2.urlopen(req).read()
        if "true" in responseText:
            return True
        else:
            return False
    except :
        return False

def commandOperation(deviceID, scoreValue):
    try:
        dataSend=generateJson(scoreValue)
	sendRequest=pycurl.Curl()
	sendRequest.setopt(pycurl.POST,1)
	sendRequest.setopt(pycurl.URL,selectURL(deviceID))
	sendRequest.setopt(pycurl.HTTPHEADER, __header__)
	sendRequest.setopt(pycurl.POSTFIELDS,dataSend)
	sendRequest.perform()
        if sendRequest.getinfo(pycurl.RESPONSE_CODE) == 200:
            return True
        else:
            return False
    except :
        return False

