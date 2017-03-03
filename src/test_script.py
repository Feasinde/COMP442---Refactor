# from LexicalAnalyser import Lexer
from ParseTable import getParseTable

with open('code_sample_from_assignment.txt') as file:
	input_string = file.read()

# tokeniser = Lexer(input_string)
# token = tokeniser.nextToken()
# while token != '$':
# 	print(token)
# 	token = tokeniser.nextToken()

parse_table = getParseTable()
for i in parse_table['L4']: print(i)