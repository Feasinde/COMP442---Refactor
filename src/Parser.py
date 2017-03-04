from LexicalAnalyser import Lexer

class Parser:
	def __init__(self, rulz, terminals, parse_table, input_string=''):
		self._stack = ['$']
		self._rulz = rulz
		self._terminals = terminals
		self._table = parse_table
		self._input = input_string

	def _push(self, t):
		self._stack.append(t)

	def _pop(self):
		self._stack.pop()

	def _top(self):
		return self._stack[-1]

	def _setInput(self, input_string):
		self._input = input_string

	def _inverse_RHS_multiple_push(self, rule):
		length_of_production = len(rule._production)
		for i in range(length_of_production):
			self._push(rule._production[-i-1])

	def skipErrors(self,error_token,rule):
		lookahead = error_token[0]
		error_line = error_token[2]
		print('Syntax error at line',error_line)
		if lookahead == '$' or lookahead in rule._follow:
			self._pop()
		# while lookahead not in rule._first or ('EPSILON' in rule._first and lookahead not in rule._follow):
		for i in range(20):
			token = self._tokeniser.nextToken()
			print('lookahead =',lookahead,'Symbol = ',rule._symbol,'FIRST = ',rule._first,'FOLLOW =',rule._follow)
			lookahead = token[0]		
	
	def _parse(self,print_stack=False):
		## Initialise tokeniser
		self._tokeniser = Lexer(self._input)

		## set error to False
		error = False

		## push first production rule into stack
		self._push(self._rulz[0]._symbol)
		rule_x = self._rulz[0]

		token = self._tokeniser.nextToken()
		a = token[0]
		while self._top() != '$':
			x = self._top()
			if x in self._terminals:
				if x == a:
					self._pop()
					token = self._tokeniser.nextToken()
					a = token[0]
				else:
					self.skipErrors(token,rule_x)
					error = True
			elif x == 'EPSILON': self._pop() # fuck off eps
			else:
				try:
					rule_x = self._table[x][a]
					self._pop()
					self._inverse_RHS_multiple_push(rule_x)
				except KeyError:
					self.skipErrors(token,rule_x)
					error = True
			if print_stack != False: print(self._stack)
		if a != '$' or error == True:
			print('Something went wrong')
		else: print('EVERYTHING IS AWESOME')