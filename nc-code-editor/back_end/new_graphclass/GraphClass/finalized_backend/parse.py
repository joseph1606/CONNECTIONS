import dask.dataframe as dd
from keys import *


def parseData(csv):
    df = dd.read_csv(csv, skipinitialspace=True).compute()

    if df.isna().values.any():
        raise ValueError("Error: No columns are allowed to be empty")

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
        # and capitalize first letter of each word.
        # Also handles error checking for duplicate names (paul,paul,data,data)
        for x in range(len(two)):
            two[x] = two[x].strip()
            two[x] = two[x].title()
            if one[x] == two[x]:
                raise ValueError(
                    "Error: Person 1 cannot have the same name as Person 2"
                )

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
        currkey = keys[i].split(",")
        currvalue = values[i].split(",")

        # Error if not a relationships have a corresponding value, or vice versa
        if len(currkey) != len(currvalue):
            print(currkey, len(currkey))
            for i, v in enumerate(currvalue):
                print(i, v)
            raise ValueError(ERR_UNEVEN_VALUES)

        # Loops through all relationships given in current cell
        x = 0
        while x < len(currkey):
            key = currkey[x].strip().replace("$comma$", ",")
            if (
                key.isspace() or not key
            ):  # if the key is empty or whitespace an error occurs
                raise ValueError(ERR_UNEVEN_VALUES)

            value = currvalue[x].strip().replace("$comma$", ",")
            if (
                value.isspace() or not value
            ):  # if the value is empty or whitespace an error occurs
                raise ValueError(ERR_UNEVEN_VALUES)

            # Handles author nodes
            if key == "AUTHORID" and offset == 0:

                author_info = dict()

                author_info[key] = value.replace("$comma$", ",")

                # Gets author url
                x = x + 1
                key = currkey[x]
                value = currvalue[x].replace("$comma$", ",")
                if key != "AUTHORURL":
                    raise ValueError(ERR_AUTHOR_FORMAT)
                author_info[key] = value

                # Gets author aliases
                x = x + 1
                key = currkey[x]
                value = currvalue[x].replace("$comma$", ",")
                if key != "AUTHORALIASES":
                    raise ValueError(ERR_AUTHOR_FORMAT)
                if value == "None":
                    author_info[key] = []
                else:
                    author_info[key] = value.split("/")

                author_info["PAPERS"] = []

                # Gets all papers
                x = x + 1
                if x < len(currkey):
                    key = currkey[x]
                    value = currvalue[x].replace("$comma$", ",")
                else:
                    key = ""
                    value = ""
                while key == "PAPER":
                    # Splits paper data into a list
                    paper_info = value.split("/")
                    if len(paper_info) != 4:
                        raise ValueError("Error: Incorrect paper node format")

                    # Turns paper year back into an int
                    paper_info[1] = int(paper_info[1])

                    # Turns author ids into a list
                    if paper_info[3] == "None":
                        paper_info[3] = []
                    else:
                        paper_info[3] = paper_info[3].split("#")

                    # Turns author ids into a list of tuples
                    if paper_info[2] == "None":
                        paper_info[2] = []
                    else:
                        authors = paper_info[2].split("#")

                        # Turns list into list of (name,id) tuples
                        ids = paper_info[3]
                        paper_info[2] = list()
                        for y in range(len(authors)):
                            paper_info[2].append((authors[y], ids[y]))

                    author_info["PAPERS"].append(paper_info)
                    x = x + 1
                    if x < len(currkey):
                        key = currkey[x]
                        value = currvalue[x].replace("$comma$", ",")
                    else:
                        key = ""
                        value = ""

                pairing["AUTHORINFO"] = author_info

            # If the current key marks a directed graph, adjusts value to the correct format
            # Correct format is 'example1/example2'
            elif key == DIRECTED_CSV:
                rel = value.split("/")

                # name1,name2,DIRECTED,mentor/mentee
                if offset == 1:
                    # Error if too many or too little '/'s are used
                    if len(rel) != 2:
                        raise ValueError(ERR_DIRECTED_FORMAT)
                    # Error if either side of the '/' is empty
                    if not rel[0] or not rel[1]:
                        raise ValueError(ERR_DIRECTED_FORMAT)
                    value = (rel[0].title(), rel[1].title())

                    if key in pairing:
                        pairing[key].append(
                            value
                        )  # If key already exists, append value to existing list
                    else:
                        pairing[key] = [value]

                # name1,DIRECTED,name2/mentor/mentee
                elif offset == 0:
                    # Error if too many or too little '/'s are used
                    if len(rel) != 3:
                        raise ValueError(ERR_DIRECTED_FORMAT)

                    # Error if any part is empty
                    if not rel[0] or not rel[1] or not rel[2]:
                        raise ValueError(ERR_DIRECTED_FORMAT)

                    # returns {name2: [(mentor,mentee)]} such that name1 -> name2, mentor/mentee
                    value1 = rel[0].title()
                    value2 = (rel[1].title(), rel[2].title())

                    if key in pairing:
                        if rel[0].title() in pairing[key]:
                            pairing[key][value1].append(value2)
                        else:
                            pairing[key][value1] = [value2]
                    else:
                        pairing[key] = {value1: [value2]}

                x = x + 1

            # Change all non author info to .title case
            else:
                key = key.title()
                value = value.title()
                # Saves the key,value pair to the dictionary
                if key in pairing:
                    pairing[key].append(
                        value
                    )  # If key already exists, append value to existing list
                else:
                    pairing[key] = [value]

                x = x + 1

        three.append(pairing)

    return (one, two, three)
