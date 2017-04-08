########################################################
## Driver program for the 2017 COMP 442 final project ##
## compiler, by Andrés Lou, 27142374                  ##
########################################################

from LexicalAnalyser import Lexer
from ParseTable import *
from Parser import Parser
import argparse

# Setup flags and parameters
parser = argparse.ArgumentParser(prog='Lexer', description='Takes source code file and allegedly compiles it')
parser.add_argument('-f','--file')
parser.add_argument('-t','--tokenise', action='store_true')
parser.add_argument('-o','--output')
parser.add_argument('-p','--parse', action='store_true')
parser.add_argument('-s','--symbol_tables', action='store_true')
parser.add_argument('-d','--derivation',action='store_true')
parser.add_argument('-k','--stack',action='store_true')
args = parser.parse_args()

## Open output file if -o is included
if args.output == None:
    output = False
else: output = True
if output:
    op = open(args.output, 'w')
    op.close()

with open(args.file,'r') as file:
	input_string = file.read()

## Tokeniser
if args.tokenise:
	tokenise = True
else: tokenise = False

if tokenise:
	tokeniser = Lexer(input_string)
	token = tokeniser.nextToken()
	print('hoal')
	while token[0] != '$':
		if output:
			with open(args.output,'a') as op:
				op.write(str(token)+'\n')
				token = tokeniser.nextToken()
		else:
			print(token)
			token = tokeniser.nextToken()

## Symbol tables
if args.parse:
	parse = True
else: parse = False

if args.symbol_tables:
	output_tables = True
else: output_tables = False

if args.derivation:
	output_derivation = True
else: output_derivation = False

if args.stack:
	output_stack = True
else: output_stack = False

if parse:
	parse_table = getParseTable()
	rulz = getRules()
	terminals = getTerminals()

	parser = Parser(rulz, terminals, parse_table, input_string)
	if output:
		op = open(args.output,'w')
		# parser._parse(print_stack=False,print_derivation=False,print_symtables=False,op_file=op)
		parser._parse(print_stack=output_stack,print_derivation=output_derivation,print_symtables=output_tables,op_file=op,second_pass=True)
		op.close
	else:
		# parser._parse(print_stack=False,print_derivation=False,print_symtables=False)
		parser._parse(print_stack=output_stack,print_derivation=output_derivation,print_symtables=output_tables,second_pass=True)