import requests
from AutherNode import AuthorNode, PaperNode


def fetch_author(query):
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={query}&fields=name,aliases,url,papers.title,papers.year,papers.authors&limit=5"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_author_options(aliases):
    list_of_aliases = []
    if aliases["total"] > 0:
        for i, author in enumerate(aliases["data"]):
            name = author.get('name')
            url = author.get('url')
            print(f"{i + 1}. {name} ({url})")
            list_of_aliases.append(name)
            
    return list_of_aliases

'''def select_author_from_list(list_of_aliases):
    try:
        selected_index = int(input("Enter the number corresponding to the desired author: ")) - 1
        selected_author = list_of_aliases[selected_index]
        return selected_author
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number.")
        return None'''

def parse_author_data(author_data):
    author_nodes = []
    if author_data["total"] > 0:
        for author in author_data["data"]:
            name = author.get("name")
            aliases = author.get("aliases")
            authorId = author.get("authorId")
            url = author.get("url")
            papers = []
            if "papers" in author:
                paper_count = 0  # Counter to track the number of papers processed
                for paper in author["papers"]:
                    if paper_count >= 2:
                        break  # Exit loop if ten papers have been processed
                    title = paper.get("title")
                    year = paper.get("year")
                    authors = []
                    authorIds = []
                    if "authors" in paper:
                        for coauthor in paper["authors"]:
                            authors.append(coauthor.get("name"))
                            authorIds.append(coauthor.get("authorId"))
                    papers.append(PaperNode(title, year, authors, authorIds))
                    paper_count += 1
            author_node = AuthorNode(name, None, aliases, authorId, url, papers)
            author_nodes.append(author_node)
    return author_nodes

def makeAuthor(name):
    disamb = fetch_author(name)
    list_of_aliases = display_author_options(disamb)

    # print statement here, end function
    print("Enter the number corresponding to the desired author: ")

    # parts[-1] will be the index
    selected_author = list_of_aliases[0]

    if selected_author:
        author_nodes = parse_author_data(disamb)
        selected_author_node = None
        for author in author_nodes:
            if author.name == selected_author:
                selected_author_node = author
                break
        
        if selected_author_node:
          #print_author_details(selected_author_node)
          #print(selected_author_node.name)
          #print(type(selected_author_node))
          return selected_author_node  
        else:
            print("Selected author not found in the retrieved data.")

    else:
        print("No data found. Try again")

def create_coauthor_nodes(author_node):
    coauthor_nodes = []  # List to store coauthor nodes
    # Iterate through each paper of the author
    for paper in author_node.papers:
        r = requests.post('https://api.semanticscholar.org/graph/v1/author/batch',
            params={'fields': 'name,aliases,authorId,url'},
            json={"ids":paper.authorIds}
        )
        coauthors_data = r.json()
        for coauthor_data in coauthors_data:
            if coauthor_data['name'] != author_node.name:
                coauthor_node = AuthorNode(
                    name=coauthor_data['name'],
                    attributes=None,
                    aliases=coauthor_data['aliases'],
                    authorId=coauthor_data['authorId'],
                    url=coauthor_data['url'],
                    papers=[]  # Assuming we don't have papers for coauthors initially
                )
            coauthor_nodes.append(coauthor_node)
    return coauthor_nodes

def generate_author_list(author_name):
    author_list = []
    author = makeAuthor(author_name)
    if author:
        author_list.append(author)
        coauthors = create_coauthor_nodes(author)
        author_list.extend(coauthors)  # Extend the list with coauthors
        for each in author_list:
            print(each.name)
    else:
        print("Author not found.")

def print_author_details(auth):
            print("Name:", auth.name)
            print("Aliases:", ", ".join(auth.aliases))
            print("URL:", auth.url)
            if auth.papers:
                print("Papers:")
                for paper in auth.papers:
                    print("\tTitle:", paper.title)
                    print("\tYear:", paper.year)
                    print("\tAuthors:")
                    for author in paper.authors:
                        print(f"\t\tName: {author[0]}, Author ID: {author[1]}")
                    print()
            else:
                print("No papers found")


#user_input = "James Purtilo"
#author = makeAuthor(user_input)
#create_coauthor_nodes(author)
#generate_author_list(user_input)