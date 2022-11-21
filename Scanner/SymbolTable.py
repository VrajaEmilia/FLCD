from Scanner.HashTable import HashTable


class SymbolTable:
    def __init__(self):
        self.__identifierHashTable =  HashTable(30)
        self.__constantsHashTable = HashTable(30)

    def addIdentifier(self,identifier):
        return self.__identifierHashTable.addElement(identifier)

    def addConstant(self, constant):
        return self.__constantsHashTable.addElement(constant)

    def hasIdentifier(self,identifier):
        return self.__identifierHashTable.getElement(identifier)

    def hasConstant(self,constant):
        return self.__constantsHashTable.getElement(constant)

    def __str__(self) -> str:
        return 'identifier : \n' + self.__identifierHashTable.__str__() + '\n constants: \n' + self.__constantsHashTable.__str__()


