#from APITesting import print_semscholar as sem_print

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
