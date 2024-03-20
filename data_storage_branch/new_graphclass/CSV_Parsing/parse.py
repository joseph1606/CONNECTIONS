import dask.dataframe as dd

def parseData(csv):
    df = dd.read_csv(csv).compute()
    cols = list()
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
        pairing[keys[i]] = values[i]
        three.append(pairing)

    return (one, two, three)

def saveData(csv):
    pass


# temp test prints
print(parseData('new_connections/data_storage_branch/new_graphclass/GraphClass/Tester/Paul/test2.csv'))
print(parseData('new_connections/data_storage_branch/new_graphclass/GraphClass/Tester/Paul/test.csv'))