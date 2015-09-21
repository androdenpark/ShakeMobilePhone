import urllib,urllib2,copy,time,json,httplib


__apiKey__="A5ADC758-D2E7-3330-96C52E3B267B"

DeviceJsonObjNormal={}
DeviceJsonObjNormal["apikey"]=__apiKey__
DeviceJsonObjNormal["description"]="mobile phone"
DeviceJsonObjNormal["image"]="img5A7EC91C-680E-16B0-85B5E5FF29A1"
DeviceJsonObjNormal["manufacturedate"]=""
DeviceJsonObjNormal["typename"]="mobile"
DeviceJsonObjNormal["version"]="1.0"


__addDeviceUrl__="http://ptopenlab.com/iotdm/api/"+__apiKey__+"/devices"

def generateAddDeviceJson(theName, theUUID, theCreateTime):
    #returnJson=copy.deepcopy(DeviceJsonObjNormal)
    returnJson=DeviceJsonObjNormal
    returnJson["sn"]=theUUID
    returnJson["did"]=theUUID
    returnJson["name"]=theName
    DeviceJsonObjNormal["registerdate"]=theCreateTime
    return returnJson

def addDevice(theName, theUUID, theCreateTime):
    try:
        dataSend=json.dumps(generateAddDeviceJson(theName, theUUID, theCreateTime))
        req=urllib2.Request(__addDeviceUrl__,dataSend,headers={'Content-type':'application/json'})
        responseText= urllib2.urlopen(req, timeout=50).read()
        if "true" in responseText:
            return True
        else:
            print responseText
            return False
    except Exception as e:
        print e
        return False


def getDeviceList():
    try:
        responseText=urllib2.urlopen(__addDeviceUrl__).read()
        deviceDict=json.loads(responseText)
        return [value["did"] for value in deviceDict] 
    except:
        return None

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
    except Exception as e:
        print e
        return False



if __name__=="__main__":
    print addDevice("tryt", "sdgfdsgfdshgfdh",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
    #print getDeviceList()
    print deleteDeviceByUUID("S3E5B98")
