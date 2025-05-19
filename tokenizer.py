class Tokenizer:
    def __init__(self):
        self.errors = []
        self.whitespace = {' ', '\t', '\n'}

        self.alphabet = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.number = set("0123456789")
        self.digit = set("123456789")
        self.alphadig = self.alphabet | self.number

        self.asciicmnt = {chr(i) for i in range(32, 127) if chr(i) not in {'/', '*'}}
        self.ascii = {chr(i) for i in range(32, 127) if chr(i)}
        self.asciistr = {chr(i) for i in range(32, 127) if chr(i) != '"'}
        self.asciichr = {chr(i) for i in range(32, 127) if chr(i) not in {'\\', "'"}}
        self.strdelim = {',', ';', ' ', ':', ')', '}', '+'}
        self.letterdelim = {' ', ';', ',', ':', '}', ')'}
        
        self.dtdelim = {' ', '\t'}
        self.opdelim = {'+', '-', '*', '/', '%', '**', '&', '|', '!', '<', '>', '='}
        self.iddelim = {' ', ';', ',', '.', '(', ')', '{', '[', ']', ':'} | self.opdelim
        self.digdelim = {' ', ';', ':', ',', '}', ')', ']'} | self.opdelim
        self.pardelim = {'('}
        self.conddelim = {'(', ' '}

        self.delim1 = {'{'} | self.whitespace
        self.delim2 = {' ', '{'}
        self.delim3 = {' ', ')', ';', ','}
        self.delim4 = {';', ')'} | self.alphadig
        self.delim5 = {' ', '~', '('} | self.alphadig
        self.delim6 = {' ', '\n'}
        self.delim7 = {' ', '"', '('} | self.alphadig
        self.delim6 = {' ', '\n'}
        self.delim9 = {'('} | self.alphabet
        self.delim10 = {' ', '~', '"', '\'', '('} | self.alphadig
        self.delim11 = {'"', '~', '\'', ' ', '{', '('} | self.alphadig
        self.delim12 = {'(',')', '!', '\'', '"', ' '} | self.alphadig
        self.delim13 = {';', '{', ')', ']', '<', '>', '=', '|', '&', '+', '-', '/', '*', '%', ' ', ':', ',', '\n'}
        self.delim14 = {']', ' ', '('} | self.alphadig
        self.delim15 = {'=', ';', ' ', '\n', '[', ')'}
        self.delim16 = {'\'', '"', '~', ' ', '\n', '{', '}'} | self.alphadig
        self.delim17 = {';', '}', ',', ' ', '\n'} | self.alphabet

    def next_char(self):
        if self.index < len(self.code):
            char = self.code[self.index]
            self.index += 1
            return char
        return None

    def peek_char(self):
        if self.index < len(self.code):
            return self.code[self.index]
        return None
    
    def step_back(self):
        if self.index > 0:
            self.index -= 1

    def tokenize(self, code):
        self.code = code
        tokens = []
        self.index = 0
        state = 0
        lexeme = ""
        line = 1
        column = 0

        while True:
            char = self.next_char()
            column += 1

            if char is None and state == 0:
                break

            print(f"State: {state}, char: {repr(char)}, Lexeme: {repr(lexeme)}, Line: {line}, Column {column}")

            match state:
                case 0:
                    #column -= 2
                    lexeme = ""
                    #whitespaces
                    if char in self.whitespace:
                        if char == '\n':
                            line += 1
                            column = 0
                        continue

                    #keywords
                    elif char == 'b': #b
                        state = 1
                        lexeme += char
                    elif char == 'd': #d
                        state = 6
                        lexeme += 'd'
                    elif char == 'e': #e
                        state = 27
                        lexeme += 'e'
                    elif char == 'f': #f
                        state = 40
                        lexeme += 'f'
                    elif char == 'i': #i - int
                        state = 54
                        lexeme += 'i' 
                    elif char == 'l': #l - letter
                        state = 66
                        lexeme += 'l'
                    elif char == 'm': #m - main
                        state = 73
                        lexeme += "m"
                    elif char == 'o': #o - option
                        state = 78
                        lexeme += 'o'
                    elif char == 'r': #r - read
                        state = 85
                        lexeme += 'r'
                    elif char == 's': #s - scope
                        state = 96
                        lexeme += 's'
                    elif char == 't': #t - task
                        state = 113
                        lexeme += 't'
                    elif char == 'u': #u - unit
                        state = 124
                        lexeme += 'u'
                    elif char == 'w': #w - while
                        state = 129
                        lexeme += 'w'
                    
                    #symbols
                    elif char == '+':
                        state = 135
                        lexeme += char

                    elif char == '-':
                        state = 141
                        lexeme += char

                    elif char == '*':
                        state = 147
                        lexeme += char

                    elif char == '/':
                        state = 155
                        lexeme += char
                    
                    elif char == '%':
                        state = 159
                        lexeme += char

                    elif char == '>':
                        state = 163
                        lexeme += char

                    elif char == '<':
                        state = 167
                        lexeme += char

                    elif char == '!':
                        state = 171
                        lexeme += char

                    elif char == '&':
                        state = 175
                        lexeme += char

                    elif char == '|':
                        state = 178
                        lexeme += char

                    elif char == ',':
                        state = 181
                        lexeme += char
                    
                    elif char == ':':
                        state = 183
                        lexeme += char
                    
                    elif char == ';':
                        state = 185
                        lexeme += char

                    elif char == '(':
                        state = 187
                        lexeme += char
                    
                    elif char == ')':
                        state = 189
                        lexeme += char
                    
                    elif char == '[':
                        state = 191
                        lexeme += char
                    
                    elif char == ']':
                        state = 193
                        lexeme += char
                    
                    elif char == '{':
                        state = 195
                        lexeme += char
                    
                    elif char == '}':
                        state = 197
                        lexeme += char
            
                    elif char == '=':
                        state = 199
                        lexeme += char

                    elif char == '.':
                        state = 203
                        lexeme += char
                    
                    #num literals
                    elif char == '0':
                        state = 205
                        lexeme += char
                    elif char.isdigit() and char != '0':
                        state = 208
                        lexeme += char
                    elif char == '~':
                        state = 207
                        lexeme += char

                     #string and letter
                    elif char == "'":
                        state = 245
                        lexeme += "'"
                    elif char == '"':
                        state = 249
                        lexeme += '"'

                    #identifier
                    elif char.isalpha():
                        state = 252
                        lexeme += char

                    #error handling
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): Invalid Character ( {repr(char)} ).")

                #KEYWORDS
                case 1: 
                    if char == 'o':
                        state = 2
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
    
                case 2:
                    if char == 'o':
                        state = 3
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()                            
                            state = 0 
                
                case 3:
                    if char == 'l':
                        state = 4
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()                            
                            state = 0 
                
                case 4: #Delim
                    if char in self.dtdelim:
                        state = 5
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:  
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0
                
                case 5: #Tokenize
                    column -= 2
                    tokens.append((lexeme, "bool", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 6:
                    if char == 'e':
                        state = 7
                        lexeme += 'e'
                    elif char == 'i':
                        state = 20
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0  
                
                case 7:
                    if char == 'c':
                        state = 8
                        lexeme += 'c'
                    elif char == 'f':
                        state = 14
                        lexeme += 'f'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0      
                
                case 8: 
                    if char == 'i':
                        state = 9
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0      
                
                case 9: 
                    if char == 'm':
                        state = 10
                        lexeme += 'm'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0      
                
                case 10: 
                    if char == 'a':
                        state = 11
                        lexeme += 'a'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0      
                
                case 11: 
                    if char == 'l':
                        state = 12
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0      
                
                case 12: #Delim
                    if char in self.dtdelim:
                        state = 13
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0
         
                
                case 13: #Tokenize
                    column -= 2
                    tokens.append((lexeme, "decimal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 14:
                    if char == 'a':
                        state = 15
                        lexeme += 'a'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0     
                        
                case 15: 
                    if char == 'u':
                        state = 16
                        lexeme += 'u'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                            
                        
                case 16: 
                    if char == 'l':
                        state = 17
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
    
                case 17: 
                    if char == 't':
                        state = 18
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                            
                        
                case 18:
                    if char == ':':
                        state = 19
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0
                          
           
                case 19:
                    column -= 2
                    tokens.append((lexeme, "default", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 20:
                    if char == 's':
                        state = 21
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        

                case 21:
                    if char == 'p':
                        state = 22
                        lexeme += 'p'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                                
                
                case 22:
                    if char == 'l':
                        state = 23
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                                    
                
                case 23:
                    if char == 'a':
                        state = 24
                        lexeme += 'a'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                                    
                
                case 24:
                    if char == 'y':
                        state = 25
                        lexeme += 'y'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                                    
                
                case 25:
                    if char in self.pardelim:
                        state = 26
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                            
                
                case 26:
                    column -= 2
                    tokens.append((lexeme, "display", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 27:
                    if char == 'l':
                        state = 28
                        lexeme += 'l'
                    
                    elif char == 'm':
                        state = 35
                        lexeme += 'm'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                             

                case 28:
                    if char == 's':
                        state = 29
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                             

                case 29:
                    if char == 'e':
                        state = 30
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                                   

                case 30:
                    if char == 'i':
                        state = 32
                        lexeme += 'i'
                    elif char in self.delim1:
                        state = 31
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                        
                case 31:
                    column -= 2
                    tokens.append((lexeme, "else", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 32: 
                    if char == 'f':
                        state = 33
                        lexeme += 'f'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                        
                case 33:
                    if char in self.conddelim:
                        state = 34
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
           
                case 34:
                    column -= 2
                    tokens.append((lexeme, "elseif", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 35:
                    if char == 'p':
                        state = 36
                        lexeme += 'p'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                            
                case 36:
                    if char == 't':
                        state = 37
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                            
                case 37:
                    if char == 'y':
                        state = 38
                        lexeme += 'y'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                            
                case 38:
                    if char == ' ':
                        state = 39
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
           
                case 39:
                    column -= 2
                    tokens.append((lexeme, "empty", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 40:
                    if char == 'a':
                        state = 41
                        lexeme += 'a'
                    elif char == 'i':
                        state = 46
                        lexeme += 'i'
                    elif char == 'o':
                        state = 51
                        lexeme += 'o'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                                
                case 41:
                    if char == 'l':
                        state = 42
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                                
                case 42:
                    if char == 's':
                        state = 43
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                                
                case 43:
                    if char == 'e':
                        state = 44
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                                
                case 44:
                    if char in self.delim3:
                        state = 45
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
           
                case 45:
                    column -= 2
                    tokens.append((lexeme, "false", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 46:
                    if char == 'x':
                        state = 47
                        lexeme += 'x'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                                
                case 47:
                    if char == 'e':
                        state = 48
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                                
                case 48:
                    if char == 'd':
                        state = 49
                        lexeme += 'd'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                                
                case 49:
                    if char == ' ':
                        state = 50
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
           
                case 50:
                    column -= 2
                    tokens.append((lexeme, "fixed", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 51:
                    if char == 'r':
                        state = 52
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                        
                case 52:
                    if char in self.conddelim:
                        state = 53
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
           
                case 53:
                    column -= 2
                    tokens.append((lexeme, "for", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
           
                case 54:
                    if char == 'f':
                        state = 55
                        lexeme += 'f'
                    elif char == 'n':
                        state = 57 
                        lexeme += 'n'
                    elif char == 's':
                        state = 60
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 55:
                    if char in self.conddelim:
                        state = 56
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                case 56:
                    column -= 2
                    tokens.append((lexeme, "if", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 57:
                    if char == 't':
                        state = 58
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 58:
                    if char in self.dtdelim:
                        state = 59 
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                case 59:
                    column -= 2
                    tokens.append((lexeme, "int", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 60:
                    if char == 'n': 
                        state = 62
                        lexeme += 'n'
                    elif char == ' ':
                        state = 61
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                case 61:
                    column -= 2
                    tokens.append((lexeme, "is", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                        
                case 62:
                    if char == 'o': 
                        state = 63
                        lexeme += 'o'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 63:
                    if char == 't': 
                        state = 64
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 64:
                    if char == ' ':
                        state = 65
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0
                        
                case 65:
                    column -= 2
                    tokens.append((lexeme, "isnot", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                        
                case 66:
                    if char == 'e':
                        state = 67
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 67:
                    if char == 't':
                        state = 68
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 68:
                    if char == 't':
                        state = 69
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 69:
                    if char == 'e':
                        state = 70
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 70:
                    if char == 'r':
                        state = 71
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 71:
                    if char in self.dtdelim:
                        state = 72
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0

                case 72:
                    column -= 2
                    tokens.append((lexeme, "letter", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                        
                case 73:
                    if char == 'a':
                        state = 74
                        lexeme += 'a'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 74:
                    if char == 'i':
                        state = 75
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 75:
                    if char == 'n':
                        state = 76
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 76:
                    if char in self.pardelim:
                        state = 77
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0 
                        
                case 77:
                    column -= 2
                    tokens.append((lexeme, "main", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                        
                case 78:
                    if char == 'p':
                        state = 79
                        lexeme += 'p'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0

                case 79:
                    if char == 't':
                        state = 80
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 80:
                    if char == 'i':
                        state = 81
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                        
                case 81:
                    if char == 'o':
                        state = 82
                        lexeme += 'o'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 82:
                    if char == 'n':
                        state = 83
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 83:
                    if char == ' ':
                        state = 84
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0
                        
                case 84:
                    column -= 2
                    tokens.append((lexeme, "option", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 85:
                    if char == 'e':
                        state = 86
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                    
                case 86:
                    if char == 'a':
                        state = 87
                        lexeme += 'a'
                    elif char == 't':
                        state = 91
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 87:
                    if char == 'd':
                        state = 88
                        lexeme += 'd'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 88:
                    if char == 's':
                        state = 89
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 89:
                    if char in self.pardelim:
                        state = 90
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0

                case 90:
                    column -= 2
                    tokens.append((lexeme, "reads", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 91:
                    if char == 'u':
                        state = 92
                        lexeme += 'u'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 92:
                    if char == 'r':
                        state = 93
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 93:
                    if char == 'n':
                        state = 94
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 94:
                    if char == ' ':
                        state = 95
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0
                        
                case 95:
                    column -= 2
                    tokens.append((lexeme, "return", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 96:
                    if char == 'e':
                        state = 97
                        lexeme += 'e'
                    elif char == 'k':
                        state = 103
                        lexeme += 'k'
                    elif char == 't':
                        state = 107
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 97:
                    if char == 'l':
                        state = 98
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 98:
                    if char == 'e':
                        state = 99
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 99:
                    if char == 'c':
                        state = 100
                        lexeme += 'c'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 100:
                    if char == 't':
                        state = 101
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 101:
                    if char in self.conddelim:
                        state = 102
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                        state = 0

                case 102:
                    column -= 2
                    tokens.append((lexeme, "select", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                        
                case 103:
                    if char == 'i':
                        state = 104
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 104:
                    if char == 'p':
                        state = 105
                        lexeme += 'p'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 105:
                    if char == ';':
                        state = 106
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                    self.step_back()
                        state = 0

                case 106:
                    column -= 2
                    tokens.append((lexeme, "skip", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 107:
                    if char == 'r':
                        state = 108
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 108:
                    if char == 'i':
                        state = 109
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 109:
                    if char == 'n':
                        state = 110
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 110:
                    if char == 'g':
                        state = 111
                        lexeme += 'g'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 111:
                    if char in self.dtdelim:
                        state = 112
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back() 
                        state = 0
                        
                case 112:
                    column -= 2
                    tokens.append((lexeme, "string", line, column))
                    if char is not None:
                        self.step_back() 
                    state =  0

                case 113:
                    if char == 'a':
                        state = 114
                        lexeme += 'a'
                    elif char == 'r':
                        state = 118
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 114:
                    if char == 's':
                        state = 115
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 115:
                    if char == 'k':
                        state = 116
                        lexeme += 'k'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                           
                case 116:
                    if char == ' ':
                        state = 117
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0
                        
                case 117:
                    column -= 2
                    tokens.append((lexeme, "task", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 118:
                    if char == 'u':
                        state = 119
                        lexeme += 'u'
                    elif char == 'y':
                        state = 122
                        lexeme += 'y'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 119:
                    if char == 'e':
                        state = 120
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 120:
                    if char in self.delim3:
                        state = 121
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                case 121:
                    column -= 2
                    tokens.append((lexeme, "true", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 122:
                    if char in self.delim2:
                        state = 123
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                case 123:
                    column -= 2
                    tokens.append((lexeme, "try", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 124:
                    if char == 'n':
                        state = 125
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                    
                case 125:
                    if char == 'i':
                        state = 126
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 126:
                    if char == 't':
                        state = 127
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 127:
                    if char == ' ':
                        state = 128
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                case 128:
                    column -= 2
                    tokens.append((lexeme,"unit", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 129:
                    if char == 'h':
                        state = 130
                        lexeme += 'h'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 130:
                    if char == 'i':
                        state = 131
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 131:
                    if char == 'l':
                        state = 132
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 132:
                    if char == 'e':
                        state = 133
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 255
                            if char is not None:
                                self.step_back()
                        else:
                            column -= 1
                            if char is None:

                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                            else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                                if char == '\n':
                                    column = 0
                                if char is not None:
                                    self.step_back()
                            state = 0 
                        
                case 133:
                    if char in self.conddelim:
                        state = 134
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 254
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:

                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                        
                case 134:
                    column -= 2
                    tokens.append((lexeme, "while", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                # Symbols
                case 135:
                    if char in self.delim7:
                        state = 136
                        if char is not None:
                            self.step_back()
                    elif char == '+':
                        state = 137
                        lexeme += char
                    elif char == '=':                        
                        state = 139
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 136:
                    column -= 2
                    tokens.append((lexeme, "+", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 137:
                    if char in self.delim4:
                        state = 138
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 138:
                    column -= 2
                    tokens.append((lexeme, "++", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
    
                case 139:
                    if char in self.delim5:
                        state = 140
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 140:
                    column -= 2
                    tokens.append((lexeme, "+=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 141:
                    if char in self.delim5:
                        state = 142
                        if char is not None:
                            self.step_back()
                    elif char == '-':
                        state = 143
                        lexeme += char
                    elif char == '=':                        
                        state = 145
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 142:
                    column -= 2
                    tokens.append((lexeme, "-", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 143:
                    if char in self.delim4:
                        state = 144
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 144:
                    column -= 2
                    tokens.append((lexeme, "--", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 145:
                    if char in self.delim5:
                        state = 146
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 146:
                    column -= 2
                    tokens.append((lexeme, "-=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 147:
                    if char in self.delim5:
                        state = 148
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 149
                        lexeme += char
                    elif char == '*':                        
                        state = 151
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 148:
                    column -= 2
                    tokens.append((lexeme, "*", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 149:
                    if char in self.delim5:
                        state = 150
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                    self.step_back()
                        state = 0
                
                case 150:
                    column -= 2
                    tokens.append((lexeme, "*=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 151:
                    if char in self.delim5:
                        state = 152
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 153
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 152:
                    column -= 2
                    tokens.append((lexeme, "**", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 153:
                    if char in self.delim5:
                        state = 154
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 154:
                    column -= 2
                    tokens.append((lexeme, "**=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 155:
                    if char in self.delim5:
                        state = 156
                        if char is not None:
                            self.step_back()
                    elif char == '/':
                        state = 256
                    elif char == '*':
                        state = 258
                    elif char == '=':
                        state = 157
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 156:
                    column -= 2
                    tokens.append((lexeme, "/", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 157:
                    if char in self.delim5:
                        state = 158
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 158:
                    column -= 2
                    tokens.append((lexeme, "/=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 159:
                    if char in self.delim5:
                        state = 160
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 161
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 160:
                    column -= 2
                    tokens.append((lexeme, "%", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 161:
                    if char in self.delim5:
                        state = 162
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 162:
                    column -= 2
                    tokens.append((lexeme, "%=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 163:
                    if char in self.delim5:
                        state = 164
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 165
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 164:
                    column -= 2
                    tokens.append((lexeme, ">", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 165:
                    if char in self.delim5:
                        state = 166
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 166:
                    column -= 2
                    tokens.append((lexeme, ">=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 167:
                    if char in self.delim5:
                        state = 168
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 169
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 168:
                    column -= 2
                    tokens.append((lexeme, "<", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 169:
                    if char in self.delim5:
                        state = 170
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '&lt;=' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 170:
                    column -= 2
                    tokens.append((lexeme, "<=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 171:
                    if char in self.delim9:
                        state = 172
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 173
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 172:
                    column -= 2
                    tokens.append((lexeme, "!", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 173:
                    if char in self.delim10:
                        state = 174
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 174:
                    column -= 2
                    tokens.append((lexeme, "!=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 175:
                    if char == '&':
                        state = 176
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 176:
                    if char in self.delim5:
                        state = 177
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 177:
                    column -= 2
                    tokens.append((lexeme, "&&", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 178:
                    if char == '|':
                        state = 179
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 179:
                    if char in self.delim5:
                        state = 180
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 180:
                    column -= 2
                    tokens.append((lexeme, "||", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 181:
                    if char in self.delim11:
                        state = 182
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 182:
                    column -= 2
                    tokens.append((lexeme, ",", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0

                case 183:
                    if char in self.delim6:
                        state = 184
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 184:
                    column -= 2
                    tokens.append((lexeme, ":", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0

                case 185:
                    if char is None or char in self.delim6:
                        state = 186
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 186:
                    column -= 2
                    tokens.append((lexeme, ";", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0
                    
                case 187:
                    if char in self.delim12:
                        state = 188
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 188:
                    column -= 2
                    tokens.append((lexeme, "(", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0
                    
                case 189:
                    if char in self.delim13:
                        state = 190
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 190:
                    column -= 2
                    tokens.append((lexeme, ")", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0    

                case 191:
                    if char in self.delim14:
                        state = 192
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 192:
                    column -= 2
                    tokens.append((lexeme, "[", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0 

                case 193:
                    if char in self.delim15:
                        state = 194
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 194:
                    column -= 2
                    tokens.append((lexeme, "]", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0  

                case 195:
                    if char in self.delim16:
                        state = 196
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 196:
                    column -= 2
                    tokens.append((lexeme, "{", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0

                case 197:
                    if char is None or char in self.delim17:
                        state = 198
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 198:
                    column -= 2
                    tokens.append((lexeme, "}", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0

                case 199:
                    if char in self.delim11:
                        state = 200
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 201
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
                case 200:
                    column -= 2
                    tokens.append((lexeme, "=", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0
                
                case 201:
                    if char in self.delim10:
                        state = 202
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 202:
                    column -= 2
                    tokens.append((lexeme, "==", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 203:
                    if char in self.alphabet:
                        state = 204
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                            state = 0

                case 204:
                    column -= 2
                    tokens.append((lexeme, ".", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                # int and decimal Literals (State 212 - 266)
                case 205:
                    if char in self.digdelim:
                        state = 206
                        if char is not None:
                            self.step_back()
                    elif char == '.':
                        state = 226
                        lexeme += char
                        
                    elif char and char.isdigit():
                        lexeme += char
                        self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' leading zero error.")
                        state = 0
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 206:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 207:
                    if char in self.digit and char != 0:
                        state = 208
                        lexeme += char
                    elif char == '0':
                        state = 263
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 208:
                    if char in self.digdelim:
                        state = 209
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 210
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 209:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 210:
                    if char in self.digdelim:
                        state = 211
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 212
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 211:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 212:
                    if char in self.digdelim:
                        state = 213
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 214
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 213:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 214:
                    if char in self.digdelim:
                        state = 215
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 216
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 215:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 216:
                    if char in self.digdelim:
                        state = 217
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 218
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 217:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 218:
                    if char in self.digdelim:
                        state = 219
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 220
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 219:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 220:
                    if char in self.digdelim:
                        state = 221
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 222
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 221:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 222:
                    if char in self.digdelim:
                        state = 223
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 224
                        lexeme += char
                    elif char == '.':
                        state = 226
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 223:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 224:
                    if char in self.digdelim:
                        state = 225
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                         lexeme += char
                         self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' exceeds 9 digit limit.'")
                         state = 0
                    elif char == '.':
                        state = 241
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 225:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 226:
                    if char and char.isdigit():
                        state = 227
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 227:
                    if char in self.digdelim:
                        state = 228
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 229
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 228:
                    column -= 2
                    tokens.append((lexeme, "decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 229:
                    if char in self.digdelim:
                        state = 230
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 231
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0 

                case 230:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 231:
                    if char in self.digdelim:
                        state = 232
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 233
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0
                
                case 232:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 233:
                    if char in self.digdelim:
                        state = 234
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 235
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 234:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 235:
                    if char in self.digdelim:
                        state = 236
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 237
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 236:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 237:
                    if char in self.digdelim:
                        state = 238
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 239
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 238:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 239:
                    if char in self.digdelim:
                        state = 240
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 241
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 240:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 241:
                    if char in self.digdelim:
                        state = 242
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 243
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 242:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 243:
                    if char in self.digdelim:
                        state = 244
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        lexeme += char
                        self.errors.append(f"(Line {line}, Column {column}): decimal '{lexeme}' exceeds 9 digit limit.'")
                        state = 0
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): decimal literal '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 244:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                #String and letter literals
                case 245:
                    if char in self.asciichr:
                        state = 246
                        lexeme += char
                    elif char == '\\':
                        state = 264
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): ({lexeme}) Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 246:
                    if char == "'":
                        state = 247
                        lexeme += char
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): {lexeme} Expected (\').")
                        if char is not None:
                            self.step_back()
                        state = 0

                case 247:
                    if char in self.letterdelim:
                        state = 248
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): letter literal {lexeme} Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): letter literal {lexeme} Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0

                case 248:
                    column -= 2
                    tokens.append((lexeme, "letter_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 249:
                    if char in self.asciistr:
                        state = 249
                        lexeme += char
                    elif char == '"':
                        state = 250
                        lexeme += char
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): {lexeme} Expected character ( \" ).")
                        if char is not None:
                            self.step_back()
                        state = 0

                case 250:
                    if char in self.strdelim:
                        state = 251
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): string literal {lexeme} Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): string literal {lexeme} Invalid Delimiter ( {repr(char)} ).")
                            if char is not None:
                                self.step_back()
                        state = 0

                case 251:
                    column -= 2
                    tokens.append((lexeme, "string_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0


                # Identifier (State 252 - 255)
                case 252: 
                    if char and (char.isalpha() or char.isdigit() or char == '_'):
                        lexeme += char
                        state = 254                  
                    elif char in self.iddelim:
                        state = 253
                        if char is not None:
                            self.step_back()
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                            
                        state = 0

                case 253:
                    column -= 2
                    tokens.append((lexeme, "identifier", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 254:
                    if char and (char.isalpha() or char.isdigit() or char == '_'):
                        lexeme += char
                        
                        if len(lexeme) > 25:  # Identifier length limit
                            self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' exceeds 25 characters.")
                            state = 0

                    elif char in self.iddelim:
                        state = 255
                        if char is not None:
                            self.step_back()
                    
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0 

                case 255:
                    column -= 2
                    tokens.append((lexeme, "identifier", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                #Comments

                case 256:
                    if char in self.ascii:
                        state = 256
                    elif char == '\n':
                        line += 1
                        state = 257
                    else:
                        if char is not None:
                            self.step_back()
                        state = 0

                case 257:
                    if char is not None:
                        self.step_back()
                    state = 0

                case 258:
                    if char in self.asciicmnt:
                        state = 259
                    elif char == '\n':
                        line += 1
                        state = 259
                    elif char == '*':
                        state = 284
                    else:
                        if char is not None:
                            self.step_back()
                        state = 0

                case 259:
                    if char in self.asciicmnt:
                        state = 259
                    elif char == '\n':
                        line += 1
                        state = 259
                    elif char == '*' and self.peek_char() == '/':
                        state = 260
                    else:
                        column -= 1
                        state = 259

                case 260:
                    if char == '/':
                        state = 261
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 261:
                    if char == '\n':
                        line += 1
                        state = 262
                    else:
                        if char is not None:
                            self.step_back()
                        state = 0

                case 262:
                    if char is not None:
                        self.step_back()
                    state = 0

                #Period
                case 263:
                    if char == '.':
                        state = 226
                        lexeme += char
                    elif char and char.isdigit():
                        lexeme += char
                        self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid leading zero'")
                        state = 0
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): Negative zero can only be followed by a period.")
                        state = 0

                case 264:
                    if char == '0':
                        state = 246
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): ({lexeme}) Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char is not None:
                                self.step_back()
                        state = 0
                
        return tokens, self.errors