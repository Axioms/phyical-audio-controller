from serial import *
import sys
import json
import pipewire_python
import audioUtils as audio
serial = Serial('/dev/ttyUSB0', 1000000, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
NodeNames = ["java","java", "WEBRTC VoiceEngine","Firefox","Scream"]

while True:
    bytesToRead = serial.inWaiting()
    #text = serial.read(bytesToRead).decode("utf-8")
    text = serial.readline().decode("utf-8")
    if(len(text) > 0 and text[0:1] == "{" and (text[-3:])[0:1] == "}"):
        #print(text, end="")
        try:
            jsonText = json.loads(text)
            if(jsonText["a"] == "volume"):
                nodeId = audio.GetNodeID(NodeNames[jsonText["e"]])
                audio.SetVolume(nodeId, jsonText["v"])
            elif(jsonText["a"] == "press"):
                nodeId = audio.GetNodeID(NodeNames[jsonText["e"]])
                audio.ToggleMute(nodeId)
            elif(jsonText["a"] == "reset"):
                sys.exit()

            print(text)

        except:
            print("err")
        
        print(jsonText)