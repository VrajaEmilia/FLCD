import re

from Model.Scanner import Scanner

scanner1 = Scanner('Tests/TestP1/p1', 'Tests/TestP1/pif_p1.out', 'Tests/TestP1/st_p1.out')
scanner1.scan()

scanner2 = Scanner('Tests/TestP2/p2', 'Tests/TestP2/pif_p2.out', 'Tests/TestP2/st_p2.out')
scanner2.scan()

scanner3 = Scanner('Tests/TestP3/p3', 'Tests/TestP3/pif_p3.out', 'Tests/TestP3/st_p3.out')
scanner3.scan()

scanner3err = Scanner('Tests/TestP3err/p3err', 'Tests/TestP3err/pif_p3err.out', 'Tests/TestP3err/st_p3err.out')
scanner3err.scan()
