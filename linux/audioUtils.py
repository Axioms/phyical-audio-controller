import subprocess
import re, time
import audioMapping
import math

VOLUME_LEVEL_REGEX=r'(^\s{4}Prop:\skey\sSpa:Pod:Object:Param:Props:channelVolumes.*(\r\n|\r|\n))(^\s{6}Array:\schild.*(\r\n|\r|\n))(\s{8}Float\s.*(\r\n|\r|\n))'
MUTE_STATUS_REGEX=r'(^\s{4}Prop:\skey\sSpa:Pod:Object:Param:Props:mute.*(\r\n|\r|\n))(\s{6}Bool\s.*(\r\n|\r|\n))'
# pw-cli set-param <clientID> Props '{ mute: false, channelVolumes: [ 0.98, 0.98 ] }'
# id=$(pw-dump | jq '.[] | select(.type == "PipeWire:Interface:Node") | select(.info.props["application.name"] == "Scream") | .id')
# pw-cli e <clientID> Props

def GetNodeID(name: str) -> int:
    output = subprocess.run(['echo -n $(pw-dump | jq \'.[] | select(.type == "PipeWire:Interface:Node") | select(.info.props["application.name"] == "' + name + '") | .id\')'], shell=True, capture_output=True)
    return int(output.stdout.decode('UTF-8'))

def SetVolume(nodeId: int, volume: int):
    internalVolume = audioMapping.GetFloatValue(volume)
    output = subprocess.run(["pw-cli set-param "+ str(nodeId) +" Props '{ mute: false, channelVolumes: ["+ str(internalVolume) +", "+ str(internalVolume) +"] }'"], shell=True, capture_output=True)
    print(output.stdout.decode('UTF-8'))

def GetVolume(nodeId: int) -> int:
    output = subprocess.run(["pw-cli e " + str(nodeId) + " Props"], shell=True, capture_output=True)
    regex = re.compile(VOLUME_LEVEL_REGEX, re.MULTILINE)
    result = re.findall(regex, output.stdout.decode('UTF-8'))
    audioLevel = result[0][4].strip()
    return audioMapping.GetIntVlaue(float(audioLevel[6:]))

def GetMuteStatus(nodeId: int) -> bool:
    output = subprocess.run(["pw-cli e " + str(nodeId) + " Props"], shell=True, capture_output=True)
    regex = re.compile(MUTE_STATUS_REGEX, re.MULTILINE)
    result = re.findall(regex, output.stdout.decode('UTF-8'))
    muteStatus = result[0][2].strip()
    return muteStatus[5:].lower() == "true"

def ToggleMute(nodeId: int):
    output = subprocess.run(["pw-cli set-param "+ str(nodeId) +" Props '{ mute: "+ ("true" if GetMuteStatus(nodeId) == False else "false") +"}'"], shell=True, capture_output=True)
    print(output.stdout.decode('UTF-8'))

def createMapping():
    id = GetNodeID("Scream")
    volumeLevel = 100
    oldVolume = 0.001
    volume = 0.0
    while oldVolume > 0:
        volume = GetVolume(id)
        if(oldVolume != volume):
            oldVolume = volume
            print(str(volumeLevel) + ", " + str(volume))
            volumeLevel -= 1
        time.sleep(0.1)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    id = GetNodeID("Scream")
    ToggleMute(id)
    ToggleMute(id)
    GetMuteStatus(id)
    print(GetVolume(id))
    SetVolume(id, 50)
    print(GetVolume(id))
    SetVolume(id, 26)
    print(GetVolume(id))
    #createMapping()
    