from django.template import loader, Context,RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

import time, datetime, random, json

from IotPlatformInterface import deviceOperation,streamOperation

__uuid_len__=20
__aliveTimeInterval__=3600
__lastRefreshTime__=datetime.datetime.now()


def registerDevicePageRequest(request):
    return render_to_response('deviceRegister.html',context_instance = RequestContext(request))


def shakePhonePageRequest(request):
    if request.method == 'POST' and request.POST.has_key("theName"):
        userName=request.POST['theName']
        userID=request.POST['theID']
        deviceOperation.link2Context(userID)
        return render_to_response('shakeYourPhone.html',{'name':userName,'ID':userID},
                                  context_instance = RequestContext(request))
    else:
        return registerDevicePageRequest(request)


def sorryPageRequest(request):
    return render_to_response('sorry.html',context_instance = RequestContext(request))


def introductionPageRequest(request):
    return render_to_response('introduction.html',context_instance = RequestContext(request))




def userDataPost(request):
    if request.POST.has_key("deviceIDRequest"):
        return getRegisterID(request)
    if request.POST.has_key("postScore"):
        return addScore2Stream(int(request.POST["scoreData"]),str(request.POST["theID"]))
    if request.POST.has_key("getScoreHistory"):
	return getHistory(request.POST["userID"])
    else:
        return render_to_response('deviceRegister.html',context_instance = RequestContext(request))





def getHistory(deviceID):
    try:
	theHistoryList=streamOperation.getStreamHistoryList(deviceID)
	historyDict={}
	historySortedList=[]
	for value in theHistoryList:
	    timestamp=int(value[0]/1000)
	    timestr=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
	    historySortedList.append([timestr[11:],int(value[1])])
	historyDict["historyList"]= historySortedList
	return HttpResponse(json.dumps(historyDict))
    except Exception as e:
	return HttpResponse("Error"+": "+ str(e))
		

def getRegisterID(request):
    try:
        theUUID=request.POST['deviceID']
        theName=request.POST['userName']
        if len(theUUID) < __uuid_len__ :
            theUUID=generateUUID(theName)
	else:
	    deviceOperation.addDevice(theName,theUUID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))		
        return HttpResponse(theUUID)
    except Exception as e:
        return HttpResponse('Error:'+str(e))



def addScore2Stream(theScore, deviceID):
    try:
        if not streamOperation.addDataStream(deviceID, theScore):
            return HttpResponse('Error:addDataStream failded!'+deviceID+" "+str(theScore))
        return HttpResponse(getRank(deviceID))
    except Exception as e:
        return HttpResponse(str(e)+'Error')


def getRank(theUUID):
    contextResponse=deviceOperation.getAllContextData()
    if contextResponse["CT"+theUUID][0] is None:
	return "Error"
    userInfoDict = contextResponse["CT"+theUUID][0]
    currentValue = userInfoDict["value"]
    currentTime = userInfoDict["timestamp"]
        
    userScoreList=sorted(refreshContextUser(currentTime,contextResponse), reverse=True)
    theRank=userScoreList.index(currentValue)+1
    try:
        thePlayingNum=userScoreList.index(0)+1
    except:
        thePlayingNum=len(userScoreList)
    finally:    
        return str(theRank)+"%"+str(thePlayingNum)
    

def refreshContextUser(theStamptime,userContextList):
    #if (datetime.datetime.now() - __lastRefreshTime__).seconds < __aliveTimeInterval__:
    #    return

    ScoreList=[]
    for key,streamData in userContextList.items():
	if streamData[0] is None:
	    continue
        if theStamptime - streamData[0]["timestamp"] > 1000*__aliveTimeInterval__:
            deviceOperation.unlinkFromContext(streamData[0]["did"])
	    continue
	ScoreList.append(streamData[0]["value"])

    return ScoreList
            
        
def generateUUID(theName):
    def UUIDGenerate(theLen):
        theUUID=''
        for i in range(theLen):
                theUUID += random.choice("ABCDEFGHIGKLMNOPQRSTUVWXYZ1234567890")
        return theUUID
       
    theUUID = UUIDGenerate(__uuid_len__)
    
    while(not deviceOperation.addDevice(theName,theUUID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
        theUUID = UUIDGenerate(__uuid_len__)
            
    return theUUID


