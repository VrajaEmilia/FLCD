from Scanner.Scanner import Scanner
from Parser.Grammar import Grammar
g = Grammar("Parser/g2.in")
print(g)
print(g.checkCFG(['INCEPUT','{','d','}',';','{','b','}','SFARSIT']))