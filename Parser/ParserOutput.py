from tabulate import tabulate
class Node:
    def __init__(self, index, info, parent, rightSibling):
        self.info = info
        self.rightSibling = rightSibling
        self.parent = parent
        self.index = index

    def __str__(self) -> str:
        return "{" + str(self.index) + ", "+ str(self.info) + ", " + str(self.parent) + ", " + str(self.rightSibling)+ "}"


class ParserOutput:
    def __init__(self, workingStack, productions):
        self.__workingStack = workingStack
        self.__productions = productions
        self.tree = []
        self.buildParsingTree()

    def buildParsingTree(self):
        info, productionIndex = self.__workingStack[0]
        root = Node(0, info, None, None)
        self.tree.append(root)
        self.buildRecursive(1, info)

    def buildRecursive(self, index, parent):
        #we stop if we reached end of working stack
        if index == len(self.__workingStack):
            return
        #for a nonterminal
        if type(self.__workingStack[index]) is tuple:
            info = self.__workingStack[index][0]
            #if the current node is not a child of parameter parent then we are done with the subtree and we return
            if not self.isParent(parent, info):
                return
            #else we find the sibling and we construct the node
            sibling = self.findRightSibling(index,parent)
            node = Node(index,info,parent,sibling)
            self.tree.append(node)
            #node is nonterminal so we found a subtree
            #we parse that subtree
            self.buildRecursive(index+1, info)
            #if the node has a sibling we continue to parse the working stack
            if sibling:
                self.buildRecursive(sibling, parent)
        #for terminal
        else:
            info = self.__workingStack[index]
            # if the current node is not a child of parameter parent then we are done with the subtree and we return
            if not self.isParent(parent, info):
                return
            #else we construct the sibling and continue parsing the working stack
            sibling = self.findRightSibling(index,parent)
            node = Node(index,info,parent,sibling)
            self.tree.append(node)
            self.buildRecursive(index+1,parent)

    def isParent(self, parent, child):
        for key in self.__productions.keys():
            if parent in key:
                for element in self.__productions[key]:
                    if child in element:
                        return True
        return False

    def findRightSibling(self,index,parent):
        for i in range(index+1,len(self.__workingStack)):
            if type(self.__workingStack[i]) is tuple:
                potentialRightSibling = self.__workingStack[i][0]
            else:
                potentialRightSibling = self.__workingStack[i]
            if self.isParent(parent,potentialRightSibling):
                return i
        return None

    def findParentIndex(self, parent):
        for i in range(len(self.tree)):
            if self.tree[i].info == parent:
                return i

    def __str__(self):
        table = []
        headers = ["index","info","parent","right sibling"]
        for node in self.tree:
            line = (node.index,node.info,self.findParentIndex(node.parent),node.rightSibling)
            table.append(line)
        return tabulate(table,headers,"grid")

    def printToFile(self,file):
        f = open(file,"a")
        f.truncate(0)
        f.write(self.__str__())
