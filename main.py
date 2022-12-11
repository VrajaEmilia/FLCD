from Scanner.Scanner import Scanner
from Parser.Grammar import Grammar
from Parser.ParserOutput import ParserOutput
g = Grammar("Parser/g2.in")
config = g.parse(['INCEPUT','{','dec','}',';','{','stmt','}','SFARSIT'])
po = ParserOutput(config.workingStack,g.getProductions())
print(po)
po.printToFile('Parser/table.out')