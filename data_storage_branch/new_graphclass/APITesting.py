import requests
import matplotlib.pyplot as plt

class AuthorNode:
    def __init__(self, name, aliases, url, papers=None):
        self.name = name
        self.aliases = aliases
        self.url = url
        self.papers = papers if papers else []

    def add_paper(self, paper):
        self.papers.append(paper)

class PaperNode:
    def __init__(self, title, year, authors=None):
        self.title = title
        self.year = year
        self.authors = authors if authors else []

    def add_author(self, author):
        self.authors.append(author)


def fetch_semantic_scholar_data(query):
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={query}&fields=name,aliases,url,papers.title,papers.year,papers.authors&limit=5"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
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


user_input = input("Enter a name: ")

author_data = fetch_semantic_scholar_data(user_input)

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


if author_data:
    for author in parse_author_data(author_data):
        visualize_author_node(author)
        #print(author)
else:
    print("No data found.")
