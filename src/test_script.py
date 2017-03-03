from LexicalAnalyser import Lexer

with open('code_sample_from_assignment.txt') as file:
	input_string = file.read()

tokeniser = Lexer(input_string)
for i in range(100): print(tokeniser.nextToken())
# for i in range(len(input_string)):
# 	token = tokeniser.nextToken()
# 	print(token[1])