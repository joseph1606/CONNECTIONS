import dask.dataframe as dd
import dask.array as da
import pandas

def parseData(csv):
    df = dd.read_csv(csv).compute()
    #df = df

    if df.isna().values.any():
        return "Error: No columns are allowed to be empty"
    
    offset = 0

    one = df.get(df.columns[0]).tolist()
    for x in range(len(one)):
        one[x] = one[x].capitalize()

    two = None
    if len(df.columns) == 4:
        two = df.get(df.columns[1]).tolist()
        for x in range(len(two)):
            two[x] = two[x].capitalize()
        offset = 1
    elif len(df.columns) != 3:
        return "Error: Incorrect format"

    
    three = []
    keys = df.get(df.columns[1 + offset]).tolist()
    values = df.get(df.columns[2 + offset]).tolist()
    
    #print(one)
    #print(keys)
    #print(values)

    
    for i in range(len(keys)):
        pairing = dict()
        currkey = keys[i].split(',')
        currvalue = values[i].split(',')

        if len(currkey) != len(currvalue):
            return "Error: All relationships must have corresponding value"
            
        for x in range(len(currkey)):
            key = currkey[x].strip() 
            value = currvalue[x].strip()
            if key in pairing:
                pairing[key].append(value)  # If key already exists, append value to existing list
            else:
                pairing[key] = [value]
        three.append(pairing)
        

    return (one, two, three)

# To do: need to rework to work with the correct data being passed in
#def saveData(nodes):
def saveData(filePath, values):

    data = {'Person 1': values[0]}
    if(values[1] != None):
        data['Person 2'] = values[1]

    ks = list()
    vs = list()
    for x in values[2]:
        ks.append(','.join(list(x)))
        vs.append(','.join(list(x.values())))

    data['Relationship'] = ks
    data['Relationship Value'] = vs

    pandas_df = pandas.DataFrame(data)
    df = dd.from_pandas(pandas_df, npartitions=1)
    df.compute().to_csv(filePath, index=False)

# temp testing
test1 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/test1-load.csv')
test2 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/test2-load.csv')
test3 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/test3-load.csv')
error1 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error1.csv')
error2 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error2.csv')
error3 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error3.csv')
#error4 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error4.csv')
#error5 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error5.csv')
error6 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error6.csv')
error7 = parseData('new_connections-Group2Backend/nc-code-editor/back_end/new_graphclass/CSV_Parsing/Paul/Tester/error7.csv')



print(test1)
print(test2)
print(test3)
print(error1)
print(error2)
print(error3)
#print(error4)
#print(error5)
print(error6)
print(error7)


#saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test1-save.csv', test1)
#saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test2-save.csv', test2)
#saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test3-save.csv', test3)
