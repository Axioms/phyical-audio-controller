from serial import *
import time
import json
import audioUtils as audio
serial: Serial = None
# Use @@ for default sink
NodeNames = ["@@","spotify","Firefox", "WEBRTC VoiceEngine","Scream"]

def proccessReset():
    audioLevels = []
    for node in NodeNames:
        if(node == "@@"):
            audioLevels.append(str(audio.GetDefaultSinkVolume()))
        else:
            nodeId = audio.GetNodeID(node)
            if(nodeId[0] != -1):
                audioLevels.append(str(audio.GetVolume(nodeId)))
            else:
                audioLevels.append("0")
    return ( "<" + (",".join(audioLevels)) + ">").encode('utf-8')

while True:
    if serial is None:
        print("waiting for serial connection ...")
        try:
            serial = Serial('/dev/ttyUSB0', 1000000)
        except:
            time.sleep(5)
            continue
    try:
        bytesToRead = serial.inWaiting()
        #text = serial.read(bytesToRead).decode("utf-8")
        try:
            text = serial.readline().decode("utf-8").strip()
            #print(text)
        except:
            #print("decode err")
            pass
        if(len(text) > 0 and text[0:1] == "{" and text[-1:] == "}"):
            #print(text, end="")
            try:
                jsonText = json.loads(text)
                if(jsonText["a"] == "volume"):
                    print("volume")
                    if(NodeNames[jsonText["e"]] == "@@"):
                        audio.SetDefaultSinkVolume(jsonText["v"])
                    else:
                        nodeId = audio.GetNodeID(NodeNames[jsonText["e"]])
                        audio.SetVolume(nodeId, jsonText["v"])
                elif(jsonText["a"] == "press"):
                    print("mute")
                    if(NodeNames[jsonText["e"]] == "@@"):
                        audio.ToggleDefaultSinkMute()
                    else:
                        nodeId = audio.GetNodeID(NodeNames[jsonText["e"]])
                        audio.ToggleMute(nodeId)
                elif(jsonText["a"] == "sync"):
                    print("sync")
                    data = proccessReset()
                    serial.write(data)
                #print(jsonText)
            except Exception as e:
                #print("err")
                pass
    except:
        print("serial Connection Lost...")
        serial = None
        pass
