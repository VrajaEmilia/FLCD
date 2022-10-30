import re

from Model.Scanner import Scanner

scanner = Scanner('p1')
scanner.parse()
print(re.findall('[<=+/*]','number<=0'))

