from api import fetch_semantic_scholar_data, display_author_data

user_input = input("Enter a name: ")

data = fetch_semantic_scholar_data(user_input)
if data:
    # print(data)
    display_author_data(data)
