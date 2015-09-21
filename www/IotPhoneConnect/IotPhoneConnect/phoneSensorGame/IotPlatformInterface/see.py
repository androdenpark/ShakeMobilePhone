import time
import json
import pycurl
import logging

deviceUrl1 = "https://crl.ptopenlab.com:8800/iotdm/api/A5ADC758-D2E7-3330-96C52E3B267B/context/820b41ce-152e-4341-9bea-7ccfb75e3beb/executecommand"
deviceUrl2 = "https://crl.ptopenlab.com:8800/iotdm/api/A5ADC758-D2E7-3330-96C52E3B267B/context/5b6b5a91-9b70-4801-a00a-0e6b975d61be/executecommand"
header = ['Accept:*/*', 'Content-Type:application/json']
cmd = {"aid":"","cid":"","did":"","typename":"","command":"","paramsType":"","params":""}

def cmdPost(postUrl, cmdJson):
    pc = pycurl.Curl()  
    pc.setopt(pycurl.POST, 1)
    #pc.setopt(pycurl.VERBOSE, 1)
    pc.setopt(pycurl.URL, postUrl)
    pc.setopt(pycurl.HTTPHEADER, header)
    pc.setopt(pycurl.POSTFIELDS, cmdJson)
    pc.perform()
    respCode = pc.getinfo(pycurl.RESPONSE_CODE)
    pc.close()
    return respCode




logging.basicConfig(level=logging.INFO, format='%(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
cmd["command"] = "turnOn"
respCode = cmdPost(deviceUrl1, json.dumps(cmd))
logging.info("respCode: %d" % respCode)
time.sleep(1)
cmd["command"] = "shakeSpeed"
cmd["params"] = "100"
respCode = cmdPost(deviceUrl1, json.dumps(cmd))
logging.info("respCode: %d" % respCode)
