import urllib,urllib2,copy,time,json,httplib

__apiKey__="A5ADC758-D2E7-3330-96C52E3B267B"

__streamUrl__="http://ptopenlab.com/iotdm/api/"+__apiKey__+"/devicestreams"

StreamJsonObjNormal={}
StreamJsonObjNormal["typename"]="mobile"

__score__='score'




def generateAddDataStreamJson(theUUID, theValue, theStreamName=__score__):
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

def getStreamCurrentReading(theUUID, theStreamName=__score__):
    getStreamReadingURL=__streamUrl__+"/"+theUUID+"/datastreams/"+theStreamName
    try:
        responseText=urllib2.urlopen(getStreamReadingURL).read()
        streamReadingDict=json.loads(responseText)
        return int(streamReadingDict["value"])
    except Exception as e:
        return None

def getStreamHistoryList(theUUID, theStreamName=__score__):
    getStreamHistoryURL=__streamUrl__+"/"+theUUID+"/datastreams/"+ theStreamName +"/history"
    try:
        responseText=urllib2.urlopen(getStreamHistoryURL).read()
        streamHistoryDictList=json.loads(responseText)
        return [[value["timestamp"],value["value"]] for value in streamHistoryDictList]
    except Exception as e:
        return None

def addDataStream(theUUID, theValue):
    addDataStreamURL=__streamUrl__+"/"+theUUID+"/datastreams"
    try:
        dataSend=json.dumps(generateAddDataStreamJson(theUUID, theValue))
        req=urllib2.Request(addDataStreamURL,dataSend,headers={'Content-type':'application/json'})
        responseText= urllib2.urlopen(req).read()
        if "true" in responseText:
            return True
        else:
            return False
    except Exception as e:
        return False  

if __name__=="__main__":
	addDataStream("U0LI86G0Q2BMZOXF4GGL",123)
