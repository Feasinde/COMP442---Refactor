from LexicalAnalyser import Lexer
from ParseTable import *
from Parser import Parser

with open('code_sample.txt') as file:
	input_string = file.read()

# tokeniser = Lexer(input_string)
# token = tokeniser.nextToken()
# while token[0] != '$':
# 	print(token)
# 	token = tokeniser.nextToken()

parse_table = getParseTable()
rulz = getRules()
terminals = getTerminals()
	

parser = Parser(rulz, terminals, parse_table, input_string)
parser._parse(print_stack=False,print_derivation=True,print_symtables=False)

# table = SymbolTable('table')
# table.addSymbol('f1', 'function', ['float','int[2][2]', 'float'])
# table.addSymbol('f2', 'function', ['float'])
# table.addSymbol('class2', 'class', None)
# table.addSymbol('var1','variable','int[2]')
# table.printTable()

# table2 = SymbolTable('otra_cosa')
# table.printTable()
# table2.printTable()

# print(table.lookUpSymbol('f1'))
# print(table.lookUpSymbol('f2'))
# print(table.lookUpSymbol('f3'))
# print(type(table))
# print(type(table) == SymbolTable)