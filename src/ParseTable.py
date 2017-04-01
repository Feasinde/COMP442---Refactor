from enum import Enum

## Create directives enum class
class Directive(Enum):
	CREATE_GLOBAL_TABLE = 1
	CREATE_CLASS_ENTRY_AND_TABLE = 2
	CREATE_PROGRAM_TABLE = 3
	CREATE_FUNCTION_ENTRY_AND_TABLE = 4
	CREATE_VARIABLE_ENTRY = 5
	CLOSE_SCOPE = 7
	CAPTURE_TOKEN = 8
	CAPTURE_DIMENSIONALITY = 11
	POP_SEMANTIC_STACK = 12

## Create SymbolTable class

class SymbolTable():
	## A symbol table contains a list of symbols, each of which is a
	## list of strings representing the information of the entry

	def __init__(self,name_of_table):
		self.symbols = []
		self.name = name_of_table
	def addSymbol(self,_name,_kind,_type=None,_link=None):
		self.symbols.append([_name, _kind, _type, _link])

	def printTable(self):
		print('---',self.name,'---------------------------------------------------')
		for i in self.symbols:
			print(i)
		print('-------------------------------------------------------------------\n')

## Create rule object

class Rule:
	def __init__(self, first_set, follow_set, symbol, production):
		self._symbol = symbol
		self._first = first_set
		self._follow = follow_set
		self._production = production

## Add rules from the grammar

rulz = []
rulz.append(Rule({'class', 'program'}, {}, 'prog', [Directive.CREATE_GLOBAL_TABLE, 'N1', 'progBody',Directive.CLOSE_SCOPE]))
rulz.append(Rule({'class'}, {}, 'classDecl', ['class',Directive.CAPTURE_TOKEN,'id',Directive.CREATE_CLASS_ENTRY_AND_TABLE,'{', 'A1', '}',Directive.CLOSE_SCOPE,';']))
rulz.append(Rule({'program'},{}, 'progBody', ['program',Directive.CREATE_PROGRAM_TABLE,'funcBody',Directive.CLOSE_SCOPE, ';', 'N3']))
rulz.append(Rule({'float', 'id', 'int'}, {}, 'funcHead', ['type', 'id', '(', 'fParams', ')']))
rulz.append(Rule({'float', 'id', 'int'}, {}, 'funcDef', [Directive.CAPTURE_TOKEN,'funcHead',Directive.CREATE_FUNCTION_ENTRY_AND_TABLE,'funcBody',Directive.CLOSE_SCOPE]))
rulz.append(Rule({'{'}, {}, 'funcBody', ['{', 'A4', '}']))
rulz.append(Rule({'id'}, {}, 'statement', ['assignStat', ';']))
rulz.append(Rule({'return'}, {}, 'statement',['return', '(', 'expr', ')', ';']))
rulz.append(Rule({'put'}, {}, 'statement',['put', '(', 'expr', ')', ';']))
rulz.append(Rule({'get'}, {}, 'statement',['get', '(', 'variable', ')', ';']))
rulz.append(Rule({'if'}, {}, 'statement',['if', '(', 'expr', ')', 'then', 'statBlock', 'else', 'statBlock', ';']))
rulz.append(Rule({'for'}, {}, 'statement',['for', '(', 'type', 'id', 'assignOp', 'expr', ';', 'relExpr', ';', 'assignStat', ')', 'statBlock', ';']))
rulz.append(Rule({'id'}, {}, 'assignStat',['variable', 'assignOp', 'expr']))
rulz.append(Rule({'EPSILON'}, {';', 'else'}, 'statBlock', ['EPSILON']))
rulz.append(Rule({'for', 'if', 'get', 'put', 'return', 'id'}, {}, 'statBlock', ['statement']))
rulz.append(Rule({'{'}, {}, 'statBlock',['{', 'N4', '}']))
rulz.append(Rule({'(', 'not', 'id', 'float_num', 'integer', '+', '-'}, {}, 'expr',['arithExpr', 'L1']))
rulz.append(Rule({'(', 'num', 'not', 'id', '+', '-'}, {}, 'relExpr',['arithExpr', 'relOp', 'arithExpr']))
rulz.append(Rule({'(', 'not', 'id', 'float_num', 'integer', '+', '-'}, {}, 'arithExpr',['term', 'L2']))
rulz.append(Rule({'+'}, {}, 'sign', ['+']))
rulz.append(Rule({'-'}, {}, 'sign',['-']))
rulz.append(Rule({'(', 'not', 'id', 'float_num', 'integer', '+', '-'}, {}, 'term',['factor', 'L3']))
rulz.append(Rule({'+', '-'}, {}, 'factor',['sign', 'factor']))
rulz.append(Rule({'id'}, {}, 'factor', ['A8', 'L4']))
rulz.append(Rule({'not'}, {}, 'factor', ['not', 'factor']))
rulz.append(Rule({'float_num', 'integer'}, {}, 'factor', ['num']))
rulz.append(Rule({'('}, {}, 'factor',['(', 'arithExpr', ')']))
rulz.append(Rule({'id'}, {}, 'variable', ['A8']))
rulz.append(Rule({'['}, {}, 'indice', ['[', 'arithExpr', ']']))
rulz.append(Rule({'['}, {}, 'arraySize',['[', 'integer', ']']))
rulz.append(Rule({'int'}, {}, 'type', ['int']))
rulz.append(Rule({'id'}, {}, 'type', ['id']))
rulz.append(Rule({'float'}, {}, 'type', ['float']))
rulz.append(Rule({'EPSILON'}, {')'}, 'fParams', ['EPSILON']))
rulz.append(Rule({'float', 'id', 'int'}, {}, 'fParams', ['type', 'id', 'N5', 'N8']))
rulz.append(Rule({'EPSILON'}, {')'}, 'aParams', ['EPSILON']))
rulz.append(Rule({'(', 'num', 'not', 'id', '+', '-'}, {}, 'aParams', ['expr', 'N9']))
rulz.append(Rule({','}, {}, 'fParamsTail', [',','type', 'id', 'N5']))
rulz.append(Rule({','}, {}, 'aParamsTail',[',','expr']))
rulz.append(Rule({'='}, {}, 'assignOp', ['=']))
rulz.append(Rule({'>='}, {}, 'relOp',['>=']))
rulz.append(Rule({'>'}, {}, 'relOp',['>']))
rulz.append(Rule({'=='}, {}, 'relOp',['==']))
rulz.append(Rule({'<>'}, {}, 'relOp',['<>']))
rulz.append(Rule({'<='}, {}, 'relOp',['<=']))
rulz.append(Rule({'<'}, {}, 'relOp',['<']))
rulz.append(Rule({'or'}, {}, 'addOp',['or']))
rulz.append(Rule({'-'}, {}, 'addOp',['-']))
rulz.append(Rule({'+'}, {}, 'addOp',['+']))
rulz.append(Rule({'and'}, {}, 'multOp',['and']))
rulz.append(Rule({'/'}, {}, 'multOp',['/']))
rulz.append(Rule({'*'}, {}, 'multOp',['*']))
rulz.append(Rule({'EPSILON'}, {'program'}, 'N1',['EPSILON']))
rulz.append(Rule({'class'}, {}, 'N1',['classDecl', 'N1']))
rulz.append(Rule({'EPSILON'}, {'$'}, 'N3',['EPSILON']))
rulz.append(Rule({'float', 'id', 'int'}, {}, 'N3',['funcDef', ';', 'N3']))
rulz.append(Rule({'EPSILON'}, {'}'}, 'N4',['EPSILON']))
rulz.append(Rule({'for', 'if', 'get', 'put', 'return', 'id'}, {}, 'N4',['statement', 'N4']))
rulz.append(Rule({'EPSILON'}, {';', ',', '}', 'float', 'id', 'int', 'for', 'if', 'get', 'put', 'return', ')'}, 'N5',['EPSILON']))
rulz.append(Rule({'['}, {}, 'N5',['arraySize', 'N5']))
rulz.append(Rule({'EPSILON'}, {'.', ';', ')', ',', '<', '<=', '<>', '==', '>', '>=', ']', '+', '-', 'or', '*', '/', 'and', '(', '='}, 'N7',['EPSILON']))
rulz.append(Rule({'['}, {}, 'N7',['indice', 'N7']))
rulz.append(Rule({'EPSILON'}, {')'}, 'N8',['EPSILON']))
rulz.append(Rule({','}, {}, 'N8',['fParamsTail', 'N8']))
rulz.append(Rule({'EPSILON'}, {')'}, 'N9',['EPSILON']))
rulz.append(Rule({','}, {}, 'N9',['aParamsTail', 'N9']))
rulz.append(Rule({'EPSILON'}, {';', ')', ',', '}', 'id', 'for', 'if', 'get', 'put', 'return', 'float', 'int'}, 'L1', ['EPSILON']))
rulz.append(Rule({'<', '<=', '<>', '==', '>', '>='}, {}, 'L1',['relOp', 'arithExpr']))
rulz.append(Rule({'EPSILON'}, {';', ')', ',', '}', 'id', 'for', 'if', 'get', 'put', 'return', 'float', 'int', '<', '<=', '<>', '==', '>', '>=', ']'}, 'L2', ['EPSILON']))
rulz.append(Rule({'+', '-', 'or'}, {}, 'L2', ['addOp', 'term', 'L2']))
rulz.append(Rule({'EPSILON'}, {';', ')', ',', '}', 'id', 'for', 'if', 'get', 'put', 'return', 'float', 'int', '<', '<=', '<>', '==', '>', '>=', ']', '+', '-', 'or'}, 'L3', ['EPSILON']))
rulz.append(Rule({'*','/', 'and'}, {}, 'L3', ['multOp', 'factor', 'L3']))
rulz.append(Rule({'EPSILON'}, {';', ')', ',', '}', 'id', 'for', 'if', 'get', 'put', 'return', 'float', 'int', '<', '<=', '<>', '==', '>', '>=', ']', '+', '-', 'or', '*', '/', 'and'}, 'L4', ['EPSILON']))
rulz.append(Rule({'('}, {}, 'L4', ['(', 'aParams', ')']))
rulz.append(Rule({'EPSILON'}, {'}'}, 'A1', ['EPSILON']))
rulz.append(Rule({'float', 'id', 'int'}, {}, 'A1', ['A2', 'A1']))
rulz.append(Rule({'float', 'id', 'int'}, {}, 'A2',[Directive.CAPTURE_TOKEN,'type', 'id', 'A3']))
rulz.append(Rule({'[', ';'}, {';'}, 'A3', ['N5',Directive.CREATE_VARIABLE_ENTRY, ';']))
rulz.append(Rule({'('}, {}, 'A3', ['(', 'fParams', ')',Directive.CREATE_FUNCTION_ENTRY_AND_TABLE, 'funcBody',Directive.CLOSE_SCOPE, ';']))
rulz.append(Rule({'EPSILON'}, {'}'}, 'A4', ['EPSILON']))
rulz.append(Rule({'id', 'for', 'if', 'get', 'put', 'return', 'float', 'int'}, {}, 'A4', ['A5', 'A4']))
rulz.append(Rule({'for', 'if', 'get', 'put', 'return', 'float', 'int'}, {}, 'A5', ['A7']))
rulz.append(Rule({'id'}, {}, 'A5',[Directive.CAPTURE_TOKEN,'id', 'A6']))
rulz.append(Rule({'.', '[', '='}, {}, 'A6', [Directive.POP_SEMANTIC_STACK,'N7', 'A9', 'assignOp', 'expr', ';']))
rulz.append(Rule({'id'}, {}, 'A6',['id', 'N5', Directive.CREATE_VARIABLE_ENTRY,';']))
rulz.append(Rule({'id'}, {}, 'A8', ['id', 'N7', 'A9']))
rulz.append(Rule({'EPSILON'}, {'=', ';', ')', ',', '<', '<=', '<>', '==', '>', '>=', ']', '+', '-', 'or', '*', '/', 'and', '('}, 'A9',['EPSILON']))
rulz.append(Rule({'.'}, {}, 'A9', ['.', 'A8']))
rulz.append(Rule({'float', 'int'}, {}, 'A7',[Directive.CAPTURE_TOKEN, 'A10', 'id', 'N5',Directive.CREATE_VARIABLE_ENTRY, ';']))
rulz.append(Rule({'return'}, {}, 'A7', ['return', '(', 'expr', ')', ';']))
rulz.append(Rule({'put'}, {}, 'A7', ['put', '(', 'expr', ')', ';']))
rulz.append(Rule({'get'}, {}, 'A7', ['get', '(', 'variable', ')', ';']))
rulz.append(Rule({'if'}, {}, 'A7', ['if', '(', 'expr', ')', 'then', 'statBlock', 'else', 'statBlock', ';']))
rulz.append(Rule({'for'}, {}, 'A7', ['for', '(', 'type', 'id', 'assignOp', 'expr', ';', 'relExpr', ';', 'assignStat', ')', 'statBlock', ';']))
rulz.append(Rule({'int'}, {}, 'A10', ['int']))
rulz.append(Rule({'float'}, {}, 'A10', ['float']))
rulz.append(Rule({'integer'}, {}, 'num', ['integer']))
rulz.append(Rule({'float_num'}, {}, 'num', ['float_num']))

## Build list of terminals
terminals = [
'class',
'id',
'{','}',
'.',
',',
';',
'program',
'id',
'(',')',
'if','then','else',
'for',
'get',
'put',
'return',
'+','-',
'not',
'[',']',
'integer','int','float', 'float_num',
'=','==','<>','<','>','<=','>=',
'and','or',
'*','/',
'$'
]

## Function that returns a filled parse table
def getParseTable():

	## Build dictionary of dictionaries that represents the parse table
	parse_table = {}
	for rule in rulz:
		parse_table[rule._symbol] = {}

	## Fill the table according to slide 4-18
	for rule in rulz:
		for t in terminals:
			if t in rule._first:
				parse_table[rule._symbol][t] = rule
			if 'EPSILON' in rule._first:
				for t2 in terminals:
					if t2 in rule._follow:
						parse_table[rule._symbol][t2] = rule
	return parse_table

def getRules():
	return rulz

def getTerminals():
	return terminals