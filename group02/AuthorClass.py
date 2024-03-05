#test
class Info:
    """Class for a graph"""

    def __init__(self, name):
        """Constructor for a connection must be implemented by subclass."""
        self.name = name
        self.alias = ""
        self.url = ""
        self.papers = {}

    def getName(self):
        """Getter for the work's name"""
        return self.name
