from Scanner.SymbolTable import SymbolTable
from constants.constants import reservedWords, separators, operators
import re


class Scanner:
    def __init__(self, file, pifFile, stFile):
        self.__symbolTable = SymbolTable()
        self.__pif = []
        self.__filePath = file
        self.__pifFilePath = pifFile
        self.__stFilePath = stFile
        self.__error = ''
        self.__errIdx = 0

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
        if re.findall('<=|==|>=|!=',st):
            return re.findall('<=|==|>=|!=',st)
        s = re.findall("[-=/*<>%]", st)
        return s

    def scan(self):
        f = open(self.__filePath, 'r').readlines()
        line_index = 1
        for line in f:
            line = line.replace("\n", "").replace("\t", "").split(" ")
            for token in line:
                #empty line
                if not token:
                    continue
                #revered words/operators/sep
                elif token in reservedWords or token in separators or token in operators:
                    self.__pif.append((token, -1 , line_index))
                else:
                    self.handleTokenRecursive(token, line_index)
            self.__errIdx+=1
            line_index += 1
        self.printToFile()

    def handleTokenRecursive(self, token, line_index):
        #removing , between statements
        if re.findall(',',token):
            sep = re.findall(',',token)[0]
            token = token.replace(sep,'')
            self.handleTokenRecursive(token, line_index)
            self.__pif.append((sep, -1 , line_index))
        #checking if const or identifier
        elif not Scanner.checkOperator(token):
            #int const
            if token.isnumeric():
                self.__symbolTable.addConstant(token)
                self.__pif.append(("const", self.__symbolTable.hasConstant(token), line_index))
            #bool const
            elif token == 'true' or token == 'false':
                self.__symbolTable.addConstant(token)
                self.__pif.append(("const", self.__symbolTable.hasConstant(token), line_index))
            #string or char const
            elif (token[0] == "\"" and token[len(token) - 1] == "\"") or (
                    token[0] == "'" and token[len(token) - 1] == "'"):
                self.__pif.append((token[0], -1, line_index))
                self.__symbolTable.addConstant(token[1:-1])
                self.__pif.append(("const", self.__symbolTable.hasConstant(token[1:-1]), line_index))
                self.__pif.append((token[0], -1, line_index))
            #identifier
            elif self.checkIdentifier(token):
                self.__symbolTable.addIdentifier(token)
                self.__pif.append(("identifier", self.__symbolTable.hasIdentifier(token), line_index))
            else:
                self.__error = self.__error + 'invalid token on line ' + str(self.__errIdx) + ' : ' + token + '\n'
        #splits expressions by operators
        else:
            op = Scanner.checkOperator(token)[0]
            token = token.split(op)
            token = Scanner.removeEmptyCharFromSplitToken(token)
            self.handleTokenRecursive(token[0], line_index)
            self.__pif.append((op, -1, line_index))
            self.handleTokenRecursive(token[1], line_index)

    def printToFile(self):
        f_pif = open(self.__pifFilePath, "a")
        f_symbolTable = open(self.__stFilePath, "a")
        f_pif.truncate(0)
        f_symbolTable.truncate(0)
        f_pif.write(self.pifToString())
        f_symbolTable.write(self.__symbolTable.__str__())
        self.pifToString()
        f_symbolTable.write(self.__error)

    def pifToString(self):
        s = ''
        for pair in self.__pif:
            s = s + pair[0] + '  pos:   '
            if not type(pair[1]) == int:
                s = s + str(pair[1][0]) + ' ' + str(pair[1][1])
            else:
                s = s + str(pair[1])
            s = s + ' line: ' + str(pair[2]) + '\n'
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
