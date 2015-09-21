import urllib,urllib2,copy,time,json,httplib

__apiKey__="4E919923-82F3-0A3B-9D95EAB66BAE"

__streamUrl__="http://ptopenlab.com/iotdm/api/"+__apiKey__+"/devicestreams"

StreamJsonObjNormal={}
StreamJsonObjNormal["typename"]="mobile"


def generateAddDataStreamJson(theUUID, theValue, theStreamName):
    returnJson=copy.deepcopy(StreamJsonObjNormal)
    returnJson["streamname"]=theStreamName
    returnJson["sn"]=theUUID
    returnJson["did"]=theUUID
    returnJson["cid"]=theUUID
    returnJson["value"]=str(theValue)
    return returnJson


def getDeviceStreamTypeList(theUUID):
    getStreamURL=__streamUrl__+"/"+theUUID+"/datastreams"
    try:
        responseText=urllib2.urlopen(getStreamURL).read()
        streamDictList=json.loads(responseText)
        return [value["streamname"] for value in streamDictList]
    except Exception as e:
        return None

def getStreamCurrentReading(theUUID, theStreamName):
    getStreamReadingURL=__streamUrl__+"/"+theUUID+"/datastreams/"+theStreamName
    try:
        responseText=urllib2.urlopen(getStreamReadingURL).read()
        streamReadingDict=json.loads(responseText)
        return int(streamReadingDict["value"])
    except Exception as e:
        return None

def getStreamHistoryList(theUUID, theStreamName):
    getStreamHistoryURL=__streamUrl__+"/"+theUUID+"/datastreams/"+ theStreamName +"/history"
    try:
        responseText=urllib2.urlopen(getStreamHistoryURL).read()
        streamHistoryDictList=json.loads(responseText)
        return [[value["timestamp"],value["value"]] for value in streamHistoryDictList]
    except Exception as e:
        return None

def addDataStream(theUUID, theValue, theStreamName):
    addDataStreamURL=__streamUrl__+"/"+theUUID+"/datastreams"
    try:
        dataSend=json.dumps(generateAddDataStreamJson(theUUID, theValue, theStreamName))
        req=urllib2.Request(addDataStreamURL,dataSend,headers={'Content-type':'application/json'})
        responseText= urllib2.urlopen(req).read()
        if "true" in responseText or "no context" in responseText:
            return True
        else:
            return False
    except Exception as e:
        return False  


if __name__== "__main__":
    addDataStream("UQ7SUOYZE1GPPFM5SADZDEMO", 3.15, "orientation_alpha")
