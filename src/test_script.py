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

# def getFirst(symbol):
# 	first_ = []
# 	first = set(first_)
# 	for i in parse_table[symbol]:
# 		first = first.union(parse_table[symbol][i]._first)
# 	return first

# print(getFirst('class'))

parser = Parser(rulz, terminals, parse_table, input_string)
parser._parse(print_stack=True)