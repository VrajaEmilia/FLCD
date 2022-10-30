from Model.SymbolTable import SymbolTable
from constants import reservedWords, separators, operators
import re


class Scanner:
    def __init__(self, file):
        self.__symbolTable = SymbolTable()
        self.__pif = []
        self.__filePath = file

    @staticmethod
    def checkIdentifier(st):
        s = re.findall("^[a-zA-Z]+[0-9]*", st)
        return s

    @staticmethod
    def checkSeparator(st):
        s = re.findall("[,;(){}]", st)
        return s

    @staticmethod
    def checkOperator(st):
        s = re.findall("[-=/*<>%]", st)
        return s

    def parse(self):
        f = open(self.__filePath, 'r').readlines()
        for line in f:
            line = line.replace("\n", "").replace("\t", "").split(" ")
            for i in range(len(line)):
                token = line[i]
                if token in reservedWords or token in separators or token in operators:
                    self.__pif.append((token, -1))
                #check for string const or char const
                elif (token[0] == "\"" and token[len(token) - 1] == "\"") or (
                            token[0] == "'" and token[len(token) - 1] == "'"):
                    self.__pif.append((token[0], -1))
                    self.__symbolTable.addConstant(token[1:-1])
                    self.__pif.append((token[1:-1], self.__symbolTable.hasConstant(token[1:-1])))
                    self.__pif.append((token[0], -1))
                else:
                    #check for identifiers
                    if not Scanner.checkSeparator(token) and not Scanner.checkOperator(token):
                        if Scanner.checkIdentifier(token):
                            self.__symbolTable.addConstant(token)
                            self.__pif.append((token, self.__symbolTable.hasConstant(token)))
                    #check for identifiers followed by separators
                    elif Scanner.checkSeparator(token) and not Scanner.checkOperator(token):
                        self.__symbolTable.addConstant(token[:-1])
                        self.__pif.append((token[:-1], self.__symbolTable.hasConstant(token[:-1])))
                        self.__pif.append((token[len(token)-1],-1))
                    #check for expressions
                    elif Scanner.checkOperator(token):
                        if(Scanner.checkSeparator(token)):
                            self.handleExpression(token[:-1])
                            self.__pif.append((token[len(token)-1],-1))
                        else:
                            self.handleExpression(token)
                    else:
                        print(token)

    def handleExpression(self, token):
        print(token)



