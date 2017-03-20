from LexicalAnalyser import Lexer
from ParseTable import *
from Parser import Parser

with open('code_sample_from_assignment.txt') as file:
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
parser._parse(print_stack=False)
# bparser.printSymbolTables()

# table = SymbolTable('table')
# table.addSymbol('f1', 'function', ['float','int[2][2]', 'float'])
# table.addSymbol('f2', 'function', ['float'])
# table.addSymbol('class2', 'class', None)
# print(table.printTable())

