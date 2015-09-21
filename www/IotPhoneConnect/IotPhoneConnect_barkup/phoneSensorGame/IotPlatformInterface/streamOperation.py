
import urllib,urllib2,copy,time,json,httplib

__apiKey__="A5ADC758-D2E7-3330-96C52E3B267B"

__streamUrl__="http://ptopenlab.com/iotdm/api/"+__apiKey__+"/devicestreams"
__streamName__="score"

StreamJsonObjNormal={}
StreamJsonObjNormal["streamname"]=__streamName__
StreamJsonObjNormal["typename"]="mobile"

def generateAddDataStreamJson(theUUID, theValue):
    returnJson=StreamJsonObjNormal
    returnJson["sn"]=theUUID
    returnJson["did"]=theUUID
    returnJson["cid"]=theUUID
    returnJson["value"]=str(theValue)
    return returnJson


def getDeviceDataStreamList(theUUID):
    getStreamURL=__streamUrl__+"/"+theUUID+"/datastreams"
    try:
        responseText=urllib2.urlopen(getStreamURL).read()
        streamDictList=json.loads(responseText)
        return [value["streamname"] for value in streamDictList]
    except Exception as e:
        print e
        return None

def getStreamCurrentReading(theUUID):
    getStreamReadingURL=__streamUrl__+"/"+theUUID+"/datastreams/"+__streamName__
    try:
        responseText=urllib2.urlopen(getStreamReadingURL).read()
        streamReadingDict=json.loads(responseText)
        return int(streamReadingDict["value"])
    except Exception as e:
        print e
        return None

def getStreamHistoryList(theUUID):
    getStreamHistoryURL=__streamUrl__+"/"+theUUID+"/datastreams/"+__streamName__+"/history"
    try:
        responseText=urllib2.urlopen(getStreamHistoryURL).read()
        streamHistoryDictList=json.loads(responseText)
        return [int(value["value"]) for value in streamHistoryDictList]
    except Exception as e:
        print e
        return None

def addDataStream(theUUID, theValue):
    return
    addDataStreamURL=__streamUrl__+"/"+theUUID+"/datastreams"
    try:
        dataSend=json.dumps(generateAddDataStreamJson(theUUID, theValue))
        req=urllib2.Request(addDataStreamURL,dataSend,headers={'Content-type':'application/json'})
        responseText= urllib2.urlopen(req).read()
        if "true" in responseText:
            return True
        else:
            print responseText
            return False
    except Exception as e:
        print e
        return False  


if __name__=="__main__":
    print addDataStream("S3E5B98", 103)
    print getDeviceDataStreamList("S3E5B98")
    print getStreamCurrentReading("S3E5B98")
    print getStreamHistoryList("S3E5B98")
