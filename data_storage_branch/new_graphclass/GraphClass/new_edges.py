import new_graphclass.GraphClass.new_node as new_node


class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2


class AuthorEdge(Edge):
    def __init__(
        self, prim_auth: new_node.Author, sec_auth: new_node.Author, shared_works: str
    ):
        super().__init__(prim_auth, sec_auth)
        self.prim_auth = prim_auth
        self.sec_auth = sec_auth
        self.shared_works = shared_works.split(",")


class MentorEdge(Edge):
    def __init__(
        self, mentor: new_node.Mentor, student: new_node.Student, institutions: str
    ):
        super().__init__(mentor, student)
        self.mentor = mentor
        self.student = student
        self.institutuions = institutions.split(",")


class MiscEdge(Edge):
    def __init__(self, node1: new_node.Node, node2: new_node.Node, properties: str):
        super().__init__(node1, node2)
        self.properties = properties.split(",")
