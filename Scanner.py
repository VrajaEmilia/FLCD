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
        if st == 'true' or st == 'false':
            return None
        if Scanner.checkSeparator(st):
            return None
        if Scanner.checkOperator(st):
            return None
        s = re.findall("^[a-zA-Z]+[0-9]*", st)
        return s

    @staticmethod
    def checkSeparator(st):
        s = re.findall("[,;(){}'\"]", st)
        return s

    @staticmethod
    def checkOperator(st):
        s = re.findall("[-=/*<>%]", st)
        return s

    def scan(self):
        error = ''
        error_index = 1
        f = open(self.__filePath, 'r').readlines()
        for line in f:
            line = line.replace("\n", "").replace("\t", "").split(" ")
            for token in line:
                if not token:
                    continue
                elif token in reservedWords or token in separators or token in operators:
                    self.__pif.append((token, -1))
                elif not self.checkOperator(token):
                    if (token[0] == "\"" and token[len(token) - 1] == "\"") or (
                            token[0] == "'" and token[len(token) - 1] == "'"):
                        self.__pif.append((token[0], -1))
                        self.__symbolTable.addConstant(token[1:-1])
                        self.__pif.append((token[1:-1], self.__symbolTable.hasConstant(token[1:-1])))
                        self.__pif.append((token[0], -1))
                    elif token.isnumeric():
                        self.__symbolTable.addConstant(token)
                        self.__pif.append((token,self.__symbolTable.hasConstant(token)))
                    elif self.checkIdentifier(token):
                        self.__symbolTable.addIdentifier(token)
                        self.__pif.append((token, self.__symbolTable.hasIdentifier(token)))
                    else:
                        error = error + 'invalid token on line ' + str(error_index) + '\n'
                else:
                    self.handleExpression(token)
            error_index+=1

        self.printToFile(error)

    def handleExpression(self, token):
        if not Scanner.checkOperator(token):
            if token.isnumeric():
                self.__symbolTable.addConstant(token)
                self.__pif.append((token, self.__symbolTable.hasConstant(token)))
            elif token == 'true' or token == 'false':
                self.__symbolTable.addConstant(token)
                self.__pif.append((token, self.__symbolTable.hasConstant(token)))
            elif self.checkIdentifier(token):
                self.__symbolTable.addIdentifier(token)
                self.__pif.append((token, self.__symbolTable.hasIdentifier(token)))
        else:
            op = Scanner.checkOperator(token)[0]
            token = token.split(op)
            token = Scanner.removeEmptyCharFromSplitToken(token)
            self.handleExpression(token[0])
            self.__pif.append((op, -1))
            self.handleExpression(token[1])

    def printToFile(self,error):
        f_pif = open("pif.out", "a")
        f_symbolTable = open("st.out", "a")
        f_pif.truncate(0)
        f_symbolTable.truncate(0)
        f_pif.write(self.pifToString())
        f_symbolTable.write(self.__symbolTable.__str__())
        self.pifToString()
        f_symbolTable.write(error)

    def pifToString(self):
        s = ''
        for pair in self.__pif:
            s = s + pair[0] + '  pos:   '
            if not type(pair[1]) == int:
                s = s + str(pair[1][0]) + ' ' + str(pair[1][1]) + '\n'
            else:
                s = s + str(pair[1]) + '\n'
        return s

    @staticmethod
    def removeEmptyCharFromSplitToken(token):
        newToken = []
        for item in token:
            if item == '':
                continue
            else:
                newToken.append(item)
        return newToken
