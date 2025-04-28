class Tokenizer:
    def __init__(self):
        self.errors = []
        self.whitespace = {' ', '\t', '\n'}

        self.alphabet = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.number = set("0123456789")
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
        
        self.code = ""
        self.index = 0
        self.line_number = 1
        self.column = 1

    def next_char(self):
        if self.index < len(self.code):
            char = self.code[self.index]
            self.index += 1
            return char
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

            #print(f"State: {state}, char: {repr(char)}, Lexeme: {repr(lexeme)}, Line: {line}, Column {column}")

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
                        state = 60
                        lexeme += 'l'
                    elif char == 'm': #m - main
                        state = 67
                        lexeme += "m"
                    elif char == 'o': #o - option
                        state = 72
                        lexeme += 'o'
                    elif char == 'r': #r - read
                        state = 79
                        lexeme += 'r'
                    elif char == 's': #s - scope
                        state = 90
                        lexeme += 's'
                    elif char == 't': #t - task
                        state = 112
                        lexeme += 't'
                    elif char == 'u': #u - unit
                        state = 123
                        lexeme += 'u'
                    elif char == 'w': #w - while
                        state = 128
                        lexeme += 'w'
                    elif char == 'n':
                        state = 188
                        lexeme += 'n'
                    

                    #identifier
                    elif char.isalpha():
                        state = 275
                        lexeme += char
                    

                    #num literals
                    elif char == '0':
                        state = 212
                        lexeme += char
                    elif char.isdigit() and char != '0':
                        state = 215
                        lexeme += char
                    elif char == '~':
                        state = 214
                        lexeme += char

                    #symbols
                    elif char == '+':
                        state = 134
                        lexeme += char

                    elif char == '-':
                        state = 140
                        lexeme += char

                    elif char == '*':
                        state = 146
                        lexeme += char

                    elif char == '/':
                        state = 154
                        lexeme += char
                    
                    elif char == '%':
                        state = 158
                        lexeme += char

                    elif char == '>':
                        state = 162
                        lexeme += char

                    elif char == '<':
                        state = 166
                        lexeme += char

                    elif char == '!':
                        state = 170
                        lexeme += char

                    elif char == '&':
                        state = 174
                        lexeme += char

                    elif char == '|':
                        state = 177
                        lexeme += char

                    elif char == ',':
                        state = 194
                        lexeme += char
                    
                    elif char == ':':
                        state = 196
                        lexeme += char
                    
                    elif char == ';':
                        state = 198
                        lexeme += char

                    elif char == '(':
                        state = 200
                        lexeme += char
                    
                    elif char == ')':
                        state = 202
                        lexeme += char
                    
                    elif char == '[':
                        state = 204
                        lexeme += char
                    
                    elif char == ']':
                        state = 206
                        lexeme += char
                    
                    elif char == '{':
                        state = 208
                        lexeme += char
                    
                    elif char == '}':
                        state = 210
                        lexeme += char
            
                    elif char == '=':
                        state = 288
                        lexeme += char

                    elif char == '.':
                        state = 292
                        lexeme += char

                    #string and letter
                    elif char == "'":
                        state = 268
                        lexeme += "'"
                    elif char == '"':
                        state = 272
                        lexeme += '"'

                    #error handling
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): Invalid Character ( {repr(char)} ).")

                #KEYWORDS
                case 1: 
                    if char == 'o':
                        state = 2
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
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
                    elif char == 'f':
                        state = 14
                        lexeme += 'f'
                    elif char == 'i':
                        state = 20
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0  
                
                case 7:
                    if char == 'c':
                        state = 8
                        lexeme += 'c'
                    elif char == 'f':
                        state = 14
                        lexeme += 'f'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0      
                
                case 8: 
                    if char == 'i':
                        state = 9
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0      
                
                case 9: 
                    if char == 'm':
                        state = 10
                        lexeme += 'm'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0      
                
                case 10: 
                    if char == 'a':
                        state = 11
                        lexeme += 'a'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0      
                
                case 11: 
                    if char == 'l':
                        state = 12
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0      
                
                case 12: #Delim
                    if char in self.dtdelim:
                        state = 13
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0     
                        
                case 15: 
                    if char == 'u':
                        state = 16
                        lexeme += 'u'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0 
                            
                        
                case 16: 
                    if char == 'l':
                        state = 17
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0 
                        
    
                case 17: 
                    if char == 't':
                        state = 18
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                            state = 0 
                            
                        
                case 18:
                    if char == ':':
                        state = 19
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                                self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                        state = 182
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.delim2:
                            state = 278
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
                    elif char == 's':
                        state = 180
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.dtdelim:
                            state = 278
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
                            state = 0
                        
                case 59:
                    column -= 2
                    tokens.append((lexeme, "int", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 60:
                    if char == 'e': 
                        state = 61
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 61:
                    if char == 't':
                        state = 62
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 62:
                    if char == 't': 
                        state = 63
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'e': 
                        state = 64
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'r': 
                        state = 65
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 65:
                    if char in self.dtdelim:
                        state = 66
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.dtdelim:
                            state = 278
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
                            state = 0
                        
                case 66:
                    column -= 2
                    tokens.append((lexeme, "letter", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 67:
                    if char == 'a':
                        state = 68
                        lexeme += 'a'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'i':
                        state = 69
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'n':
                        state = 70
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char in self.pardelim:
                        state = 71
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.pardelim:
                            state = 278
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
                            state = 0
                        
                case 71:
                    column -= 2
                    tokens.append((lexeme, "main", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 72:
                    if char == 'p':
                        state = 73
                        lexeme += 'p'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 73:
                    if char == 't':
                        state = 74
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'o':
                        state = 76
                        lexeme += 'o'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'n':
                        state = 77
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 77:
                    if char == ' ':
                        state = 78
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0
                        
                case 78:
                    column -= 2
                    tokens.append((lexeme, "option", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 79:
                    if char == 'e':
                        state = 80
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'a':
                        state = 81
                        lexeme += 'a'
                    elif char == 't':
                        state = 85
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'd':
                        state = 82
                        lexeme += 'd'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 's':
                        state = 83
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char in self.pardelim:
                        state = 84
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.delim2:
                            state = 278
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
                            state = 0
                        
                case 84:
                    column -= 2
                    tokens.append((lexeme, "reads", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 85:
                    if char == 'u':
                        state = 86
                        lexeme += 'u'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'r':
                        state = 87
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'n':
                        state = 88
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == ' ':
                        state = 89
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0
                        
                case 89:
                    column -= 2
                    tokens.append((lexeme, "return", line, column))
                    if char is not None:
                        self.step_back() #l
                    state = 0

                case 90:
                    if char == 'c':
                        state = 91
                        lexeme += 'c'
                    elif char == 'e':    #S"E"LECT add in case 90
                        state = 96
                        lexeme += 'e'
                    elif char == 'k':      #S"K"IP add in case 90
                        state = 102
                        lexeme += 'k'
                    elif char == 't':         #S"T"RING add in case 90
                        state = 106
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                 
                    

                case 91:
                    if char == 'o':
                        state = 92
                        lexeme += 'o'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'p':
                        state = 93
                        lexeme += 'p'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'e':
                        state = 94
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char in self.pardelim:
                        state = 95
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.pardelim:
                            state = 278
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
                            state = 0
                        
                case 95:
                    column -= 2
                    tokens.append((lexeme, "scope", line, column))#check
                    if char is not None:
                        self.step_back()
                    state = 0

                case 96:
                    if char == 'l':
                        state = 97
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'e':
                        state = 98
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'c':
                        state = 99
                        lexeme += 'c'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 't':
                        state = 100
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char in self.conddelim:
                        state = 101
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.delim2:
                            state = 278
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
                            state = 0
                        
                case 101:
                    column -= 2
                    tokens.append((lexeme, "select", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 102:
                    if char == 'i':
                        state = 103
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 103:
                    if char == 'p':
                        state = 104
                        lexeme += 'p'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == ';':
                        state = 105
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ';':
                            state = 278
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
                            state = 0
                        
                case 105:
                    column -= 2
                    tokens.append((lexeme, "skip", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 106:
                    if char == 'r':
                        state = 107
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 107:
                    if char == 'i':
                        state = 108
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'n':
                        state = 109
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'g':
                        state = 110
                        lexeme += 'g'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char in self.dtdelim:
                        state = 111
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.dtdelim:
                            state = 278
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
                            state = 0
                        
                case 111:
                    column -= 2
                    tokens.append((lexeme, "string", line, column))
                    if char is not None:
                        self.step_back() 
                    state =  0

                case 112:
                    if char == 'a':
                        state = 113
                        lexeme += 'a'
                    elif char == 'r':
                        state = 117
                        lexeme += 'r'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 113:
                    if char == 's':
                        state = 114
                        lexeme += 's'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'k':
                        state = 115
                        lexeme += 'k'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == ' ':
                        state = 116
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0
                        
                case 116:
                    column -= 2
                    tokens.append((lexeme, "task", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 117:
                    if char == 'u':
                        state = 118
                        lexeme += 'u'
                    elif char == 'y':
                        state = 121
                        lexeme += 'y'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 118:
                    if char == 'e':
                        state = 119
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char in self.delim3:
                        state = 120
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.delim3:
                            state = 278
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
                            state = 0
                        
                case 120:
                    column -= 2
                    tokens.append((lexeme, "true", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 121:
                    if char in self.delim2:
                        state = 122
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ':':
                            state = 278
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
                            state = 0
                        
                case 122:
                    column -= 2
                    tokens.append((lexeme, "try", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 123:
                    if char == 'n':
                        state = 124
                        lexeme += 'n'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                    
                case 124:
                    if char == 'i':
                        state = 125
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 't':
                        state = 126
                        lexeme += 't'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == ' ':
                        state = 127
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0
                        
                case 127:
                    column -= 2
                    tokens.append((lexeme,"unit", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 128:
                    if char == 'h':
                        state = 129
                        lexeme += 'h'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                        
                case 129:
                    if char == 'i':
                        state = 130
                        lexeme += 'i'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'l':
                        state = 131
                        lexeme += 'l'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char == 'e':
                        state = 132
                        lexeme += 'e'
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                    if char in self.conddelim:
                        state = 133
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.delim2:
                            state = 278
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
                            state = 0
                        
                case 133:
                    column -= 2
                    tokens.append((lexeme, "while", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                # Symbols
                case 134:
                    if char in self.delim7:
                        state = 135
                        if char is not None:
                            self.step_back()
                    elif char == '+':
                        state = 136
                        lexeme += char
                    elif char == '=':                        
                        state = 138
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 135:
                    column -= 2
                    tokens.append((lexeme, "+", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 136:
                    if char in self.delim4:
                        state = 137
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
                
                case 137:
                    column -= 2
                    tokens.append((lexeme, "++", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 138:
                    if char in self.delim5:
                        state = 139
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
                
                case 139:
                    column -= 2
                    tokens.append((lexeme, "+=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 140:
                    if char in self.delim5:
                        state = 141
                        if char is not None:
                            self.step_back()
                    elif char == '-':
                        state = 142
                        lexeme += char
                    elif char == '=':                        
                        state = 144
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0
                
                case 141:
                    column -= 2
                    tokens.append((lexeme, "-", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 142:
                    if char in self.delim4:
                        state = 143
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
                
                case 143:
                    column -= 2
                    tokens.append((lexeme, "--", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 144:
                    if char in self.delim5:
                        state = 145
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
                
                case 145:
                    column -= 2
                    tokens.append((lexeme, "-=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 146:
                    if char in self.delim5:
                        state = 147
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 148
                        lexeme += char
                    elif char == '*':                        
                        state = 150
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0
                
                case 147:
                    column -= 2
                    tokens.append((lexeme, "*", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 148:
                    if char in self.delim5:
                        state = 149
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
                
                case 149:
                    column -= 2
                    tokens.append((lexeme, "*=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 150:
                    if char in self.delim5:
                        state = 151
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 152
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0
                
                case 151:
                    column -= 2
                    tokens.append((lexeme, "**", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 152:
                    if char in self.delim5:
                        state = 153
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
                
                case 153:
                    column -= 2
                    tokens.append((lexeme, "**=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 154:
                    if char in self.delim5:
                        state = 155
                        if char is not None:
                            self.step_back()
                    elif char == '/':
                        state = 280
                    elif char == '*':
                        state = 282
                    elif char == '=':
                        state = 156
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0
                
                case 155:
                    column -= 2
                    tokens.append((lexeme, "/", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 156:
                    if char in self.delim5:
                        state = 157
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
                
                case 157:
                    column -= 2
                    tokens.append((lexeme, "/=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 158:
                    if char in self.delim5:
                        state = 159
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 160
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0
                
                case 159:
                    column -= 2
                    tokens.append((lexeme, "%", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 160:
                    if char in self.delim5:
                        state = 161
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
                
                case 161:
                    column -= 2
                    tokens.append((lexeme, "%=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 162:
                    if char in self.delim5:
                        state = 163
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 164
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 163:
                    column -= 2
                    tokens.append((lexeme, ">", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 164:
                    if char in self.delim5:
                        state = 165
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

                case 165:
                    column -= 2
                    tokens.append((lexeme, ">=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 166:
                    if char in self.delim5:
                        state = 167
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 168
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 167:
                    column -= 2
                    tokens.append((lexeme, "<", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 168:
                    if char in self.delim5:
                        state = 169
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

                case 169:
                    column -= 2
                    tokens.append((lexeme, "<=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 170:
                    if char in self.delim9:
                        state = 171
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 172
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 171:
                    column -= 2
                    tokens.append((lexeme, "!", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 172:
                    if char in self.delim10:
                        state = 173
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

                case 173:
                    column -= 2
                    tokens.append((lexeme, "!=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 174:
                    if char == '&':
                        state = 175
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 175:
                    if char in self.delim5:
                        state = 176
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

                case 176:
                    column -= 2
                    tokens.append((lexeme, "&&", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 177:
                    if char == '|':
                        state = 178
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 178:
                    if char in self.delim5:
                        state = 179
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

                case 179:
                    column -= 2
                    tokens.append((lexeme, "||", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 180:
                    if char == ' ':
                        state = 181
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0  
                case 181:
                    column -= 2
                    tokens.append((lexeme, "ins", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0
                
                case 182:
                    if char == ' ':
                        state = 183
                        if char is not None:
                            self.step_back()
                    elif char == 'n':
                        state = 184
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0

                case 183:
                    column -= 2
                    tokens.append((lexeme, "is", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 184:
                    if char == 'o':
                        state = 185
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                case 185:
                    if char == 't':
                        state = 186
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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
                case 186:
                    if char == ' ':
                        state = 187
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0  
                case 187:
                    column -= 2
                    tokens.append((lexeme, "isnot", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 188:
                    if char == 'o':
                        state = 189
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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

                case 189:
                    if char == 't':
                        state = 190
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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

                case 190:
                    if char == 'i':
                        state = 191
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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

                case 191:
                    if char == 'n':
                        state = 192
                        lexeme += char
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char in self.iddelim:
                            state = 278
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

                case 192: #Delim
                    if char == ' ':
                        state = 193
                        if char is not None:
                            self.step_back()
                    elif char is not None and (char.isalpha() or char.isdigit() or char == '_'):
                        state = 275
                        lexeme += char
                    else:
                        if char == ' ':
                            state = 278
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
                            state = 0
                
                case 193: #Tokenize
                    column -= 2
                    tokens.append((lexeme, "notin", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 194:
                    if char in self.delim11:
                        state = 195
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

                case 195:
                    column -= 2
                    tokens.append((lexeme, ",", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0

                case 196:
                    if char in self.delim6:
                        state = 197
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

                case 197:
                    column -= 2
                    tokens.append((lexeme, ":", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0

                case 198:
                    if char is None or char in self.delim6:
                        state = 199
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

                case 199:
                    column -= 2
                    tokens.append((lexeme, ";", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0
                    
                case 200:
                    if char in self.delim12:
                        state = 201
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

                case 201:
                    column -= 2
                    tokens.append((lexeme, "(", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0
                    
                case 202:
                    if char in self.delim13:
                        state = 203
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

                case 203:
                    column -= 2
                    tokens.append((lexeme, ")", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0    

                case 204:
                    if char in self.delim14:
                        state = 205
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

                case 205:
                    column -= 2
                    tokens.append((lexeme, "[", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0 

                case 206:
                    if char in self.delim15:
                        state = 207
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

                case 207:
                    column -= 2
                    tokens.append((lexeme, "]", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0  

                case 208:
                    if char in self.delim16:
                        state = 209
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

                case 209:
                    column -= 2
                    tokens.append((lexeme, "{", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0

                case 210:
                    if char is None or char in self.delim17:
                        state = 211
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

                case 211:
                    column -= 2
                    tokens.append((lexeme, "}", line, column))
                    if char is not None:
                            self.step_back()
                    state = 0 

                # int and decimal Literals (State 212 - 266)
                case 212:
                    if char in self.digdelim:
                        state = 213
                        if char is not None:
                            self.step_back()
                    elif char == '.':
                        state = 241
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

                case 213:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 214:
                    if char in self.number and char != 0:
                        state = 215
                        lexeme += char
                    elif char == '0':
                        state = 287
                        lexeme += char
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

                case 215:
                    if char in self.digdelim:
                        state = 216
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 217
                        lexeme += char
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

                case 216:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 217:
                    if char in self.digdelim:
                        state = 218
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 219
                        lexeme += char
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

                case 218:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 219:
                    if char in self.digdelim:
                        state = 220
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 221
                        lexeme += char
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

                case 220:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 221:
                    if char in self.digdelim:
                        state = 222
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 223
                        lexeme += char
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

                case 222:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 223:
                    if char in self.digdelim:
                        state = 224
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 225
                        lexeme += char
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

                case 224:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 225:
                    if char in self.digdelim:
                        state = 226
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 227
                        lexeme += char
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

                case 226:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 227:
                    if char in self.digdelim:
                        state = 228
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 229
                        lexeme += char
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

                case 228:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
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

                case 230:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
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

                case 232:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
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

                case 234:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
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

                case 236:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
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

                case 238:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 239:
                    if char in self.digdelim:
                        state = 240
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                         lexeme += char
                         self.errors.append(f"(Line {line}, Column {column}): int literal '{lexeme}' exceeds 13 digit limit.'")
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

                case 240:
                    column -= 2
                    tokens.append((lexeme, "int_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 241:
                    if char and char.isdigit():
                        state = 242
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
                    if char in self.digdelim:
                        state = 243
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 244
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

                case 243:
                    column -= 2
                    tokens.append((lexeme, "decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 244:
                    if char in self.digdelim:
                        state = 245
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 246
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

                case 245:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 246:
                    if char in self.digdelim:
                        state = 247
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 248
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
                
                case 247:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 248:
                    if char in self.digdelim:
                        state = 249
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 250
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

                case 249:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 250:
                    if char in self.digdelim:
                        state = 251
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 252
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

                case 251:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 252:
                    if char in self.digdelim:
                        state = 253
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 254
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

                case 253:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 254:
                    if char in self.digdelim:
                        state = 255
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 256
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

                case 255:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 256:
                    if char in self.digdelim:
                        state = 257
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 258
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

                case 257:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 258:
                    if char in self.digdelim:
                        state = 259
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 260
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

                case 259:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 260:
                    if char in self.digdelim:
                        state = 261
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 262
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

                case 261:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 262:
                    if char in self.digdelim:
                        state = 263
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 264
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

                case 263:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 264:
                    if char in self.digdelim:
                        state = 265
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        state = 266
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

                case 265:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 266:
                    if char in self.digdelim:
                        state = 267
                        if char is not None:
                            self.step_back()
                    elif char and char.isdigit():
                        lexeme += char
                        self.errors.append(f"(Line {line}, Column {column}): decimal '{lexeme}' exceeds 13 digit limit.'")
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

                case 267:
                    column -= 2
                    tokens.append((lexeme,"decimal_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                #String and letter literals
                case 268:
                    if char in self.asciichr:
                        state = 269
                        lexeme += char
                    elif char == '\\':
                        state = 294
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

                case 269:
                    if char == "'":
                        state = 270
                        lexeme += char
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): {lexeme} Expected (\').")
                        if char is not None:
                            self.step_back()
                        state = 0

                case 270:
                    if char in self.letterdelim:
                        state = 271
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

                case 271:
                    column -= 2
                    tokens.append((lexeme, "letter_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 272:
                    if char in self.asciistr:
                        state = 272
                        lexeme += char
                    elif char == '"':
                        state = 273
                        lexeme += char
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): {lexeme} Expected character ( \" ).")
                        if char is not None:
                            self.step_back()
                        state = 0

                case 273:
                    if char in self.strdelim:
                        state = 274
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

                case 274:
                    column -= 2
                    tokens.append((lexeme, "string_literal", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0


                # Identifier (State 275 - 278)
                case 275: 
                    if char and (char.isalpha() or char.isdigit() or char == '_'):
                        lexeme += char
                        state = 277                        
                    elif char in self.iddelim:
                        state = 276
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
                        state = 0

                case 276:
                    column -= 2
                    tokens.append((lexeme, "identifier", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 277:
                    if char and (char.isalpha() or char.isdigit() or char == '_'):
                        lexeme += char
                        
                        if len(lexeme) > 25:  # Identifier length limit
                            self.errors.append(f"(Line {line}, Column {column}): Identifier '{lexeme}' exceeds 25 characters.")
                            state = 0

                    elif char in self.iddelim:
                        state = 278
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
                        state = 0 

                case 278:
                    column -= 2
                    tokens.append((lexeme, "identifier", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                #Comments

                case 280:
                    if char in self.ascii:
                        state = 280
                    elif char == '\n':
                        line += 1
                        state = 281
                    else:
                        if char is not None:
                            self.step_back()
                        state = 0

                case 281:
                    if char is not None:
                        self.step_back()
                    state = 0

                case 282:
                    if char in self.asciicmnt:
                        state = 283
                    elif char == '\n':
                        line += 1
                        state = 283
                    elif char == '*':
                        state = 284
                    else:
                        if char is not None:
                            self.step_back()
                        state = 0

                case 283:
                    if char in self.asciicmnt:
                        state = 283
                    elif char == '\n':
                        line += 1
                        state = 283
                    elif char == '*':
                        state = 284
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                            if char == '\n':
                                column = 0
                        state = 0

                case 284:
                    if char == '/':
                        state = 285
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 285:
                    if char == '\n':
                        line += 1
                        state = 286
                    else:
                        if char is not None:
                            self.step_back()
                        state = 0

                case 286:
                    if char is not None:
                        self.step_back()
                    state = 0

                #Period
                case 287:
                    if char == '.':
                        state = 241
                        lexeme += char

                    elif char and char.isdigit():
                        lexeme += char
                        self.errors.append(f"(Line {line}, Column {column}): '{lexeme}' Invalid leading zero'")
                        state = 0
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): Negative zero can only be followed by a period.")
                        state = 0

                case 288:
                    if char in self.delim5:
                        state = 289
                        if char is not None:
                            self.step_back()
                    elif char == '=':
                        state = 290
                        lexeme += char
                    else:
                        column -= 1
                        if char is None:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Missing Delimiter.")
                        else:
                            self.errors.append(f"(Line {line}, Column {column}): Symbol '{lexeme}' Invalid Delimiter ( {repr(char)} ).")
                            if char == '\n':
                                column = 0
                        state = 0

                case 289:
                    column -= 2
                    tokens.append((lexeme, "=", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 290:
                    if char in self.delim5:
                        state = 291
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

                case 291:
                    column -= 2
                    tokens.append((lexeme, "==", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 292:
                    if char in self.alphabet:
                        state = 293
                        if char is not None:
                            self.step_back()
                    else:
                        self.errors.append(f"(Line {line}, Column {column}): Invalid Delimiter ( {repr(char)} ).")
                        if char == '\n':
                            column = 0
                        state = 0

                case 293:
                    column -= 2
                    tokens.append((lexeme, ".", line, column))
                    if char is not None:
                        self.step_back()
                    state = 0

                case 294:
                    if char == '0':
                        state = 269
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