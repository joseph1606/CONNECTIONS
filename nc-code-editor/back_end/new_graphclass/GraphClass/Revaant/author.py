#from APITesting import print_semscholar as sem_print

from Joel.Node import Node

author_list = []

class AuthorNode(Node):
    def __init__(self, name, attributes, aliases, authorId, url, papers=None):
        super().__init__(name, attributes)
        self.aliases = aliases if aliases else []
        self.authorId = authorId
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

#def makeAuthor(name):
