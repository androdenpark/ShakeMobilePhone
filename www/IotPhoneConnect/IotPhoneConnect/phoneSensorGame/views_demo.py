from django.template import loader, Context,RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
import time, datetime, random, json
from IotPlatformInterface import deviceOperation_demo, streamOperation_demo

__uuid_len__=20+4

def demo_getPageByIDRequest(request, deviceID):
    if len(deviceID) != __uuid_len__ :
	return HttpResponse("undefined url, please check it!")
    
    deviceID=demo_registerDevice(deviceID, "DemoUser")

    if deviceID is None:
	return HttpResponse("Error!")

    return render_to_response('phoneSensorCenter_demo.html',{'ID':deviceID},
                                        context_instance = RequestContext(request))

def demo_getIntroPageRequest(request, deviceID):
    if len(deviceID) != __uuid_len__ :
	return HttpResponse("undefined url, please check it!")
    
    deviceID=demo_registerDevice(deviceID, "DemoUser")

    if deviceID is None:
	return HttpResponse("Error!")

    return render_to_response('demoIntroduction.html',{'userID':deviceID},context_instance = RequestContext(request))



def demo_userDataPost(request):
    if request.POST.has_key("postStreamData"):
	return demo_addStreamData(request)
    if request.POST.has_key("getStreamHistory"):
	return demo_getStreamHistory(request.POST["deviceID"], request.POST["streamName"])
    else:
        return render_to_response("No page found!")


def demo_getStreamHistory(deviceID, streamName):
    try:
	theHistoryList=streamOperation_demo.getStreamHistoryList(deviceID, streamName)
	historyDict={}
	historySortedList=[]
	for value in theHistoryList:
	    timestamp=int(value[0]/1000)
	    timestr=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
	    historySortedList.append([timestr[11:],float(value[1])])
	historyDict["historyList"]= historySortedList
	return HttpResponse(json.dumps(historyDict))
    except Exception as e:
	return HttpResponse("Error"+": "+ str(e))
		

def demo_registerDevice(theUUID, theName):
    try:
        #theUUID=request.POST['deviceID']
        #theName="DemoUser"
        if len(theUUID) < __uuid_len__ :
            theUUID=demo_generateUUID(theName)
	else:
	    deviceOperation_demo.addDevice(theName, theUUID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))		
        return theUUID
    except Exception as e:
        return None


def demo_addStreamData(request):
    try:
	deviceID=request.POST["deviceID"]
	postData=json.loads(request.POST["content"])
	for value in postData:
     	    if not streamOperation_demo.addDataStream(deviceID, float(value["value"]), value["name"]):
            	return HttpResponse('Error: addDataStream failded'+" at "+ str(value))
        return HttpResponse("Success")
    except Exception as e:
        return HttpResponse("Error: "+str(e))

        
def demo_generateUUID(theName):
    def UUIDGenerate(theLen):
        theUUID=''
        for i in range(theLen):
                theUUID += random.choice("ABCDEFGHIGKLMNOPQRSTUVWXYZ1234567890")
        return theUUID+"DEMO"
       
    theUUID = UUIDGenerate(__uuid_len__)
    
    while(not deviceOperation_demo.addDevice(theName,theUUID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))):
        theUUID = UUIDGenerate(__uuid_len__)
            
    return theUUID


