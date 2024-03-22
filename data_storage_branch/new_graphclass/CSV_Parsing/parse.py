import dask.dataframe as dd
import pandas

def parseData(csv):
    df = dd.read_csv(csv)
    df = df.where(df.notnull(), None).compute()

    offset = 0

    one = df.get(df.columns[0]).tolist()
    two = None
    if len(df.columns) == 4:
        two = df.get(df.columns[1]).tolist()
        offset = 1
    
    three = []
    keys = df.get(df.columns[1 + offset]).tolist()
    values = df.get(df.columns[2 + offset]).tolist()
    for i in range(len(keys)):
        pairing = dict()
        currkey = keys[i].split(',')
        currvalue = values[i].split(',')
        for x in range(len(currkey)):
            pairing[currkey[x]] = currvalue[x]
        three.append(pairing)

    return (one, two, three)

# To do: need to rework to work with the correct data being passed in
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
test1 = parseData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test1-load.csv')
test2 = parseData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test2-load.csv')
test3 = parseData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test3-load.csv')


#print(test1)
#print(test2)
#print(test3)


saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test1-save.csv', test1)
saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test2-save.csv', test2)
saveData('data_storage_branch/new_graphclass/CSV_Parsing/Tester/test3-save.csv', test3)