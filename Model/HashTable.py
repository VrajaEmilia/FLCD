class HashTable:
    def __init__(self, size = 100):
        self.__elements = []
        for i in range(size):
            self.__elements.append([])
        self.__size = size
        self.__orderedElements = []

    def getElements(self):
        return self.__elements

    def hashFunction(self,element):
        return abs(hash(element) % self.__size)

    def getElement(self, element):
        pos = self.hashFunction(element)
        for index,item in enumerate(self.__elements[pos]):
            if(item == element):
                return pos, index
        return None

    def addElement(self,element):
        if self.getElement(element) is None:
            pos = self.hashFunction(element)
            self.__elements[pos].append(element)
            self.__orderedElements.append((element,(pos, len(self.__elements[pos]) - 1)))
            return pos, len(self.__elements[pos]) - 1
        return None

    def __str__(self) -> str:
        s = ''
        for element in self.__orderedElements:
            s = s + element[0] + "  pos:  " + str(element[1][0]) + ' ' + str(element[1][1]) + '\n'
        return s


