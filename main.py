from Scanner.Scanner import Scanner
from Parser.Grammar import Grammar
g = Grammar("Parser/g2.in")
print(g)
print(g.checkCFG())
print(g.parse(['INCEPUT','{','dec','}',';','{','stmt','}','SFARSIT']))