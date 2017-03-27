import re
from LexicalAnalyser import Lexer
from ParseTable import Directive, SymbolTable

class Parser:
	symbol_tables = []
	scope_stack = []
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
	def handleSymbolTable(self,directive,table_info):
		## begin adding class symbol to current scope
		if directive.name == 'CREATE_CLASS_ENTRY_AND_TABLE':
			class_id = table_info.split()[1]
			current_class = SymbolTable(class_id)
			self.scope_stack[-1].addSymbol(class_id,'class')
			self.scope_stack.append(current_class)
		
		## begin adding program symbol to current scope,
		## which should be the global scope
		if directive.name == 'CREATE_PROGRAM_TABLE':
			program_table = SymbolTable('Program')
			self.scope_stack[-1].addSymbol('program', 'program')
			self.scope_stack.append(program_table)
		
		## begin adding variable entry to current scope
		if directive.name == 'CREATE_VARIABLE_ENTRY':
			var_type = table_info.split()[0]
			var_id = table_info.split()[1]
			var_array_dimensions = re.findall('\[ ([0-9]) \]',table_info)
			if var_array_dimensions != []:
				var_dimensionality = ''
				for i in var_array_dimensions:
					var_dimensionality = var_dimensionality+'['+i+']'
				var_type = var_type+var_dimensionality
			self.scope_stack[-1].addSymbol(var_id, 'variable',var_type)

		## begin adding function entry to current scope
		if directive.name == 'CREATE_FUNCTION_ENTRY_AND_TABLE':
			func_type = table_info.split()[0]
			func_id = table_info.split()[1]
			func_params = re.findall('\( .* \)',table_info)
			print(table_info)
			print(func_params)

	def printSymbolTables(self):
		print('These are the symbols of each symtable:')
		for i in self.symbol_tables:
			for j in i.symbols: print(j)

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
		self.scope_stack.append(SymbolTable('Global'))
		
		while self._top() != '$':
			x = self._top()
			if x in self._terminals:
				if x == a:
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
				self.handleSymbolTable(x,string_symtable)
				string_symtable = ''
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
		else: print('EVERYTHING IS AWESOME')