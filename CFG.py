cfg = {
    "<program>": [["<global_dec>", "<function_list>", "main", "(", ")", "{", "<local_dec>", "<statement_list>", "}"]],

    "<global_dec>": [["<global_dec_tail>", "<global_dec>"],
                     ["λ"]],

    "<global_dec_tail>": [["fixed", "<data_type>", "identifier", "=", "<literal>", "<fixed_tail>"],
                        ["<data_type>", "identifier", "<dec_tail>"],
                        ["unit", "identifier", "<global_unit_tail>"]],

    "<data_type>": [
        ["int"],
        ["decimal"],
        ["string"],
        ["letter"],
        ["bool"]],

    "<literal>": [
        ["<num_literal>"],
        ["string_literal"],
        ["letter_literal"],
        ["<bool_literal>"]],

    "<num_literal>": [
        ["int_literal"],
        ["decimal_literal"]],

    "<bool_literal>": [
        ["true"],
        ["false"]],

    "<fixed_tail>": [
        [";"],
        [",", "identifier", "=", "<literal>", "<fixed_tail>"]],

    "<dec_tail>": [
        ["<variable_tail>"],
        ["[", "<array_format>"]],

    "<variable_tail>": [
        [";"],
        [",", "identifier", "<variable_tail>"],
        ["=", "<expression>", "<initial_tail>"]],

    "<initial_tail>": [
        [";"],
        [",", "identifier", "<variable_tail>"]],

    "<array_format>": [
        ["<size>", "]", "<array_tail>"],
        ["]", "=", "{", "<array_val>", "}", ";"]],

    "<array_val>": [
        ["<literal>", "<array_literal_tail>"],
        ["λ"]],

    "<size>": [
        ["int_literal"]],

    "<array_tail>": [
        [";"],
        ["=", "{", "<array_val>", "}", ";"],
        ["[", "<size>", "]", "<array_2d_tail>"]],

    "<array_2d_tail>": [
        [";"],
        ["=", "{", "{", "<array_val>", "}", "<group_tail>", "}", ";"]],

    "<array_literal_tail>": [
        [",", "<literal>", "<array_literal_tail>"],
        ["λ"]],

    "<group_tail>": [
        [",", "{", "<array_val>", "}", "<group_tail>"],
        ["λ"]],

    "<global_unit_tail>": [
        ["{", "<member_dec>", "}"],
        ["identifier", "<global_initial_unit>"]
    ],

    "<global_initial_unit>": [
        [";"],
        ["=", "{", "<unit_val>", "}", ";"]],

    "<member_dec>": [
        ["<data_type>", "identifier", ";", "<member_dec>"],
        ["λ"]],

    "<unit_val>": [
        ["<literal>", "<unit_val_tail>"],
        ["λ"]],

    "<unit_val_tail>": [
        [",", "<literal>", "<unit_val_tail>"],
        ["λ"]],

    "<function_list>": [
        ["<function_dec>", "<function_list>"],
        ["λ"]],

    "<function_dec>": [
        ["task", "identifier", "(", "<parameter>", ")", "{", "<local_dec>", "<statement_list>", "<return_stmt>", "}"],
        ["empty", "identifier", "(", "<parameter>", ")", "{", "<local_dec>", "<statement_list>", "}"]],

    "<parameter>": [
        ["<param_list>"],
        ["λ"]],

    "<param_list>": [
        ["<data_type>", "identifier", "<param_tail>"]],

    "<param_tail>": [
        [",", "<data_type>", "identifier", "<param_tail>"],
        ["λ"]],

    "<local_dec>": [["<local_dec_tail>", "<local_dec>"],
                     ["λ"]],


    "<local_dec_tail>": [
        ["fixed", "<data_type>", "identifier", "=", "<literal>", "<fixed_tail>"],
        ["<data_type>", "identifier", "<dec_tail>"],
        ["unit", "identifier", "<local_unit_tail>"]],

    "<statement_list>": [["<statement_tail>", "<statement_list>"],
                     ["λ"]],

    "<option_statement_list>": [["<statement_tail>", "<option_statement_list>"],
                     ["λ"]],

    "<statement_tail>": [
        ["identifier", "<statement_id_tail>"],
        ["<inc_dec_operator>", "identifier", ";"],
        ["<cond_stmt>"],
        ["<loop_stmt>"],
        ["display", "(", "<display_content>", ")", ";"]],

    "<statement_id_tail>": [
        ["(", "<argument_list>", ")",";"],
        ["<assignment_op>", "<assign_val>", ";"],
        ["[", "<arithmetic_exp>", "]", "<access_arr_tail>", "<assignment_op>", "<assign_val>", ";"],
        [".", "identifier", "<assignment_op>", "<assign_val>", ";"],
        ["<inc_dec_operator>", ";"]],

    "<access_arr_tail>": [
        ["[", "<arithmetic_exp>", "]"],
        ["λ"]],

    "<inc_dec_operator>": [
        ["++"],
        ["--"]],

    "<argument_list>": [
        ["<arithmetic_exp>", "<argument_tail>"],
        ["λ"]],

    "<argument_tail>": [
        [",", "<arithmetic_exp>", "<argument_tail>"],
        ["λ"]],

    "<local_unit_tail>": [
        ["{", "<member_dec>", "}"],
        ["identifier", "<local_initial_unit>"]
    ],

    "<local_initial_unit>": [
        [";"],
        ["=", "{", "<unit_val>", "}", ";"]],

    "<assignment_op>": [
        ["="],
        ["+="],
        ["-="],
        ["*="],
        ["%="],
        ["/="],
        ["**="]],

    "<assign_val>": [
        ["<expression>"],
        ["reads", "(", ")"]],

    "<expression>": [
        ["<expression_operand>", "<expression_tail>"]],

    "<expression_tail>": [
        ["<expression_operator>", "<expression_operand>", "<expression_tail>"],
        ["λ"]],

    "<expression_operand>": [["<value>"],
                             ["(", "<expression>", ")"],
                             ["!", "(", "<expression>", ")"]],

    "<expression_operator>": [
        ["+"],
        ["-"],
        ["*"],
        ["/"],
        ["%"],
        ["**"],
        ["=="],
        ["!="],
        ["<"],
        [">"],
        ["<="],
        [">="],
        ["&&"],
        ["||"],
        ["is"],
        ["isnot"],
        ["ins"],
        ["notin"]],

    "<value>": [
        ["<literal>"],
        ["identifier", "<value_id_tail>"]],

    "<value_id_tail>": [
        ["(", "<argument_list>", ")"],
        ["[", "<arithmetic_exp>", "]", "<access_arr_tail>"],
        [".", "identifier"],
        ["λ"]],

    "<arithmetic_exp>": [
        ["<arithmetic_operand>", "<arithmetic_tail>"]],

    "<arithmetic_tail>": [
        ["<arithmetic_operator>", "<arithmetic_operand>", "<arithmetic_tail>"],
        ["λ"]],

    "<arithmetic_operand>": [
        ["<value>"],
        ["(", "<arithmetic_exp>", ")"]],

    "<arithmetic_operator>": [
        ["+"], 
        ["-"], 
        ["*"], 
        ["/"], 
        ["%"], 
        ["**"]],

    "<cond_stmt>": [
        ["<if_stmt>", "<elseif_stmt>", "<else_stmt>"],
        ["<select_stmt>"]],

    "<if_stmt>": [
        ["if", "(", "<condition>", ")", "{", "<statement_list>", "}"]],

    "<elseif_stmt>": [
        ["elseif", "(", "<condition>", ")", "{", "<statement_list>", "}", "<elseif_stmt>"],
        ["λ"]],

    "<else_stmt>": [
        ["else", "{", "<statement_list>", "}"],
        ["λ"]],

    "<select_stmt>": [
        ["select", "(", "identifier", ")", "{", "<options>", "default", ":", "<statement_list>", "}"]],

    "<options>": [
        ["option", "<pattern>", ":", "<option_statement_list>", "skip", ";", "<options>"],
        ["λ"]],

    "<pattern>": [
        ["identifier"],
        ["<literal>"]],

    "<loop_stmt>": [
        ["while", "(", "<condition>", ")", "{", "<statement_list>", "}"],
        ["try", "{", "<statement_list>", "}", "while", "(", "<condition>", ")", ";"],
        ["for", "(", "identifier", "=", "<arithmetic_exp>", ";", "<condition>", ";", "identifier", "<inc_dec_operator>", ")", "{", "<statement_list>", "}"]],

    "<condition>": [
        ["<condition_operand>", "<condition_tail>"]],

    "<condition_tail>": [
        ["<condition_operator>", "<condition_operand>", "<condition_tail>"],
        ["λ"]],

    "<condition_operand>": [
        ["<value>"],
        ["(", "<expression>", ")"],
        ["!", "(", "<expression>", ")"]],

    "<condition_operator>": [
        ["=="], ["!="], ["<"], [">"], ["<="], [">="], 
        ["&&"], ["||"], ["is"], ["isnot"], ["ins"], ["notin"]],

    "<display_content>": [
        ["<displayval>", "<display_tail>"],
        ["λ"]],

    "<display_tail>": [
        ["+", "<displayval>", "<display_tail>"],
        ["λ"]],

    "<return_stmt>": [
        ["return", "<arithmetic_exp>", ";"]],

    "<displayval>": [
        ["string_literal"],
        ["identifier", "<value_id_tail>"]],

}

def compute_first_set(cfg):
    first_set = {non_terminal: set() for non_terminal in cfg.keys()}

    def first_of(symbol):
        if symbol not in cfg:
            return {symbol} 

        if symbol in first_set and first_set[symbol]:
            return first_set[symbol]

        result = set()
        
        for production in cfg[symbol]:
            for sub_symbol in production:
                if sub_symbol not in cfg: # terminal
                    result.add(sub_symbol)
                    break  
                else: # non-terminal
                    sub_first = first_of(sub_symbol)
                    result.update(sub_first - {"λ"})  
                    if "λ" not in sub_first:
                        break  
            
            else: # all symbols in the production derive λ
                result.add("λ")

        first_set[symbol] = result
        return result

    for non_terminal in cfg:
        first_of(non_terminal)

    return first_set

def compute_follow_set(cfg, start_symbol, first_set):
    follow_set = {non_terminal: set() for non_terminal in cfg.keys()}
    follow_set[start_symbol].add("$")  

    changed = True  

    while changed:
        changed = False 
    
        for non_terminal, productions in cfg.items():
            for production in productions:
                for i, item in enumerate(production):
                    if item in cfg:  # nt only
                        follow_before = follow_set[item].copy()

                        if i + 1 < len(production):  # A -> <alpha>B<beta>
                            beta = production[i + 1]
                            if beta in cfg:  # if <beta> is a non-terminal
                                follow_set[item].update(first_set[beta] - {"λ"})
                                if "λ" in first_set[beta]:
                                    follow_set[item].update(follow_set[beta])
                            else:  # if <beta> is a terminal
                                follow_set[item].add(beta)
                        else:  # nothing follows B
                            follow_set[item].update(follow_set[non_terminal])

                        if follow_set[item] != follow_before:
                            changed = True  

    return follow_set

def compute_predict_set(cfg, first_set, follow_set):
    predict_set = {}  

    for non_terminal, productions in cfg.items():
        for production in productions:
            production_key = (non_terminal, tuple(production))  # A = (A,(prod))
            predict_set[production_key] = set()

            first_alpha = set()
            for symbol in production:
                if symbol in first_set:  # non-terminal
                    first_alpha.update(first_set[symbol] - {"λ"})
                    if "λ" not in first_set[symbol]:
                        break
                else:  # terminal
                    first_alpha.add(symbol)
                    break
            else:  
                first_alpha.add("λ")

            predict_set[production_key].update(first_alpha - {"λ"})

            # if λ in first_alpha, add follow set of lhs to predict set
            if "λ" in first_alpha:
                predict_set[production_key].update(follow_set[non_terminal])

    return predict_set

def gen_parse_table():
    parse_table = {}
    for (non_terminal, production), predict in predict_set.items():
        if non_terminal not in parse_table:
            parse_table[non_terminal] = {}
        for terminal in predict:
            if terminal in parse_table[non_terminal]:
                raise ValueError(f"Grammar is not LL(1): Conflict in parse table for {non_terminal} and {terminal}")
            parse_table[non_terminal][terminal] = production

    return parse_table  

first_set = compute_first_set(cfg)
follow_set = compute_follow_set(cfg, "<program>", first_set)
predict_set = compute_predict_set(cfg, first_set, follow_set)
parse_table = gen_parse_table()

class ParseTreeNode:
    def __init__(self, symbol, lexeme=None, line=None, column=None):
        self.symbol = symbol  # Grammar symbol (terminal or non-terminal)
        self.lexeme = lexeme  # Actual text for terminals
        self.line = line      # Line number
        self.column = column  # Column number
        self.children = []
        self.parent = None

    def add_child(self, child):
        if child:
            child.parent = self
            self.children.append(child)
            
    def __str__(self, level=0):
        indent = "  " * level
        if self.symbol in cfg:  # Non-terminal
            result = f"{indent}{self.symbol}\n"
        else:  # Terminal
            if self.lexeme:
                result = f"{indent}{self.symbol}\n"
            else:
                result = f"{indent}{self.symbol}\n"
                
        for child in self.children:
            result += child.__str__(level + 1)
        return result
        
    def print_tree(self):
        """Print the parse tree with proper indentation."""
        print(self.__str__())

class LL1Parser:
    def __init__(self, cfg, parse_table, follow_set):
        self.cfg = cfg
        self.parse_table = parse_table
        self.follow_set = follow_set
        self.node_stack = []  # Stack for parse tree nodes
        self.symbol_stack = []  # Stack for grammar symbols
        self.input_tokens = []
        self.index = 0
        self.parse_tree = None
        self.errors = []

    def parse(self, tokens):
        # Initialize stacks
        self.symbol_stack = ["$", "<program>"]  # Start with end marker and start symbol
        self.input_tokens = tokens + [("$", "$", -1, 0)]  # Append EOF
        self.index = 0
        self.errors = []
        
        # Create root node for the parse tree
        root = ParseTreeNode("<program>")
        self.node_stack = [None, root]  # Match with symbol stack ($ has no node)
        self.parse_tree = root
        
        while self.symbol_stack:
            top_symbol = self.symbol_stack.pop()
            top_node = self.node_stack.pop()
            
            current_lexeme = self.input_tokens[self.index][0]
            current_token = self.input_tokens[self.index][1]  # Token type
            current_line = self.input_tokens[self.index][2]   # Line number
            current_column = self.input_tokens[self.index][3] # Column position

            # print(f"Stack: {self.symbol_stack}, Top: {top_symbol}, Token: {current_token}, Column: {current_column}")  # Debugging line

            # Skip lambda productions
            if top_symbol == "λ":
                # Add lambda node to parent
                if top_node:
                    lambda_node = ParseTreeNode("λ")
                    top_node.add_child(lambda_node)
                continue

            # Terminal match
            if top_symbol not in self.cfg:  # It's a terminal
                if top_symbol == current_token:
                    self.index += 1
                else:
                    # Terminal mismatch - syntax error
                    self.syntax_error(current_line, current_lexeme, {top_symbol}, current_column)
                    return False, self.errors, None
            
            # Non-terminal processing
            elif top_symbol in self.cfg:  # It's a non-terminal
                if current_token in self.parse_table.get(top_symbol, {}):
                    production = self.parse_table[top_symbol][current_token]
                    
                    # Create nodes for each symbol in the production
                    # Reversed twice to maintain correct order in the tree
                    # (stack is LIFO, so we push in reverse)
                    temp_nodes = []
                    for symbol in production:
                        if symbol != "λ":  # Handle non-lambda symbols
                            new_node = ParseTreeNode(symbol)
                            temp_nodes.append((symbol, new_node))
                        else:  # Handle lambda explicitly
                            lambda_node = ParseTreeNode("λ")
                            if top_node:
                                top_node.add_child(lambda_node)
                    
                    # Add nodes to parent in correct order (left to right)
                    for symbol, node in temp_nodes:
                        if top_node:
                            top_node.add_child(node)
                    
                    # Push to stacks in reverse order (for correct processing order)
                    for symbol, node in reversed(temp_nodes):
                        self.symbol_stack.append(symbol)
                        self.node_stack.append(node)
                else:
                    # No production rule - syntax error
                    expected_tokens = set(self.parse_table.get(top_symbol, {}).keys())
                    self.syntax_error(current_line, current_lexeme, expected_tokens, current_column)
                    return False, self.errors, None
            
            # End marker
            elif top_symbol == "$":
                if current_token == "$":
                    break
                else:
                    self.syntax_error(current_line, current_lexeme, {"$"}, current_column)
                    return False, self.errors, None
        
        # Check if we processed all input
        if self.index < len(self.input_tokens) - 1:
            remaining_token = self.input_tokens[self.index]
            self.syntax_error(remaining_token[2], remaining_token[0], {"EOF"}, remaining_token[3])
            return False, self.errors, None

        return True, [], self.parse_tree

    def syntax_error(self, line, found, expected, column):
        """Record a syntax error with correct expected tokens and line number."""
        if line == -1 and column == 0:  # Use last valid line number if not set
            line = self.input_tokens[self.index - 1][2] if self.index > 0 else 1
            column = self.input_tokens[self.index - 1][3] if self.index > 0 else 1
        
        if not self.symbol_stack:  
            # Stack is empty → only report unexpected token
            error_message = f"❌ Syntax Error at (line {line}, column {column}): Unexpected '{found}'"
        elif found == '$':  
            # Special case: No unexpected token, just missing expected ones
            error_message = f"❌ Syntax Error at (line {line}, column {column}): Missing expected token(s): {', '.join(expected)}"
        else:
            # Normal case: Unexpected token + expected tokens
            error_message = f"❌ Syntax Error at (line {line}, column {column}): Unexpected '{found}' (Expected {', '.join(expected)})"

        self.errors.append(error_message)
       



# Run Parser
# parser = LL1Parser(cfg, parse_table, follow_set)
# parser.parse(tokens)

# for non_terminal, productions in cfg.items():
#     for i, item in enumerate(productions):
#         print(f"-{productions[i]}-")

# print("First Sets:")
# for non_terminal, first in first_set.items():
#     first_str = ", ".join(first)
#     print(f"-[{first_str}]-")

# print("\nFollow Sets:")
# for non_terminal, follow in follow_set.items():
#     follow_str = ", ".join(follow)
#     print(f"-[{follow_str}]-")

# def display_predict_sets(predict_set):
#     print("\nPredict Sets:")
#     for (non_terminal, production), predict in predict_set.items():
#         production_str = " ".join(production)
#         print(f"First({production_str})=")

# display_predict_sets(predict_set)

# def display_parse_table(parse_table):
#     print()
#     for non_terminal, rules in parse_table.items():
#         print(f"{non_terminal}")
#         for terminal, production in rules.items():
#             print(f"  Terminal: {terminal} -> Production: {production}")
#         print()  

# display_parse_table(parse_table)

def check_ambiguity(cfg, predict_set):
    ambiguous_productions = []

    for non_terminal, productions in cfg.items():
        prediction_sets = [predict_set[(non_terminal, tuple(prod))] for prod in productions]
        for i in range(len(prediction_sets)):
            for j in range(i + 1, len(prediction_sets)):
                if prediction_sets[i].intersection(prediction_sets[j]):
                    ambiguous_productions.append((non_terminal, productions[i], productions[j]))

    if ambiguous_productions:
        print("\nAmbiguities found in the CFG:")
        for non_terminal, prod1, prod2 in ambiguous_productions:
            print(f"  {non_terminal} -> {prod1} | {prod2}")
    else:
        print("\nNo ambiguities found in the CFG.")

check_ambiguity(cfg, predict_set)