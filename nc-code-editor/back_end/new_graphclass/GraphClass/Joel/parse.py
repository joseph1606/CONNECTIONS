import dask.dataframe as dd


def parseData(csv):
    df = dd.read_csv(csv).compute()

    if df.isna().values.any():
        raise ValueError("Error: No columns are allowed to be empty")
    
    offset = 0

    # stores as a list all the names (strings) that were put first under the column of person1
    one = df.get(df.columns[0]).tolist()

    #going through the list of person1, if it's a space an error will occur
    # otherwise it will remove whitespace before/after and capitalize first letter of each word
    for x in range(len(one)):
        if one[x].isspace():
                raise ValueError("Enter Person 1")
        one[x] = one[x].strip()
        one[x] = one[x].title()

    two = None

    #checks if the CSV is of type 2 which has 4 columns 
    if len(df.columns) == 4:
        # stores as a list all the names (strings) that were put first under the column of person2
        two = df.get(df.columns[1]).tolist()

        #going through the list of person2, if it's a space/whitespace an error will occur
        # otherwise it will remove whitespace before/after and capitalize first letter of each word
        for x in range(len(two)):
            if two[x].isspace():
                raise ValueError("Enter Person 2")
            two[x] = two[x].strip()
            two[x] = two[x].title()
        offset = 1

    elif len(df.columns) != 3:
        raise ValueError("Error: Incorrect format")

    three = []
    keys = df.get(df.columns[1 + offset]).tolist()
    values = df.get(df.columns[2 + offset]).tolist()
    
    
    for i in range(len(keys)):
        pairing = dict()
        currkey = keys[i].split(',')
        currvalue = values[i].split(',')

        if len(currkey) != len(currvalue):
            raise ValueError("Error: All relationships must have corresponding value")
            
        for x in range(len(currkey)):
            key = currkey[x].strip() 
            if key.isspace() or not key: #if the key is empty or whitespace an error occurs
                raise ValueError("Enter relationship")
            value = currvalue[x].strip()
            if value.isspace() or not value: #if the value is empty or whitespace an error occurs
                raise ValueError("Enter relationship value")
            if key in pairing:
                pairing[key].append(value)  # If key already exists, append value to existing list
            else:
                pairing[key] = [value]
        three.append(pairing)
        

    return (one, two, three)
