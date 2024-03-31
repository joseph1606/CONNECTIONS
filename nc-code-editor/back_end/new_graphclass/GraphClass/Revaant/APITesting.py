import requests
from author import AuthorNode, PaperNode


def fetch_semantic_scholar_data(query):
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

def select_author_from_list(list_of_aliases):
    try:
        selected_index = int(input("Enter the number corresponding to the desired author: ")) - 1
        selected_author = list_of_aliases[selected_index]
        return selected_author
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number.")
        return None

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
                for paper in author["papers"]:
                    title = paper.get("title")
                    year = paper.get("year")
                    authors = [author_name.get("name") for author_name in paper.get("authors", [])]
                    papers.append(PaperNode(title, year, authors))
            author_node = AuthorNode(name, aliases, authorId, url, papers)
            author_nodes.append(author_node)
    return author_nodes

def makeAuthor(name):
    disamb = fetch_semantic_scholar_data(name)
    list_of_aliases = display_author_options(disamb)

    selected_author = select_author_from_list(list_of_aliases)

    if selected_author:
        author_nodes = parse_author_data(disamb)
        selected_author_node = next((author for author in author_nodes if author.name == selected_author), None)
        
        if selected_author_node:
            print("Name:", selected_author_node.name)
            print("Aliases:", ", ".join(selected_author_node.aliases))
            print("Author Id:", selected_author_node.authorId)
            print("URL:", selected_author_node.url)

            if selected_author_node.papers:
                for paper in selected_author_node.papers:
                    print("\tTitle:", paper.title)
                    print("\tYear:", paper.year)
                    if len(paper.authors) > 1:
                        coauthors = [author for author in paper.authors if author != selected_author_node.name]
                        print("\tCoauthors:", ", ".join(coauthors))
                    print()

        else:
            print("Selected author not found in the retrieved data.")
    else:
        print("No data found.")

user_input = input("Enter Name:")
makeAuthor(user_input)