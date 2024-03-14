import json


class Node:
    def __init__(self, IDs, name: str):
        """Constructor that sets an author's information. The ID is a tuple of all database ids
        (when one is added, the programmer should add another id to the tuple in the data collection.
        If a database is not used, like when searching just patents, a -1 should be entered. For example,
        (semantic scholar ID, patent ID, -1) if you have 3 databases and are only using the first two).
        """
        if len(IDs) != IDConstants.NUM_DATABASES:
            raise Exception("Need a placeholder ID for each database not used!")

        self.IDs = IDs  # Note that the ID is tuple of ids from each database
        self.name = name
        # confidence interval that an id for a database is accurate
        self.confidenceInterval = (100, 50)


class Author(Node):
    def __init__(self, IDs, name: str, works: list):
        super().__init__(IDs, name)

        # ordered works by date
        self.works = works
        self.works = sorted(works, key=lambda x: x.date)


class Mentor(Node):
    def __init__(self, IDs, name: str, students: list, mentors: list = [], institutions: str):
        # mentor can have a mentor/mentors, if this is the case we make a list of the mentors
        super().__init_(IDs, name)

        self.students = students
        self.students = sorted(students, lambda x: x.name)

        self.mentors = sorted(mentors, lambda x: x.name)
        self.institutions = institutions.split(",")


class Student(Node):
    def __init__(self, IDs, name: str, mentor: str, institutions: str):
        super().__init__(IDs, name)

        self.mentor = [mentor]
        self.institutions = institutions.split(",")


class Misc(Node):
    def __init__(self, IDs, name: str, connections: str):
        super().__init__(IDs, name)

        # whatever relationship is created with whoever
        # assumes string of name(s) with comma delimeter
        self.connections = connections.split(",")
