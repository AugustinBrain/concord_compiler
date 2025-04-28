class Symbol:
    def __init__(self, name, symbol_type, data_type=None, value=None, is_fixed=False, line=None, column=None, dimension=0, sizes=None):
        self.name = name
        self.symbol_type = symbol_type  # variable, function, unit, parameter
        self.data_type = data_type      # int, decimal, string, letter, bool
        self.value = value
        self.is_fixed = is_fixed
        self.line = line
        self.column = column
        self.dimension = dimension
        self.sizes = sizes

    def __repr__(self):
        return f"Symbol(name = {self.name}, type = {self.symbol_type}, data_type = {self.data_type}, value = {self.value}, fixed = {self.is_fixed}, line = {self.line}, column = {self.column}, dimension = {self.dimension}, sizes = {self.sizes})"


class Semantic:
    def __init__(self):
        self.symbol_table = {}  # Dictionary {scope: {symbol_name: Symbol}}
        self.unit_table = {}
        self.errors = []
        self.current_scope = "global"
        self.scope_stack = ["global"]
        self.tokens = []
        self.index = 0

        self.valid_types = {
            "int": ["int_literal", "bool", "decimal_literal"],
            "decimal": ["int_literal", "decimal_literal", "bool"],
            "bool": ["true", "false", "int_literal", "decimal_literal"],
            "letter": ["letter_literal"],
            "string": ["string_literal"]
        }

    def semantic_analyzer(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.data_types = {"int", "decimal", "bool", "letter", "string"}

        if self.current_scope not in self.symbol_table:
            self.symbol_table[self.current_scope] = {}

        while self.index < len(tokens):
            lexeme, token_type, line, column = tokens[self.index]

            if token_type == "fixed":
                self.fixed_declaration()
            elif token_type == 'unit':
                # Check if this is a unit type declaration or unit variable declaration
                next_token = self.tokens[self.index + 1][0]
                next_next_token = self.tokens[self.index + 2][0] if self.index + 2 < len(tokens) else None
                
                # If pattern is "unit X {" then it's a type declaration
                if next_next_token == "{":
                    self.unit_declaration()
                # Otherwise "unit X y" is a variable declaration
                else:
                    self.unit_variable_declaration()
            elif token_type in self.data_types:
                self.variable_declaration()
            elif token_type == "task" or token_type == "empty" or token_type == "main": #task are functions with return value, empty no return value.
                self.function_declaration()
            
            else:
                self.index += 1

        return self.errors
    
    #FUNCTION: Check if variable is already declared
    def is_duplicate_variable(self, var_name, line, column):
        if var_name in self.symbol_table[self.current_scope] or var_name in self.symbol_table["global"]:
            self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): Variable '{var_name}' is already declared."
            )
            return True  # Variable already exists
        return False

    #FUNCTION: Perform type checking
    def is_type_mismatch(self, data_type, value_type, var_name, line, column):
        conditions = {"if", "elseif", "while"}
        # data_type = int, value_type = int_literal
        valid_types = {
            "int": ["int_literal", "bool", "decimal_literal", "user_input"],  # int 
            "decimal": ["int_literal", "decimal_literal", "bool", "user_input"],  # decimal
            "bool": ["bool", "int_literal", "decimal_literal", "user_input"],  # bool 
            "letter": ["letter_literal", "user_input"],  # letter literals
            "string": ["string_literal", "user_input"],  # string literals
        }
        # Error case
        if value_type == "error":
            return True
        
        # Check if the value type is in the list of valid types for the target type
        if value_type in valid_types.get(data_type, []):
            return False  # No mismatch if it's a valid conversion
        else:
            if var_name in conditions:
                self.errors.append(
                    f"⚠️ Semantic Error at (line {line}, column {column}): Condition returns incorrect value. "
                    f"Expected '{self.valid_types[data_type]}', got '{value_type}'."
                )
            else:
                    self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): Assign Value Mismatch for '{var_name}'. "
                f" Expected '{self.valid_types[data_type]}', got '{value_type}'."
            )
            return True  # Type mismatch
        return False
    
    def is_type_compatible(self, expected, actual):
        """ Checks if a given actual data type matches the expected type """
        type_map = {
            "int": ["int_literal", "user_input"],
            "decimal": ["decimal_literal", "int_literal", "user_input"],
            "bool": ["true", "false", "user_input"],
            "letter": ["letter_literal", "user_input"],
            "string": ["string_literal", "user_input"],
        }
        return actual in type_map.get(expected, [])

    #FUNCTION: Store variable in the symbol table
    def store_variable(self, var_name, symbol_type, data_type, is_fixed, line, column, dimension, sizes=None):
        self.symbol_table[self.current_scope][var_name] = Symbol(
            name=var_name,
            symbol_type= symbol_type,
            data_type=data_type,
            value=None,  # Value assignment can be handled separately
            is_fixed=is_fixed,
            line=line,
            column=column,
            dimension=dimension,
            sizes=sizes
        )

    # Fixed Declarations 
    def fixed_declaration(self):
        symbol_type = "fixed_declaration"
        dimension = 0
        self.index += 1  # Move past 'fixed'
        data_type = self.tokens[self.index][1]  # Get data type

        while True:  # Loop to handle multiple declarations
            self.index += 1  # Move to variable identifier
            var_name, token_type, line, column = self.tokens[self.index]

            # Check if variable already exists
            if self.is_duplicate_variable(var_name, line, column):
                return  # Stop processing this declaration

            self.index += 1  # Move to '=' symbol
            self.index += 1  # Move to value assigned
            value_type = self.tokens[self.index][1]

            # Perform Type Checking
            if self.is_type_mismatch(data_type, value_type, var_name, line, column):
                return  # Stop processing if there's a type mismatch

            # Store the variable in the symbol table
            self.store_variable(var_name, symbol_type, data_type, is_fixed=True, line=line, column=column, dimension=dimension)

            self.index += 1  # Move to ',' or ';'
            if self.tokens[self.index][1] == ";":  # End of declaration
                break  # Exit the loop
            elif self.tokens[self.index][1] == ",":  # Continue to next variable
                continue

    # ---------------- UNIT DECLARATION ---------------- #
    def unit_declaration(self):
        """ Handles unit type definition (e.g., unit record { ... }) """
        self.index += 1  # Move past 'unit'
        unit_name, _, line, column = self.tokens[self.index]

        # Check if unit name is already declared
        if unit_name in self.unit_table:
            self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): Unit '{unit_name}' is already declared."
            )

            return

        self.index += 1  # Move to '{'
        self.index += 1  # Move inside the unit block

        unit_fields = []  # Store fields of the unit

        while self.tokens[self.index][0] != "}":
            field_type, field_type_token, line, column = self.tokens[self.index]

            # Ensure it's a valid data type
            if field_type_token not in self.data_types:
                self.errors.append(
                    f"⚠️ Semantic Error at (line {line}, column {column}): Invalid data type '{field_type}' in unit definition."
                )
                return

            self.index += 1  # Move to field name
            field_name, _, line, column = self.tokens[self.index]

            # Store field information
            unit_fields.append((field_name, field_type))

            self.index += 1  # Move past field name
            if self.tokens[self.index][0] == ";":
                self.index += 1  # Move to next field or closing '}'

        # Store unit in unit table
        self.unit_table[unit_name] = unit_fields
        self.index += 1  # Move past '}'

    # ---------------- UNIT VARIABLE DECLARATION ---------------- #
    def unit_variable_declaration(self):
        """ Handles unit variable declaration (e.g., unit record r1;) or initialization (unit record r2 = {...};) """
        self.index += 1  # Move past 'unit'
        unit_name, _, line, column = self.tokens[self.index]

        # Ensure the unit type exists
        if unit_name not in self.unit_table:
            self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): Unit '{unit_name}' is not declared."
            )
            return

        self.index += 1  # Move to variable name
        var_name, _, line, column = self.tokens[self.index]

        # Ensure variable is not already declared
        if var_name in self.symbol_table[self.current_scope]:
            self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): Variable '{var_name}' is already declared."
            )
            return

        # Move to next token
        self.index += 1

        # Check for initialization
        if self.tokens[self.index][0] == "=":
            self.index += 1  # Move past '='


            self.index += 1  # Move inside '{'

            unit_fields = self.unit_table[unit_name]
            expected_field_count = len(unit_fields)
            provided_values = []

            while self.tokens[self.index][0] != "}":
                provided_values.append(self.tokens[self.index])
                self.index += 1

                if self.tokens[self.index][0] == ",":
                    self.index += 1  # Move to next value

            # Check for correct number of values
            if len(provided_values) != expected_field_count:
                self.errors.append(
                    f"⚠️ Semantic Error at (line {line}, column {column}): Unit '{unit_name}' expected {expected_field_count} values, but got {len(provided_values)}."
                )
                return

            # Check for correct data types
            for (field_name, expected_type), (value, actual_type, line, column) in zip(unit_fields, provided_values):
                if not self.is_type_compatible(expected_type, actual_type):
                    self.errors.append(
                        f"⚠️ Semantic Error at (line {line}, column {column}): Field '{field_name}' in unit '{unit_name}' expects '{expected_type}', but got '{actual_type}'."
                    )
                    return

            self.index += 1  # Move past '}'

        # Store the unit variable in the symbol table
        self.symbol_table[self.current_scope][var_name] = Symbol(
            name=var_name,
            symbol_type="unit_variable",
            data_type=unit_name,
            value=None,
            line=line,
            column=column,
        )

    def variable_declaration(self):
        symbol_type = "variable_declaration"
        data_type = self.tokens[self.index][1] # Get data type
        dimension = 0
        sizes = None

        while True:
            self.index += 1  # Move to variable identifier            
            var_name, token_type, line, column = self.tokens[self.index]

            # Check if variable already exists
            if self.is_duplicate_variable(var_name, line, column):
                # Skip to next declaration or end
                while self.index < len(self.tokens) and self.tokens[self.index][1] != ";" and self.tokens[self.index][1] != ",":
                    self.index += 1
                if self.index >= len(self.tokens) or self.tokens[self.index][1] == ";":
                    break
                else:  # comma found
                    continue

            self.index += 1  # Move to symbol after variable

            if self.tokens[self.index][1] == "[":
                symbol_type, dimension, sizes = self.array_declaration(line)
            
            if self.tokens[self.index][1] == "=":

                self.index += 1  # Move to value assigned

                if dimension > 0: # Array Initialization
                    if self.tokens[self.index][1] == "{":
                        array_size, value_type = self.array_initialization(data_type, dimension)

                        # If sizes weren't specified during declaration, set them from initialization
                        if sizes is None:
                            sizes = array_size
                        else:
                            # Verify that initialized size matches declared size
                            if not self.verify_array_size_match(sizes, array_size, var_name, line, column):
                                return  # Stop processing if size mismatch
                else:
                    value_type = self.validate_expression()  # Validate full expression
                    # Perform Type Checking for scalar variables
                    if self.is_type_mismatch(data_type, value_type, var_name, line, column):
                        # self.errors.append(
                        #     f"Validation Stopped: Data Type {data_type}, Value Type {value_type} at line {line}, column {column}"
                        # )
                        return  # Stop processing if there's a type mismatch
                    
            # Store the variable in the symbol table
            self.store_variable(var_name, symbol_type, data_type, is_fixed=False, line=line, column=column, dimension=dimension, sizes=sizes)

            # while self.tokens[self.index][1] != ";":
            #     self.index -= 1
            if self.tokens[self.index][1] == ";":
                break
            if self.tokens[self.index][1] == ",":  # Continue to next variable
                continue
 
    def array_declaration(self, line):
        symbol_type = "array_declaration"
        dimension = 0
        sizes = []

        self.index += 1 # After [ -> int_literal or ]
        if self.tokens[self.index][1] == "int_literal": # [2 <-
            if int(self.tokens[self.index][0]) > 0:
                sizes.append(int(self.tokens[self.index][0]))
                self.index += 1 # [2] <-
            else:
                self.errors.append(f"⚠️ Semantic Error at (line {line}): Array size must be a positive integer")
                self.index += 1 # [2] <-
        else:
            sizes = None

        self.index += 1 # After ]
        dimension = 1

        if self.tokens[self.index][1] == "[":
            self.index += 1 # Move to [2][2 <-
            sizes.append(int(self.tokens[self.index][0]))
            self.index += 1 # [2][2] <-
            dimension = 2
            self.index += 1

        return symbol_type, dimension, sizes

    def array_initialization(self, data_type, dimension):
        self.index += 1  # After {
        element_count = 0
        row_count = 0
        col_count = 0
        max_col_count = 0
        value_type = None

        if dimension == 1:
            while self.index < len(self.tokens) and self.tokens[self.index][1] != "}":
                lexeme = self.tokens[self.index][0]
                value_type = self.tokens[self.index][1]

                # Check for type mismatch
                if self.is_type_mismatch(data_type, value_type, lexeme, self.tokens[self.index][2], self.tokens[self.index][3]):
                    return None, "error"

                element_count += 1
                self.index += 1  # Move past value

                # Expecting ',' or '}'
                if self.tokens[self.index][1] == ",":
                    self.index += 1  # Move to next value
                elif self.tokens[self.index][1] == "}":
                    break

            self.index += 1  # Move past '}'
            return [element_count], value_type  # Return array size and type

        elif dimension == 2:
            while self.index < len(self.tokens) and self.tokens[self.index][1] != "}":
                if self.tokens[self.index][1] == "{":
                    row_count += 1
                    col_count = 0
                    self.index += 1  # Move past '{'

                    while self.index < len(self.tokens) and self.tokens[self.index][1] != "}":
                        value_type = self.tokens[self.index][1]

                        # Check for type mismatch
                        if self.is_type_mismatch(data_type, value_type, "", self.tokens[self.index][2], self.tokens[self.index][3]):
                            return None, "error"

                        col_count += 1
                        self.index += 1  # Move past value

                        if self.tokens[self.index][1] == ",":
                            self.index += 1  # Move to next value
                        elif self.tokens[self.index][1] == "}":
                            break

                    max_col_count = max(max_col_count, col_count)
                    self.index += 1  # Move past '}'

                    if self.tokens[self.index][1] == ",":
                        self.index += 1  # Move to next row
                    elif self.tokens[self.index][1] == "}":
                        break

            self.index += 1  # Move past '}'
            return [row_count, max_col_count], value_type  # Return array size and type

    def verify_array_size_match(self, declared_sizes, init_sizes, var_name, line, column):
        """Verify that declared array sizes match or exceed initialization sizes"""
        if len(declared_sizes) != len(init_sizes):
            self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): Dimension mismatch for array '{var_name}'."
            )
            return False
            
        for i in range(len(declared_sizes)):
            if declared_sizes[i] is not None and declared_sizes[i] < init_sizes[i]:
                self.errors.append(
                    f"⚠️ Semantic Error at (line {line}, column {column}): Exceeding elements in array '{var_name}', dimension {i+1}. Expected max {declared_sizes[i]}, got {init_sizes[i]}."
                )
                return False
                
        return True
    
    def function_declaration(self):
        return_type = "empty"
        if self.tokens[self.index][1] == "main":
            self.index -= 1
        self.index += 1  # Move past 'task' or 'empty'
        function_name, token_type, line, column = self.tokens[self.index]  # Get function name
        conditions = {"if", "elseif", "while"}

        # Check if function name is already declared in global scope
        if function_name in self.symbol_table["global"]:
            self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): '{function_name}' is already declared."
            )
            # return
        
        # Create a new scope for this function
        self.symbol_table[function_name] = {}

        # Set current scope to function
        self.current_scope = function_name
        self.scope_stack.append(function_name)  # Push function scope

        self.index += 1  # Move to '('
        self.index += 1  # Move inside parameters

        parameters = []  # Store parameter information for function signature

        # Parse parameters
        while self.tokens[self.index][0] != ")":
            param_type, token_type, line, column = self.tokens[self.index]  # Get parameter type
            
            self.index += 1  # Move to parameter name
            param_name, token_type, line, column = self.tokens[self.index]
            
            # Store parameter inside function scope
            self.symbol_table[function_name][param_name] = Symbol(
                name=param_name,
                symbol_type="parameter",
                data_type=param_type,
                line=line,
                column=column
            )

             # Add to parameter list
            parameters.append((param_name, param_type))

            self.index += 1  # Move to ',' or ')'
            if self.tokens[self.index][0] == ",":
                self.index += 1  # Move to next parameter
        
        self.index += 1 # Move past )


        # Parse function body
        if self.tokens[self.index][0] == "{":
            self.index += 1  # Move past '{'
        
            brace_level = 1

            while self.index < len(self.tokens) and brace_level > 0:
                lexeme, token_type, line, column = self.tokens[self.index]
                
                if lexeme == "{":
                    brace_level += 1
                elif lexeme == "}":
                    brace_level -= 1
                    if brace_level == 0:  # End of function
                        break
                
                # Process local variable declarations
                if token_type in self.data_types:
                    self.variable_declaration()
                    continue  # variable_declaration already advances the index

                elif token_type == "fixed":
                    self.fixed_declaration()
                    continue  # fixed_declaration already advances the index
                
                elif token_type == "unit":
                    # Handle unit variable declarations
                    next_token = self.tokens[self.index + 1][0] if self.index + 1 < len(self.tokens) else None
                    next_next_token = self.tokens[self.index + 2][0] if self.index + 2 < len(self.tokens) else None
                    
                    if next_next_token == "{":
                        self.unit_declaration()
                    else:
                        self.unit_variable_declaration()
                    continue

                # Process statements
                elif token_type == "identifier":
                    if self.tokens[self.index + 1][0] == "++" or self.tokens[self.index + 1][0] == "--":
                        # Check if identifier exists in any scope
                        if lexeme not in self.symbol_table[self.current_scope] and lexeme not in self.symbol_table["global"]:
                            self.errors.append(
                                f"⚠️ Semantic Error at (line {line}, column {column}): Undeclared identifier '{lexeme}'"
                            )
                            # Skip to end of statement for error recovery
                            while self.index < len(self.tokens) and self.tokens[self.index][1] != ";":
                                self.index += 1
                            if self.index < len(self.tokens):
                                self.index += 1  # Move past semicolon
                            return
                        else:
                            type_mapping = {
                                        "int": "int_literal",
                                        "decimal": "decimal_literal",
                                        "bool": "bool",
                                        "letter": "letter_literal",
                                        "string": "string_literal"
                            }
                            
                            if lexeme in self.symbol_table.get(self.current_scope, {}):
                                symbol = self.symbol_table[self.current_scope][lexeme]
                            elif lexeme in self.symbol_table.get("global", {}):
                                symbol = self.symbol_table["global"][lexeme]

                        self.index += 1
                        target_type = "int"
                        value_type = type_mapping.get(symbol.data_type)
                        # Perform Type Checking for scalar variables
                        if self.is_type_mismatch(target_type, value_type, lexeme, line, column):
                            # self.errors.append(
                            #     f"Validation Stopped: Data Type {data_type}, Value Type {value_type} at line {line}, column {column}"
                            # )
                            return
                        self.index += 1
                    else:
                        self.validate_id_statement()

                elif token_type == "++" or token_type == "--":
                    target_type = "int"
                    self.index += 1 # Move to identifier
                    
                    lexeme, token_type, line, column = self.tokens[self.index]        

                    # Check if identifier exists in any scope
                    if lexeme not in self.symbol_table[self.current_scope] and lexeme not in self.symbol_table["global"]:
                        self.errors.append(
                            f"⚠️ Semantic Error at (line {line}, column {column}): Undeclared identifier '{lexeme}'"
                        )
                        # Skip to end of statement for error recovery
                        while self.index < len(self.tokens) and self.tokens[self.index][1] != ";":
                            self.index += 1
                        if self.index < len(self.tokens):
                            self.index += 1  # Move past semicolon
                        return
                    else:
                        type_mapping = {
                        "int": "int_literal",
                        "decimal": "decimal_literal",
                        "bool": "bool",
                        "letter": "letter_literal",
                        "string": "string_literal"
                        }

                        if lexeme in self.symbol_table.get(self.current_scope, {}):
                            symbol = self.symbol_table[self.current_scope][lexeme]
                        elif lexeme in self.symbol_table.get("global", {}):
                            symbol = self.symbol_table["global"][lexeme]

                        value_type = type_mapping.get(symbol.data_type)
                        # Perform Type Checking for scalar variables
                        if self.is_type_mismatch(target_type, value_type, lexeme, line, column):
                            # self.errors.append(
                            #     f"Validation Stopped: Data Type {data_type}, Value Type {value_type} at line {line}, column {column}"
                            # )
                            return

                elif token_type in conditions:
                    lexeme, token_type, line, column = self.tokens[self.index]   
                    self.index += 1 # Move past if
                    condition_type = self.validate_expression()
                    if self.tokens[self.index][1] == "{":
                        brace_level += 1
                    type_mapping = {
                        "int_literal": "int",
                        "decimal_literal": "decimal",
                        "letter_literal": "letter",
                        "string_literal": "string",
                        "bool": "bool"
                    }
                    target_type = "bool"
                    if self.is_type_mismatch(target_type, condition_type, lexeme, line, column):
                        return

                elif token_type == "select":
                    self.index += 1  # Move past 'select'
                    brace_level += 1
                    expr_type = self.validate_expression()
                
                elif token_type == "option":
                    self.index += 1  # Move past 'option'
                    expr_type = self.validate_expression()

                elif token_type == "for":
                    self.index += 2  # Move past 'for('
            
                    for_initial = self.validate_expression()

                    type_mapping = {
                        "int_literal": "int",
                        "decimal_literal": "decimal",
                        "letter_literal": "letter",
                        "string_literal": "string",
                        "bool": "bool"
                    }

                    target_type = "int"
                    if self.is_type_mismatch(target_type, for_initial, lexeme, line, column):
                        return
                    
                    



                elif token_type == "ins":
                    if self.tokens[self.index + 1][1] == "identifier":
                        self.index += 1  # Move past 'for'
                        lexeme, token_type, line, column = self.tokens[self.index]
                
                        if token_type == "identifier":
                            # Get variable type from symbol table
                            type_mapping = {
                                "int": "int_literal",
                                "decimal": "decimal_literal",
                                "bool": "bool",
                                "letter": "letter_literal",
                                "string": "string_literal"
                            }

                            symbol = None
                            if lexeme in self.symbol_table.get(self.current_scope, {}):
                                symbol = self.symbol_table[self.current_scope][lexeme]

                            elif lexeme in self.symbol_table.get("global", {}):
                                symbol = self.symbol_table["global"][lexeme]

                            else:
                                self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Undeclared identifier '{lexeme}'")
                                return "error"
                            
                            if symbol.symbol_type == "function" or symbol.symbol_type == "unit_variable":
                                self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): '{lexeme}' Invalid type. Can only be identifier or array")
                                return "error"
                
                elif token_type == "display":
                    self.index += 1  # Move past display
                    
                    while token_type != ")":
                        self.index += 1
                        lexeme, token_type, line, column = self.tokens[self.index]

                        if token_type == "identifier":
                             # Check if identifier exists in any scope
                            if lexeme not in self.symbol_table[self.current_scope] and lexeme not in self.symbol_table["global"]:
                                self.errors.append(
                                    f"⚠️ Semantic Error at (line {line}, column {column}): Undeclared identifier '{lexeme}'"
                                )

                            else:
                                type_mapping = {
                                            "int": "int_literal",
                                            "decimal": "decimal_literal",
                                            "bool": "bool",
                                            "letter": "letter_literal",
                                            "string": "string_literal"
                                }
                                
                                if lexeme in self.symbol_table.get(self.current_scope, {}):
                                    symbol = self.symbol_table[self.current_scope][lexeme]
                                elif lexeme in self.symbol_table.get("global", {}):
                                    symbol = self.symbol_table["global"][lexeme]

                                # Handle array access
                                if symbol.dimension > 0:  # Check if it's an array
                                    if self.tokens[self.index + 1][0] == "[":
                                        self.index += 2  # Move past identifier and first opening bracket
                                        
                                        # Validate that the index is an integer
                                        idx_type = self.validate_expression()
                                        if idx_type != "int_literal":
                                            self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array index must be an integer")
                                            return "error"
                                        
                                        # For 2D arrays, handle the second dimension
                                        if symbol.dimension > 1:
                                            if self.tokens[self.index + 1][0] == "[":
                                                self.index += 1 # Move to 2nd index
                                                idx_type = self.validate_expression()
                                                if idx_type != "int_literal":
                                                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array index must be an integer")
                                                    return "error"
                                            else:
                                                # Error: Array variable used without indexing
                                                self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): 2D Array variable '{lexeme}' missing index")
                                                return "error"
                                        
                                    else:
                                        # Error: Array variable used without indexing
                                        self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array variable '{lexeme}' must have index")
                                        return "error"

                                
                                elif symbol.symbol_type == "function":  # Is a function call
                                    self.index += 1  # Move past function name
                                    if self.tokens[self.index][0] == "(":
                                        self.index += 1  # Move past '('
                                        
                                        # Retrieve expected parameters
                                        expected_params = symbol.value  # List of (param_name, param_type)
                                        received_params = []
                                        
                                        # Handle empty parameter list
                                        if self.tokens[self.index][0] == ")":
                                            self.index += 1  # Move past ')'
                                        else:
                                            # Process parameters
                                            param_count = 0
                                            while self.index < len(self.tokens):
                                                param_type = self.validate_expression(entered_param=True)
                                                received_params.append(param_type)
                                                param_count += 1
                                                
                                                
                                                current_token = self.tokens[self.index][0]
                                                
                                                if current_token == ")":
                                                    #self.index += 1  # Move past ')'
                                                    break
                                                elif current_token == ",":
                                                    self.index += 1  # Move past comma to next parameter
                                                else:
                                                    break
                                        
                                        # Check parameter count
                                        if len(received_params) != len(expected_params):
                                            self.errors.append(
                                                f"⚠️ Semantic Error at (line {line}, column {column}): Function call '{lexeme}' expects {len(expected_params)} argument(s), but got {len(received_params)}."
                                            )
                                            return "error"
                                        
                                        # Check parameter types
                                        for i, ((expected_name, expected_type), received_type) in enumerate(zip(expected_params, received_params)):
                                            expected_mapped_type = type_mapping.get(expected_type, expected_type)
                                            received_mapped_type = received_type  # received_type is already mapped
                                            
                                            # Check if types are compatible (numeric types can be mixed)
                                            if expected_mapped_type != received_mapped_type:
                                                # Special case: allow numeric type compatibility
                                                numeric_types = ["int_literal", "decimal_literal", "bool"]
                                                if not (expected_mapped_type in numeric_types and received_mapped_type in numeric_types):
                                                    self.errors.append(
                                                        f"⚠️ Semantic Error at (line {line}, column {column}): Argument type mismatch in '{lexeme}' at position {i+1}: Expected '{expected_type}', got '{received_type}'."
                                                    )
                                                    return "error"
                                        # Check for semicolon (function calls as statements should end with semicolon)
                                        if self.index < len(self.tokens) and self.tokens[self.index][0] == ";":
                                            self.index += 1  # Move past semicolon
                                            return symbol.data_type  # Return function return type
                                    else:
                                        self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Expected '(argument/s)' after function name '{lexeme}'")
                                        return "error"

                                elif symbol.symbol_type == "unit_variable":
                                    # Get the unit type (stored in symbol's data_type)
                                    unit_type = symbol.data_type
                                    # Move to the dot operator
                                    self.index += 1
                                    if self.tokens[self.index][0] != ".":
                                        self.errors.append(
                                            f"⚠️ Semantic Error at (line {line}, column {column}): Expected '.' after unit variable."
                                        )
                                        return "error"
                                    # Move to the field name (unit member)
                                    self.index += 1
                                    field_name, _, field_line, field_column = self.tokens[self.index]

                                    # Check if the unit type exists in the unit table
                                    if unit_type not in self.unit_table:
                                        self.errors.append(
                                            f"⚠️ Semantic Error at (line {line}, column {column}): Unit type '{unit_type}' is not declared."
                                        )
                                        return "error"
                                    
                                    # Check if the field exists in the unit
                                    unit_fields = self.unit_table[unit_type]
                                    field_type = None

                                    for name, type_ in unit_fields:
                                        if name == field_name:
                                            field_type = type_
                                            break
                                    
                                    if field_type is None:
                                        self.errors.append(
                                            f"⚠️ Semantic Error at (line {field_line}, column {field_column}): Field '{field_name}' not found in unit '{unit_type}'."
                                        )
                                        return "error"
                                    
                                    # Move past the field name
                                    # self.index += 1

                                    type_mapping = {
                                        "int": "int_literal",
                                        "decimal": "decimal_literal",
                                        "bool": "bool",
                                        "letter": "letter_literal",
                                        "string": "string_literal"
                                    }


                elif token_type == "return":
                    self.index += 1  # Move past 'return'
                    expr_type = self.validate_expression()
                
                    # Map literal types to their base types
                    type_mapping = {
                        "int_literal": "int",
                        "decimal_literal": "decimal",
                        "letter_literal": "letter",
                        "string_literal": "string",
                        "bool": "bool"
                    }
                
                    # Convert the expression type to base type if needed
                    return_type = type_mapping.get(expr_type, expr_type)
                    if return_type == "error":
                        return
                
                self.index += 1
                # Store function in global scope with parameters and return type
            
        # Store function in global scope with parameters and correct return type
        self.symbol_table["global"][function_name] = Symbol(
            name=function_name, 
            symbol_type="function", 
            data_type=return_type,  # Will now be the base type like "int" instead of "int_literal"
            value=parameters,  # Store parameters for argument validation
            line=line, 
            column=column
        )
        
        # Reset scope after function declaration
        self.current_scope = self.scope_stack.pop()  # Pop back to previous scope (should be "global")
        

    def validate_id_statement(self):
        lexeme, token_type, line, column = self.tokens[self.index]        

        # Check if identifier exists in any scope
        if lexeme not in self.symbol_table[self.current_scope] and lexeme not in self.symbol_table["global"]:
            self.errors.append(
                f"⚠️ Semantic Error at (line {line}, column {column}): Undeclared identifier '{lexeme}'"
            )
            # Skip to end of statement for error recovery
            while self.index < len(self.tokens) and self.tokens[self.index][1] != ";":
                self.index += 1
            return
        else:
            type_mapping = {
                        "int": "int_literal",
                        "decimal": "decimal_literal",
                        "bool": "bool",
                        "letter": "letter_literal",
                        "string": "string_literal"
            }
            
            if lexeme in self.symbol_table.get(self.current_scope, {}):
                symbol = self.symbol_table[self.current_scope][lexeme]
            elif lexeme in self.symbol_table.get("global", {}):
                symbol = self.symbol_table["global"][lexeme]

            # Handle array access
            if symbol.dimension > 0:  # Check if it's an array
                if self.tokens[self.index + 1][0] == "[":
                    self.index += 2  # Move past identifier and first opening bracket
                    
                    # Validate that the index is an integer
                    idx_type = self.validate_expression()
                    if idx_type != "int_literal" and idx_type != "user_input":
                        self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array index must be an integer")
                        return "error"
                    
                    # For 2D arrays, handle the second dimension
                    if symbol.dimension > 1 and self.tokens[self.index + 1][0] == "[":
                        self.index += 1 # Move to 2nd index
                        idx_type = self.validate_expression()
                        if idx_type != "int_literal" and idx_type != "user_input":
                            self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array index must be an integer")
                            return "error"
                        else:
                            # Error: Array variable used without indexing
                            if self.tokens[self.index][0] != "]":
                                self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Missing closing bracket ']'")
                                return "error"
                            self.index += 1  # Move past closing bracket
                    else:
                        # Check for closing bracket for 1D array
                        if self.tokens[self.index][0] != "]":
                            self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Missing closing bracket ']'")
                            return "error"
                        self.index += 1  # Move past closing bracket
                    
                    # Return the type of the array element
                    target_type = symbol.data_type
                else:
                    # Error: Array variable used without indexing
                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array variable '{lexeme}' must have index")
                    return "error"

                # Set target_type for assignment check
                target_type = symbol.data_type
                value_type = type_mapping.get(target_type, target_type)

            elif symbol.symbol_type == "fixed_declaration":
                # Error: Array variable used without indexing
                self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): '{lexeme}' Cannot assign value to fixed variable")
                return "error"
            
            elif symbol.symbol_type == "function":  # Is a function call
                self.index += 1  # Move past function name
                if self.tokens[self.index][0] == "(":
                    self.index += 1  # Move past '('
                    
                    # Retrieve expected parameters
                    expected_params = symbol.value  # List of (param_name, param_type)
                    received_params = []
                    
                    # Handle empty parameter list
                    if self.tokens[self.index][0] == ")":
                        self.index += 1  # Move past ')'
                    else:
                        # Process parameters
                        param_count = 0
                        while self.index < len(self.tokens):
                            param_type = self.validate_expression(entered_param=True)
                            received_params.append(param_type)
                            param_count += 1
                            
                            
                            current_token = self.tokens[self.index][0]
                            
                            if current_token == ")":
                                break
                            elif current_token == ",":
                                self.index += 1  # Move past comma to next parameter
                            else:
                                break
                    
                    # Check parameter count
                    if len(received_params) != len(expected_params):
                        self.errors.append(
                            f"⚠️ Semantic Error at (line {line}, column {column}): Function call '{lexeme}' expects {len(expected_params)} argument(s), but got {len(received_params)}."
                        )
                        return "error"
                    
                    # Check parameter types
                    for i, ((expected_name, expected_type), received_type) in enumerate(zip(expected_params, received_params)):
                        expected_mapped_type = type_mapping.get(expected_type, expected_type)
                        received_mapped_type = received_type  # received_type is already mapped
                        
                        # Check if types are compatible (numeric types can be mixed)
                        if expected_mapped_type != received_mapped_type:
                            # Special case: allow numeric type compatibility
                            numeric_types = ["int_literal", "decimal_literal", "bool"]
                            if not (expected_mapped_type in numeric_types and received_mapped_type in numeric_types):
                                self.errors.append(
                                    f"⚠️ Semantic Error at (line {line}, column {column}): Argument type mismatch in '{lexeme}' at position {i+1}: Expected '{expected_type}', got '{received_type}'."
                                )
                                return "error"
                    # Check for semicolon (function calls as statements should end with semicolon)
                    if self.index < len(self.tokens) and self.tokens[self.index][0] == ";":
                        self.index += 1  # Move past semicolon
                        return symbol.data_type  # Return function return type
                else:
                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Expected '(argument/s)' after function name '{lexeme}'")
                    return "error"

            elif symbol.symbol_type == "unit_variable":
                # Get the unit type (stored in symbol's data_type)
                unit_type = symbol.data_type
                # Move to the dot operator
                self.index += 1
                if self.tokens[self.index][0] != ".":
                    self.errors.append(
                        f"⚠️ Semantic Error at (line {line}, column {column}): Expected '.' after unit variable."
                    )
                    return "error"
                # Move to the field name (unit member)
                self.index += 1
                field_name, _, field_line, field_column = self.tokens[self.index]

                # Check if the unit type exists in the unit table
                if unit_type not in self.unit_table:
                    self.errors.append(
                        f"⚠️ Semantic Error at (line {line}, column {column}): Unit type '{unit_type}' is not declared."
                    )
                    return "error"
                
                # Check if the field exists in the unit
                unit_fields = self.unit_table[unit_type]
                field_type = None

                for name, type_ in unit_fields:
                    if name == field_name:
                        field_type = type_
                        break
                
                if field_type is None:
                    self.errors.append(
                        f"⚠️ Semantic Error at (line {field_line}, column {field_column}): Field '{field_name}' not found in unit '{unit_type}'."
                    )
                    return "error"
                
                # Move past the field name
                self.index += 1
                
                # Set target_type to the field's type, not the unit type
                target_type = field_type
                
            else:
                # Regular variable (not an array)
                target_type = symbol.data_type
            
            assign_op = {'+=', '-=', '*=', '/=', '%=', '**='}

            if symbol.symbol_type != "function":
                if self.tokens[self.index][0] == "=":
                    self.index += 1 # Move to value after =
                    value_type = self.validate_expression()

                    # For unit variables, we need special handling
                    if symbol.symbol_type == "unit_variable":
                        # We've already validated that the field exists and set target_type to field_type
                        if self.is_unit_field_type_mismatch(target_type, value_type, field_name, field_line, field_column):
                            return
                    else:
                        # Perform Type Checking for scalar variables
                        if self.is_type_mismatch(target_type, value_type, lexeme, line, column):
                            return
                elif self.tokens[self.index][0] in assign_op:
                    op = self.tokens[self.index][0]
                    if target_type == "letter" and op != "+=":
                        self.errors.append(
                        f"⚠️ Semantic Error at (line {line}, column {column}): Cannot use '{op}' on letter_literal."
                        )
                        return "error"
                    
                    self.index += 1 # Move to value after op
                    value_type = self.validate_expression()
                    
                    # For unit variables, we need special handling
                    if symbol.symbol_type == "unit_variable":
                        # Check if the operation is valid for the field type
                        if target_type == "string" and op != "+=":
                            self.errors.append(
                                f"⚠️ Semantic Error at (line {field_line}, column {field_column}): Cannot use '{op}' on string field '{field_name}'."
                            )
                            return "error"
                        elif target_type == "letter" and op != "+=":
                            self.errors.append(
                                f"⚠️ Semantic Error at (line {field_line}, column {field_column}): Cannot use '{op}' on letter field '{field_name}'."
                            )
                            return "error"
                        
                        # We've already validated that the field exists
                        if self.is_unit_field_type_mismatch(target_type, value_type, field_name, field_line, field_column):
                            return
                    else:
                        # Perform Type Checking for scalar variables
                        if self.is_type_mismatch(target_type, value_type, lexeme, line, column):
                            return

    # Add this new function to check type mismatches for unit fields specifically
    def is_unit_field_type_mismatch(self, data_type, value_type, field_name, line, column):
        """Check if there's a type mismatch for unit field assignments"""
        # Special case: user_input is compatible with all types
        if value_type == "user_input":
            return False  # No mismatch - user_input can be assigned to any type
        
        # Map value_type to expected base types
        type_mapping = {
            "int_literal": "int",
            "decimal_literal": "decimal",
            "letter_literal": "letter",
            "string_literal": "string",
            "bool": "bool"
        }
        
        # Get the base type for the value type
        base_value_type = type_mapping.get(value_type, value_type)
        
        # Check for type compatibility
        if data_type != base_value_type:
            # Special case: allow numeric type compatibility (int, decimal)
            numeric_types = ["int", "decimal"]
            if not (data_type in numeric_types and base_value_type in numeric_types):
                self.errors.append(
                    f"⚠️ Semantic Error at (line {line}, column {column}): Type mismatch for unit field '{field_name}':"
                    f" Expected '{data_type}', got '{value_type}'."
                )
                return True  # There is a mismatch
        return False  # No mismatch

        
    def validate_expression(self, entered_param = False):
        """
        Parses and validates an expression using operator precedence, returning the final type.
        """
        start_index = self.index
        
        # Token types categorized
        operands = {"int_literal", "decimal_literal", "true", "false", "letter_literal", "string_literal", "identifier"}
        operators = {"+", "-", "*", "/", "%", "**", "!", "==", "!=", "<", ">", "<=", ">=", "||", "&&", "ins", "notin", "is", "isnot"}
        
        # Add built-in functions
        built_in_functions = {"reads"}

        # Operator precedence levels (lower number = higher precedence)
        precedence = {
            "!": 1,           # Logical NOT (unary)
            "**": 2,          # Exponentiation
            "*": 3, "/": 3, "%": 3,  # Multiplicative
            "+": 4, "-": 4,   # Additive
            "<": 5, ">": 5, "<=": 5, ">=": 5,  # Relational
            "==": 6, "!=": 6, # Equality
            "ins": 7, "notin": 7, "is": 7, "isnot": 7,  # Membership/identity
            "&&": 8,          # Logical AND
            "||": 9           # Logical OR
        }
        
        # Define result types for different operations
        boolean_operators = {"==", "!=", "<", ">", "<=", ">=", "&&", "||", "ins", "notin", "is", "isnot", "!"}
        
        # Define type compatibility for binary operators
        type_compatibility = {
            "+": {
                ("int_literal", "int_literal"): "int_literal",
                ("int_literal", "decimal_literal"): "int_literal",
                ("decimal_literal", "int_literal"): "int_literal",
                ("decimal_literal", "decimal_literal"): "int_literal",
                ("string_literal", "string_literal"): "string_literal",
                ("bool", "bool"): "int_literal",
                ("bool", "int_literal"): "int_literal",
                ("int_literal", "bool"): "int_literal",
                ("bool", "decimal_literal"): "int_literal",
                ("decimal_literal", "bool"): "int_literal",
                # Add user_input compatibility
                ("user_input", "int_literal"): "int_literal",
                ("int_literal", "user_input"): "int_literal",
                ("user_input", "decimal_literal"): "decimal_literal",
                ("decimal_literal", "user_input"): "decimal_literal",
                ("user_input", "string_literal"): "string_literal",
                ("string_literal", "user_input"): "string_literal",
                ("user_input", "bool"): "int_literal",
                ("bool", "user_input"): "int_literal",
                ("user_input", "user_input"): "user_input",
            },
            "-": {
                ("int_literal", "int_literal"): "int_literal",
                ("int_literal", "decimal_literal"): "int_literal",
                ("decimal_literal", "int_literal"): "int_literal",
                ("decimal_literal", "decimal_literal"): "int_literal",
                ("bool", "bool"): "int_literal",
                ("bool", "int_literal"): "int_literal",
                ("int_literal", "bool"): "int_literal",
                ("bool", "decimal_literal"): "int_literal",
                ("decimal_literal", "bool"): "int_literal",
                # Add user_input compatibility
                ("user_input", "int_literal"): "int_literal",
                ("int_literal", "user_input"): "int_literal",
                ("user_input", "decimal_literal"): "decimal_literal",
                ("decimal_literal", "user_input"): "decimal_literal",
                ("user_input", "bool"): "int_literal",
                ("bool", "user_input"): "int_literal",
                ("user_input", "user_input"): "user_input",
            },
            "*": {
                ("int_literal", "int_literal"): "int_literal",
                ("int_literal", "decimal_literal"): "int_literal",
                ("decimal_literal", "int_literal"): "int_literal",
                ("decimal_literal", "decimal_literal"): "int_literal",
                ("bool", "bool"): "int_literal",
                ("bool", "int_literal"): "int_literal",
                ("int_literal", "bool"): "int_literal",
                ("bool", "decimal_literal"): "int_literal",
                ("decimal_literal", "bool"): "int_literal",
                # Add user_input compatibility
                ("user_input", "int_literal"): "int_literal",
                ("int_literal", "user_input"): "int_literal",
                ("user_input", "decimal_literal"): "decimal_literal",
                ("decimal_literal", "user_input"): "decimal_literal",
                ("user_input", "bool"): "int_literal",
                ("bool", "user_input"): "int_literal",
                ("user_input", "user_input"): "user_input",
            },
            "/": {
                ("int_literal", "int_literal"): "int_literal", # Division always produces decimal
                ("int_literal", "decimal_literal"): "int_literal",
                ("decimal_literal", "int_literal"): "int_literal",
                ("decimal_literal", "decimal_literal"): "int_literal",
                ("bool", "bool"): "int_literal",
                ("bool", "int_literal"): "int_literal",
                ("int_literal", "bool"): "int_literal",
                ("bool", "decimal_literal"): "int_literal",
                ("decimal_literal", "bool"): "int_literal",
                # Add user_input compatibility
                ("user_input", "int_literal"): "int_literal",
                ("int_literal", "user_input"): "int_literal",
                ("user_input", "decimal_literal"): "decimal_literal",
                ("decimal_literal", "user_input"): "decimal_literal",
                ("user_input", "bool"): "int_literal",
                ("bool", "user_input"): "int_literal",
                ("user_input", "user_input"): "user_input",
            },
            "%": {
                ("int_literal", "int_literal"): "int_literal",
                ("int_literal", "decimal_literal"): "int_literal",
                ("decimal_literal", "int_literal"): "int_literal",
                ("decimal_literal", "decimal_literal"): "int_literal",
                ("bool", "bool"): "int_literal",
                ("bool", "int_literal"): "int_literal",
                ("int_literal", "bool"): "int_literal",
                ("bool", "decimal_literal"): "int_literal",
                ("decimal_literal", "bool"): "int_literal",
                # Add user_input compatibility
                ("user_input", "int_literal"): "int_literal",
                ("int_literal", "user_input"): "int_literal",
                ("user_input", "decimal_literal"): "decimal_literal",
                ("decimal_literal", "user_input"): "decimal_literal",
                ("user_input", "bool"): "int_literal",
                ("bool", "user_input"): "int_literal",
                ("user_input", "user_input"): "user_input",
            },
            "**": {
                ("int_literal", "int_literal"): "int_literal",  # Power operation might produce a non-integer
                ("int_literal", "decimal_literal"): "int_literal",
                ("decimal_literal", "int_literal"): "int_literal",
                ("decimal_literal", "decimal_literal"): "int_literal",
                ("bool", "bool"): "int_literal",
                ("bool", "int_literal"): "int_literal",
                ("int_literal", "bool"): "int_literal",
                ("bool", "decimal_literal"): "int_literal",
                ("decimal_literal", "bool"): "int_literal",
                # Add user_input compatibility
                ("user_input", "int_literal"): "int_literal",
                ("int_literal", "user_input"): "int_literal",
                ("user_input", "decimal_literal"): "decimal_literal",
                ("decimal_literal", "user_input"): "decimal_literal",
                ("user_input", "bool"): "int_literal",
                ("bool", "user_input"): "int_literal",
                ("user_input", "user_input"): "user_input",
            },
        }
        
        def evaluate_operation(op, left_type, right_type=None):
            """Evaluate the type resulting from applying operator op to operand(s)"""
            if op in boolean_operators:
                # For boolean operations with user_input, always return bool
                if left_type == "user_input" or (right_type and right_type == "user_input"):
                    return "bool"
                # Boolean operators always return bool
                if op == "!":  # Unary NOT
                    if left_type in ["bool", "int_literal", "decimal_literal", "user_input"]:
                        return "bool"
                    else:
                        #self.errors.append("E1")
                        return "error"
                        
                # Handle comparison operators
                elif op in ["==", "!="]:
                    # Equality operators can compare same types or numeric types
                    if left_type == right_type or (left_type in ["int_literal", "decimal_literal", "bool", "user_input", "string_literal", "letter_literal"] and 
                                                right_type in ["int_literal", "decimal_literal", "bool", "user_input", "string_literal", "letter_literal"]):
                        return "bool"
                    else:
                        #self.errors.append("E2")
                        return "error"
                        
                elif op in ["<", ">", "<=", ">="]:
                    # Relational operators require numeric types
                    if left_type in ["int_literal", "decimal_literal", "bool", "user_input"] and right_type in ["int_literal", "decimal_literal", "bool", "user_input"]:
                        return "bool"
                    else:
                        #self.errors.append("E3")
                        return "error"
                        
                elif op in ["&&", "||"]:
                    # Logical operators require boolean types
                    if left_type in ["bool", "user_input"] and right_type in ["bool", "user_input"]:
                        return "bool"
                    else:
                        #self.errors.append("E4")
                        return "error"
                        
                elif op in ["ins", "notin", "is", "isnot"]:
                    # Membership and identity operators
                    return "bool"
            else:
                    # Arithmetic operators
                if op in type_compatibility:
                    # Special handling for user_input
                    if left_type == "user_input" or right_type == "user_input":
                        if left_type == "user_input" and right_type == "user_input":
                            return "user_input"
                        elif left_type == "user_input":
                            return right_type
                        else: # right_type == "user_input"
                            return left_type
                    
                    result_type = type_compatibility[op].get((left_type, right_type))
                    return result_type if result_type else "error"
                
            self.errors.append("Unsupported Operation")
            return "error"  # Unsupported operation

        # Stack-based evaluation
        operand_stack = []   # Stack to hold operand types
        operator_stack = []  # Stack to hold operators
        
        # Helper function to apply operators
        def apply_operator():
            if not operator_stack:
                return
                
            op = operator_stack.pop()
            
            if op == "!":  # Unary operator
                if not operand_stack:
                    self.errors.append("⚠️ Semantic Error: Missing operand for '!'")
                    return "error"
                    
                operand = operand_stack.pop()
                result = evaluate_operation(op, operand)
                
                if result == "error":
                    self.errors.append(f"⚠️ Semantic Error at (line {line}): Cannot apply '!' to {operand}")
                    return "error"
                    
                operand_stack.append(result)
            else:  # Binary operator
                if len(operand_stack) < 2:
                    self.errors.append(f"⚠️ Semantic Error at (line {line}): Not enough operands for operator '{op}'")
                    return "error"
                    
                right = operand_stack.pop()
                left = operand_stack.pop()
                result = evaluate_operation(op, left, right)
                
                if result == "error":
                    self.errors.append(f"⚠️ Semantic Error at (line {line}): Type Mismatch '{op}' not supported between instances of {left} and {right}")
                    return "error"
                    
                operand_stack.append(result)
        
        # Special case: empty expression
        if self.index >= len(self.tokens) or self.tokens[self.index][1] in {";", ","}:
            # If this is part of a parameter list, allow it
            if entered_param is True:
                return "string_literal"  # Default return for empty param lists
            return "error"
        
        # Process tokens
        while self.index < len(self.tokens):
            lexeme, token_type, line, column = self.tokens[self.index]
            
            # Special handling for built-in reads() function
            if lexeme == "reads":
                self.index += 1  # Move past 'reads'
                if self.index < len(self.tokens) and self.tokens[self.index][0] == "(":
                    self.index += 1  # Move past '('
                    
                    # Check if there are any arguments (should be none for reads)
                    if self.tokens[self.index][0] != ")":
                        # Process parameters if any (which might be an error for reads)
                        while self.index < len(self.tokens):
                            param_type = self.validate_expression(entered_param=True)
                            if self.tokens[self.index][0] == ")":
                                break
                            elif self.tokens[self.index][0] == ",":
                                self.index += 1  # Move past comma
                            else:
                                break
                    
                    # Move past closing parenthesis
                    if self.index < len(self.tokens) and self.tokens[self.index][0] == ")":
                        self.index += 1
                    
                    # Add user_input type to the operand stack
                    operand_stack.append("user_input")
                    continue
                else:
                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Expected '(' after 'reads'")
                    return "error"
                
            elif token_type == "identifier":
                # Get variable type from symbol table
                type_mapping = {
                    "int": "int_literal",
                    "decimal": "decimal_literal",
                    "bool": "bool",
                    "letter": "letter_literal",
                    "string": "string_literal"
                }

                symbol = None
                if lexeme in self.symbol_table.get(self.current_scope, {}): # Check if lexeme exist
                    symbol = self.symbol_table[self.current_scope][lexeme]

                elif lexeme in self.symbol_table.get("global", {}):
                    symbol = self.symbol_table["global"][lexeme]

                else:
                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Undeclared identifier '{lexeme}'")
                    # Skip to end of statement for error recovery
                    while self.index < len(self.tokens) and self.tokens[self.index][1] != ";":
                        self.index += 1
                    if self.index < len(self.tokens):
                        self.index += 1  # Move past semicolon
                    return "error"
                
                if self.index + 1 < len(self.tokens) and self.tokens[self.index + 1][0] == "[":
                    # Check if variable is actually an array
                    if symbol.dimension == 0 and symbol.data_type != "string":  # Not an array
                        self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Variable '{lexeme}' is not an array")
                        return "error"

                # Handle array access - FIX HERE
                # Add in the array access handling section:
                if symbol.dimension > 0 or symbol.data_type == "string":  # Check if it's an array OR a string
                    # First increment past the identifier
                    self.index += 1
                    
                    # Check if next token is a bracket
                    if self.index < len(self.tokens) and self.tokens[self.index][0] == "[":
                        self.index += 1  # Move past first opening bracket
                        
                        # Validate that the index is an integer
                        idx_type = self.validate_expression()
                        if idx_type != "int_literal" and idx_type != "user_input":
                            self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array index must be an integer")
                            return "error"
                        
                        # Check and consume the closing bracket
                        if self.index < len(self.tokens) and self.tokens[self.index][0] == "]":
                            self.index += 1  # Move past the closing bracket
                        else:
                            self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Missing closing bracket ']'")
                            return "error"
                        
                        # For 2D arrays, handle the second dimension
                        if symbol.dimension > 1 and self.index < len(self.tokens):
                            if self.tokens[self.index][0] == "[":
                                self.index += 1  # Move past opening bracket
                                idx_type = self.validate_expression()
                                if idx_type != "int_literal" and idx_type != "user_input":
                                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array index must be an integer")
                                    return "error"
                                
                                # Check and consume the second closing bracket
                                if self.index < len(self.tokens) and self.tokens[self.index][0] == "]":
                                    self.index += 1  # Move past the second closing bracket
                                else:
                                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Missing closing bracket ']'")
                                    return "error"
                            else:
                                # Error: 2D Array variable used without second index
                                if symbol.dimension > 1:  # Only report error if it's actually a 2D array
                                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): 2D Array variable '{lexeme}' missing second index")
                                    return "error"
                        
                        # Important change: Push the correct type to stack
                        # For strings, indexing should return letter_literal
                        if symbol.data_type == "string":
                            operand_stack.append("letter_literal")
                        else:
                            operand_stack.append(type_mapping.get(symbol.data_type, symbol.data_type))
                    else:
                        # Error: Array variable used without indexing
                        self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Array variable '{lexeme}' must have index")
                        return "error"
                
                elif symbol.symbol_type == "function":  # Is a function call
                    self.index += 1  # Move past function name
                    if self.tokens[self.index][0] == "(":
                        self.index += 1  # Move past '('
                        
                        # Retrieve expected parameters
                        expected_params = symbol.value  # List of (param_name, param_type)
                        received_params = []
                        
                        # Handle empty parameter list
                        if self.tokens[self.index][0] == ")":
                            self.index += 1  # Move past ')'
                            operand_stack.append(type_mapping.get(symbol.data_type, symbol.data_type))
                        else:
                            # Process parameters
                            param_count = 0
                            while self.index < len(self.tokens):
                                param_type = self.validate_expression(entered_param=True)
                                received_params.append(param_type)
                                param_count += 1
                                
                                current_token = self.tokens[self.index][0]
                                
                                if current_token == ")":
                                    self.index += 1  # Move past ')'
                                    break
                                elif current_token == ",":
                                    self.index += 1  # Move past comma to next parameter
                                else:
                                    break
                        
                        # Check parameter count
                        if len(received_params) != len(expected_params):
                            self.errors.append(
                                f"⚠️ Semantic Error at (line {line}, column {column}): Function call '{lexeme}' expects {len(expected_params)} argument(s), but got {len(received_params)}."
                            )
                            return "error"
                        
                        # Check parameter types
                        for i, ((expected_name, expected_type), received_type) in enumerate(zip(expected_params, received_params)):
                            expected_mapped_type = type_mapping.get(expected_type, expected_type)
                            received_mapped_type = received_type  # received_type is already mapped
                            
                            # Check if types are compatible (numeric types can be mixed)
                            if expected_mapped_type != received_mapped_type and received_mapped_type != "user_input":
                                # Special case: allow numeric type compatibility
                                numeric_types = ["int_literal", "decimal_literal", "bool"]
                                if not (expected_mapped_type in numeric_types and received_mapped_type in numeric_types):
                                    self.errors.append(
                                        f"⚠️ Semantic Error at (line {line}, column {column}): Argument type mismatch in '{lexeme}' at position {i+1}: Expected '{expected_type}', got '{received_type}'."
                                    )
                                    return "error"

                        operand_stack.append(type_mapping.get(symbol.data_type, symbol.data_type))
                    else:
                        self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Expected '(argument/s)' after function name '{lexeme}'")
                        return "error"

                elif symbol.symbol_type == "unit_variable":
                    # Get the unit type (stored in symbol's data_type)
                    unit_type = symbol.data_type
                    # Move to the dot operator
                    self.index += 1
                    if self.index < len(self.tokens) and self.tokens[self.index][0] != ".":
                        self.errors.append(
                            f"⚠️ Semantic Error at (line {line}, column {column}): Expected '.' after unit variable."
                        )
                        return "error"
                    # Move to the field name (unit member)
                    self.index += 1
                    field_name, _, field_line, field_column = self.tokens[self.index]

                    # Check if the unit type exists in the unit table
                    if unit_type not in self.unit_table:
                        self.errors.append(
                            f"⚠️ Semantic Error at (line {line}, column {column}): Unit type '{unit_type}' is not declared."
                        )
                        return "error"
                    
                    # Check if the field exists in the unit
                    unit_fields = self.unit_table[unit_type]
                    field_type = None

                    for name, type_ in unit_fields:
                        if name == field_name:
                            field_type = type_
                            break
                    
                    if field_type is None:
                        self.errors.append(
                            f"⚠️ Semantic Error at (line {field_line}, column {field_column}): Field '{field_name}' not found in unit '{unit_type}'."
                        )
                        return "error"
                    
                    # Move past the field name
                    self.index += 1

                    type_mapping = {
                        "int": "int_literal",
                        "decimal": "decimal_literal",
                        "bool": "bool",
                        "letter": "letter_literal",
                        "string": "string_literal"
                    }

                    operand_stack.append(type_mapping.get(field_type, field_type))
                else:
                    # Regular variable (not an array)
                    operand_stack.append(type_mapping.get(symbol.data_type, symbol.data_type))
                    self.index += 1  # Move past identifier
                
            
            elif token_type in {"int_literal", "decimal_literal", "true", "false", "letter_literal", "string_literal"}:
                # Convert true/false to bool for consistency
                if token_type in {"true", "false"}:
                    operand_stack.append("bool")
                else:
                    operand_stack.append(token_type)
                self.index += 1  # Move past the literal
            
            elif token_type == "(":
                operator_stack.append(token_type)
                self.index += 1  # Move past opening parenthesis
            
            elif token_type == ")":
                # Process all operators until the matching opening parenthesis
                while operator_stack and operator_stack[-1] != "(":
                    apply_operator()
                
                # Remove the opening parenthesis
                if operator_stack and operator_stack[-1] == "(":
                    operator_stack.pop()
                    self.index += 1  # Move past closing parenthesis
                elif entered_param is True:
                    break
                else:
                    self.errors.append(f"⚠️ Semantic Error at (line {line}, column {column}): Mismatched parentheses")
                    return "error"
            
            elif token_type == "]":
                # Process all operators until the matching opening bracket or parenthesis
                while operator_stack and operator_stack[-1] not in ["(", "["]:
                    apply_operator()
                
                # This should be handled by the array access logic, but just in case
                if not entered_param:
                    break

            elif lexeme in operators:
                # Special handling for unary operators
                if lexeme == "!" and (self.index == start_index or self.tokens[self.index - 1][1] in operators or self.tokens[self.index - 1][1] == "("):
                    # Unary NOT
                    while operator_stack and operator_stack[-1] != "(" and precedence.get(operator_stack[-1], 999) <= precedence[lexeme]:
                        apply_operator()
                    operator_stack.append(lexeme)
                else:
                    # Binary operators
                    while (operator_stack and operator_stack[-1] != "(" and 
                        precedence.get(operator_stack[-1], 999) <= precedence.get(lexeme, 999)):
                        apply_operator()
                    operator_stack.append(lexeme)
                self.index += 1  # Move past the operator
            
            elif token_type in {";", ",", "{"}:
                # End of expression reached
                break
            
            else:
                # Unrecognized token - move past it to avoid infinite loop
                self.index += 1
        
        # Apply all remaining operators
        while operator_stack:
            op = operator_stack[-1]
            if op == "(":
                operator_stack.pop()  # Just pop the unmatched parenthesis instead of reporting error
                continue
            apply_operator()
        
        # Final result type should be on top of the operand stack
        if not operand_stack:
            self.errors.append("⚠️ Expression evaluation error occurred")
            return "error"
        
        return operand_stack[-1]


    def print_symbol_table(self):
        print("\n========== Symbol Table ==========")
        for scope, symbols in self.symbol_table.items():
            print(f"\nScope: {scope}")
            for name, symbol in symbols.items():
                print(f"  {symbol}")

        print("\n========== Unit Table ==========")
        for unit_name, fields in self.unit_table.items():
            print(f"\nUnit: {unit_name}")
            for field_name, field_type in fields:
                print(f"  - {field_name}: {field_type}")


    def print_errors(self):
        if not self.errors:
            print("\n✅ No Semantic Errors Found.")
        else:
            print("\n⚠️ Semantic Errors:")
            for error in self.errors:
                print(error)