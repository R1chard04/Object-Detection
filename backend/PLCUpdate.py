import pylogix
from pylogix import PLC

# print(dir(pylogix))
# help(pylogix.PLC)

def readPLC(camTagName):
    with PLC() as comm:
        comm.IPAddress = '10.110.50.201'
        Operator_Swipe = comm.Read(camTagName)
        return Operator_Swipe.Value
        

# send one for pass and zero for fail for each feature, Run when it requires to write the value
def writePLC(tagName, resultError):
    # if ok == True :
        with PLC("10.110.50.201") as comm:       
            Feature_all = comm.Write(tagName, resultError)
            # print(Feature_all.TagName, Feature_all.Value, Feature_all.Status)
            # print(station)
            # print("Transfer done")
    # else:
    #     print("Transfer fail - result unvalid")


def verifyResult(station, result):
    verified = False
    BT1XXStation = ["OP100", "OP120", "OP140"]
    stationResult = [4, 0, 0]

    for i in range(len(BT1XXStation)):
        if station == BT1XXStation[i]:
            # print(stationResult[i])
            verified = True
   
    return verified, station, result
        
 # needs to work on this that how I can only pass one result if it is not found
 #        else: 
 #           print("Station not found")

def transferToPLC(station, result):
   verified = verifyResult(station, result)
   writePLC(verified[0],verified[1], verified[2] )






