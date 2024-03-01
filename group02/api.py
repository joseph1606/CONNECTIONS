import requests

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

def display_author_data(author_data):
    if author_data["total"] > 0:
        print("Works")
        for author in author_data["data"]:
            print("Name:", author.get("name"))
            print("Aliases:", author.get("aliases"))
            print("URL:", author.get("url"))
            if "papers" in author:
                print("Papers:")
                for paper in author["papers"]:
                    print("\tTitle:", paper.get("title"))
                    print("\tYear:", paper.get("year"))
                    if "authors" in paper:
                        print("\tAuthors:")
                        for coauthor in paper["authors"]:
                            print("\t\tName:", coauthor.get("name"))
                    print("\t-------------------")
            print("===================")


# # Example usage:
query = "JamesPurtilo"
data = fetch_semantic_scholar_data(query)
if data:
    print(data)
    display_author_data(data)
