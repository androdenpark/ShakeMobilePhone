



import urllib,urllib2,copy,time,json,httplib

__apiKey__="A5ADC758-D2E7-3330-96C52E3B267B"
__contextIDBase__="CT"
__contextURL__="http://ptopenlab.com/iotdm/api/"+__apiKey__+"/context/"

DeviceJsonObjNormal={}
DeviceJsonObjNormal["apikey"]=__apiKey__
DeviceJsonObjNormal["description"]="mobile phone"
DeviceJsonObjNormal["image"]="img5A7EC91C-680E-16B0-85B5E5FF29A1"
DeviceJsonObjNormal["manufacturedate"]=""
DeviceJsonObjNormal["typename"]="mobile"
DeviceJsonObjNormal["version"]="1.0"


__addDeviceUrl__="http://ptopenlab.com/iotdm/api/"+__apiKey__+"/devices"

def generateContextURL(theUUID):
    contextID=__contextIDBase__+theUUID
    return __contextURL__+contextID+"/device/"

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
    except :
        return False

def link2Context(theUUID):
    try:
        addContextURL=generateContextURL(theUUID)+theUUID+"/link"
        req=urllib2.Request(addContextURL,json.dumps({}),headers={'Content-type':'application/json'})
        responseText=urllib2.urlopen(req).read()
        if "true" in responseText:
            return True
        else:
            return 
    except Exception as e:
        print e
        return False

def unlinkFromContext(theUUID):
    try:
        unlinkContextURL=generateContextURL(theUUID)+theUUID+"/unlink"
        req=urllib2.Request(unlinkContextURL,json.dumps({}),headers={'Content-type':'application/json'})
        responseText=urllib2.urlopen(req).read()
        if "true" in responseText:
            return True
        else:
            return False
    except :
        return False
    
def getAllContextData():
    getAllContextDataURL=__contextURL__ +"current/all"
    try:
        responseText=urllib2.urlopen(getAllContextDataURL).read()
        deviceDict=json.loads(responseText)
        return deviceDict
    except:
        return None



if __name__=="__main__":
	getAllContextData()
	link2Context("TQIURGNTGNLMKMPWG78S")
	addDataStream("TQIURGNTGNLMKMPWG78S",123)
