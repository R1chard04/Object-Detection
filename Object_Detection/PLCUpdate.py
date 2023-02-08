from pylogix import PLC

# This script has to run every half second
with PLC() as comm:
    comm.IPAddress = '10.110.50.201'
    Operator_Swipe = comm.Read('AA_TEST.1')
    print(Operator_Swipe.TagName, Operator_Swipe.Value, Operator_Swipe.Status)

# send one for pass and zero for fail for each feature, Run when it requires to write the value

def updatePLC(array):
    with PLC("10.110.50.201") as comm:

        # Left part OK / NOK
        Feature_1 = comm.Write("AA_TEST.2", 1)
        print(Feature_1.TagName, Feature_1.Value, Feature_1.Status)

        # Right part OK / NOK
        Feature_2 = comm.Write("AA_TEST.3", 1)
        print(Feature_2.TagName, Feature_2.Value, Feature_2.Status)

        # Top part OK / NOK
        Feature_3 = comm.Write("AA_TEST.4", 1)
        print(Feature_3.TagName, Feature_3.Value, Feature_3.Status)

        # Bottom part OK / NOK
        Feature_4 = comm.Write("AA_TEST.5", 1)
        print(Feature_4.TagName, Feature_4.Value, Feature_4.Status)
