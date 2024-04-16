import requests
import matplotlib.pyplot as plt
from GraphClass.Tester.Revaant.author import AuthorNode, PaperNode


def fetch_semantic_scholar_data(query):
    """
    Fetches data from the Semantic Scholar API based on the provided query.

    Args:
    - query (str): The author's name or query string.

    Returns:
    - dict: JSON response from the API containing author information.
    """
    # Construct the API URL with the provided query
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={query}&fields=name,aliases,url,papers.title,papers.year,papers.authors&limit=5"
    
    try:
        # Make a GET request to the API and handle potential HTTP errors
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_author_options(aliases):
    """
    Displays a numbered list of author options based on the provided aliases.

    Args:
    - aliases (dict): Dictionary containing author information.

    Returns:
    - list: List of author names.
    """
    list_of_aliases = []
    if aliases["total"] > 0:
        # Iterate over the authors in the response and print their names and URLs
        for i, author in enumerate(aliases["data"]):
            name = author.get('name')
            url = author.get('url')
            print(f"{i + 1}. {name} ({url})")
            list_of_aliases.append(name)
            
    return list_of_aliases

def select_author_from_list(list_of_aliases):
    """
    Allows the user to select an author from the displayed list.

    Args:
    - list_of_aliases (list): List of author names.

    Returns:
    - str: Selected author's name.
    """
    try:
        # Prompt the user to input the number corresponding to the desired author
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
            url = author.get("url")
            papers = []
            if "papers" in author:
                for paper in author["papers"]:
                    title = paper.get("title")
                    year = paper.get("year")
                    authors = []
                    if "authors" in paper:
                        for coauthor in paper["authors"]:
                            authors.append(coauthor.get("name"))
                    papers.append(PaperNode(title, year, authors))
            author_node = AuthorNode(name, aliases, url, papers)
            author_nodes.append(author_node)
    return author_nodes

def visualize_author_node(author_node):
    # Create a plot
    plt.figure(figsize=(10, 6))

    # Plot the author node
    plt.text(
        0.5,
        0.5,
        f"Author: {author_node.name}\nAliases: {', '.join(author_node.aliases)}\nURL: {author_node.url}",
        ha="center",
        va="center",
        bbox=dict(facecolor="lightblue", alpha=0.5),
    )

    # Plot the papers
    for i, paper in enumerate(author_node.papers):
        plt.text(
            0.5,
            0.3 - 0.15 * i,
            f"Paper {i+1}:\nTitle: {paper.title}\nYear: {paper.year}\nAuthors: {', '.join(paper.authors)}",
            ha="center",
            va="center",
            bbox=dict(facecolor="lightgreen", alpha=0.5),
        )

    plt.axis("off")
    plt.title("Author and Papers")
    plt.show()


user_input = input("Enter Name:")
disamb = fetch_semantic_scholar_data(user_input)
list_of_aliases = display_author_options(disamb)

selected_author = select_author_from_list(list_of_aliases)

if selected_author:
    author_nodes = parse_author_data(disamb)
    selected_author_node = None
    for author in author_nodes:
        if author.name == selected_author:
            selected_author_node = author
            break
    
    if selected_author_node:
        print("Name:", selected_author_node.name)
        print("Aliases:", ", ".join(selected_author_node.aliases))
        print("URL:", selected_author_node.url)

        if selected_author_node.papers:
            for paper in selected_author_node.papers:
                print("\tTitle:", paper.title)
                print("\tYear:", paper.year)
                print("\tAuthors:", ", ".join(paper.authors))
                print()
    else:
        print("Selected author not found in the retrieved data.")
else:
    print("No data found.")