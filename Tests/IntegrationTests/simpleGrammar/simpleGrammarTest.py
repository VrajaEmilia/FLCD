from Parser.Grammar import Grammar
from Parser.ParserOutput import ParserOutput
from Scanner.Scanner import Scanner

def read_w_from_pif(pif_filepath):
    with open(pif_filepath) as fp:
        w = []
        for line in fp:
            w.append(line.split(" ")[0])
    return w

def main():
    s = Scanner('simpleProblem.in', 'pif.out', 'st.out')
    s.scan()
    g = Grammar('simpleGrammar.in')
    w = read_w_from_pif("pif.out")
    config = g.parse(w)
    print(config.workingStack)
    if config.state == "f":
        po = ParserOutput(config.workingStack, g.getProductions())
        po.printToFile('parserResult.out')


main()