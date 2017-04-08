import re
from LexicalAnalyser import Lexer
from ParseTable import *

class Parser:
	## stores all generated symbol tables
	symbol_tables = []

	## handles all semantic manipulation including 
	## symbol table creation and type chiecking
	semantic_stack = []

	## holds all terminal symbols
	terminals = getTerminals()

	## error flag indicates syntax or semantic errors
	error = False

	def __init__(self, rulz, terminals, parse_table, input_string=''):
		self._stack = ['$']
		self._rulz = rulz
		self._terminals = terminals
		self._table = parse_table
		self._input = input_string
		
		## holds the source code derivation
		self.current_derivation = ['prog']

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

	## Auxiliary methods that returns the First and Follow sets
	def getFirst(self, symbol):
		if symbol in self._terminals: return set([symbol])
		first_ = []
		first = set(first_)
		for i in self._table[symbol]:
			first = first.union(self._table[symbol][i]._first)
		return first

	def getFollow(self, symbol):
		if symbol in self._terminals: return set([])
		first_ = []
		first = set(first_)
		for i in self._table[symbol]:
			first = first.union(self._table[symbol][i]._follow)
		return first

	## Auxiliary methods that check whether a symbol is
	## contained in the current or encompassing scopes and
	## that return the symbol's type
	def lookUp(self,id):
		is_id_declared = False
		for n in range(1,len(self.semantic_stack)+1):
			if type(self.semantic_stack[-n]) == SymbolTable:
				if self.semantic_stack[-n].lookUpSymbol(id): return True
		return is_id_declared

	def getType(self,id):
		for n in range(1,len(self.semantic_stack)+1):
			if type(self.semantic_stack[-n]) == SymbolTable:
				if self.semantic_stack[-n].lookUpSymbol(id): 
					return self.semantic_stack[-n].getTypeOfSymbol(id)
		return None

	## Auxiliar method that checks the type validity
	## of an expression
	def checkType(self,expression):
		expr = expression
		expr_kind = None

		## determine the kind of expression to check: Boolean, arithmetic or invocative
		if ('>' or '<' or '>=' or '<=' or '==' or '!=' or 'or' or 'and' or 'not') in expr:
			expr_kind = 'Boolean'
		elif ('+' or '-' or '*' or '/') in expr:
			expr_kind = 'arithmetic'
		else: expr_kind = 'invocative'

		## get the type of all ids by referring to the symtable
		for token in expr:
			token_types = []
			token_type = None
			# if token == 'id': 
			# 	print('HOAL')
			# 	print(self.lookUp(token))
				

	def update_derivation(self,rule):
		symbol_to_derivate = ''
		terminals_head = []

		## remove semantic directives from rule, which
		## are unneeded
		production_no_sem = []
		for token in rule._production:
			if type(token) != Directive:
				production_no_sem.append(token)

		token_index = 0
		while self.current_derivation[token_index] in self.terminals:
			terminals_head.append(self.current_derivation[token_index])
			token_index+= 1
		symbol_to_derivate = self.current_derivation[token_index]
		production_tail = self.current_derivation[token_index+1:]
		self.current_derivation = terminals_head + production_no_sem + production_tail

	## Create and handle symbol tables. Returns truth value
	## that determines whether parsed tokens are added to
	## the semstack
	def handleSymbolTable(self,directive):

		## create global table at the beginning of 
		## the program and add it as the bottom element
		## of the semstack
		if directive.name == 'CREATE_GLOBAL_TABLE':
			self.semantic_stack.append(SymbolTable('Global'))
			return False

		## create class and add as a symbol to the current
		## scope
		if directive.name == 'CREATE_CLASS_ENTRY_AND_TABLE':

			## pop class id from the semstack
			class_name = self.semantic_stack.pop()
			new_class = SymbolTable(class_name)
			self.semantic_stack[-1].addSymbol(class_name,'class',_link=new_class)
			self.semantic_stack.append(new_class)
			return False

		## create program table and add to the current scope
		## current scope must be the global scope
		if directive.name == 'CREATE_PROGRAM_TABLE':
			self.semantic_stack[-1].addSymbol('program','Main program')
			self.semantic_stack.append(SymbolTable('Program'))
			return False

		## set capture_token flag to True so that parsed
		## tokens are added to the semstack
		if directive.name == 'CAPTURE_TOKEN':
			return True

		if directive.name == 'CREATE_VARIABLE_ENTRY':
			var_dim = []
			## gather dimensionalities if the variable
			## is an array
			while self.semantic_stack[-1] == ']':
				self.semantic_stack.pop()
				var_dim.append(self.semantic_stack.pop())
				self.semantic_stack.pop()

			## pop from the semstack the id and type
			## of the variable
			var_id = self.semantic_stack.pop()
			var_type = self.semantic_stack.pop()

			## format each dimensionality value by adding
			## '[' and ']' around it
			for i in range(len(var_dim)):
				var_dim[i] = '['+var_dim[i]+']'

			## dimenionalities are popped in reverse order
			## so we have to reverse once again
			var_dim = ''.join(list(reversed(var_dim)))

			## add variable symbol to current scope
			self.semantic_stack[-1].addSymbol(var_id,'variable',var_type+var_dim)
			return False

		if directive.name == 'CREATE_FUNCTION_ENTRY_AND_TABLE':
			func_params = []

			## gather all parameters, if any, from the function
			## parameters lists
			while self.semantic_stack[-1] != '(':
				self.semantic_stack.pop()
				if self.semantic_stack[-1] != '(':
					param_dim = []

					## similar to what is done with arrays, we gather
					## the dimensionalities of all parameters
					while self.semantic_stack[-1] == ']':
						self.semantic_stack.pop()
						param_dim.append(self.semantic_stack.pop())
						self.semantic_stack.pop()

					## pop from the semstack the id and type
					## of each parameter
					param_id = self.semantic_stack.pop()
					param_type = self.semantic_stack.pop()

					## format the parameters by adding '[' and ']'
					## around them
					for i in range(len(param_dim)):
						param_dim[i] = '['+param_dim[i]+']'

					## dimensionalities are popped from the semstack in reverse
					## order so we have to reverse them once again
					param_dim = ''.join(list(reversed(param_dim)))

					## not all parameters include dimensionalities
					if param_dim != '':
						func_params.append((param_type,param_id,param_dim))
					else:
						func_params.append((param_type,param_id))
			
			## pop '(' from semstack...
			self.semantic_stack.pop()

			## ...and pop the function id and type.
			func_id = self.semantic_stack.pop()
			func_type = self.semantic_stack.pop()

			## parameters are popped in reverse order and have
			## to be reversed once again
			func_params = list(reversed(func_params))

			## create the function's symtable
			new_func = SymbolTable(func_id)
			if func_params != []:
				formatted_func_params = []
				for parameter in func_params:
					if len(parameter) == 3:
						formatted_func_params.append(parameter[0]+parameter[2])
					else:
						formatted_func_params.append(parameter[0])
				self.semantic_stack[-1].addSymbol(func_id,'Function',func_type+' : '+', '.join(formatted_func_params),new_func)
			else: 
				self.semantic_stack[-1].addSymbol(func_id,'Function',func_type,_link=new_func)

			## add the function to the semstack
			self.semantic_stack.append(new_func)

			## add the function parameters as symbols on the
			## function symtable
			if func_params != []:
				for i in func_params:
					if len(i) == 3:
						self.semantic_stack[-1].addSymbol(i[1],'Parameter',i[0]+i[2])
					else: self.semantic_stack[-1].addSymbol(i[1],'Parameter',i[0])
			return False

		if directive.name == 'CHECK_DEFINITION':
			id = ''
			scope = ''
			scoped = False
			while scope == '':
				n = len(self.semantic_stack)
				for i in range(1,n):
					if type(self.semantic_stack[-i]) == SymbolTable:
						scope = self.semantic_stack[-i].name
					n -= 1
			
			while self.semantic_stack[-1] != Directive.CAPTURE_TYPE:
				id = self.semantic_stack.pop()
			self.semantic_stack.pop()
			if self.semantic_stack[-1] == '.':
				self.semantic_stack.pop()
				scope_id = self.semantic_stack[-1]
				print(scope_id)
				scoped = self.lookUp(scope_id)

			if not self.lookUp(id) and scoped == False:
				self.error = True
				print("Undefined identifier '"+id+"' in scope '"+scope+"'")
			return False

		if directive.name == 'CHECK_EXPRESSION_TYPE':
			exp_types = []
			## pop the semstack gathering tokens until reaching
			## the point where the type checking began
			while self.semantic_stack[-1] != Directive.CAPTURE_TYPE:
				exp_types.append(self.semantic_stack.pop())
			self.semantic_stack.pop()
			self.checkType(exp_types)
			exp_types = list(reversed(exp_types))
			# print(' '.join(exp_types))
			return False

		if directive.name == 'CHECK_ASSIGNMENT_TYPE':
			assign_statement = []
			while self.semantic_stack[-1] != Directive.CAPTURE_TYPE:
				assign_statement.append(self.semantic_stack.pop())
				print(' '.join(list(reversed(assign_statement))))
			self.semantic_stack.pop()
			return False

		if directive.name == 'POP_SEMANTIC_STACK':
			self.semantic_stack.pop()

		if directive.name == 'CLOSE_SCOPE':
			# self.semantic_stack[-1].printTable()
			# print(self.lookUp('var1'))
			# print(self.getType('var1'))
			self.symbol_tables.append(self.semantic_stack.pop())
		return False

	def printSymbolTables(self,output_file):
		for i in range(len(self.symbol_tables)):
			self.symbol_tables[-1-i].printTable(output_file=output_file)

	def _parse(self,print_stack=False,print_derivation=False,print_symtables=False,op_file=None):
		## Initialise tokeniser
		self._tokeniser = Lexer(self._input)

		## push first production rule into stack
		self._push(self._rulz[0]._symbol)
		rule_x = self._rulz[0]
		token = self._tokeniser.nextToken()
		a = token[0]
		line_errors = []

		capture_token = False
		capture_token_type = False
		
		while self._top() != '$':
			x = self._top()
			if x in self._terminals:
				if x == a:
					if capture_token: 
						self.semantic_stack.append(token[1])
					if capture_token_type:
						self.semantic_stack.append(token[1])
					self._pop()
					token = self._tokeniser.nextToken()
					a = token[0]
				else:
					print(x,a)
					line_errors.append(token[2])
					
					## Begin skip error section
					if a == '$' or a in self.getFollow(self._top()):
						self._pop()
					else:
						while a not in self.getFirst(self._top()) or a in self.getFollow(self._top()):
							token = self._tokeniser.nextToken()
							a = token[0]
					## End skip error section
					self.error = True
			elif x == 'EPSILON': self._pop() # fuck off eps
			elif type(x) == Directive:
				if x.name == 'CAPTURE_TYPE':
					capture_token_type = True
					self.semantic_stack.append(x)
					# print('At the moment of pushing the directive, the top of the semstack is',self.semantic_stack[-1])
				if x.name == 'CHECK_DEFINITION':
					capture_token_type = False
				capture_token = self.handleSymbolTable(x)
				self._pop()

			else:
				try:
					rule_x = self._table[x][a]
					self._pop()
					self._inverse_RHS_multiple_push(rule_x)
					self.update_derivation(rule_x)
					if print_derivation:
						if op_file != None:
							op_file.write(''.join(self.current_derivation)+'\n')
						else:
							print(''.join(self.current_derivation))
				except KeyError:
					line_errors.append(token[2])
				
					## Begin skip error section
					if a == '$' or a in self.getFollow(self._top()):
						self._pop()
					else:
						while (a not in self.getFirst(self._top()) or a in self.getFollow(self._top())) and a != '$':
							token = self._tokeniser.nextToken()
							a = token[0]
					## End skip error section
					
					self.error = True
			if print_stack != False: 
				if op_file != None:
					op_file.write(str(self._stack)+'\n')
				else:
					print(self._stack)
		if a != '$' or self.error == True:
			print('Something went wrong.')
			if line_errors != []:
				print('Syntax error on lines',str(line_errors))
		else: 
			if print_symtables:
				self.printSymbolTables(output_file=op_file)
			print('EVERYTHING IS AWESOME')
