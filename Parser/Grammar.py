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
        key = productionsSet.split("->")[0].strip()
        values = productionsSet.split("->")[1].strip().split("|")
        for value in values:
            value = value.strip()
            if key not in self.__P.keys():
                self.__P[key] = []
            self.__P[key].append(value)

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
            [nonterminal + " -> " + " | ".join(self.__P[nonterminal]) for nonterminal in self.__P]
        ) + '\n'

    def getProductionsForNonterminal(self, nonterminal):
        return self.__P[nonterminal]

    def getProductionsStringForNonterminal(self, nonterminal):
        return nonterminal + " -> " + ' | '.join(self.__P[nonterminal]) + "\n"

    def __check__cfg_words(self, w):
        splitW = w.strip("\n").split(" ")
        print(splitW)

    def __check_CFG_handler(self, w, initial_w):
        if len(w) > len(initial_w):
            return False
        if w == initial_w:
            return True

        for char in w:
            if char in self.__N:
                for prod in self.__P[char]:
                    if self.__check_CFG_handler(w.replace(char, prod, 1), initial_w):
                        return True

        return False

    def __check_CFG_handler2(self, w, initial_w):
        if len(w) > len(initial_w):
             return False
        if w == initial_w:
             return True
        for token in w:
            if token in self.__N:
                for value in self.__P[token]:
                    index = w.index(token)
                    new_w = copy.deepcopy(w[:index] + value.split(" ") + w[index + 1:])
                    if self.__check_CFG_handler2(new_w, initial_w):
                        return True
        return False
        #
        # positions = {}
        # for nonterminal in self.__N:
        #     positions[nonterminal] = w.find(nonterminal)
        #
        # min = -1
        # toBeReplaced = ""
        # for i in positions:
        #     if positions[i] != -1:
        #         if min == -1:
        #             min = positions[i]
        #             toBeReplaced = i
        #         else:
        #             if min > positions[i]:
        #                 min = positions[i]
        #                 toBeReplaced = i
        #
        # for prod in self.__P[toBeReplaced]:
        #     if self.__check_CFG_handler(w.replace(toBeReplaced, prod, 1), initial_w):
        #         return True
        #
        # return False

    def checkCFG(self, w):
        return self.__check_CFG_handler2(["S"], w)
