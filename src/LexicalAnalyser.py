import re
import argparse
import time
from os.path import isfile

            ################################################
            ########## Begin lexer implementation ##########
            ################################################

c = None

class Lexer:
        s_source_program = ""
        i_index = -1
        i_line_number = 1

        ## Constructor takes the source program as a string
        def __init__(self, s_source_program=""):
                self.s_source_program = s_source_program

        ## Returns next character in the source program string.
        ## If first-time call, returns first character in the
        ## source program string
        def __nextChar(self):
                self.i_index+=1
                if self.i_index >= len(self.s_source_program): return ""
                return self.s_source_program[self.i_index]

        ## Returns previous character in the source program string
        def __backupChar(self):
                self.i_index-=1
                return self.s_source_program[self.i_index]

        ## Returns character immediately ahead of current character
        def __lookAhead(self):
                if self.i_index + 1 == len(self.s_source_program):
                    return " "
                return self.s_source_program[self.i_index+1]

        ## Returns true if string is a reserved word
        def __isReservedWord(self, s_word):
                reserved_words = ["if",
                "then",
                "else",
                "for",
                "class",
                "int",
                "float",
                "get",
                "put",
                "return",
                "program",
                "and", "or", "not",
                ]
                if s_word in reserved_words: return True
                return False

        ## Create error log or open existing error log
        def __logError(self, s_invalid_char):
            if not isfile('error_log.txt'):
                with open('error_log.txt', 'w') as error_log:
                    pass
            localtime = time.asctime( time.localtime(time.time()) )
            with open('error_log.txt','a') as error_log:
                error_log.write(localtime + ": Invalid character '" + s_invalid_char + "' at line " + str(self.i_line_number)+'\n')

        ## Resets source program string and index
        def reset(self, s_source_program):
                self.s_source_program = s_source_program
                self.i_index = -1
        
        def readToken(self):
            c = self.__nextChar()
            letter_match = re.search("[_a-zA-Z]", c)
            if letter_match:
                l_token = [c]
                c = self.__nextChar()
                ## Determine all alphanumeric characters in token
                alphanumeric_match = re.search("[_a-zA-Z0-9]",c)
                while alphanumeric_match:
                    l_token.append(c)
                    c = self.__nextChar()
                    alphanumeric_match = re.search("[_a-zA-Z0-9]",c)
                c = self.__backupChar()
                s_token = "".join(l_token)
                ## Determine if s_token is a reserved word
                if self.__isReservedWord(s_token): return (s_token,s_token,self.i_line_number)
                return ("id",s_token,self.i_line_number)
            ## Determine if c is a number
            number_match = re.search("[1-9]",c)
            if number_match:
                l_token = [c]
                c = self.__nextChar()
                ## Determine if there are any numbers after initial
                ## number
                number_match = re.search("[0-9]",c)
                while number_match:
                    l_token.append(c)
                    c = self.__nextChar()
                    number_match = re.search("[0-9]",c)
                ## Determine if there is a fraction. If not return
                ## token as a digit
                if c == ".":
                    c_ahead = self.__lookAhead()
                    number_match = re.search("[0-9]",c_ahead)
                    if not number_match:
                        c = self.__backupChar()
                        s_token = "".join(l_token)
                        return ("integer",s_token,self.i_line_number)
                    while number_match:
                        l_token.append(c)
                        c = self.__nextChar()
                        number_match = re.search("[0-9]",c)
                    while l_token[-1] == '0':
                        c = self.__backupChar()
                        l_token.pop()
                    if c == '0':
                        l_token.append(c)
                    else: c = self.__backupChar()
                    s_token = "".join(l_token)
                    return ("float_num", s_token,self.i_line_number)
                c = self.__backupChar()
                s_token = "".join(l_token)
                return ("integer", s_token,self.i_line_number)
            ## Determine if c is the number 0 or if it is the beginning
            ## of a float
            if c == '0':
                l_token = [c]
                c = self.__nextChar()
                if c == ".":
                    c_ahead = self.__lookAhead()
                    if re.search("[0-9]",c_ahead):
                        l_token.append(c)
                        c = self.__nextChar()
                        while re.search('[1-9]',c):
                            l_token.append(c)
                            c = self.__nextChar()
                        while l_token[-1] == '0':
                            self.__backupChar()
                            l_token.pop()
                        if c == '0': l_token.append(c)
                        else: self.__backupChar()
                        s_token = "".join(l_token)
                        return("float_num",s_token,self.i_line_number)
                c = self.__backupChar()
                return ("integer",c,self.i_line_number)

            ## If c is a period, determine if it is the
            ##beginning of a fraction or a stand-alone punctuation mark
            if c == ".":
                l_token = [c]
                c = self.__nextChar()
                if re.search("[0-9]",c):
                    l_token.append(c)
                    c = self.__nextChar()
                    while re.search("[0-9]",c):
                        l_token.append(c)
                        c = self.__nextChar()
                    c = self.__backupChar()
                    s_token = "".join(l_token)
                    return ("FRAC", s_token,self.i_line_number)
                c = self.__backupChar()
                return (".", c,self.i_line_number)

            ## Determine if c is any punctuation mark of
            ## the following: ; : ,
            if c == ",": return (",", c,self.i_line_number)
            if c == ";": return (";", c,self.i_line_number)
            if c == ":": return (":", c,self.i_line_number)

            ## Determine if c is one of the following
            ## operators: +, -, *
            if c == "+":
                return ("+", c,self.i_line_number)

            if c == "-":
                return ("-", c,self.i_line_number)

            if c == "*":
                return ("*", c,self.i_line_number)

            # Determine if c is the operator = or if it
            # is a part of the assign operator ==
            if c == "=":
                c = self.__nextChar()
                if c == "=": return ("==", "==",self.i_line_number)
                c = self.__backupChar()
                return ("=", "=",self.i_line_number)

            ## Determine if a character is the operator < or if it
            ## is a part of either the operator <= or <>
            if c == "<":
                c = self.__nextChar()
                if c == "=": return ("<=", "<=",self.i_line_number)
                elif c == ">": return ("<>", "<>",self.i_line_number)
                else:
                    c = self.__backupChar()
                    return ("<",c,self.i_line_number)
            ## Determine if c is the operator > or if it
            ## is a part of the operator >=
            if c == ">":
                c = self.__nextChar()
                if c == "=": return (">=", ">=",self.i_line_number)
                c = self.__backupChar()
                return (">", ">",self.i_line_number)

            ## Determine if c is the division operator / or
            ## if it is a part of a comment marker /* or //
            if c == "/":
                c_ahead = self.__lookAhead()
                if c_ahead == "/":
                    while not c == "\n" and self.i_index < len(self.s_source_program):
                        c = self.__nextChar()
                elif c_ahead == "*":
                    c = self.__nextChar()
                    b_comment_block = True
                    while b_comment_block:
                        c = self.__nextChar()
                        if c == "*":
                            c = self.__nextChar()
                            if c == "/":
                                b_comment_block = False
                        if self.i_index >= len(self.s_source_program):
                            b_comment_block = False
                elif not c_ahead == "/" or not c_ahead == "*":
                    return ("/", "/", self.i_line_number)

            ## Determine if c is a parenthesis, a curly bracket,
            ## or a bracket
            if c == "(": return ("(", c,self.i_line_number)
            if c == "{": return ("{", c,self.i_line_number)
            if c == "[": return ("[", c,self.i_line_number)

            if c == ")": return (")", c,self.i_line_number)
            if c == "}": return ("}", c,self.i_line_number)
            if c == "]": return ("]", c,self.i_line_number)

            ## Determine if c is a line break, whitespace or tab
            if c == '\n': 
                self.i_line_number+= 1
                return 'WHITE_SPACE'
            if c == ' ': return 'WHITE_SPACE'
            if c == '\t': return 'WHITE_SPACE'

            ## Determine if c is the empty string and thus EOF
            if c == '': return '$'

            ## Determine if c is an illegal character
            illegal_match = re.search('.',c)
            if illegal_match:
                self.__logError(c)
                return 'WHITE_SPACE'

        def nextToken(self):
            token = self.readToken()
            while token == 'WHITE_SPACE':
                token = self.readToken()
            return token
            ###############################################
            ########### End Lexer implementation ##########
            ###############################################
                                 ###
                                 ###
                                 ###
                               #######
                                #####
                                 ###
                                  # 
            ###############################################
            #### Begin command line call implementation ###
            ###############################################

## Setup flags and parameters
# parser = argparse.ArgumentParser(prog='Lexer', description='Takes a source string or a file and outputs its tokens')
# parser.add_argument('-f','--file')
# parser.add_argument('-s','--string')
# parser.add_argument('-o','--output')
# args = parser.parse_args()

# if args.output == None:
#     output = False
# else: output = True
# ## Open output file if -o is included
# if output:
#     op = open(args.output, 'w')

# ## If parameter is a string, tokenise from string
# if not args.string == None:
#     s_source = args.string
#     analyser = Lexer(s_source)
#     token = ""
#     while not token == None:
#         token = analyser.nextToken()
#         if not token == None and not token == "":
#             if output:
#                 op.write(str(token)+'\n')
#             else: print(token)

# ## If parameter is a file, tokenise from file
# if not args.file == None:
#     with open(args.file) as file:
#         analyser = Lexer()
#         for line in file:
#             analyser.reset(line)
#             token = ""
#             while not token == None:
#                 token = analyser.nextToken()
#                 if not token == None and not token == "":
#                     if output:
#                         op.write(str(token)+'\n')
#                     else: print(token)
#             analyser.i_line_number+=1
# if output:
#     op.close()