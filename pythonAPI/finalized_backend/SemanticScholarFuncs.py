import requests
import time
from AuthorNode import AuthorNode, PaperNode

"""
Edited: 


Only function to be used is: generate_author_dict(author_name, choice, numpapers)
Examples of execution:
dict1 = generate_author_dict()
dict2 = generate_author_dict(6) 
numpaper is a numeric value that the user can enter and corresponds to the number of papers of the author to be processed.
If numpaper is missing, default value is 5
choice is the choice of author from using searchAuthor. the user will have to remember and input the choice.
If choice is missing, default value is 1

generate_author_dict() returns a dictionary where each key is a PaperNode object corresponding to each paper of the initial
author and the value is a list of coauthor nodes corresponding to that Paper
 
"""


# Function to fetch author data from the Semantic Scholar API
def fetch_author(query):
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={query}&fields=name,aliases,url,papers.title,papers.year,papers.authors&limit=10"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Error fetching data: SemanticScholarAPI could not be reached. Please try again shortly.")
        # print(f"Error fetching data: {e}")
        # return None


# Function to display author options based on retrieved data
def display_author_options(aliases):
    list_of_aliases = []
    if aliases["total"] > 0:
        for i, author in enumerate(aliases["data"]):
            name = author.get("name")
            url = author.get("url")
            print(f"{i + 1}. {name} ({url})")
            list_of_aliases.append(name)

    return list_of_aliases

# Function to retrieve all author options
def get_author_options(author_name):
    list_of_aliases = []
    if author_name["total"] > 0:
        for author in sorted(author_name["data"], key=lambda x: x["name"]):
            name = author.get("name")
            url = author.get("url")
            list_of_aliases.append((name, url))
    return list_of_aliases

# Function to print author options
def print_author_options(list_of_aliases):
    sorted_aliases = sorted(list_of_aliases, key=lambda x: x[0])  # Sort by author name
    for i, (name, url) in enumerate(sorted_aliases, start=1):
        print(f"{i}. {name} ({url})")


# Function to select an author from the displayed options
def select_author_from_list(list_of_aliases, choice):
    # for i, (name, url) in enumerate(list_of_aliases, start=1):
    #     print(f"{i}. {name} ({url})")
    try:
        selected_index = choice - 1
        selected_author = list_of_aliases[selected_index]
        return selected_author
    except (ValueError, IndexError):
        raise ValueError(f"Invalid input. Please enter a valid number.")
        # print("Invalid input. Please enter a valid number.")
        # return None


# Function to parse author data retrieved from the API response
def parse_author_data(author_data, numpapers):
    author_nodes = []
    if author_data["total"] > 0:
        for author in author_data["data"]:
            name = author.get("name")
            aliases = author.get("aliases")
            authorId = author.get("authorId")
            url = author.get("url")
            papers = []
            if "papers" in author:
                paper_count = 0

                for paper in author["papers"]:
                    if paper_count >= numpapers:
                        break  # Exit loop if chosen number of papers have been processed
                    title = paper.get("title")
                    year = paper.get("year")
                    authors = []
                    authorIds = []
                    if "authors" in paper:
                        for coauthor in paper["authors"]:
                            authors.append(
                                (coauthor.get("name"), coauthor.get("authorId"))
                            )  # Store as tuple
                            authorIds.append(coauthor.get("authorId"))
                    papers.append(PaperNode(title, year, authors, authorIds))
                    paper_count += 1
            author_node = AuthorNode(name, None, aliases, authorId, url, papers)
            author_nodes.append(author_node)
    return author_nodes

def AuthorSearch(name):
    disamb = fetch_author(name)
    list_of_aliases = get_author_options(disamb)
    print_author_options(list_of_aliases)

# Function to make an AuthorNode object based on user input
def makeAuthor(name, choice, numpapers):
    disamb = fetch_author(name)
    list_of_aliases = get_author_options(disamb)

    selected_author = select_author_from_list(list_of_aliases, choice)

    if selected_author:
        author_nodes = parse_author_data(disamb, numpapers)
        selected_author_node = None
        for author in author_nodes:
            if author.name == selected_author[0]:
                selected_author_node = author
                break

        if selected_author_node:
            return selected_author_node
        else:
            raise NameError(f"Selected author not found in the retrieved data.")
            # print("Selected author not found in the retrieved data.")

    else:
        raise IndexError(f"No data found for author: {name}")
        # print("No data found. Try again")

# Function to create coauthor nodes for a given author node
def create_coauthor_nodes(author_node):
    coauthors_dict = {}  # Dictionary to store coauthor nodes for each paper
    #coauthor_mapping = {}  # Dictionary to map coauthor authorIds to nodes
    coauthor_mapping = {author_node.authorId: author_node}
    # Iterate through each paper of the author
    for paper in author_node.papers:
        while True:
            r = requests.post(
                "https://api.semanticscholar.org/graph/v1/author/batch",
                params={"fields": "name,aliases,authorId,url"},
                json={"ids": paper.authorIds},
            )
            coauthors_data = r.json()
            if r.status_code == 200:
                break
            elif r.status_code == 429:
                time.sleep(30)
            else:
                raise ConnectionError(f"Error fetching data: SemanticScholarAPI could not be reached. Please try again shortly.")
        for coauthor_data in coauthors_data:
            coauthor_id = coauthor_data["authorId"]
            if coauthor_id != author_node.authorId:
                if coauthor_id not in coauthor_mapping:
                    coauthor_node = AuthorNode(
                        name=coauthor_data["name"],
                        attributes=None,
                        aliases=coauthor_data["aliases"],
                        authorId=coauthor_data["authorId"],
                        url=coauthor_data["url"],
                        papers=[],  # Assuming we don't have papers for coauthors initially
                    )
                    coauthor_mapping[coauthor_id] = coauthor_node
                else:
                    coauthor_node = coauthor_mapping[coauthor_id]

                coauthor_node.papers.append(paper)  # Add paper to coauthor's paper list
                coauthors_dict.setdefault(paper, []).append(
                    coauthor_node
                )  # Add coauthor node to paper's coauthor list
        coauthors_dict.setdefault(paper, []).append(author_node)
    if not coauthors_dict: # Handling empty coauthors data
        raise KeyError(f"No coauthors found for the given author.")
        # print("No coauthors found for the given author.")
    return (coauthors_dict, coauthor_mapping)


"""
    To be used as generate_author_dict(numpapers) where numpapers is the number 
    of papers to be processed for the author. 
    Initial value is set to 5.
    # returns dict with below format:
    {
        papernode1 : list of authornodes,
        papernode2 : list of authornodes2
    }
"""


# Function to generate a dictionary containing coauthors for a given author
def generate_author_dict(author_name:str, choice:int, numpapers:int):
    author = makeAuthor(author_name, choice, numpapers)
    if author:
        coauthors_dict,coauthors_map = create_coauthor_nodes(author)
        #print_coauthor_info(coauthors_dict)  # printing each author for checking
        return (coauthors_dict,coauthors_map)
    else:
        raise KeyError(f"Author not found: {author_name}")
        # print("Author not found. Please try again:") #->   CHANGE TO ERROR MESSAGE
        # return None


"""
Workflow: generate_author_dict(numpapers) -> makeAuthor(author_name) -> disamb = fetch_author(name), list_of_aliases = display_author_options(disamb), selected_author = select_author_from_list(list_of_aliases), parse_author_data(disamb, numpapers)
    (if makeAuthor returns valid author)     |-> create_coauthor_nodes(makeAuthor(author_name))
"""


"""
Below functions used for printing
"""


# Function to print coauthor information
def print_coauthor_info(coauthors_dict):
    i = 1
    for paper, coauthors_list in coauthors_dict.items():
        print(
            f"Paper {i}:", paper.title
        )  # Assuming 'title' is an attribute of the Paper object
        print("Coauthors:")
        for coauthor_node in coauthors_list:
            print_author_details(coauthor_node)
        i += 1


# Function to print author details
def print_author_details(auth):
    print("\tName:", auth.name)
    print("\tAliases:", ", ".join(auth.aliases))
    print("\tURL:", auth.url)
    if auth.papers:
        print("\tPapers:")
        for paper in auth.papers:
            print("\t\tTitle:", paper.title)
            print("\t\tYear:", paper.year)
            print("\t\tAuthors:")
            for author in paper.authors:
                print(f"\t\t\tName: {author[0]}, Author ID: {author[1]}")
            print()
    else:
        print("No papers found")


# Both methods of execution:
# generate_author_dict("Jim Purtilo")
# generate_author_dict(6)
