from Scanner.Scanner import Scanner
from Parser.Grammar import Grammar
from Parser.ParserOutput import ParserOutput

def read_w_from_pif(pif_filepath):
    with open(pif_filepath) as fp:
        w = []
        for line in fp:
            w.append(line.split(" ")[0])
    return w

def simpleTests():
    s = Scanner('Tests/TestP1/p1', 'Tests/TestP1/pif_p1.out', 'Tests/TestP1/st_p1.out')
    s2 = Scanner('Tests/TestP1/p1', 'Tests/TestP1/pif_p1.out', 'Tests/TestP1/st_p1.out')
    s.scan()
    g = Grammar('Tests/IntegrationTests/simpleGrammar/simpleGrammar.in')
    w = read_w_from_pif("Tests/TestP1/pif_p1.out")
    config = g.parse(w)
    if config.state == "f":
        po = ParserOutput(config.workingStack,g.getProductions())
        po.printToFile('ParserTests/p1_parser_result')

def main():
    g = Grammar("Tests/IntegrationTests/simpleGrammar/simpleGrammar.in")
    #g = Grammar("Tests/complexGrammar.in")
    if g.checkCFG():
        w = read_w_from_pif("Tests/TestP1/pif_p1.out")
      #  print(w)
      #  print(g)
        config = g.parse(['INCEPUT', '{', 'dec', '}', ';', '{', 'stmt', '}', 'SFARSIT'])
        #config = g.parse(w)
        if config.state == "f":
            po = ParserOutput(config.workingStack, g.getProductions())
            po.printToFile("Tests/TestP1/parser_outp1")
    else:
        print("not cfg")
    # po = ParserOutput(config.workingStack, g.getProductions())
    # print(po)
    # po.printToFile('Parser/table.out')

main()