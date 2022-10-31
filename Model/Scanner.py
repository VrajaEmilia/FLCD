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
                        if Scanner.checkSeparator(token):
                            self.handleExpression(token[:-1])
                            self.__pif.append((token[len(token)-1],-1))
                        else:
                            self.handleExpression(token)
                    else:
                        print(token)

        self.printToFile()
    def handleExpression(self, token):
        if not Scanner.checkOperator(token):
            if Scanner.checkIdentifier(token):
                self.__symbolTable.addIdentifier(token)
                self.__pif.append((token,self.__symbolTable.hasIdentifier(token)))
            else:
                self.__symbolTable.addConstant(token)
                self.__pif.append((token,self.__symbolTable.hasConstant(token)))
        elif re.findall('==',token):
            self.handleExpression(token.split('==')[0])
            self.__pif.append(('==', -1))
            self.handleExpression(token.split('==')[1])
        elif re.findall('<=', token):
            self.handleExpression(token.split('<=')[0])
            self.__pif.append(('<=', -1))
            self.handleExpression(token.split('<=')[1])
        elif re.findall('>=', token):
            self.handleExpression(token.split('>=')[0])
            self.__pif.append(('>=', -1))
            self.handleExpression(token.split('>=')[1])
        elif re.findall('!=', token):
            self.handleExpression(token.split('!=')[0])
            self.__pif.append(('!=', -1))
            self.handleExpression(token.split('!=')[1])
        elif Scanner.checkOperator(token):
            op = Scanner.checkOperator(token)[0]
            self.handleExpression(token.split(op)[0])
            self.__pif.append((op,-1))
            self.handleExpression(token.split(op)[1])

    def printToFile(self):
        f_pif= open("pif.out","a")
        f_symbolTable = open("st.out","a")
        f_pif.write(self.pifToString())
        f_symbolTable.write(self.__symbolTable.__str__())
        self.pifToString()

    def pifToString(self):
        s = ''
        for pair in self.__pif:
            s = s + pair[0] + '  pos:   '
            if not type(pair[1])==int:
                s = s + str(pair[1][0]) + ' ' + str(pair[1][1]) + '\n'
            else:
                s = s + str(pair[1]) + '\n'
        return s