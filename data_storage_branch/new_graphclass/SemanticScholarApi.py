import requests

# Pulls data from Semantic Scholar API; currently solves 

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

# Example usage:
author_data = fetch_semantic_scholar_data("john")
list_of_aliases = display_author_options(author_data)

selected_author = select_author_from_list(list_of_aliases)
if selected_author:
    print(f"You selected: {selected_author}")
