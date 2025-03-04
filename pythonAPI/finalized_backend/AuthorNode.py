# from APITesting import print_semscholar as sem_print

from NodeClass import Node


class AuthorNode(Node):
    def __init__(self, name, attributes, aliases, authorId, url, papers=None):
        super().__init__(name, attributes)
        self.aliases = aliases if aliases else []
        self.authorId = authorId
        self.url = url
        self.papers = papers if papers else []

    def paper_list(node):
        p = []
        for paper in node.papers:
            p.append(paper.title)

        return sorted(p)


class PaperNode:
    def __init__(self, title, year, authors=None, authorIds=None):
        self.title = title
        self.year = year
        self.authors = authors if authors else []
        self.authorIds = authorIds if authorIds else []
