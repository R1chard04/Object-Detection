import pylogix
from pylogix import PLC



# Things to implement #

"""
1. verify the result array - it should cross check with the standard size of the array for the particular station.
2. Needs to pick up for the tag name for the individual station
3. If return value of the array is not enough then it should throw the error 

"""

# This script has to run every half second

def readPLC(camTagName):
    with PLC() as comm:
        comm.IPAddress = '10.110.50.201'
        Operator_Swipe = comm.Read(camTagName)
        print(Operator_Swipe.TagName, Operator_Swipe.Value, Operator_Swipe.Status)

# send one for pass and zero for fail for each feature, Run when it requires to write the value

def readTagPLC():
    with PLC("10.110.50.201") as comm:
        tags = comm.GetTagList()
        for t in tags.Value:
            print("Tag:", t.TagName, t.DataType)


def writePLC(station, resultError):
    with PLC("10.110.50.201") as comm:

     
        Feature_all = comm.Write("Camera_Output.1", resultError)
        print(Feature_all.TagName, Feature_all.Value, Feature_all.Status)
        print(station)


        # # Right part OK / NOK
        # Feature_2 = comm.Write("AA_TEST.3", 1)
        # print(Feature_2.TagName, Feature_2.Value, Feature_2.Status)

        # # Top part OK / NOK
        # Feature_3 = comm.Write("AA_TEST.4", 1)
        # print(Feature_3.TagName, Feature_3.Value, Feature_3.Status)

        # # Bottom part OK / NOK
        # Feature_4 = comm.Write("AA_TEST.5", 1)
        # print(Feature_4.TagName, Feature_4.Value, Feature_4.Status)

# writePLC("OP100", [0,0,0,0])
# readPLC('AA_test.2')
# readPLC('AA_test.3')
# readPLC('AA_test.4')
# readPLC('AA_test.5')




# class allenBradley :
#     def __init__(self, station, results):
#         self.station = station
#         self.results = results

#     def crossVerify(self):
#         stationName = ["OP100","OP120", "OP140"]
#         stationResults = [4, 1, 1]
        

#         print("Valid data")
        
# preVerified = allenBradley("OP100", "Hello")
# print(preVerified.station)
# print(preVerified.results)
# preVerified.crossVerify()
