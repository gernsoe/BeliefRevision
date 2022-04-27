class Node:
    def __init__(self, data):
       self.leftNode = None
       self.rightNode = None
       self.data = data


class Interpretor:

    def __init__(self, root_node):
        self.root_node = root_node

    def is_operator(self, data):
        pass

    def init_tree(self):
        self.root_node.leftNode = Node("&")
        self.root_node.leftNode.rightNode = Node("r")
        self.root_node.leftNode.leftNode = Node("p")
        self.root_node.rightNode = Node("q")

    def print_tree(self, current_node):
        if ((current_node.leftNode is None) and (current_node.rightNode is None)):
            return current_node.data
        if (current_node.leftNode is None):
            return current_node.data
        if (current_node.rightNode is None):
            return current_node.data
        else:
            print("(" + self.print_tree(current_node.leftNode) + current_node.data + self.print_tree(current_node.rightNode))

inter = Interpretor(Node("|"))
inter.init_tree()
inter.print_tree(inter.root_node)


