class HashTable:
    def __init__(self, size = 10):
        self.__elements = []
        for i in range(size):
            self.__elements.append([])
        self.__size = size

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
            return pos, len(self.__elements[pos]) - 1
        return None
