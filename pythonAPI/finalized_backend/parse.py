import dask.dataframe as dd
from keys import *


"""
Pauls comments

To do after CDR
i) Needs to be able to handle leading whitespace
ii) Needs to be able to save graphs with directed edges
    - Depending on implementation, throwing an error if directed is in a type1 csv.
"""

"""
Joels Comments
iv) The attribute values for a DIRECTED type need to be in lowercase
"""


# to do: leading whitespace cannot be read by dask, must look into this more
def parseData(csv):
    df = dd.read_csv(csv).compute()

    if df.isna().values.any():
        raise ValueError(
            "No columns are allowed to be empty, no leading whitespace is allowed"
        )

    offset = 0

    # stores as a list all the names (strings) that were put first under the column of person1
    one = df.get(df.columns[0]).tolist()

    # going through the list of person1, this will remove whitespace before/after
    # and capitalize first letter of each word
    for x in range(len(one)):
        one[x] = one[x].strip()
        one[x] = one[x].title()

    # checks if the CSV is of type 2 which has 4 columns
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
        raise ValueError("Incorrect format")

    # Gets the relationships and relationship values
    three = []
    keys = df.get(df.columns[1 + offset]).tolist()
    values = df.get(df.columns[2 + offset]).tolist()

    # Loops through all relationships, and adds to the three list a dictionary, in which the keys
    # are the relationship, and the values are the corresponding relationship values
    for i in range(len(keys)):
        pairing = dict()
        currkey = keys[i].split(",")
        currvalue = values[i].split(",")

        # Error if not a relationships have a corresponding value, or vice versa
        if len(currkey) != len(currvalue):
            raise ValueError("All relationships must have corresponding value")

        # Loops through all relationships given in current cell
        for x in range(len(currkey)):
            key = currkey[x].strip().title()
            if (
                key.isspace() or not key
            ):  # if the key is empty or whitespace an error occurs
                raise ValueError(
                    "All relationships must have corresponding value"
                )

            value = currvalue[x].strip()
            if (
                value.isspace() or not value
            ):  # if the value is empty or whitespace an error occurs
                raise ValueError(
                    "All relationships must have corresponding value"
                )

            # If the current key marks a directed graph, adjusts value to the correct format
            # Correct format is 'example1/example2'
            if key == DIRECTED:
                rel = value.split("/")

                # Error if too many or too little '/'s are used
                if len(rel) != 2:
                    raise ValueError("Incorrect directed relationship format")
                # Error if either side of the '/' is empty
                if not rel[0] or not rel[1]:
                    raise ValueError("Incorrect directed relationship format")
                value = (rel[0].title(), rel[1].title())
            else:
                value = value.title()
            # Saves the key,value pair to the dictionary
            if key in pairing:
                pairing[key].append(
                    value
                )  # If key already exists, append value to existing list
            else:
                pairing[key] = [value]

        three.append(pairing)

    return (one, two, three)