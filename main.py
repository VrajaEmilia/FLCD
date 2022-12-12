from Scanner.Scanner import Scanner
# from Parser.Grammar import Grammar
# from Parser.ParserOutput import ParserOutput
# g = Grammar("Parser/g2.in")
# config = g.parse(['INCEPUT','{','dec','}',';','{','stmt','}','SFARSIT'])
# po = ParserOutput(config.workingStack,g.getProductions())
# print(po)
# po.printToFile('Parser/table.out')
scanner = Scanner('Tests/TestP1/p1','Tests/TestP1/pif_p1.out','Tests/TestP1/st_p1.out')
scanner.scan()
scanner2 = Scanner('Tests/TestP2/p2','Tests/TestP2/pif_p2.out','Tests/TestP2/st_p2.out')
scanner2.scan()
scanner3 = Scanner('Tests/TestP3/p3','Tests/TestP3/pif_p3.out','Tests/TestP3/st_p3.out')
scanner3.scan()