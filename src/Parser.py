import re
from LexicalAnalyser import Lexer
from ParseTable import Directive, SymbolTable

class Parser:
	symbol_tables = []
	semantic_stack = []
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
	
	## Create and handle symbol tables
	def handleSymbolTable(self,directive):
		if directive.name == 'CREATE_GLOBAL_TABLE':
			self.semantic_stack.append(SymbolTable('Global'))
			return False
		if directive.name == 'CREATE_CLASS_ENTRY_AND_TABLE':
			class_name = self.semantic_stack.pop()
			new_class = SymbolTable(class_name)
			self.semantic_stack[-1].addSymbol(class_name,'class',_link=new_class)
			self.semantic_stack.append(new_class)
			return False
		if directive.name == 'CREATE_PROGRAM_TABLE':
			self.semantic_stack[-1].addSymbol('program','Main program')
			self.semantic_stack.append(SymbolTable('Program'))
			return False
		if directive.name == 'CAPTURE_TOKEN':
			return True
		if directive.name == 'CREATE_VARIABLE_ENTRY':
			var_dim = []
			while self.semantic_stack[-1] == ']':
				self.semantic_stack.pop()
				var_dim.append(self.semantic_stack.pop())
				self.semantic_stack.pop()
			var_id = self.semantic_stack.pop()
			var_type = self.semantic_stack.pop()
			for i in range(len(var_dim)):
				var_dim[i] = '['+var_dim[i]+']'
			var_dim = ''.join(list(reversed(var_dim)))
			self.semantic_stack[-1].addSymbol(var_id,'variable',var_type+var_dim)
			return False
		if directive.name == 'CREATE_FUNCTION_ENTRY_AND_TABLE':
			func_params = []
			while self.semantic_stack[-1] != '(':
				self.semantic_stack.pop()
				if self.semantic_stack[-1] != '(':
					param_dim = []
					while self.semantic_stack[-1] == ']':
						self.semantic_stack.pop()
						param_dim.append(self.semantic_stack.pop())
						self.semantic_stack.pop()
					param_id = self.semantic_stack.pop()
					param_type = self.semantic_stack.pop()
					for i in range(len(param_dim)):
						param_dim[i] = '['+param_dim[i]+']'
					param_dim = ''.join(list(reversed(param_dim)))
					if param_dim != '':
						func_params.append((param_type,param_id,param_dim))
					else:
						func_params.append((param_type,param_id))
			self.semantic_stack.pop()
			func_id = self.semantic_stack.pop()
			func_type = self.semantic_stack.pop()
			func_params = list(reversed(func_params))
			new_func = SymbolTable(func_id)
			if func_params != []:
				self.semantic_stack[-1].addSymbol(func_id,'Function',func_type+':'+str(func_params),new_func)
			else: self.semantic_stack[-1].addSymbol(func_id,'Function',func_type,_link=new_func)
			self.semantic_stack.append(new_func)
			if func_params != []:
				for i in func_params:
					if len(i) == 3:
						self.semantic_stack[-1].addSymbol(i[1],'Parameter',i[0]+i[2])
					else: self.semantic_stack[-1].addSymbol(i[1],'Parameter',i[0])
			return False
		if directive.name == 'POP_SEMANTIC_STACK':
			self.semantic_stack.pop()

		if directive.name == 'CLOSE_SCOPE':
			self.symbol_tables.append(self.semantic_stack.pop())
		return False
		## begin adding class symbol to current scope

	def printSymbolTables(self):
		for i in range(len(self.symbol_tables)):
			self.symbol_tables[-1-i].printTable()

	def _parse(self,print_stack=False):
		## Initialise tokeniser
		self._tokeniser = Lexer(self._input)

		## set error flag to False
		error = False

		## push first production rule into stack
		self._push(self._rulz[0]._symbol)
		rule_x = self._rulz[0]
		token = self._tokeniser.nextToken()
		a = token[0]
		line_errors = []

		## string that stores each parsed token from which
		## type name and array indices are extracted to create
		## symtables
		string_symtable = token[1]

		## create global symbol table and add to scope
		## stack and symbol table list
		capture_token = False
		
		while self._top() != '$':
			x = self._top()
			if x in self._terminals:
				if x == a:
					if capture_token: 
						self.semantic_stack.append(token[1])
					self._pop()
					token = self._tokeniser.nextToken()
					a = token[0]

					## add parsed token to string_symtable
					string_symtable = string_symtable + ' '+token[1]
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
					
					error = True
			elif x == 'EPSILON': self._pop() # fuck off eps
			elif type(x) == Directive:
				capture_token = self.handleSymbolTable(x)
				self._pop()

			else:
				try:
					rule_x = self._table[x][a]
					self._pop()
					self._inverse_RHS_multiple_push(rule_x)
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
					
					error = True
			if print_stack != False: print(self._stack)
		if a != '$' or error == True:
			print('Something went wrong.')
			print('Syntax error on lines',str(line_errors))
		else: 
			self.printSymbolTables()
			print('EVERYTHING IS AWESOME')
