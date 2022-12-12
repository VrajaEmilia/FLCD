from Scanner.Scanner import Scanner
from Parser.Grammar import Grammar
from Parser.ParserOutput import ParserOutput

def read_w_from_pif(pif_filepath):
    with open(pif_filepath) as fp:
        w = []
        for line in fp:
            w.append(line.split(" ")[0])
    return w

def main():
    #g = Grammar("Parser/g2.in")
    g = Grammar("Tests/Emi_Grammar.in")
    w = read_w_from_pif("Tests/TestP1/pif_p1.out")
    print(w)
    print(g)
    # config = g.parse(['INCEPUT', '{', 'dec', '}', ';', '{', 'stmt', '}', 'SFARSIT'])
    config = g.parse(w)
    if(config.state == "f"):
        po = ParserOutput(config.workingStack, g.getProductions())
        print(po)
        #po.printToFile("Test/TestP1/parser_out1.txt")

main()