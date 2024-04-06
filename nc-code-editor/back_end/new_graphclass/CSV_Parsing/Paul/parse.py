
# To delete, needs to imported instead
class Node:
    def __init__(self, name: str, attributes: dict = None):
        self.name = name
        self.attributes = attributes

    def getName(self):
        return self.name

    def getAttributes(self):
        return self.attributes



import dask.dataframe as dd
import pandas

# to do, deal with whitespace
def parseData(csv):
    df = dd.read_csv(csv).compute()

    if df.isna().values.any():
       raise ValueError("Error: No columns are allowed to be empty, no leading whitespace is allowed")
    
    offset = 0
    
    # stores as a list all the names (strings) that were put first under the column of person1
    one = df.get(df.columns[0]).tolist()

    # going through the list of person1, this will remove whitespace before/after 
    # and capitalize first letter of each word
    for x in range(len(one)):
        one[x] = one[x].strip()
        one[x] = one[x].title()

    #checks if the CSV is of type 2 which has 4 columns 
    two = None
    if len(df.columns) == 4:
        # stores as a list all the names (strings) that were put first under the column of person2
        two = df.get(df.columns[1]).tolist()

        # going through the list of person2, this will remove whitespace before/after 
        # and capitalize first letter of each word
        for x in range(len(two)):
            two[x] = two[x].strip()
            two[x] = two[x].title()
            
        offset = 1
    elif len(df.columns) != 3:
        raise ValueError("Error: Incorrect format")

    # Gets the relationships and relationship values
    three = []
    keys = df.get(df.columns[1 + offset]).tolist()
    values = df.get(df.columns[2 + offset]).tolist()
    
    # Loops through all relationships, and adds to the three list a dictionary, in which the keys
    # are the relationship, and the values are the corresponding relationship values
    for i in range(len(keys)):
        pairing = dict()
        currkey = keys[i].split(',')
        currvalue = values[i].split(',')

        # Error if not a relationships have a corresponding value, or vice versa
        if len(currkey) != len(currvalue):
            raise ValueError("Error: All relationships must have corresponding value")
            
        # Loops through all relationships given in current cell
        for x in range(len(currkey)):
            key = currkey[x].strip()
            if key.isspace() or not key: #if the key is empty or whitespace an error occurs
                raise ValueError("Error: All relationships must have corresponding value")
            
            value = currvalue[x].strip()
            if value.isspace() or not value: #if the value is empty or whitespace an error occurs
                raise ValueError("Error: All relationships must have corresponding value")
            
            # If the current key marks a directed graph, adjusts value to the correct format
            # Correct format is 'example1/example2'
            if key == 'DIRECTED':
                rel = value.split("/")

                # Error if too many or too little '/'s are used
                if len(rel) != 2:
                    raise ValueError("Error: Incorrect directed relationship format")
                # Error if either side of the '/' is empty
                if (not rel[0] or not rel[1]):
                    raise ValueError("Error: Incorrect directed relationship format")
                value = (rel[0], rel[1])
            
            # Saves the key,value pair to the dictionary
            if key in pairing:
                pairing[key].append(value)  # If key already exists, append value to existing list
            else:
                pairing[key] = [value]
        
        three.append(pairing)

    return (one, two, three)

# to do: cannot save graphs with directed edges
# to do: needs testing
def saveData(nodes, filePath):
    names = list()
    attributes = list()

    # Gets all information out of the list of nodes
    for id, node in nodes:
        names.append(node.getName())
        attributes.append(node.getAttributes())

    # Formats data in the correct way
    data = dict()
    ks = list()
    vs = list()
    for x in attributes:
        ks.append(','.join(list(x.keys())))
        vs.append(','.join(list(x.values())))

    # Puts all data into a dictionary
    data["Person 1"] = names
    data['Relationship'] = ks
    data['Relationship Value'] = vs

    # Saves dictionary to csv
    pandas_df = pandas.DataFrame(data)
    df = dd.from_pandas(pandas_df, npartitions=1)
    df.compute().to_csv(filePath, index=False)




# temp testing
#test1 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/test1-load.csv')
#test2 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/test2-load.csv')
#test3 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/test3-load.csv')
#error1 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error1.csv')
#error2 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error2.csv')
#error3 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error3.csv')
#error4 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error4.csv')
#error5 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error5.csv')
#error6 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error6.csv')
#error7 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error7.csv')
#test = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/test2.csv')

#print(test)


#print(test1)
#print(test2)
#print(test3)
#print(error1)
#print(error2)
#print(error3)
#print(error4)
#print(error5)
#print(error6)
#print(error7)


#saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test1-save.csv', test1)
#saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test2-save.csv', test2)
#saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test3-save.csv', test3)
