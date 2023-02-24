class BinaryNameAssigner:
    def __init__(self, array):
        self.array = array

    def assign(self):
        # create an empty list to store assigned names
        assigned_names = []  
        # iterate over each element of the array
        for i in range(len(self.array)):  
            # prompt the user for a name
            name = input(f"Enter name for part occurance {i+1}: ")
            # add the name to the list of assigned names
            assigned_names.append(name)  
        # return the list of assigned names    
        return assigned_names