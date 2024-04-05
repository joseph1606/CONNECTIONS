import dask.dataframe as dd

def parseData(csv):
    df = dd.read_csv(csv)
    df = df.where(df.notnull(), None).compute()

    offset = 0

    # stores as a list all the names (strings) that were put first under the column of person1
    one = df.get(df.columns[0]).tolist()

    #if names have whitespace before or after the actual string it removes this
    one = [o.strip() for o in one]

    two = None

    #checks if the CSV is of type 2 which has 4 columns 
    if len(df.columns) == 4:
        # stores as a list all the names (strings) that were put first under the column of person2
        two = df.get(df.columns[1]).tolist()
        
        offset = 1

        #if names have whitespace before or after the actual string it removes this
        two = [o.strip() for o in two]
    
    three = []
    keys = df.get(df.columns[1 + offset]).tolist()
    values = df.get(df.columns[2 + offset]).tolist()
    for i in range(len(keys)):
        currkey = keys[i].split(',')
        currvalue = values[i].split(',')
        pairing = {}  # Initialize a dictionary for each iteration
        for x in range(len(currkey)):
            key = currkey[x].strip()  # Remove any leading/trailing whitespace
            value = currvalue[x].strip()  # Remove any leading/trailing whitespace
            if key in pairing:
                pairing[key].append(value)  # If key already exists, append value to existing list
            else:
                pairing[key] = [value]  # If key doesn't exist, create a new list with value
        three.append(pairing)  # Append the dictionary to the list

    return (one, two, three)
