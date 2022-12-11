import copy
class Grammar:
    def __init__(self, N, E, P, S):
        self.__N = N
        self.__E = E
        self.__S = S
        self.__P = P

    def __init__(self, filename):
        with open(filename, "r") as f_in:
            for line in f_in:
                if line[0] == 'N':
                    self.__N = self.__parseSet(line)
                elif line[0] == 'E':
                    self.__E = self.__parseSet(line)
                elif line[0] == 'S':
                    self.__S = line.strip().replace(" ", "").split("=")[1]
                elif line[0] == 'P':
                    self.__P={}
                    text = line.strip()
                    try:
                        l = f_in.readline().strip()
                        while l:
                            self.__parseProductions(l)
                            l = f_in.readline().strip()
                    except StopIteration:
                        pass

    def __parseSet(self, line):
        set = line.split("=")[1].strip().split(" ")
        return set

    def __parseProductions(self, productionsSet):
        key = tuple(productionsSet.split("->")[0].strip().split(" "))
        values = productionsSet.split("->")[1].strip().split("|")
        for value in values:
            value = value.strip()
            if key not in self.__P.keys():
                self.__P[key] = []
            self.__P[key].append(value.split(" "))

    def getNonTerminalsString(self):
        return 'N = { ' + ', '.join(self.__N) + ' }\n'

    def getTerminalsString(self):
        return 'E = { ' + ', '.join(self.__E) + ' }\n'

    def getProductionsString(self):
        return 'S = {\n' + ',\n'.join(
            [nonterminal + " -> " + self.__P[nonterminal].join(" | ") for nonterminal in self.__P]
        ) + '\n}\n'

    def __str__(self):
        return 'N = ' + " ".join(self.__N) + '\n' \
               + 'E = ' + ' '.join(self.__E) + '\n' \
               + 'S = ' + self.__S + '\n'\
               + 'P = \n' + '\n'.join(
            [" ".join(nonterminal) + " -> " + " | ".join(" ".join(production) for production in self.__P[nonterminal]) for nonterminal in self.__P]
        ) + '\n'

    def getProductionsForNonterminal(self, nonterminal):
        return self.__P[nonterminal]

    def getProductionsStringForNonterminal(self, nonterminal):
        return nonterminal + " -> " + ' | '.join(self.__P[nonterminal]) + "\n"

    def getProductions(self):
        return self.__P

    def checkCFG(self):
        for key in self.__P:
            if len(key) > 1 or key[0] not in self.__N:
                return False
        return True

    class Configuration:
        def __init__(self,w,S):
            self.w = w
            self.state = "q"
            self.index = 0
            self.workingStack = []
            self.inputStack = [S]

        def currentSymbol(self):
            return self.w[self.index]

    def expand(self, config : Configuration):
        head = config.inputStack[-1]
        config.workingStack.append((head,0))
        config.inputStack.pop()
        production = self.__P[(head,)][0]
        for i in reversed(production):
            config.inputStack.append(i)

    def advance(self, config: Configuration):
        head = config.inputStack[-1]
        config.workingStack.append(head)
        config.inputStack.pop()
        config.index += 1

    def momentary_insuccess(self, config: Configuration):
        config.state = "b"

    def back(self, config: Configuration):
        terminal = config.workingStack[-1]
        config.workingStack.pop()
        config.inputStack.append(terminal)
        config.index -= 1

    def another_try(self, config: Configuration):
        nonterminal,prodIndex = config.workingStack[-1]
        productions = self.__P[(nonterminal,)]
        for i in range(len(productions[prodIndex])):
            config.inputStack.pop()
        config.workingStack.pop()

        if len(productions) > prodIndex + 1:
            prodIndex += 1
            config.workingStack.append((nonterminal,prodIndex))
            newProduction = productions[prodIndex]
            for i in reversed(newProduction):
                config.inputStack.append(i)
            config.state = "q"
        else:
            config.inputStack.append(nonterminal)
            if config.index == 0 and config.inputStack[-1] == self.__S:
                config.state = "e"

    def success(self, config: Configuration):
        config.state = "f"

    def parse(self,w):
        config = self.Configuration(w,self.__S)
        while config.state != "f" and config.state != "e":
            if config.state == "q":
                if config.index >= len(w) and config.inputStack == []:
                    self.success(config)
                else:
                    if config.inputStack[-1] in self.__N:
                        self.expand(config)
                    else:
                        if config.inputStack[-1] == config.currentSymbol():
                            self.advance(config)
                        else:
                            self.momentary_insuccess(config)
            else:
                if config.state == "b":
                    if config.workingStack[-1] in self.__E:
                        self.back(config)
                    else:
                        self.another_try(config)

        if config.state == "e":
            print("Parse result: Error")
            return ""
        else:
            print("Parse result: Sequence accepted")
            return config
