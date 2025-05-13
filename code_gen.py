class CodeGenerator:
    def __init__(self):
        self.output_code = []
        self.indentation = 0
        self.variable_types = {}  # Keep track of variable types
        self.struct_definitions = {}  # Track struct definitions
        self.current_scope = "global"  # Track current function scope, default to global
        self.debug_mode = True  # Enable debug output
        
    def add_line(self, line):
        self.output_code.append('    ' * self.indentation + line)
    
    def debug(self, message):
        """Add debug output if debug mode is enabled"""
        if self.debug_mode:
            print(f"CODE_GEN DEBUG: {message}")
    
    def generate_code(self, tokens):
        """Generate executable code from tokens"""
        self.output_code = []
        self.variable_types = {"global": {}}  # Initialize global scope
        
        # Print token information for debugging
        if self.debug_mode:
            self.debug(f"Processing {len(tokens)} tokens")
            for i, token in enumerate(tokens[:20]):  # Print first 20 tokens for debugging
                self.debug(f"Token {i}: {token}")
        
        self._process_tokens(tokens)
        return '\n'.join(self.output_code)
    
    def _process_tokens(self, tokens):
        # Add necessary imports/headers for the output code
        self.add_line("#include <stdio.h>")
        self.add_line("#include <stdlib.h>")
        self.add_line("#include <string.h>")
        self.add_line("#include <stdbool.h>")  # Added for bool support
        self.add_line("#ifdef _WIN32")
        self.add_line("#include <windows.h>")  # Added Sleep support
        self.add_line("#else")
        self.add_line("#include <unistd.h>")
        self.add_line("#endif")
        self.add_line("#include <ctype.h>")
        self.add_line("")
        
        # Add helper functions for string handling
        self._add_helper_functions()

        # Add helper functions for input
        self._add_gui_input_functions()
        
        # Process global declarations first
        i = 0
        while i < len(tokens):
            # Skip comments
            if i < len(tokens) - 1 and tokens[i][0] == '/' and tokens[i+1][0] == '/':
                # Single line comment
                self.debug("Processing single line comment")
                comment_text = "// "
                i += 2  # Skip past //
                while i < len(tokens) and tokens[i][0] != '\n':
                    comment_text += tokens[i][0] + " "
                    i += 1
                self.add_line(comment_text)
                continue
            
            if i < len(tokens) - 1 and tokens[i][0] == '/' and tokens[i+1][0] == '*':
                # Multi-line comment
                self.debug("Processing multi-line comment")
                comment_text = ["/*"]
                i += 2  # Skip past /*
                
                while i < len(tokens) - 1 and not (tokens[i][0] == '*' and tokens[i+1][0] == '/'):
                    comment_text.append(tokens[i][0])
                    i += 1
                
                if i < len(tokens) - 1:
                    i += 2  # Skip past */
                    comment_text.append("*/")
                
                self.add_line(" ".join(comment_text))
                continue

            # Check for unit (struct) declarations
            if tokens[i][0] == 'unit' and i + 2 < len(tokens) and tokens[i+1][1] == 'identifier' and tokens[i+2][0] == '{':
                self.debug(f"Found unit declaration at index {i}")
                i = self._process_unit_declaration(tokens, i)
                continue
            
            # Check for global variable declarations
            if self._is_variable_declaration(tokens, i) and self.current_scope == "global":
                i = self._process_variable_declaration(tokens, i)
            elif self._is_function_declaration(tokens, i):
                i = self._process_function(tokens, i)
            elif self._is_unit_declaration(tokens, i):
                i = self._process_unit_declaration(tokens, i)            
            else:
                i += 1
        
    def _add_helper_functions(self):
        # Helper function for display
        self.add_line("// Helper function for display")
        self.add_line("void display(const char* message) {")
        self.indentation += 1
        self.add_line("printf(\"%s\\n\", message);") # For Palindrome
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for displaying integers
        self.add_line("// Helper function for displaying integers")
        self.add_line("void display_int(int value) {")
        self.indentation += 1
        self.add_line("printf(\"%d\\n\", value);")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for displaying doubles
        self.add_line("// Helper function for displaying doubles")
        self.add_line("void display_double(double value) {")
        self.indentation += 1
        self.add_line("printf(\"%f\\n\", value);")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")

        # Helper function for displaying char
        self.add_line("// Helper function for displaying char")
        self.add_line("void display_char(char value) {")
        self.indentation += 1
        self.add_line("printf(\"%c\\n\", value);")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for integer to string conversion
        self.add_line("// Helper function for integer to string conversion")
        self.add_line("char* int_to_str(int value) {")
        self.indentation += 1
        self.add_line("char* buffer = malloc(20);")
        self.add_line("sprintf(buffer, \"%d\", value);")
        self.add_line("return buffer;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for string concatenation
        self.add_line("// Helper function for string concatenation")
        self.add_line("char* concat_str(const char* str1, const char* str2) {")
        self.indentation += 1
        self.add_line("char* result = malloc(strlen(str1) + strlen(str2) + 1);")
        self.add_line("strcpy(result, str1);")
        self.add_line("strcat(result, str2);")
        self.add_line("return result;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for string and int concatenation
        self.add_line("// Helper function for string concatenation with integers")
        self.add_line("char* concat_str_int(const char* str, int value) {")
        self.indentation += 1
        self.add_line("char* int_str = int_to_str(value);")
        self.add_line("char* result = concat_str(str, int_str);")
        self.add_line("free(int_str);")
        self.add_line("return result;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")

    def _add_gui_input_functions(self):
        """Add helper functions for GUI-based user input"""
        # We don't need the volatile flags anymore since we're using direct I/O
        
        # Helper function for reading integer input with error handling
        self.add_line("// Helper function for reading integer input")
        self.add_line("int read_int() {")
        self.indentation += 1
        self.add_line("int value = 0;")
        self.add_line("int valid_input = 0;")
        self.add_line("char buffer[1024];")
        self.add_line("")
        self.add_line("while (!valid_input) {")
        self.indentation += 1
        self.add_line("printf(\"_waiting_for_input|\\n\");")
        self.add_line("fflush(stdout);")
        self.add_line("")
        self.add_line("if (fgets(buffer, sizeof(buffer), stdin) == NULL) {")
        self.indentation += 1
        self.add_line("printf(\"...\\n\");")
        self.add_line("continue;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")

        self.add_line("// Handle ~ as negative sign")
        self.add_line("if (buffer[0] == '~') {")
        self.indentation += 1
        self.add_line("buffer[0] = '-';")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")

        self.add_line("// Check if input is a valid integer")
        self.add_line("char* endptr;")
        self.add_line("value = (int)strtol(buffer, &endptr, 10);")
        self.add_line("if (*endptr != '\\n' && *endptr != '\\0') {")
        self.indentation += 1
        self.add_line("printf(\"Invalid input. Please enter a valid integer.\\n\");")
        self.add_line("fflush(stdout);")
        self.indentation -= 1
        self.add_line("} else {")
        self.indentation += 1
        self.add_line("valid_input = 1;")
        self.indentation -= 1
        self.add_line("}")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("return value;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for reading decimal input with error handling
        self.add_line("// Helper function for reading double input")
        self.add_line("double read_decimal() {")
        self.indentation += 1
        self.add_line("double value = 0.0;")
        self.add_line("int valid_input = 0;")
        self.add_line("char buffer[1024];")
        self.add_line("")
        self.add_line("while (!valid_input) {")
        self.indentation += 1
        self.add_line("printf(\"_waiting_for_input|\\n\");")
        self.add_line("fflush(stdout);")
        self.add_line("")
        self.add_line("if (fgets(buffer, sizeof(buffer), stdin) == NULL) {")
        self.indentation += 1
        self.add_line("printf(\"...\\n\");")
        self.add_line("continue;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")

        self.add_line("// Handle ~ as negative sign")
        self.add_line("if (buffer[0] == '~') {")
        self.indentation += 1
        self.add_line("buffer[0] = '-';")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")

        self.add_line("// Check if input is a valid decimal")
        self.add_line("char* endptr;")
        self.add_line("value = strtof(buffer, &endptr);")
        self.add_line("if (*endptr != '\\n' && *endptr != '\\0') {")
        self.indentation += 1
        self.add_line("printf(\"Invalid input. Please enter a valid decimal number.\\n\");")
        self.add_line("fflush(stdout);")
        self.indentation -= 1
        self.add_line("} else {")
        self.indentation += 1
        self.add_line("valid_input = 1;")
        self.indentation -= 1
        self.add_line("}")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("return value;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for reading character input with error handling
        self.add_line("// Helper function for reading character input")
        self.add_line("char read_letter() {")
        self.indentation += 1
        self.add_line("char value = '\\0';")
        self.add_line("int valid_input = 0;")
        self.add_line("char buffer[1024];")
        self.add_line("")
        self.add_line("while (!valid_input) {")
        self.indentation += 1
        self.add_line("printf(\"_waiting_for_input|\\n\");")
        self.add_line("fflush(stdout);")
        self.add_line("")
        self.add_line("if (fgets(buffer, sizeof(buffer), stdin) == NULL) {")
        self.indentation += 1
        self.add_line("printf(\"...\\n\");")
        self.add_line("continue;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("// Ignore whitespace and check if only one character was entered")
        self.add_line("size_t len = strlen(buffer);")
        self.add_line("int char_count = 0;")
        self.add_line("for (size_t i = 0; i < len; i++) {")
        self.indentation += 1
        self.add_line("if (buffer[i] != ' ' && buffer[i] != '\\t' && buffer[i] != '\\n') {")
        self.indentation += 1
        self.add_line("value = buffer[i];")
        self.add_line("char_count++;")
        self.indentation -= 1
        self.add_line("}")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("if (char_count != 1) {")
        self.indentation += 1
        self.add_line("printf(\"Invalid input. Please enter a single character.\\n\");")
        self.add_line("fflush(stdout);")
        self.indentation -= 1
        self.add_line("} else {")
        self.indentation += 1
        self.add_line("valid_input = 1;")
        self.indentation -= 1
        self.add_line("}")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("return value;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Helper function for reading string input with error handling
        self.add_line("// Helper function for reading string input")
        self.add_line("char* read_string() {")
        self.indentation += 1
        self.add_line("char buffer[1024];")
        self.add_line("int valid_input = 0;")
        self.add_line("")
        self.add_line("while (!valid_input) {")
        self.indentation += 1
        self.add_line("printf(\"_waiting_for_input|\\n\");")
        self.add_line("fflush(stdout);")
        self.add_line("")
        self.add_line("if (fgets(buffer, sizeof(buffer), stdin) == NULL) {")
        self.indentation += 1
        self.add_line("printf(\"...\\n\");")
        self.add_line("continue;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("// Remove trailing newline if present")
        self.add_line("size_t len = strlen(buffer);")
        self.add_line("if (len > 0 && buffer[len-1] == '\\n') {")
        self.indentation += 1
        self.add_line("buffer[len-1] = '\\0';")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("// Check if string is not empty (just spaces)")
        self.add_line("int is_empty = 1;")
        self.add_line("for (size_t i = 0; i < strlen(buffer); i++) {")
        self.indentation += 1
        self.add_line("if (buffer[i] != ' ' && buffer[i] != '\\t') {")
        self.indentation += 1
        self.add_line("is_empty = 0;")
        self.add_line("break;")
        self.indentation -= 1
        self.add_line("}")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("if (is_empty) {")
        self.indentation += 1
        self.add_line("printf(\"Input cannot be empty. Please enter a string.\\n\");")
        self.add_line("fflush(stdout);")
        self.indentation -= 1
        self.add_line("} else {")
        self.indentation += 1
        self.add_line("valid_input = 1;")
        self.indentation -= 1
        self.add_line("}")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("return strdup(buffer);")  # Create a copy of the input
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")

        # Helper function for reading boolean input with error handling
        self.add_line("// Helper function for reading boolean input")
        self.add_line("bool read_bool() {")
        self.indentation += 1
        self.add_line("char buffer[1024];")
        self.add_line("int valid_input = 0;")
        self.add_line("bool value = false;")
        self.add_line("")
        self.add_line("while (!valid_input) {")
        self.indentation += 1
        self.add_line("printf(\"_waiting_for_input|Enter a boolean (true/false, yes/no, 1/0): \\n\");")
        self.add_line("fflush(stdout);")
        self.add_line("")
        self.add_line("if (fgets(buffer, sizeof(buffer), stdin) == NULL) {")
        self.indentation += 1
        self.add_line("printf(\"...\\n\");")
        self.add_line("continue;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("// Remove trailing newline and whitespace")
        self.add_line("size_t len = strlen(buffer);")
        self.add_line("if (len > 0 && buffer[len-1] == '\\n') {")
        self.indentation += 1
        self.add_line("buffer[len-1] = '\\0';")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("// Convert to lowercase for easier comparison")
        self.add_line("for (size_t i = 0; i < strlen(buffer); i++) {")
        self.indentation += 1
        self.add_line("buffer[i] = tolower(buffer[i]);")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("// Check for valid boolean values")
        self.add_line("if (strcmp(buffer, \"true\") == 0 || strcmp(buffer, \"1\") == 0 || ")
        self.add_line("    strcmp(buffer, \"yes\") == 0 || strcmp(buffer, \"y\") == 0) {")
        self.indentation += 1
        self.add_line("value = true;")
        self.add_line("valid_input = 1;")
        self.indentation -= 1
        self.add_line("} else if (strcmp(buffer, \"false\") == 0 || strcmp(buffer, \"0\") == 0 || ")
        self.add_line("           strcmp(buffer, \"no\") == 0 || strcmp(buffer, \"n\") == 0) {")
        self.indentation += 1
        self.add_line("value = false;")
        self.add_line("valid_input = 1;")
        self.indentation -= 1
        self.add_line("} else {")
        self.indentation += 1
        self.add_line("printf(\"Invalid input. Please enter true/false, yes/no, or 1/0.\\n\");")
        self.add_line("fflush(stdout);")
        self.indentation -= 1
        self.add_line("}")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        self.add_line("return value;")
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
    
    def _is_function_declaration(self, tokens, index):
        # Check if this is the start of a function declaration            
        if index >= len(tokens):
            return False
            
        token1 = tokens[index]
        
        # Case 1: main function
        if token1[0] == 'main':
            if index + 1 < len(tokens) and tokens[index + 1][0] == '(':
                self.debug("Main function detected: main()")
                return True
        # Case 2: check for valid return types followed by identifier and parenthesis
        elif token1[0] in ['int', 'decimal', 'letter', 'string', 'bool', 'void', 'empty', 'task']:
            if index + 2 < len(tokens) and tokens[index+1][1] == 'identifier' and tokens[index + 2][0] == '(':
                self.debug(f"Function detected: {token1[0]} {tokens[index+1][0]}()")
                return True
                
        return False
        
    def _is_unit_declaration(self, tokens, index):
        if index + 2 < len(tokens):
            if tokens[index][0] == 'unit' and tokens[index+1][1] == 'identifier' and tokens[index+2][0] == '{':
                return True
        return False

    def _process_unit_declaration(self, tokens, index):
        # Get the struct name
        struct_name = tokens[index+1][0]
        self.debug(f"Processing unit/struct declaration: {struct_name}")
        
        # Find opening brace
        brace_index = index + 2
        if tokens[brace_index][0] != '{':
            self.debug("Missing opening brace for unit/struct declaration")
            return index + 1
        
        # Find closing brace
        end_index = self._find_matching_brace(tokens, brace_index)
        if end_index == -1:
            self.debug("Missing closing brace for unit/struct declaration")
            return index + 1
        
        # Generate struct declaration
        self.add_line(f"struct {struct_name} {{")
        self.indentation += 1
        
        # Initialize this struct in our tracking dict
        self.struct_definitions[struct_name] = {}
        
        # Process struct fields
        i = brace_index + 1
        while i < end_index:
            if self._is_variable_declaration(tokens, i):
                # Extract field type and name
                field_type = tokens[i][0]
                mapped_field_type = self._map_datatype(field_type)
                
                if i + 1 < end_index and tokens[i+1][1] == 'identifier':
                    field_name = tokens[i+1][0]
                    self.add_line(f"{mapped_field_type} {field_name};")
                    
                    # Store the field type in our struct definition tracking
                    self.struct_definitions[struct_name][field_name] = field_type
                    
                    # Skip past field declaration
                    i += 2
                    while i < end_index and tokens[i][0] != ';':
                        i += 1
                    i += 1  # Skip past semicolon
                else:
                    i += 1
            else:
                i += 1
        
        self.indentation -= 1
        self.add_line(f"}};")
        self.add_line("")
        
        return end_index + 1
    
    def _process_function(self, tokens, index):
        # Track the function return type
        return_type = "int"  # Default return type
        
        # Handle different function declaration formats
        if tokens[index][0] == 'task':
            is_task_function = True
            func_name = tokens[index + 1][0]
            param_start = index + 3  # Skip 'task', function name, and opening paren
            return_type = "int"  # Default for task
            brace_index = index + 3
        elif tokens[index][0] == 'main':
            return_type = "int"
            func_name = "main"
            brace_index = index + 2
            param_start = index + 2  # Start of parameters for main
        elif tokens[index][0] in ['int', 'decimal', 'letter', 'string', 'bool', 'void', 'empty']:
            # Standard function with return type
            return_type = self._map_datatype(tokens[index][0])
            func_name = tokens[index + 1][0]
            brace_index = index + 3  # Skip past return type, name, and opening parenthesis
            param_start = index + 3  # Start of parameters
        else:
            # Default case, shouldn't normally be reached
            return_type = "int"
            func_name = tokens[index][0]
            brace_index = index + 2
            param_start = index + 2
        
        self.debug(f"Processing function: {return_type} {func_name}()")
        
        # Create new scope for this function
        self.current_scope = func_name
        self.variable_types[self.current_scope] = {}
        
        # Parse parameters if any
        param_list = []
        i = param_start
        current_param = []
        
        # Skip to opening brace, collecting parameters along the way
        while i < len(tokens) and tokens[i][0] != '{':
            # Skip closing parenthesis
            if tokens[i][0] == ')':
                # Add the last parameter if we have tokens
                if current_param:
                    param_list.append(" ".join(current_param))
                    current_param = []
                i += 1
                continue
                
            # Skip commas between parameters
            if tokens[i][0] == ',':
                if current_param:
                    param_list.append(" ".join(current_param))
                    current_param = []
                i += 1
                continue
                
            # Add token to current parameter
            if tokens[i][0] != '(':  # Skip opening parenthesis
                current_param.append(tokens[i][0])
            i += 1
        
        # Process parameters - convert to C-style declarations
        processed_params = []
        for param in param_list:
            parts = param.split()
            if len(parts) >= 2:
                param_type = self._map_datatype(parts[0])
                param_name = parts[1]
                processed_params.append(f"{param_type} {param_name}")
                
                # Add parameter to variable types for this scope
                self.variable_types[self.current_scope][param_name] = param_type
        
        # Map 'empty' to 'void' for C output
        if return_type == 'empty':
            return_type = 'void'
        
        # Generate the function declaration
        if func_name == 'main':
            self.add_line(f"int main() {{")
        else:
            # Use the processed parameters
            self.add_line(f"{return_type} {func_name}({', '.join(processed_params)}) {{")
        
        self.indentation += 1
        
        # Find the opening brace of function body
        while brace_index < len(tokens) and tokens[brace_index][0] != '{':
            brace_index += 1
        
        if brace_index >= len(tokens):
            # Error handling if no opening brace
            self.debug(f"Missing opening brace for function {func_name}")
            self.add_line("// Error: Missing opening brace")
            self.indentation -= 1
            self.add_line("}")
            return index + 1
        
        # Find the closing brace of function body
        end_index = self._find_matching_brace(tokens, brace_index)
        
        if end_index == -1:
            # Error handling if no matching brace
            self.debug(f"Missing closing brace for function {func_name}")
            self.add_line("// Error: Missing closing brace")
            self.indentation -= 1
            self.add_line("}")
            return len(tokens)
        
        self.debug(f"Function body from index {brace_index} to {end_index}")
        
        # Process function body
        i = brace_index + 1  # Start after opening brace
        while i < end_index:
            # Check for return statement
            if i < len(tokens) and tokens[i][0] == 'return':
                return_expr = []
                i += 1  # Skip past 'return'
                while i < len(tokens) and tokens[i][0] != ';':
                    return_expr.append(tokens[i][0])
                    i += 1
                # Format the return expression
                formatted_expr = self._format_expression(return_expr)
                self.add_line(f"return {formatted_expr};")
                i += 1  # Skip past semicolon
                continue
                
            # Check for comments
            if i < len(tokens) - 1 and tokens[i][0] == '/' and tokens[i+1][0] == '/':
                # Single line comment
                comment_text = "// "
                i += 2  # Skip past //
                while i < len(tokens) and tokens[i][0] != '\n':
                    comment_text += tokens[i][0] + " "
                    i += 1
                self.add_line(comment_text)
                continue
            
            if i < len(tokens) - 1 and tokens[i][0] == '/' and tokens[i+1][0] == '*':
                # Multi-line comment
                comment_text = ["/*"]
                i += 2  # Skip past /*
                
                while i < len(tokens) - 1 and not (tokens[i][0] == '*' and tokens[i+1][0] == '/'):
                    comment_text.append(tokens[i][0])
                    i += 1
                
                if i < len(tokens) - 1:
                    i += 2  # Skip past */
                    comment_text.append("*/")
                
                self.add_line(" ".join(comment_text))
                continue
            
            # Process statements inside function
            old_i = i
            i = self._process_statement(tokens, i, end_index)
            if i == old_i:  # Prevent infinite loop
                self.debug(f"Statement processing didn't advance at index {i}, token: {tokens[i] if i < len(tokens) else 'END'}")
                i += 1
        
        # Add return for main function if there isn't one already
        if func_name == 'main' and return_type == 'int':
            self.add_line("return 0;")
        
        self.indentation -= 1
        self.add_line("}")
        self.add_line("")
        
        # Clear current scope
        self.current_scope = "global"
        
        self.debug(f"Finished processing function {func_name}, returning to index {end_index + 1}")
        return end_index + 1
    
    def _find_matching_brace(self, tokens, start_index):
        # Start from the opening brace
        if start_index >= len(tokens) or tokens[start_index][0] != '{':
            self.debug(f"No opening brace at index {start_index}")
            return -1
        
        # Find matching closing brace
        brace_count = 1
        i = start_index + 1
        
        while i < len(tokens) and brace_count > 0:
            if tokens[i][0] == '{':
                brace_count += 1
            elif tokens[i][0] == '}':
                brace_count -= 1
            i += 1
        
        if brace_count != 0:
            self.debug(f"Unmatched braces starting at index {start_index}")
            return -1
        
        return i - 1
    
    def _process_statement(self, tokens, index, end_index):
        if index >= end_index:
            return index
        
        token = tokens[index]
        token_info = f"{token[0]} ({token[1]})" if len(token) >= 2 else str(token)
        self.debug(f"Processing statement at index {index}: {token_info}")
        
        # Variable declarations
        if self._is_variable_declaration(tokens, index):
            self.debug(f"Found variable declaration at index {index}")
            return self._process_variable_declaration(tokens, index)
        
        # Increment/decrement operations
        elif self._is_increment_decrement(tokens, index):
            self.debug(f"Found increment/decrement operation at index {index}")
            return self._process_increment_decrement(tokens, index)
        
        # Unit/struct declarations
        elif self._is_unit_declaration(tokens, index):
            self.debug(f"Found unit declaration at index {index}")
            return self._process_unit_declaration(tokens, index)
        
        # Assignment statements
        elif self._is_assignment(tokens, index):
            self.debug(f"Found assignment at index {index}")
            return self._process_assignment(tokens, index)
        
        # Display statement
        elif self._is_display_statement(tokens, index):
            self.debug(f"Found display statement at index {index}")
            return self._process_display(tokens, index)
        
        # If-elseif-else statements
        elif self._is_if_statement(tokens, index):
            self.debug(f"Found if statement at index {index}")
            return self._process_if_statement(tokens, index, end_index)
        
        # Select statements (switch)
        elif self._is_select_statement(tokens, index):
            self.debug(f"Found select statement at index {index}")
            return self._process_select_statement(tokens, index, end_index)
        
        # Loop statements (while, for, try-while)
        elif self._is_loop_statement(tokens, index):
            self.debug(f"Found loop statement at index {index}")
            return self._process_loop_statement(tokens, index, end_index)
            
        # Function calls
        elif self._is_function_call(tokens, index):
            self.debug(f"Found function call at index {index}")
            return self._process_function_call(tokens, index)
        
        # Skip unknown tokens or semicolons
        self.debug(f"Unknown statement type at index {index}: {token_info}")
        return index + 1
    
    def _map_datatype(self, datatype):
        """Map custom language datatypes to C datatypes"""
        mapping = {
            'int': 'int',
            'decimal': 'double',
            'letter': 'char',
            'string': 'char*',
            'bool': 'bool',
            'empty': 'void',
            'void': 'void'
        }
        
        return mapping.get(datatype, datatype)  # Return original if not in mapping
    
    def _get_default_value(self, datatype):
        """Get default value for a datatype"""
        default_values = {
            'int': '0',
            'decimal': '0.0',
            'double': '0.0',
            'letter': "' '",  # Empty char
            'char': "''",    # Empty char
            'string': "\"\"", # Empty string
            'char*': "\"\"", # Empty string
            'bool': 'false'
        }
        return default_values.get(datatype, '0')
    
    
    def _is_increment_decrement(self, tokens, index):
        self.inc_dec = ['++', '--']
        if index < len(tokens):
            # Check for fixed (const) modifier
            if tokens[index][1] == 'identifier' and tokens[index + 1][0] in self.inc_dec:
                return True
        return False
    
    
    def _process_increment_decrement(self, tokens, index):
        """Process increment and decrement operations (++ and --)"""
        variable = tokens[index][0]
        operator = tokens[index + 1][0]
        
        self.debug(f"Processing {operator} for variable {variable}")
        
        # Map operation to C syntax
        if operator == '++':
            self.add_line(f"{variable}++;")
        elif operator == '--':
            self.add_line(f"{variable}--;")
        
        # Skip past operator and find semicolon
        i = index + 2
        while i < len(tokens) and tokens[i][0] != ';':
            i += 1
            
        return i + 1  # Skip past semicolon
    
    def _is_variable_declaration(self, tokens, index):
        """Check if tokens starting at index represent a variable declaration"""
        if index < len(tokens):
            # Check if it's a built-in data type
            datatypes = ['int', 'string', 'double', 'decimal', 'letter', 'char', 'bool', 'empty']
            if tokens[index][0] in datatypes:
                return True
                
            # Check if it's a unit (struct) declaration
            if index + 1 < len(tokens):
                if tokens[index][0] == 'unit' and tokens[index+1][1] == 'identifier':
                    return True
        return False
    
    def _process_variable_declaration(self, tokens, index):
        is_const = False
        start_index = index
        
        # Check for fixed (const) modifier
        if tokens[index][0] == 'fixed':
            is_const = True
            index += 1
        
        # Check if it's a struct instantiation
        if tokens[index][0] == 'unit' and index + 1 < len(tokens):
            self.debug(f"Processing unit instance at index {index}: {tokens[index+1][0]}")
            struct_type = tokens[index+1][0]
            index += 2  # Skip 'unit' and struct type
            
            # Process struct variable(s)
            i = index
            variables = []
            
            while i < len(tokens) and tokens[i][0] != ';':
                self.debug(f"Processing token at i={i}: {tokens[i][0]}")
                
                if tokens[i][1] == 'identifier':
                    var_name = tokens[i][0]
                    self.debug(f"Found variable name: {var_name}")
                    
                    # Add to our variable tracking
                    if self.current_scope not in self.variable_types:
                        self.variable_types[self.current_scope] = {}
                    self.variable_types[self.current_scope][var_name] = f"struct_{struct_type}"
                    
                    # Check for initialization
                    if i + 1 < len(tokens) and tokens[i + 1][0] == '=':
                        self.debug(f"Found initialization for {var_name}")
                        i += 2  # Skip past '='
                        
                        # Initialize with struct literal
                        if i < len(tokens) and tokens[i][0] == '{':
                            self.debug(f"Found struct literal initialization")
                            i += 1  # Skip '{'
                            init_values = []
                            
                            # Collect all values until closing brace
                            brace_level = 1
                            while i < len(tokens) and brace_level > 0:
                                if tokens[i][0] == '{':
                                    brace_level += 1
                                elif tokens[i][0] == '}':
                                    brace_level -= 1
                                    if brace_level == 0:
                                        break
                                    
                                if tokens[i][0] == ',':
                                    i += 1  # Skip comma
                                    continue
                                    
                                # Collect the value expression
                                expr_tokens = []
                                while i < len(tokens) and tokens[i][0] != ',' and tokens[i][0] != '}':
                                    expr_tokens.append(tokens[i][0])
                                    i += 1
                                    
                                if expr_tokens:
                                    init_values.append(self._format_expression(expr_tokens))
                            
                            # Skip closing brace
                            if i < len(tokens) and tokens[i][0] == '}':
                                i += 1
                            
                            # Format the struct initialization with proper C syntax
                            variables.append(f"{var_name} = (struct {struct_type}){{" + ", ".join(init_values) + "}")
                        else:
                            # Handle other initialization forms if needed
                            self.debug("No struct literal found after =, skipping")
                            variables.append(var_name)
                            i += 1
                    else:
                        # Default initialization for struct
                        self.debug(f"No initialization for {var_name}")
                        variables.append(var_name)
                        i += 1
                    
                    # Move past comma if present
                    if i < len(tokens) and tokens[i][0] == ',':
                        self.debug("Found comma, skipping")
                        i += 1
                else:
                    self.debug(f"Skipping non-identifier token: {tokens[i][0]}")
                    i += 1
                    
                # Safety check to prevent infinite loop
                if i >= len(tokens):
                    self.debug("Reached end of tokens")
                    break
            
            # Build the complete declaration
            declaration = f"struct {struct_type} " + ", ".join(variables)
            self.debug(f"Generated struct declaration: {declaration}")
            self.add_line(f"{declaration};")
            
            # Skip past the semicolon
            while i < len(tokens) and tokens[i][0] != ';':
                i += 1
                
            # Safety check to ensure we return a valid index
            if i < len(tokens):
                return i + 1  # Skip past semicolon
            else:
                return len(tokens)
                


        # Standard variable declaration (existing code)
        datatype = tokens[index][0]
        mapped_datatype = self._map_datatype(datatype)
        self.debug(f"Processing variable declaration of type {mapped_datatype}")
        

        # Build the declaration string
        declaration = f"{'' if not is_const else 'const '}{mapped_datatype}"
        if mapped_datatype == "empty":
            declaration = "void"
        if datatype == "string" and tokens[index + 2][0] == '[':
            datatype = "string_arr"
            
        declaration += " "
        variables = []
        
        i = index + 1
        while i < len(tokens) and tokens[i][0] != ';':
            if tokens[i][1] == 'identifier':
                var_name = tokens[i][0]
                
                # Add to our variable tracking
                if self.current_scope:
                    self.variable_types[self.current_scope][var_name] = datatype
                
                # Check for array declaration
                if i + 1 < len(tokens) and tokens[i + 1][0] == '[':
                    # Array declaration
                    array_dims = []
                    i += 1  # Skip to [
                    
                    # Process each dimension
                    while i < len(tokens) and tokens[i][0] == '[':
                        i += 1  # Skip [
                        dim_size = ""
                        while i < len(tokens) and tokens[i][0] != ']':
                            dim_size += tokens[i][0]
                            i += 1
                        if i < len(tokens):  # Skip ]
                            i += 1
                        array_dims.append(dim_size)
                    
                    # Format array declaration
                    var_decl = var_name
                    for dim in array_dims:
                        var_decl += f"[{dim}]"
                    
                    # Default initialization for arrays
                    if i < len(tokens) and tokens[i][0] == '=':
                        i += 1  # Skip =
                        # Handle array initialization
                        if tokens[i][0] == '{':
                            i += 1  # Skip first {
                            init_values = []
                            nested_level = 1
                            current_group = []
                            
                            # Handle nested arrays
                            while i < len(tokens) and nested_level > 0:
                                if tokens[i][0] == '{':
                                    nested_level += 1
                                    if nested_level == 2:  # Starting a new inner array
                                        current_group = []
                                    i += 1
                                elif tokens[i][0] == '}':
                                    nested_level -= 1
                                    if nested_level == 1:  # Ending an inner array
                                        init_values.append(f"{{{', '.join(current_group)}}}")
                                    elif nested_level == 0:  # End of entire array
                                        i += 1
                                        break
                                    i += 1
                                elif tokens[i][0] == ',':
                                    i += 1  # Skip comma
                                else:
                                    if nested_level == 2:  # In an inner array
                                        current_group.append(tokens[i][0])
                                    elif nested_level == 1 and len(array_dims) == 1:  # Single dimension array
                                        init_values.append(tokens[i][0])
                                    i += 1
                            
                            # Create the initialization string
                            if len(array_dims) > 1:  # Multi-dimensional array
                                var_decl += f" = {{{', '.join(init_values)}}}"
                            else:  # Single dimension
                                var_decl += f" = {{{', '.join(init_values)}}}"
                        else:
                            # Single value initialization (not typical for arrays)
                            init_value = self._get_default_value(datatype)
                            var_decl += f" = {{{init_value}}}"
                    else:
                        # Default initialization for arrays with appropriate default values
                        default_value = self._get_default_value(datatype)
                        # Create a list of default values based on array dimensions
                        if len(array_dims) == 1 and array_dims[0].isdigit():
                            size = int(array_dims[0])
                            default_values = ', '.join([default_value] * size)
                            var_decl += f" = {{{default_values}}}"
                        elif len(array_dims) == 2 and array_dims[0].isdigit() and array_dims[1].isdigit():
                            # Handle 2D arrays with proper initialization
                            rows = int(array_dims[0])
                            cols = int(array_dims[1])
                            inner_arrays = []
                            for _ in range(rows):
                                inner_arrays.append(f"{{{', '.join([default_value] * cols)}}}")
                            var_decl += f" = {{{', '.join(inner_arrays)}}}"
                        else:
                            # If dimension is not a simple number, initialize with single default value
                            var_decl += f" = {{{default_value}}}"
                    
                    variables.append(var_decl)
                    
                    # If we hit a comma, we need to move past it
                    if i < len(tokens) and tokens[i][0] == ',':
                        i += 1
                    
                # Check for initialization
                elif i + 1 < len(tokens) and tokens[i + 1][0] == '=':
                    i += 2  # Skip past '='
                    
                    # Check if initialization is a function call
                    if i < len(tokens) and tokens[i][1] == 'identifier' and i + 1 < len(tokens) and tokens[i + 1][0] == '(':
                        # This is a function call initialization
                        func_name = tokens[i][0]
                        i += 1  # Move past function name
                        
                        # Process the function call arguments
                        paren_level = 0
                        args = []
                        current_arg = []
                        
                        while i < len(tokens) and tokens[i][0] != ';':
                            if tokens[i][0] == '(':
                                paren_level += 1
                                if paren_level == 1:  # Skip the opening parenthesis of the main function call
                                    i += 1
                                    continue
                                else:
                                    current_arg.append(tokens[i][0])
                            elif tokens[i][0] == ')':
                                paren_level -= 1
                                if paren_level == 0:  # End of function call
                                    if current_arg:
                                        args.append(self._format_expression(current_arg))
                                    i += 1
                                    break
                                else:
                                    current_arg.append(tokens[i][0])
                            elif tokens[i][0] == ',' and paren_level == 1:
                                # Argument separator at the top level
                                if current_arg:
                                    args.append(self._format_expression(current_arg))
                                    current_arg = []
                            else:
                                current_arg.append(tokens[i][0])
                            
                            i += 1
                        
                        # Format the function call
                        func_call = f"{func_name}({', '.join(args)})"
                        variables.append(f"{var_name} = {func_call}")
                    else:
                        # Standard expression initialization
                        expr_tokens = []
                        while i < len(tokens) and tokens[i][0] != ',' and tokens[i][0] != ';':
                            expr_tokens.append(tokens[i][0])
                            i += 1
                        
                        value = self._format_expression(expr_tokens)
                        variables.append(f"{var_name} = {value}")
                    
                    # If we hit a comma, we need to move past it
                    if i < len(tokens) and tokens[i][0] == ',':
                        i += 1
                else:
                    # Auto-initialize with appropriate default value based on data type
                    default_value = self._get_default_value(datatype)
                    variables.append(f"{var_name} = {default_value}")
                    i += 1
                    
                    # If we hit a comma, we need to move past it
                    if i < len(tokens) and tokens[i][0] == ',':
                        i += 1
            else:
                i += 1
        
        declaration += ", ".join(variables)
        self.add_line(f"{declaration};")
        
        # Skip past the semicolon
        return i + 1
    
    def _is_assignment(self, tokens, index):
        self.assignment_op = ['+=', '-=', '*=', '/=', '%=', '=']
        if index + 2 < len(tokens):
            # Check for simple variable assignment
            if tokens[index][1] == 'identifier' and tokens[index + 1][0] in self.assignment_op:
                return True
                
            # Check for array assignment
            if tokens[index][1] == 'identifier' and tokens[index + 1][0] == '[':
                # Find the closing bracket(s)
                j = index + 2
                brackets = 1
                while j < len(tokens) and brackets > 0:
                    if tokens[j][0] == '[':
                        brackets += 1
                    elif tokens[j][0] == ']':
                        brackets -= 1
                    j += 1
                    
                # Check if next token after closing bracket is '='
                if j < len(tokens) and tokens[j][0] in self.assignment_op:
                    return True
                    
            # Check for struct member assignment
            if tokens[index][1] == 'identifier' and tokens[index + 1][0] == '.' and index + 3 < len(tokens):
                if tokens[index + 3][0] in self.assignment_op:
                    return True
        return False
    
    def _process_assignment(self, tokens, index):
        variable = tokens[index][0]
        
        # Helper function to check variable type in current scope or global scope
        def get_variable_type(var_name):
            # Check current scope first
            if var_name in self.variable_types.get(self.current_scope, {}):
                return self.variable_types[self.current_scope][var_name]
            # Then check global scope
            elif var_name in self.variable_types.get("global", {}):
                return self.variable_types["global"][var_name]
            # Not found in either scope
            return "unknown"
        
        var_type = get_variable_type(variable)
        array_indices = []
        assignment_op = '='  # Default
        
        i = index + 1

        # Handle struct member access
        if i < len(tokens) and tokens[i][0] == '.':
            struct_member = tokens[i+1][0]
            i += 2  # Skip '.' and member name
            
            # Get the assignment operator
            if i < len(tokens):
                assignment_op = tokens[i][0]
                i += 1  # Move past assignment operator
            
            # Determine the struct type and find its definition
            struct_type = var_type.replace("struct_", "")
            member_type = None
            
            # Look up the member type from our struct definitions
            if struct_type in self.struct_definitions and struct_member in self.struct_definitions[struct_type]:
                member_type = self.struct_definitions[struct_type][struct_member]
                self.debug(f"Found member type for {struct_type}.{struct_member}: {member_type}")
            else:
                self.debug(f"Could not find member type for {struct_type}.{struct_member}")
                # Default to string if we can't determine the type
                member_type = "string"
            
            # --- Handle struct member assignment with reads() ---
            if i < len(tokens) and tokens[i][0] == 'reads' and tokens[i+1][0] == '(' and tokens[i+2][0] == ')':
                self.add_line('printf("\\n");')  # Line for newline before input
                
                # Handle based on member type
                if member_type == "int":
                    self.add_line(f"{variable}.{struct_member} = read_int();")
                elif member_type == "double" or member_type == "decimal":
                    self.add_line(f"{variable}.{struct_member} = read_decimal();")
                elif member_type == "char" or member_type == "letter":
                    self.add_line(f"{variable}.{struct_member} = read_letter();")
                elif member_type == "bool":
                    self.add_line(f"{variable}.{struct_member} = read_bool();")
                else:
                    self.add_line(f"{variable}.{struct_member} = read_string();")
                
                # Skip past reads() and semicolon
                i += 3
                while i < len(tokens) and tokens[i][0] != ';':
                    i += 1
                return i + 1  # Skip past semicolon
            
            # --- Regular struct member assignment ---
            expr_tokens = []
            while i < len(tokens) and tokens[i][0] != ';':
                expr_tokens.append(tokens[i][0])
                i += 1
            
            expr_str = self._format_expression(expr_tokens)
            self.add_line(f"{variable}.{struct_member} {assignment_op} {expr_str};")
            
            return i + 1  # Skip past semicolon


        if i < len(tokens) and tokens[i][0] == '[':
            # Process array indices
            while i < len(tokens) and tokens[i][0] == '[':
                i += 1  # Skip [
                index_expr = []
                while i < len(tokens) and tokens[i][0] != ']':
                    index_expr.append(tokens[i][0])
                    i += 1
                i += 1  # Skip ]
                array_indices.append(self._format_expression(index_expr))
            
            # Get the assignment operator after array indices
            if i < len(tokens):
                assignment_op = tokens[i][0]
                i += 1  # Move past assignment operator
        else:
            if i < len(tokens):
                assignment_op = tokens[i][0]
                i += 1  # Move past assignment operator

        # --- ENHANCED BLOCK: Handle reads() with global scope support ---
        if i < len(tokens) and tokens[i][0] == 'reads' and tokens[i+1][0] == '(' and tokens[i+2][0] == ')':
            # Create array access or normal variable
            array_access = variable
            for idx in array_indices:
                array_access += f"[{idx}]"

            self.add_line('printf("\\n");')  # Line for newline before input

            # Handle based on variable type from either scope
            var_type = get_variable_type(variable)
            self.debug(f"Using variable type '{var_type}' for reads() assignment to {variable}")
            
            if var_type == 'int':
                self.add_line(f"{array_access} = read_int();")
            elif var_type == 'double' or var_type == 'decimal':
                self.add_line(f"{array_access} = read_decimal();")
            elif var_type == 'char' or var_type == 'letter':
                self.add_line(f"{array_access} = read_letter();")
            elif var_type == 'string':
                self.add_line(f"{array_access} = read_string();")
            elif var_type == 'bool':
                self.add_line(f"{array_access} = read_bool();")
            else:
                self.add_line(f"{array_access} = read_string();  // Unknown type, using default")
                self.debug(f"Warning: Using default string reader for unknown type '{var_type}' of {variable}")
            
            # Skip past reads() and semicolon
            i += 3
            while i < len(tokens) and tokens[i][0] != ';':
                i += 1
            return i + 1  # Skip past semicolon

        # --- STANDARD EXPRESSION ASSIGNMENT ---
        expr_tokens = []
        while i < len(tokens) and tokens[i][0] != ';':
            expr_tokens.append(tokens[i][0])
            i += 1
        
        expr_str = self._format_expression(expr_tokens)

        if array_indices:
            array_access = variable
            for idx in array_indices:
                array_access += f"[{idx}]"
            self.add_line(f"{array_access} {assignment_op} {expr_str};")
        else:
            self.add_line(f"{variable} {assignment_op} {expr_str};")

        return i + 1  # Skip past semicolon

    
    def _format_expression(self, expr_tokens):
        """Format an expression from its tokens, handling operators properly"""
        if not expr_tokens:
            return ""
            
        # Replace custom operators
        result = []
        i = 0
        while i < len(expr_tokens):
            token = expr_tokens[i]
            
            # Replace 'is' with '==' and 'isnot' with '!='
            if token == 'is':
                result.append('==')
            elif token == 'isnot':
                result.append('!=')
            # Handle compound assignment operators
            elif token == '+=':
                result.append('+=')
            elif token == '-=':
                result.append('-=')
            elif token == '*=':
                result.append('*=')
            elif token == '/=':
                result.append('/=')
            elif token == '*%=':
                result.append('%=')  # Map '*%=' to '%='
            else:
                result.append(token)
            i += 1
            
        # Join all tokens with spaces
        return " ".join(result)
    
    def _is_display_statement(self, tokens, index):
        if index < len(tokens) and tokens[index][0] == 'display':
            return True
        return False
    
    def _process_display(self, tokens, index):
        self.debug(f"Processing display statement at index {index}")

        # Find opening and closing parentheses
        i = index + 1
        while i < len(tokens) and tokens[i][0] != '(':
            i += 1
        
        if i >= len(tokens):
            self.debug("No opening parenthesis found for display statement")
            return index + 1
        
        # Extract expression inside display()
        i += 1  # Skip opening parenthesis
        expr_tokens = []
        
        # Keep track of parentheses nesting level
        paren_level = 0
        
        # Keep adding tokens until closing parenthesis at the right level
        while i < len(tokens):
            if tokens[i][0] == '(':
                paren_level += 1
                expr_tokens.append(tokens[i][0])
            elif tokens[i][0] == ')':
                if paren_level == 0:
                    break  # This is our closing parenthesis
                paren_level -= 1
                expr_tokens.append(tokens[i][0])
            else:
                expr_tokens.append(tokens[i][0])
            i += 1
        
        self.debug(f"Display expression tokens: {expr_tokens}")

        # Helper function to check variable type in current scope or global scope
        def get_variable_type(var_name):
            # Check current scope first
            if var_name in self.variable_types.get(self.current_scope, {}):
                return self.variable_types[self.current_scope][var_name]
            # Then check global scope
            elif var_name in self.variable_types.get("global", {}):
                return self.variable_types["global"][var_name]
            # Not found in either scope
            return None

        # Handle struct member access for display
        if len(expr_tokens) >= 3 and expr_tokens[1] == '.':
            struct_var = expr_tokens[0]
            struct_member = expr_tokens[2]
            
            # Check if we're dealing with a struct using helper function
            var_type = get_variable_type(struct_var)
            if var_type and var_type.startswith("struct_"):
                # Extract the struct type
                struct_type = var_type.replace("struct_", "")
                member_type = None
                
                # Look up the member type from our struct definitions
                if struct_type in self.struct_definitions and struct_member in self.struct_definitions[struct_type]:
                    member_type = self.struct_definitions[struct_type][struct_member]
                    self.debug(f"Found member type for display: {struct_type}.{struct_member}: {member_type}")
                else:
                    self.debug(f"Could not find member type for display: {struct_type}.{struct_member}")
                    # Default to string if we can't determine the type
                    member_type = "string"
                
                # Handle different member types
                if len(expr_tokens) >= 5 and expr_tokens[3] == '+':
                    # Handle struct member with concatenation (like car1.year + "\n")
                    # Generate separate printf statements for each segment
                    
                    # First segment (struct member)
                    if member_type == "int":
                        self.add_line(f"printf(\"%d\", {struct_var}.{struct_member});")
                    elif member_type == "double" or member_type == "decimal":
                        self.add_line(f"printf(\"%f\", {struct_var}.{struct_member});")
                    elif member_type == "bool":
                        self.add_line(f"printf(\"%s\", {struct_var}.{struct_member} ? \"true\" : \"false\");")
                    elif member_type == "char" or member_type == "letter":
                        self.add_line(f"printf(\"%c\", {struct_var}.{struct_member});")
                    else:
                        self.add_line(f"printf(\"%s\", {struct_var}.{struct_member});")
                    
                    # Second segment (string literal)
                    string_literal = expr_tokens[4]
                    self.add_line(f"printf(\"%s\", {string_literal});")
                    
                    # Skip past closing parenthesis and find semicolon
                    i += 1
                    while i < len(tokens) and tokens[i][0] != ';':
                        i += 1
                    return i + 1  # Skip past semicolon
                else:
                    # Simple struct member display
                    if member_type == "int":
                        self.add_line(f"printf(\"%d\", {struct_var}.{struct_member});")
                    elif member_type == "double" or member_type == "decimal":
                        self.add_line(f"printf(\"%f\", {struct_var}.{struct_member});")
                    elif member_type == "bool":
                        self.add_line(f"printf(\"%s\", {struct_var}.{struct_member} ? \"true\" : \"false\");")
                    elif member_type == "char" or member_type == "letter":
                        self.add_line(f"printf(\"%c\", {struct_var}.{struct_member});")
                    else:
                        self.add_line(f"printf(\"%s\", {struct_var}.{struct_member});")
                    
                    # Skip past closing parenthesis and find semicolon
                    i += 1
                    while i < len(tokens) and tokens[i][0] != ';':
                        i += 1
                    return i + 1  # Skip past semicolon
        
        # Handle array element handling
        var_name = expr_tokens[0] if expr_tokens else ""
        var_type = get_variable_type(var_name)  # Use helper to check both scopes
        
        if len(expr_tokens) >= 3 and var_type and '[' in expr_tokens[1]:
            var_base_type = var_type
            
            # Check if this is part of a concatenation expression
            plus_index = -1
            for j, token in enumerate(expr_tokens):
                if token == "+":
                    plus_index = j
                    break
            
            if plus_index > 0:
                # Handle concatenation - split into separate printf calls
                
                # First part - array element
                array_expr = expr_tokens[:plus_index]
                array_access = self._format_expression(array_expr)
                
                # Use appropriate printf format based on the element type
                if var_base_type == 'int':
                    self.add_line(f"printf(\"%d\", {array_access});")
                elif var_base_type == 'decimal' or var_base_type == 'double':
                    self.add_line(f"printf(\"%f\", {array_access});")
                elif var_base_type == 'bool':
                    self.add_line(f"printf(\"%s\", {array_access} ? \"true\" : \"false\");")
                elif var_base_type == 'letter' or var_base_type == 'char':
                    self.add_line(f"printf(\"%c\", {array_access});")
                elif var_base_type == 'string':
                    self.add_line(f"printf(\"%s\", {array_access}); //st")
                else:
                    self.add_line(f"printf(\"%s\", {array_access}); //sy")
                
                # Second part - string literal or other expression
                second_expr = expr_tokens[plus_index+1:]
                second_part = self._format_expression(second_expr)
                
                # Determine type of second part
                second_type = "string"  # Default assumption for string literals
                if len(second_expr) == 1:
                    second_var = second_expr[0]
                    second_var_type = get_variable_type(second_var)  # Use helper function
                    if second_var_type:
                        second_type = second_var_type
                
                # Generate appropriate printf call for second part
                if second_type == "int":
                    self.add_line(f"printf(\"%d\", {second_part});")
                elif second_type == "decimal" or second_type == "double":
                    self.add_line(f"printf(\"%f\", {second_part});")
                elif second_type == "bool":
                    self.add_line(f"printf(\"%s\", {second_part} ? \"true\" : \"false\");")
                elif second_type == "letter" or second_type == "char":
                    self.add_line(f"printf(\"%c\", {second_part});")
                else:
                    self.add_line(f"printf(\"%s\", {second_part}); //sdf")
            else:
                # No concatenation - handle as a single array access
                array_access = self._format_expression(expr_tokens)
                
                # Use appropriate printf format based on the element type
                if var_base_type == 'int':
                    self.add_line(f"printf(\"%d\", {array_access});")
                elif var_base_type == 'decimal' or var_base_type == 'double':
                    self.add_line(f"printf(\"%f\", {array_access});")
                elif var_base_type == 'bool':
                    self.add_line(f"printf(\"%s\", {array_access} ? \"true\" : \"false\");")
                elif var_base_type == 'letter' or var_base_type == 'char':
                    self.add_line(f"printf(\"%c\", {array_access});")
                elif var_base_type == 'string':
                    self.add_line(f"printf(\"%s\", {array_access}); //asd")
                else:
                    self.add_line(f"printf(\"%s\", {array_access}); //as")
            
            # Skip past closing parenthesis and find semicolon
            i += 1
            while i < len(tokens) and tokens[i][0] != ';':
                i += 1
            return i + 1  # Skip past semicolon
        
        # Handle string indexing - check if the expression is accessing a character of a string
        if len(expr_tokens) >= 3 and expr_tokens[1] == '[':
            var_name = expr_tokens[0]
            var_type = get_variable_type(var_name)  # Use helper function
            
            # Find the closing bracket
            closing_bracket_idx = -1
            for j in range(2, len(expr_tokens)):
                if ']' in expr_tokens[j]:
                    closing_bracket_idx = j
                    break
            
            if closing_bracket_idx != -1 and var_type == 'string':
                # Extract the index expression
                index_expr = self._format_expression(expr_tokens[2:closing_bracket_idx+1])
                index_expr = index_expr.replace(']', '')  # Remove closing bracket if present
                
                self.add_line(f"printf(\"%c\", {var_name}[{index_expr}]);")
                    
                # Skip past closing parenthesis and find semicolon
                i += 1
                while i < len(tokens) and tokens[i][0] != ';':
                    i += 1
                return i + 1  # Skip past semicolon
        
        # Special case for boolean values
        if len(expr_tokens) == 1:
            var_name = expr_tokens[0]
            var_type = get_variable_type(var_name)  # Use helper function
            if var_type == 'bool':
                self.add_line(f"printf(\"%s\", {var_name} ? \"true\" : \"false\");")
                # Skip past closing parenthesis and find semicolon
                i += 1
                while i < len(tokens) and tokens[i][0] != ';':
                    i += 1
                return i + 1  # Skip past semicolon
        
        # Handle string concatenation with '+' using multiple printf calls
        plus_indices = []
        for j, token in enumerate(expr_tokens):
            if token == "+":
                plus_indices.append(j)
        
        if plus_indices:
            # Multiple printf handling
            segments = []
            start_idx = 0
            
            # Split the expression into segments
            for plus_idx in plus_indices:
                segments.append(expr_tokens[start_idx:plus_idx])
                start_idx = plus_idx + 1
            
            # Add the last segment
            if start_idx < len(expr_tokens):
                segments.append(expr_tokens[start_idx:])
            
            # Generate printf calls for each segment
            for segment in segments:
                segment_expr = self._format_expression(segment)
                
                # Determine type of segment for proper formatting
                segment_type = "unknown"
                if len(segment) == 1:
                    var_name = segment[0]
                    var_type = get_variable_type(var_name)  # Use helper function
                    if var_type:
                        segment_type = var_type
                    elif var_name.startswith('"') and var_name.endswith('"'):
                        segment_type = "string"
                    elif var_name.isdigit():
                        segment_type = "int"
                    elif var_name.replace('.', '', 1).isdigit():
                        segment_type = "decimal"
                    elif var_name == "true" or var_name == "false":
                        segment_type = "bool"
                    # Check for array access
                    elif '[' in var_name and ']' in var_name:
                        array_name = var_name.split('[')[0]
                        array_type = get_variable_type(array_name)  # Use helper function
                        if array_type:
                            segment_type = array_type.rstrip('[]')
                
                # Apply proper printf based on type
                if segment_type == "int":
                    self.add_line(f"printf(\"%d\", {segment_expr});")
                elif segment_type == "decimal" or segment_type == "double":
                    self.add_line(f"printf(\"%f\", {segment_expr});")
                elif segment_type == "letter" or segment_type == "char":
                    self.add_line(f"printf(\"%c\", {segment_expr});")
                elif segment_type == "bool":
                    self.add_line(f"printf(\"%s\", {segment_expr} ? \"true\" : \"false\");")
                elif segment_type == "string":
                    # Check if this is a string literal or variable
                    if len(segment) == 1 and segment[0].startswith('"'):
                        # It's a string literal
                        self.add_line(f"printf(\"%s\", {segment_expr});")
                    else:
                        # It's a string variable or expression
                        self.add_line(f"printf(\"%s\", {segment_expr});")
                else:
                    # Default for unknown types
                    self.add_line(f"printf(\"%s\", {segment_expr});")
            
            # Skip past closing parenthesis and find semicolon
            i += 1
            while i < len(tokens) and tokens[i][0] != ';':
                i += 1
            return i + 1  # Skip past semicolon
        else:
            # Check if we're displaying a single variable
            if len(expr_tokens) == 1:
                var_name = expr_tokens[0]
                var_type = get_variable_type(var_name)  # Use helper function
                
                if var_type:
                    # Modify helper function calls to not add newlines
                    if var_type == 'int':
                        self.add_line(f"printf(\"%d\", {expr_tokens[0]});")
                    elif var_type == 'double' or var_type == 'decimal':
                        self.add_line(f"printf(\"%f\", {expr_tokens[0]});")
                    elif var_type == 'bool':
                        self.add_line(f"printf(\"%s\", {expr_tokens[0]} ? \"true\" : \"false\");")
                    elif var_type == 'char' or var_type == 'letter':
                        self.add_line(f"printf(\"%c\", {expr_tokens[0]});")
                    else:
                        self.add_line(f"printf(\"%s\", {expr_tokens[0]});")
                else:
                    # Simple display statement - no variable type found
                    expr_str = self._format_expression(expr_tokens)
                    self.add_line(f"printf(\"%s\", {expr_str});")
            else:
                # Complex expression or string literal
                expr_str = self._format_expression(expr_tokens)
                self.add_line(f"printf(\"%s\", {expr_str});")
        
        # Skip past closing parenthesis and find semicolon
        i += 1
        while i < len(tokens) and tokens[i][0] != ';':
            i += 1
            
        return i + 1  # Skip past semicolon

    def _is_if_statement(self, tokens, index):
        if index < len(tokens) and tokens[index][0] == 'if':
            return True
        return False
    
    def _process_if_statement(self, tokens, index, end_index):
        self.debug(f"Processing if statement at index {index}")
        
        # Move past 'if'
        i = index + 1
        
        # Find opening parenthesis
        while i < len(tokens) and tokens[i][0] != '(':
            i += 1
            
        if i >= len(tokens):
            self.debug("No opening parenthesis found for if statement")
            return index + 1
            
        i += 1  # Skip opening parenthesis
        
        # Extract condition
        condition_tokens = []
        paren_level = 0
        
        while i < len(tokens):
            if tokens[i][0] == '(':
                paren_level += 1
                condition_tokens.append(tokens[i][0])
            elif tokens[i][0] == ')':
                if paren_level == 0:
                    break  # This is our closing parenthesis
                paren_level -= 1
                condition_tokens.append(tokens[i][0])
            else:
                condition_tokens.append(tokens[i][0])
            i += 1
        
        # Format condition with custom operators
        cond_str = self._format_expression(condition_tokens)
        self.debug(f"If condition: {cond_str}")
        
        # Find opening brace of if block
        i += 1  # Skip closing parenthesis
        while i < len(tokens) and tokens[i][0] != '{':
            i += 1
            
        if i >= len(tokens):
            self.debug("No opening brace found for if block")
            return index + 1
        
        # Find matching closing brace for if block
        if_block_start = i
        if_block_end = self._find_matching_brace(tokens, if_block_start)
        
        if if_block_end == -1:
            self.debug("No matching closing brace found for if block")
            return index + 1
        
        # Generate if statement
        self.add_line(f"if ({cond_str}) {{")
        self.indentation += 1
        
        # Process if block statements
        j = if_block_start + 1
        while j < if_block_end:
            old_j = j
            j = self._process_statement(tokens, j, if_block_end)
            if j == old_j:  # Prevent infinite loop
                j += 1
        
        self.indentation -= 1
        self.add_line("}")
        
        # Look for elseif or else
        next_index = if_block_end + 1
        
        # We need to handle potentially multiple elseif blocks
        while next_index < len(tokens) and tokens[next_index][0] == 'elseif':
            self.debug(f"Found elseif at index {next_index}")
            elseif_index = next_index
            
            # Move past 'elseif'
            i = elseif_index + 1
            
            # Find opening parenthesis
            while i < len(tokens) and tokens[i][0] != '(':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening parenthesis found for elseif statement")
                break
                
            i += 1  # Skip opening parenthesis
            
            # Extract condition
            elseif_condition_tokens = []
            paren_level = 0
            
            while i < len(tokens):
                if tokens[i][0] == '(':
                    paren_level += 1
                    elseif_condition_tokens.append(tokens[i][0])
                elif tokens[i][0] == ')':
                    if paren_level == 0:
                        break  # This is our closing parenthesis
                    paren_level -= 1
                    elseif_condition_tokens.append(tokens[i][0])
                else:
                    elseif_condition_tokens.append(tokens[i][0])
                i += 1
            
            # Format elseif condition
            elseif_cond_str = self._format_expression(elseif_condition_tokens)
            self.debug(f"Elseif condition: {elseif_cond_str}")
            
            # Find opening brace of elseif block
            i += 1  # Skip closing parenthesis
            while i < len(tokens) and tokens[i][0] != '{':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening brace found for elseif block")
                break
            
            # Find matching closing brace for elseif block
            elseif_block_start = i
            elseif_block_end = self._find_matching_brace(tokens, elseif_block_start)
            
            if elseif_block_end == -1:
                self.debug("No matching closing brace found for elseif block")
                break
            
            # Generate elseif statement
            self.add_line(f"else if ({elseif_cond_str}) {{")
            self.indentation += 1
            
            # Process elseif block statements
            j = elseif_block_start + 1
            while j < elseif_block_end:
                old_j = j
                j = self._process_statement(tokens, j, elseif_block_end)
                if j == old_j:  # Prevent infinite loop
                    j += 1
            
            self.indentation -= 1
            self.add_line("}")
            
            # Update next_index for potential next elseif or else
            next_index = elseif_block_end + 1
        
        # Check for else block
        if next_index < len(tokens) and tokens[next_index][0] == 'else':
            self.debug(f"Found else at index {next_index}")
            
            # Find opening brace of else block
            i = next_index + 1
            while i < len(tokens) and tokens[i][0] != '{':
                i += 1
                
            if i < len(tokens):
                # Find matching closing brace for else block
                else_block_start = i
                else_block_end = self._find_matching_brace(tokens, else_block_start)
                
                if else_block_end != -1:
                    # Generate else statement
                    self.add_line("else {")
                    self.indentation += 1
                    
                    # Process else block statements
                    j = else_block_start + 1
                    while j < else_block_end:
                        old_j = j
                        j = self._process_statement(tokens, j, else_block_end)
                        if j == old_j:  # Prevent infinite loop
                            j += 1
                    
                    self.indentation -= 1
                    self.add_line("}")
                    
                    return else_block_end + 1
        
        # If we had no else block, return after the last processed block
        return next_index
    
    def _is_select_statement(self, tokens, index):
        if index < len(tokens) and tokens[index][0] == 'select':
            return True
        return False
    
    def _process_select_statement(self, tokens, index, end_index):
        self.debug(f"Processing select statement at index {index}")
        
        # Move past 'select'
        i = index + 1
        
        # Find opening parenthesis
        while i < len(tokens) and tokens[i][0] != '(':
            i += 1
            
        if i >= len(tokens):
            self.debug("No opening parenthesis found for select statement")
            return index + 1
            
        i += 1  # Skip opening parenthesis
        
        # Extract expression to switch on
        select_expr_tokens = []
        paren_level = 0
        
        while i < len(tokens):
            if tokens[i][0] == '(':
                paren_level += 1
                select_expr_tokens.append(tokens[i][0])
            elif tokens[i][0] == ')':
                if paren_level == 0:
                    break  # This is our closing parenthesis
                paren_level -= 1
                select_expr_tokens.append(tokens[i][0])
            else:
                select_expr_tokens.append(tokens[i][0])
            i += 1
        
        # Format select expression
        select_expr = self._format_expression(select_expr_tokens)
        self.debug(f"Select expression: {select_expr}")
        
        # Find opening brace of select block
        i += 1  # Skip closing parenthesis
        while i < len(tokens) and tokens[i][0] != '{':
            i += 1
            
        if i >= len(tokens):
            self.debug("No opening brace found for select block")
            return index + 1
        
        # Find matching closing brace for select block
        select_block_start = i
        select_block_end = self._find_matching_brace(tokens, select_block_start)
        
        if select_block_end == -1:
            self.debug("No matching closing brace found for select block")
            return index + 1
        
        # Start switch statement
        self.add_line(f"switch ({select_expr}) {{")
        self.indentation += 1
        
        # Process case statements
        i = select_block_start + 1
        while i < select_block_end:
            # Look for 'option', 'default', or 'skip'
            if i < len(tokens) and tokens[i][0] == 'option':
                self.debug("Found option (case) statement")
                i += 1  # Skip past 'option'
                
                # Get case value
                if i < len(tokens):
                    case_value = tokens[i][0]
                    i += 1  # Skip case value
                    
                    # Add 'case' statement
                    self.add_line(f"case {case_value}:")
                    self.indentation += 1
                    
                    # Process statements until 'skip' or next option
                    while i < select_block_end:
                        if i < len(tokens) and tokens[i][0] == 'skip':
                            self.add_line("break;")
                            i += 1  # Skip past 'skip'
                            
                            # Skip past semicolon if present
                            if i < len(tokens) and tokens[i][0] == ';':
                                i += 1
                                
                            break
                        elif i < len(tokens) and (tokens[i][0] == 'option' or tokens[i][0] == 'default'):
                            # Reached next case, add break automatically
                            self.add_line("break;")
                            break
                        else:
                            # Process statements inside this case
                            old_i = i
                            i = self._process_statement(tokens, i, select_block_end)
                            if i == old_i:  # Prevent infinite loop
                                i += 1
                    
                    self.indentation -= 1
            elif i < len(tokens) and tokens[i][0] == 'default':
                self.debug("Found default case statement")
                i += 1  # Skip past 'default'
                
                # Skip past ':' if present
                if i < len(tokens) and tokens[i][0] == ':':
                    i += 1
                
                # Add 'default' statement
                self.add_line("default:")
                self.indentation += 1
                
                # Process statements until end of select block
                while i < select_block_end:
                    if i < len(tokens) and tokens[i][0] == 'skip':
                        self.add_line("break;")
                        i += 1  # Skip past 'skip'
                        
                        # Skip past semicolon if present
                        if i < len(tokens) and tokens[i][0] == ';':
                            i += 1
                            
                        break
                    elif i < len(tokens) and (tokens[i][0] == 'option' or tokens[i][0] == 'default'):
                        # Reached next case, add break automatically
                        self.add_line("break;")
                        break
                    else:
                        # Process statements inside default case
                        old_i = i
                        i = self._process_statement(tokens, i, select_block_end)
                        if i == old_i:  # Prevent infinite loop
                            i += 1
                
                self.indentation -= 1
            else:
                i += 1
        
        # Close switch statement
        self.indentation -= 1
        self.add_line("}")
        
        return select_block_end + 1
    
    def _is_loop_statement(self, tokens, index):
        if index < len(tokens):
            if tokens[index][0] in ['while', 'for', 'try']:
                return True
        return False
    
    def _process_loop_statement(self, tokens, index, end_index):
        loop_type = tokens[index][0]
        self.debug(f"Processing {loop_type} loop at index {index}")
        
        if loop_type == 'while':
            # Standard while loop
            i = index + 1
            
            # Find opening parenthesis
            while i < len(tokens) and tokens[i][0] != '(':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening parenthesis found for while loop")
                return index + 1
                
            i += 1  # Skip opening parenthesis
            
            # Extract condition
            condition_tokens = []
            paren_level = 0
            
            while i < len(tokens):
                if tokens[i][0] == '(':
                    paren_level += 1
                    condition_tokens.append(tokens[i][0])
                elif tokens[i][0] == ')':
                    if paren_level == 0:
                        break  # This is our closing parenthesis
                    paren_level -= 1
                    condition_tokens.append(tokens[i][0])
                else:
                    condition_tokens.append(tokens[i][0])
                i += 1
            
            # Format condition
            cond_str = self._format_expression(condition_tokens)
            
            # Find opening brace of loop body
            i += 1  # Skip closing parenthesis
            while i < len(tokens) and tokens[i][0] != '{':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening brace found for while loop body")
                return index + 1
            
            # Find matching closing brace for loop body
            loop_block_start = i
            loop_block_end = self._find_matching_brace(tokens, loop_block_start)
            
            if loop_block_end == -1:
                self.debug("No matching closing brace found for while loop body")
                return index + 1
            
            # Generate while loop
            self.add_line(f"while ({cond_str}) {{")
            self.indentation += 1
            
            # Process loop body statements
            j = loop_block_start + 1
            while j < loop_block_end:
                old_j = j
                j = self._process_statement(tokens, j, loop_block_end)
                if j == old_j:  # Prevent infinite loop
                    j += 1
            
            self.indentation -= 1
            self.add_line("}")
            
            return loop_block_end + 1
            
        elif loop_type == 'try':
            # do-while equivalent (try-while)
            i = index + 1
            
            # Find opening brace of loop body
            while i < len(tokens) and tokens[i][0] != '{':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening brace found for try-while loop body")
                return index + 1
            
            # Find matching closing brace for loop body
            loop_block_start = i
            loop_block_end = self._find_matching_brace(tokens, loop_block_start)
            
            if loop_block_end == -1:
                self.debug("No matching closing brace found for try-while loop body")
                return index + 1
            
            # Look for 'while' after the block
            i = loop_block_end + 1
            if i >= len(tokens) or tokens[i][0] != 'while':
                self.debug("Missing 'while' after try block")
                return loop_block_end + 1
            
            i += 1  # Skip past 'while'
            
            # Find opening parenthesis
            while i < len(tokens) and tokens[i][0] != '(':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening parenthesis found for while condition in try-while")
                return loop_block_end + 1
                
            i += 1  # Skip opening parenthesis
            
            # Extract condition
            condition_tokens = []
            paren_level = 0
            
            while i < len(tokens):
                if tokens[i][0] == '(':
                    paren_level += 1
                    condition_tokens.append(tokens[i][0])
                elif tokens[i][0] == ')':
                    if paren_level == 0:
                        break  # This is our closing parenthesis
                    paren_level -= 1
                    condition_tokens.append(tokens[i][0])
                else:
                    condition_tokens.append(tokens[i][0])
                i += 1
            
            # Format condition
            cond_str = self._format_expression(condition_tokens)
            
            # Generate do-while loop
            self.add_line("do {")
            self.indentation += 1
            
            # Process loop body statements
            j = loop_block_start + 1
            while j < loop_block_end:
                old_j = j
                j = self._process_statement(tokens, j, loop_block_end)
                if j == old_j:  # Prevent infinite loop
                    j += 1
            
            self.indentation -= 1
            self.add_line(f"}} while ({cond_str});")
            
            # Skip past closing parenthesis and semicolon
            i += 1
            while i < len(tokens) and tokens[i][0] != ';':
                i += 1
                
            return i + 1  # Skip past semicolon
            
        elif loop_type == 'for':
            # Standard for loop
            i = index + 1
            
            # Find opening parenthesis
            while i < len(tokens) and tokens[i][0] != '(':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening parenthesis found for for loop")
                return index + 1
                
            i += 1  # Skip opening parenthesis
            
            # Extract initialization
            init_tokens = []
            while i < len(tokens) and tokens[i][0] != ';':
                init_tokens.append(tokens[i][0])
                i += 1
                
            init_str = " ".join(init_tokens)
            i += 1  # Skip past semicolon
            
            # Extract condition
            cond_tokens = []
            while i < len(tokens) and tokens[i][0] != ';':
                cond_tokens.append(tokens[i][0])
                i += 1
                
            cond_str = self._format_expression(cond_tokens)
            i += 1  # Skip past semicolon
            
            # Extract increment
            incr_tokens = []
            paren_level = 0
            
            while i < len(tokens):
                if tokens[i][0] == '(':
                    paren_level += 1
                    incr_tokens.append(tokens[i][0])
                elif tokens[i][0] == ')':
                    if paren_level == 0:
                        break  # This is our closing parenthesis
                    paren_level -= 1
                    incr_tokens.append(tokens[i][0])
                else:
                    incr_tokens.append(tokens[i][0])
                i += 1
                
            incr_str = " ".join(incr_tokens)
            
            # Find opening brace of loop body
            i += 1  # Skip closing parenthesis
            while i < len(tokens) and tokens[i][0] != '{':
                i += 1
                
            if i >= len(tokens):
                self.debug("No opening brace found for for loop body")
                return index + 1
            
            # Find matching closing brace for loop body
            loop_block_start = i
            loop_block_end = self._find_matching_brace(tokens, loop_block_start)
            
            if loop_block_end == -1:
                self.debug("No matching closing brace found for for loop body")
                return index + 1
            
            # Generate for loop
            self.add_line(f"for ({init_str}; {cond_str}; {incr_str}) {{")
            self.indentation += 1
            
            # Process loop body statements
            j = loop_block_start + 1
            while j < loop_block_end:
                old_j = j
                j = self._process_statement(tokens, j, loop_block_end)
                if j == old_j:  # Prevent infinite loop
                    j += 1
            
            self.indentation -= 1
            self.add_line("fflush(stdout);")
            self.add_line("}")
            
            return loop_block_end + 1
        
        return index + 1
    
    def _is_function_call(self, tokens, index):
        # More flexible function call detection
        if index + 1 < len(tokens):
            is_identifier = len(tokens[index]) > 1 and tokens[index][1] == 'identifier'
            next_token = tokens[index + 1][0] == '('
            
            if is_identifier and next_token:
                self.debug(f"Function call detected: {tokens[index][0]}()")
                return True
        return False
    
    def _process_function_call(self, tokens, index):
        function_name = tokens[index][0]
        self.debug(f"Processing function call: {function_name}()")
        
        # Find closing parenthesis
        i = index + 2  # Skip past function name and opening parenthesis
        
        # Check if we have parameters
        params = []
        current_param = []
        param_start = i
        
        # Keep track of parentheses
        paren_level = 1  # We've already seen one opening parenthesis
        
        while i < len(tokens) and paren_level > 0:
            if tokens[i][0] == '(':
                paren_level += 1
                current_param.append(tokens[i][0])
            elif tokens[i][0] == ')':
                paren_level -= 1
                if paren_level > 0:  # Only add if this isn't our closing parenthesis
                    current_param.append(tokens[i][0])
                else:
                    # Add the last parameter if we have tokens
                    if current_param:
                        params.append(self._format_expression(current_param))
            elif tokens[i][0] == ',' and paren_level == 1:
                # This is a top-level comma separating parameters
                params.append(self._format_expression(current_param))
                current_param = []
            else:
                current_param.append(tokens[i][0])
            i += 1
        
        # Check if this is an assignment with function call
        is_assignment = False
        if i < len(tokens) and tokens[i][0] == '=':
            is_assignment = True
            i += 1  # Skip past '='
            
        # Format the function call
        param_str = ", ".join(params)
        function_call = f"{function_name}({param_str})"
        
        # Check if we're part of an assignment or statement
        if is_assignment:
            # Find the variable being assigned
            var_name = tokens[index-2][0]  # Assumes format like "sum = add(a, b);"
            self.add_line(f"{var_name} = {function_call};")
        else:
            self.add_line(f"{function_call};")
        
        # Skip past any remaining tokens until semicolon
        while i < len(tokens) and tokens[i][0] != ';':
            i += 1
            
        return i + 1  # Skip past semicolon