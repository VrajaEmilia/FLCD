from Parser.Grammar import Grammar
from Parser.ParserOutput import ParserOutput
from Scanner.Scanner import Scanner

def read_line_of_token(index,pif_filepath):
    with open(pif_filepath) as fp:
        count = 0
        for line in fp:
            count += 1
            if(count == index):
                return line.split(" ")[-1]

def read_w_from_pif(pif_filepath):
    with open(pif_filepath) as fp:
        w = []
        for line in fp:
            w.append(line.split(" ")[0])
    return w

def testProblem(problem_file):
    s = Scanner(problem_file, 'pif.out', 'st.out')
    s.scan()
    g = Grammar('complexGrammar.in')
    w = read_w_from_pif("pif.out")
    config = g.parse(w)
    if config.state == "f":
        po = ParserOutput(config.workingStack, g.getProductions())
        po.printToFile(problem_file + "_table.out")
    else:
            print(f"Parse result: Error")
            print(f"Could not resolve {config.w[config.mostFarIndex]} on line {read_line_of_token(config.mostFarIndex,'pif.out')}")

def testP3err():
    s = Scanner('p3err', 'pif.out', 'st.out')
    s.scan()
    g = Grammar('complexGrammar.in')
    w = read_w_from_pif("pif.out")
    config = g.parse(w)
    if config.state == "f":
        po = ParserOutput(config.workingStack, g.getProductions())
        po.printToFile('Tests/IntegrationTests/ComplexGrammar/parserResult.out')

def main():
    testProblem('p2')

main()