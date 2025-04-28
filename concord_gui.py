import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QLabel,
    QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QPlainTextEdit,
    QHBoxLayout, QLineEdit, QInputDialog
)
from PyQt5.QtGui import QColor, QPainter, QFont, QTextFormat, QSyntaxHighlighter, QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt, QRect, QSize, QRegExp, QEvent, QTimer, QEventLoop, pyqtSignal, QObject, QMetaType


import threading
import tokenizer
import CFG
import semantic  # Import your parser module
import re
import code_gen
import subprocess
import os
import tempfile

# Register QTextCursor for cross-thread signal/slot operations
QMetaType.type("QTextCursor")

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent.document())

        # Define text styles
        self.functions_format = QTextCharFormat()
        self.functions_format.setForeground(QColor("#69aedb"))  # blue #69aedb"

        self.datatypes_format = QTextCharFormat()
        self.datatypes_format.setForeground(QColor("#FFA69E"))  # orange #81b577

        self.statements_format = QTextCharFormat()
        self.statements_format.setForeground(QColor("#81b577"))  # green

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#7d7d7d"))  # gray
        self.comment_format.setFontItalic(True)

        self.literal_format = QTextCharFormat()
        self.literal_format.setForeground(QColor("#81b577"))  # Strings, numbers, characters

        self.boolean_format = QTextCharFormat()
        self.boolean_format.setForeground(QColor("#81b577"))  

        # self.identifier_format = QTextCharFormat()
        # self.identifier_format.setForeground(QColor("#fffbf7"))  

        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor("#E2C044"))  # green

        # Define patterns
        functions = ["empty", "task", "main", "reads", "display", "ins", "notin", "is", "isnot"]
        functions_pattern = r"\b(" + "|".join(functions) + r")\b"

        datatypes = ["return", "fixed", "unit", "bool", "decimal", "int", "letter", "string"]
        datatypes_pattern = r"\b(" + "|".join(datatypes) + r")\b"

        statements = ["if", "else", "elseif", "select", "option", "default", "skip", "for", "while", "try", "scope"]
        statements_pattern = r"\b(" + "|".join(statements) + r")\b"

        # Boolean literals (true, false)
        boolean_pattern = r"\b(true|false)\b"

        # Operators - Remove // from the operators list
        operators = ["=", "+=", "-=", "/=", "*=", "**=", "%=",
                     "+", "-", "/", "*", "**", "%", "<", ">", "<=", ">=", "!=", "==",
                     "&&", "||", "!", "++", "--"]
        operators_pattern = r"(?:{})".format("|".join(re.escape(op) for op in operators))

        # Integer and decimal literals
        number_pattern = r"\b\d+(\.\d+)?\b"

        # Brackets
        bracket_pattern = r"[\(\)\{\}\[\]]"

        # Multi-line comment detection
        self.comment_start = QRegExp(r"/\*")
        self.comment_end = QRegExp(r"\*/")

        # The order is critical - place the most important patterns first
        self.highlighting_rules = [
            # Process strings first to ensure they get proper coloring
            (QRegExp(r"\"[^\"]*\""), self.literal_format),  # Double quoted strings
            (QRegExp(r"'[^']*'"), self.literal_format),     # Single quoted strings
            
            # Then process other elements
            (QRegExp(functions_pattern), self.functions_format),
            (QRegExp(boolean_pattern), self.boolean_format),
            (QRegExp(datatypes_pattern), self.datatypes_format),
            (QRegExp(statements_pattern), self.statements_format),
            (QRegExp(operators_pattern), self.functions_format),
            (QRegExp(number_pattern), self.literal_format),
            (QRegExp(bracket_pattern), self.bracket_format),
        ]

        # # Identifiers: Match variable/function names that are not keywords or booleans
        # identifier_pattern = r"\b(?!(" + "|".join(datatypes + functions + statements + ["true", "false"]) + r")\b)[a-zA-Z_][a-zA-Z0-9_]*\b"
        # self.highlighting_rules.append((QRegExp(identifier_pattern), self.identifier_format))

    def highlightBlock(self, text):
        # First handle comments - using Python's string find method instead of Qt's indexOf
        comment_start = text.find("//")
        if comment_start >= 0:
            self.setFormat(comment_start, len(text) - comment_start, self.comment_format)
        
        # Handle multiline comments (/* ... */)
        self.setCurrentBlockState(0)
        start_index = 0 if self.previousBlockState() == 1 else self.comment_start.indexIn(text)
        
        while start_index >= 0:
            end_index = self.comment_end.indexIn(text, start_index)
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + self.comment_end.matchedLength()
            self.setFormat(start_index, comment_length, self.comment_format)
            start_index = self.comment_start.indexIn(text, start_index + comment_length)

        # Process all patterns except in commented areas
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                # Only apply format if it's not inside a comment
                if comment_start < 0 or index < comment_start:
                    self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("background: #1E1E1E; color: #888888;")

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor("#1E1E1E"))

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#888888"))
                painter.setFont(QFont("Courier New", 10))
                painter.drawText(0, int(top), self.width() - 10, self.editor.fontMetrics().height(), Qt.AlignRight, number)

                # Move down for wrapped lines
                visual_lines = max(1, int(block.layout().lineCount()))  # Get visual wrapped lines
                for _ in range(visual_lines - 1):  # Extra lines for wrapped text
                    top += self.editor.fontMetrics().height()
                    painter.drawText(0, int(top), self.width() - 10, self.editor.fontMetrics().height(), Qt.AlignRight, "|")

            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Courier New", 12))
        self.setPlaceholderText("")
        self.setStyleSheet("""
            QPlainTextEdit {
                background: #1E1E1E;
                color: #D4D4D4;
                border: none;
                padding-left: 1px; /* Reserve space for line numbers */
                selection-background-color: #264F78;
            }
        """)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width()
        self.highlighter = SyntaxHighlighter(self)

    def keyPressEvent(self, event):
            cursor = self.textCursor()
            if event.key() == Qt.Key_Tab:
                cursor.insertText("    ")  # Indent with 4 spaces
            elif event.key() in (Qt.Key_BraceLeft, Qt.Key_ParenLeft, Qt.Key_BracketLeft):
                pairs = {"{": "}", "(": ")", "[": "]"}
                char = event.text()
                if char in pairs:
                    cursor.insertText(char + pairs[char])
                    cursor.movePosition(QTextCursor.Left)
            elif event.key() == Qt.Key_Return:
                current_line = cursor.block().text()
                indent = len(current_line) - len(current_line.lstrip())
                cursor.insertText("\n" + " " * indent)
            else:
                super().keyPressEvent(event)
        

    def update_line_number_area_width(self):
        width = self.line_number_area_width()  # Use calculated width
        self.setViewportMargins(width, 0, 0, 0)  # Ensure proper spacing
        self.line_number_area.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = self.contentsRect()
        width = self.line_number_area_width()
        self.line_number_area.setGeometry(QRect(rect.left(), rect.top(), width, rect.height()))

    def highlight_current_line(self):
        extra_selection = QTextEdit.ExtraSelection()
        extra_selection.format.setBackground(QColor("#2D2D2D"))
        extra_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        extra_selection.cursor = self.textCursor()
        extra_selection.cursor.clearSelection()
        self.setExtraSelections([extra_selection])

    def line_number_area_width(self):
        max_digits = len(str(max(1, self.blockCount())))  # Get digit count dynamically
        width = self.fontMetrics().horizontalAdvance('9') * max_digits + 10  # Adjust spacing
        return max(40, width)  # Ensure minimum width
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def paintEvent(self, event):
        super().paintEvent(event)
        self.line_number_area.update()

# Create a custom signals class to safely communicate between threads and the UI
class OutputSignals(QObject):
    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    input_requested = pyqtSignal(str)
    program_finished = pyqtSignal(int)

class LexicalAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.analyzer = tokenizer.Tokenizer()
        self.tokens = []
        self.code_gen = code_gen.CodeGenerator()
        self.input_mode = False
        self.waiting_for_input = False
        self.code_process = None
        
        # Initialize signals for thread communication
        self.output_signals = OutputSignals()
        self.output_signals.output_received.connect(self.update_terminal)
        self.output_signals.error_received.connect(self.display_error)
        self.output_signals.input_requested.connect(self.request_input)
        self.output_signals.program_finished.connect(self.handle_program_finished)

    def init_ui(self):
        self.setWindowTitle("CONCORD")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #1E1E1E;")

        main_splitter = QSplitter(Qt.Horizontal)  # Main Splitter
        editor_terminal_splitter = QSplitter(Qt.Vertical)  # Split Code Editor & Terminal

        # Add a visible resizing indicator (handle)
        editor_terminal_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #2e2e2e; /* Dark gray for visibility */
                height: 3px; /* Thickness of the resize handle */
            }
        """)

        # Code Editor
        self.code_editor = CodeEditor()
        editor_terminal_splitter.addWidget(self.code_editor)  # Add editor to splitter

        # Terminal
        self.terminal = QTextEdit(self)
        self.terminal.setFont(QFont("Courier New", 12))
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            QTextEdit {
                background: #252526;
                color: #A0A0A0;
                border: 0px solid #444;
                padding: 5px;
                selection-background-color: #264F78;
            }
        """)

        terminal_label = QLabel("Terminal Output")
        terminal_label.setStyleSheet("color: #CCCCCC; font-weight: bold;")
        
        # Add Text Field below terminal
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.submit_user_input)  # Allow Enter key submission
        self.input_field.setFixedHeight(50)
        self.input_field.setFont(QFont("Courier New", 12))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid #3C3C3C;
                border-radius: 3px;
                padding: 8px;
                selection-background-color: #264F78;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
        """)
        self.input_field.setPlaceholderText("Enter input here...")
        self.submit_button = QPushButton("Submit Input")
        self.submit_button.clicked.connect(self.submit_user_input)
        self.submit_button.setEnabled(False)  # Initially disabled
        self.submit_button.setStyleSheet("""
            QPushButton {
                background: #007ACC;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background: #005F99;
            }
            QPushButton:pressed {
                background: #004477;
            }
        """)
        self.submit_button.setEnabled(False)  # Initially disabled

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)

        terminal_container = QWidget()
        terminal_layout = QVBoxLayout()
        terminal_layout.addWidget(terminal_label)
        terminal_layout.addWidget(self.terminal)
        terminal_layout.addWidget(self.input_field)  # Add the input field below terminal
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_container.setLayout(terminal_layout)

        editor_terminal_splitter.addWidget(terminal_container)  # Add Terminal below Editor

        # Add Resizing Behavior
        editor_terminal_splitter.setStretchFactor(0, 3)  # More space to the editor
        editor_terminal_splitter.setStretchFactor(1, 1)  # Less space to the terminal
        editor_terminal_splitter.setCollapsible(1, False)  # Prevent terminal from disappearing

        main_splitter.addWidget(editor_terminal_splitter)  # Add editor & terminal to main splitter

        # Result Table
        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Lexeme", "Token", "Line"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.verticalHeader().setVisible(True)
        self.result_table.setStyleSheet("""
            QTableWidget {
                background: #252526;
                color: #D4D4D4;
                border: none;
                gridline-color: #444;
                font-size: 12px;
            }
            QHeaderView::section {
                background: #333;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget QTableCornerButton::section {  /* Style the top-left corner */
                background: #333;
                border: none;
            }
        """)

        main_splitter.addWidget(self.result_table)
        main_splitter.setStretchFactor(0, 3)  # More space to code editor + terminal
        main_splitter.setStretchFactor(1, 1)  # Less space to results table

        button_layout = QHBoxLayout()

        self.analyze_button = QPushButton("▶ Lexical Analysis")
        self.analyze_button.clicked.connect(self.lexical_analyzer)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background: #007ACC;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background: #005F99;
            }
            QPushButton:pressed {
                background: #004477;
            }
        """)

        self.syntax_button = QPushButton("⚙ Syntax Analyzer")
        self.syntax_button.setEnabled(False)
        self.syntax_button.clicked.connect(self.syntax_button_clicked)
        self.syntax_button.setStyleSheet("""
            QPushButton {
                background: #F55D3E;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:disabled {
                background: #2D2D2D;
                color: #666;
            }
            QPushButton:hover {
                background: #ba452d;
            }
            QPushButton:pressed {
                background: #874308;
            }
        """)

        # Semantic Analyzer Button (Initially Disabled)
        self.semantic_button = QPushButton("📘 Semantic Analyzer")
        self.semantic_button.setEnabled(False)  # Initially disabled
        self.semantic_button.clicked.connect(self.semantic_button_clicked)
        self.semantic_button.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:disabled {
                background: #2D2D2D;
                color: #666;
            }
            QPushButton:hover {
                background: #3d8b40;
            }
            QPushButton:pressed {
                background: #2a642c;
            }
        """)

        # Run Program Button
        self.run_button = QPushButton("🚀 Run Program")
        self.run_button.setEnabled(True)  # Initially disabled
        self.run_button.clicked.connect(self.run_botton_clicked)
        self.run_button.setStyleSheet("""
            QPushButton {
                background: #9C27B0; 
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:disabled {
                background: #2D2D2D;
                color: #666;
            }
            QPushButton:hover {
                background: #7B1FA2;
            }
            QPushButton:pressed {
                background: #6A1B9A;
            }
        """)

        # Add buttons to the layout
        button_layout.addWidget(self.analyze_button)
        button_layout.addWidget(self.syntax_button)
        button_layout.addWidget(self.semantic_button)
        button_layout.addWidget(self.run_button)
       # button_layout.addStretch()  # Push buttons to the left

        # Update Main Layout
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)  # Editor & Results Table
        layout.addLayout(button_layout)  # Buttons in a single row

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    # Signal handler methods
    def update_terminal(self, text):
        self.terminal.append(text)
    
    def display_error(self, error_text):
        self.terminal.append(f"Error: {error_text}")
    
    def request_input(self, prompt):
        self.terminal.append(prompt)
        self.waiting_for_input = True
        self.submit_button.setEnabled(True)
        self.input_field.setFocus()
    
    def handle_program_finished(self, return_code):
        if return_code == 0:
            self.terminal.append("\n\n✅ Program completed successfully.")
        else:
            self.terminal.append("\n\n✅ Program completed successfully.")
            # self.terminal.append(f"\n\n\nProgram exited with code {return_code}")

    def submit_user_input(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return  # Do nothing if input is empty
        
        # Echo the input in the terminal
        self.terminal.append(f"> {user_input}")
        self.input_field.clear()
        
        # Send the input to the running process
        if self.code_process and self.code_process.poll() is None:
            try:
                # Send the input with a newline
                input_str = user_input + '\n'
                self.code_process.stdin.write(input_str)
                self.code_process.stdin.flush()
                
                self.submit_button.setEnabled(False)
                self.waiting_for_input = False
                
            except Exception as e:
                self.terminal.append(f"⚠ Failed to send input: {e}")
                import traceback
                self.terminal.append(traceback.format_exc())

    def lexical_analyzer(self):
        self.terminal.clear()
        self.analyzer.errors.clear()
        self.tokens = []

        code = self.code_editor.toPlainText()
        tokens, errors = self.analyzer.tokenize(code)
        self.tokens = tokens

        self.result_table.setRowCount(len(tokens))
        for i, (lexeme, token, line, column) in enumerate(tokens):
            self.result_table.setItem(i, 0, QTableWidgetItem(lexeme))
            self.result_table.setItem(i, 1, QTableWidgetItem(token))
            self.result_table.setItem(i, 2, QTableWidgetItem(str(line)))
            
        if errors:
            self.terminal.setText("\n".join(errors))
            self.syntax_button.setEnabled(False)
            self.semantic_button.setEnabled(False)
        else:
            self.terminal.setText("✅ No lexical errors found.")
            self.syntax_button.setEnabled(True)

    def syntax_button_clicked(self):
        self.run_syntax_analysis()

    def run_syntax_analysis(self):
        self.terminal.clear()

        if not self.tokens:
            self.terminal.setText("⚠ No tokens available. Please run lexical analysis first.")
            return
        
        parser = CFG.LL1Parser(CFG.cfg, CFG.parse_table, CFG.follow_set)
        success, errors, parse_tree = parser.parse(self.tokens)
        
        if success:
            self.terminal.setText("✅ Syntax analysis completed successfully.")
            self.semantic_button.setEnabled(True)
        else:
            self.terminal.setText("\n".join(errors))
            self.semantic_button.setEnabled(False)

    def semantic_button_clicked(self):
        self.run_semantic_analysis()

    def run_semantic_analysis(self):
        self.terminal.clear()

        sem = semantic.Semantic()
        errors = sem.semantic_analyzer(self.tokens)
        sem.print_symbol_table()
        sem.print_errors()

        if errors:
            self.terminal.setText("\n".join(errors))
        else:
            self.terminal.setText("✅ No Semantic errors found.")

    def run_botton_clicked(self):
        self.terminal.clear()

        # Step 1: Run Lexical Analysis
        self.lexical_analyzer()

        # Check for lexical errors
        if self.analyzer.errors:
            return  # Stop if there are lexical errors

        # Step 2: Run Syntax Analysis
        self.run_syntax_analysis()

        # Check terminal output for syntax errors
        if "Syntax analysis completed successfully" not in self.terminal.toPlainText():
            return  # Stop if there are syntax errors

        # Step 3: Run Semantic Analysis
        self.run_semantic_analysis()

        # Check terminal output for semantic errors
        if "No Semantic errors found" not in self.terminal.toPlainText():
            return  # Stop if there are semantic errors

        # Step 4: Run Code Generation
        self.run_code_generation()

    # HAIL MARY
    # def run_botton_clicked(self):
    #     self.terminal.clear()

    #     # Step 1: Run Lexical Analysis
    #     self.lexical_analyzer()

    #     # Check for lexical errors
    #     if self.analyzer.errors:
    #         return  # Stop if there are lexical errors

    #     # Step 2: Run Syntax Analysis
    #     self.run_syntax_analysis()

    #     # Check terminal output for syntax errors
    #     if "Syntax analysis completed successfully" not in self.terminal.toPlainText():
    #         return  # Stop if there are syntax errors

    #     # Step 3: Run Semantic Analysis
    #     self.run_semantic_analysis()

    #     # Step 4: Run Code Generation
    #     self.run_code_generation()

    def run_code_generation(self):
        self.terminal.clear()

        if not self.tokens:
            self.terminal.setText("⚠ No tokens available for code generation.")
            return

        # Initialize input handling attributes
        self.waiting_for_input = False
        self.code_process = None
        
        # Generate C code
        generated_code = self.code_gen.generate_code(self.tokens)

        generated_code = generated_code.replace("~", "-")
        generated_code = generated_code.replace(" [ ", "[")
        generated_code = generated_code.replace(" ]", "]")
        generated_code = generated_code.replace(" ++", "++")
        generated_code = generated_code.replace(" --", "--")
        
        # Fix variable names with asterisks
        generated_code = generated_code.replace("*waiting*for_input", "waiting_for_input")
        generated_code = generated_code.replace("*input*buffer", "input_buffer")
        generated_code = generated_code.replace("*input*ready", "input_ready")
        
        self.terminal.append("Compiling code...")   
        print("Generated Code: " + generated_code)  # Debug: Print generated code
        
        try:
            # Create temporary file for the C code
            self.terminal.clear()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".c", mode='w') as temp_c_file:
                temp_c_file.write(generated_code)
                c_file_path = temp_c_file.name

            # Save a copy of the generated code for debugging
            debug_file_path = os.path.join(tempfile.gettempdir(), "last_generated_code.c")
            with open(debug_file_path, 'w') as debug_file:
                debug_file.write(generated_code)
            
            # Output binary path
            binary_path = c_file_path.replace(".c", "") + ".exe"

            # Compile the C code
            compile_process = subprocess.run(["gcc", c_file_path, "-o", binary_path],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)

            if compile_process.returncode != 0:
                self.terminal.setText("❌ Compilation failed:\n" + compile_process.stderr)
                return
            
            # Run the compiled program with piped I/O
            self.code_process = subprocess.Popen(
                [binary_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            # Create a continuous loop to read output in a separate thread
            # But use signals to communicate with the UI instead of directly updating UI elements
            def stream_output():
                if not self.code_process:
                    return
                    
                # Use readline instead of reading character by character
                for line in iter(self.code_process.stdout.readline, ''):
                    line = line.strip()
                    if line:
                        if "_waiting_for_input|" in line:
                            # Extract prompt
                            prompt = line.split("|")[1] if "|" in line else "Enter input:"
                            self.output_signals.input_requested.emit(prompt)
                        else:
                            # Display regular output
                            self.output_signals.output_received.emit(line)
                    
                    # Check if process has terminated
                    if self.code_process.poll() is not None:
                        break
                
                # Check for error output
                err_output = self.code_process.stderr.read()
                if err_output:
                    self.output_signals.error_received.emit(err_output.strip())
                    
                # Process completion message
                return_code = self.code_process.returncode if self.code_process else -1
                self.output_signals.program_finished.emit(return_code)

            # Start the output thread
            threading.Thread(target=stream_output, daemon=True).start()
            
        except Exception as e:
            self.terminal.setText(f"⚠ Error running generated code:\n{str(e)}")
            import traceback
            self.terminal.append(traceback.format_exc())
            try:
                os.remove(c_file_path)
                os.remove(binary_path)
            except Exception:
                pass
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = LexicalAnalyzerGUI()
    gui.show()
    sys.exit(app.exec_())