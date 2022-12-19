from tabulate import tabulate


class Node:
    def __init__(self, index, info, parent, rightSibling):
        self.info = info
        self.rightSibling = rightSibling
        self.parent = parent
        self.index = index

    def __str__(self) -> str:
        return "{" + str(self.index) + ", " + str(self.info) + ", " + str(self.parent) + ", " + str(
            self.rightSibling) + "}"


class ParserOutput:
    def __init__(self, workingStack, productions):
        self.__workingStack = workingStack
        self.__productions = productions
        self.tree = []
        self.workingStackIndex = 0
        self.buildParsingTree()

    def buildParsingTree(self):
        info, productionIndex = self.__workingStack[0]
        root = Node(0, info, None, None)
        self.tree.append(root)
        self.buildTree(0)
        # self.buildRecursive(1, info)

    def buildTree(self, parentIndex):
        prodCount = len(self.__productions[(self.__workingStack[self.workingStackIndex][0],)][
                            self.__workingStack[self.workingStackIndex][1]])
        # print("***",self.__productions[(self.__workingStack[self.workingStackIndex][0],)])
        for i in range(prodCount):
            self.workingStackIndex += 1
            current = self.__workingStack[self.workingStackIndex]
            if type(current) is tuple:
                info = current[0]
                node = Node(self.workingStackIndex, info, parentIndex, None)
                self.tree.append(node)
                self.buildTree(self.workingStackIndex)
            else:
                node = Node(self.workingStackIndex, current, parentIndex, None)
                self.tree.append(node)

    def isParent(self, parent, child):
        for key in self.__productions.keys():
            if parent in key:
                for element in self.__productions[key]:
                    if child in element:
                        return True
        return False

    def findRightSibling(self, node):
        for i in range(node.index + 1, len(self.tree)):
            if self.tree[i].parent == node.parent:
                return self.tree[i].index

    def findParentIndex(self, parent):
        for i in range(len(self.tree)):
            if self.tree[i].info == parent:
                return i

    def __str__(self):
        table = []
        headers = ["index", "info", "parent", "right sibling"]
        for node in self.tree:
            line = (node.index, node.info, node.parent, self.findRightSibling(node))
            table.append(line)
        return tabulate(table, headers, "grid")

    def printToFile(self, file):
        f = open(file, "a")
        f.truncate(0)
        f.write(self.__str__())
