from LexicalAnalyser import Lexer

with open('code_sample_from_assignment.txt') as file:
	input_string = file.read()

tokeniser = Lexer(input_string)
token = tokeniser.nextToken()
while token != '$':
	print(token)
	token = tokeniser.nextToken()