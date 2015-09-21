#name: aDemoOnPhone@163.com
#password: aDemoOnPhone
#API key:4E919923-82F3-0A3B-9D95EAB66BAE

import urllib,urllib2,copy,time,json,httplib

__apiKey__="4E919923-82F3-0A3B-9D95EAB66BAE"

DeviceJsonObjNormal={}
DeviceJsonObjNormal["apikey"]=__apiKey__
DeviceJsonObjNormal["description"]="mobile phone"
DeviceJsonObjNormal["image"]="img5A7EC91C-680E-16B0-85B5E5FF29A1"
DeviceJsonObjNormal["manufacturedate"]=""
DeviceJsonObjNormal["typename"]="mobile"
DeviceJsonObjNormal["version"]="1.0"


__addDeviceUrl__="http://ptopenlab.com/iotdm/api/"+__apiKey__+"/devices"

def generateAddDeviceJson(theName, theUUID, theCreateTime):
    returnJson=copy.deepcopy(DeviceJsonObjNormal)
    returnJson["sn"]=theUUID
    returnJson["did"]=theUUID
    returnJson["name"]=theName
    DeviceJsonObjNormal["registerdate"]=theCreateTime
    return returnJson

def addDevice(theName, theUUID, theCreateTime):
    try:
        dataSend=json.dumps(generateAddDeviceJson(theName, theUUID, theCreateTime))
        req=urllib2.Request(__addDeviceUrl__,dataSend,headers={'Content-type':'application/json'})
        responseText= urllib2.urlopen(req).read()
        if "true" in responseText or "registered" in responseText:
            return True
        else:
            return False
    except :
        return False



def deleteDeviceByUUID(theUUID):
    try:
        deleteDeviceURL=__addDeviceUrl__+"/"+theUUID
        req=urllib2.Request(deleteDeviceURL)
        req.get_method=lambda:"DELETE"
        responseText=urllib2.urlopen(req).read()
        if "true" in responseText:
            return True
        else:
            return False
    except :
        return False




