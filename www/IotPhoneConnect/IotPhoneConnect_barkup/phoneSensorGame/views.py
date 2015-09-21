from django.shortcuts import render

# Create your views here.

from django.template import loader, Context,RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response

import time, datetime, random

from  IotPlatformInterface import deviceOperation,streamOperation

__uuid_len__=15
__aliveTimeInterval__=3600

__maxUserNum__=500

__userScoreList__=[]

__userScoLRefTime__=datetime.datetime.now()
__userScoLRefInterval__=1

#userInfo={"name":"zyy","visitTime":datatime.datetime.now(),"score":0}
#__aliveUserList__=[]
__aliveUserDict__={}


def registerDevicePageRequest(request):    
    return render_to_response('deviceRegister.html',context_instance = RequestContext(request))

def shakePhonePageRequest(request):
    if request.method == 'POST' and request.POST.has_key("theName"):
        userName=request.POST['theName']
        userID=request.POST['theID']+request.POST['registerTime']
        if registerUser(userID, userName) is None:
            userID='INVALID'
        return render_to_response('shakeYourPhone.html',{'name':userName,'ID':userID},
                                  context_instance = RequestContext(request))
    else:
        return registerDevicePageRequest(request)


def userDataPost(request):
    #print __aliveUserList__
    if request.POST.has_key("deviceIDRequest"):
        return getRegisterNum(request)
    if request.POST.has_key("heartBeat"):
        return heartBeatProcess(str(request.POST["heartBeat"]),int(request.POST["score"]),request.POST.has_key("reset"))
    else:
        return render_to_response('deviceRegister.html',context_instance = RequestContext(request))


def getRegisterNum(request):
    print __aliveUserDict__
    #userName=request.POST['name']
    try:
        theUUID=request.POST['deviceID']
        #finaleUUID =addUser2List(str(theUUID),str(userName))
        if len(theUUID) < __uuid_len__ :
            theUUID=generateUUID()
        return HttpResponse(theUUID)
    except Exception as e:
        print e
        return HttpResponse('Exception Occurs')
    

def heartBeatProcess(theUUID,theScore, isReset):
    print __aliveUserDict__
    try:
        if not __aliveUserDict__.has_key(theUUID) :
            return HttpResponse('No user info,need to login again!')
        else:
            userInfo=__aliveUserDict__[theUUID]
            userInfo["visitTime"]=datetime.datetime.now()
            if isReset :               
                streamOperation.addDataStream(theUUID.split("%")[0], userInfo["score"])
                userInfo["score"]=0
            elif userInfo["score"] < theScore:                
                userInfo["score"]=theScore
            return HttpResponse(getRank(theUUID))
    except Exception as e:
        print e
        return HttpResponse('error, need to login again!')


def userScoreListRefresh():
    if (__userScoLRefTime__-datetime.datetime.now()).seconds<__userScoLRefInterval__:
        return __userScoreList__
    
    __userScoreList__=[]

    for key, value in __aliveUserDict__.items():
        if((datetime.datetime.now()-value["visitTime"]).seconds > __aliveTimeInterval__):
	    try:
	    	del __aliveUserDict__[key]
            	deviceOperation.deleteDeviceByUUID(key.spilt("%")[0])
            	continue
	    except:
		pass
            
        value["scoreForRank"]=value["score"]
        __userScoreList__.append(value["scoreForRank"])

    return sorted(__userScoreList__, reverse=True)

def getRank(theUUID):
    theScoreList=userScoreListRefresh()
    theScore=(__aliveUserDict__[theUUID])["scoreForRank"]
    theRank=theScoreList.index(theScore)+1
    try:
        thePlayingNum=theScoreList.index(0)+1
    except:
        thePlayingNum=len(theScoreList)
    finally:
        return str(theRank)+"%"+str(thePlayingNum)+"%"+str(theScore)
        
def generateUUID():
    def UUIDGenerate(theLen):
        theUUID=''
        for i in range(theLen):
                theUUID += random.choice("ABCDEFGHIGKLMNOPQRSTUVWXYZ1234567890")
        return theUUID+"%"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

    #theUUID=deleteDeadUser()
    #if theUUID is not None:
    #    return theUUID
    #else:        
    theUUID = UUIDGenerate(__uuid_len__)
    while(__aliveUserDict__.has_key(theUUID)):
        theUUID = UUIDGenerate(__uuid_len__)
            
    return theUUID

#userInfo={"name":"zyy","ID":"ADSFSAFDSAFDSAF","visitTime":datatime.datetime.now(),"score":0}

def deleteDeadUser():
    for key, value in __aliveUserDict__.items():
        if((datetime.datetime.now()-value["visitTime"]).seconds > __aliveTimeInterval__):
	    try:
            	del __aliveUserDict__[key]
            	deviceOperation.deleteDeviceByUUID(key.spilt("%")[0])
            	return key
	    except:
		return key
    return None

def addUser2List(theUUID, userName):
    if len(__aliveUserDict__) >= __maxUserNum__ and not __aliveUserDict__.has_key(theUUID):
            return None

    userInfo={}
    userInfo["name"]=userName
    userInfo["visitTime"]=datetime.datetime.now()
    userInfo["score"]=0

    if not __aliveUserDict__.has_key(theUUID):
        deviceInfo=theUUID.split("%")
        deviceDID=deviceInfo[0]
        deviceCreateTime=deviceInfo[1]
	if not deviceOperation.addDevice(userName,deviceDID,deviceCreateTime):
		print "failed to add device!"
    
    __aliveUserDict__[theUUID]=userInfo
    return theUUID      

def userInfoReset(theUUID, userName):
    userInfo=__aliveUserDict__[theUUID]
    userInfo["name"]=userName
    userInfo["visitTime"]=datetime.datetime.now()
    userInfo["score"]=0
    return True


def registerUser(theUUID, theName):
    if not __aliveUserDict__.has_key(theUUID):
        return addUser2List(theUUID,theName)
    else:
        return userInfoReset(theUUID,theName)        








