import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QLabel,
    QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QPlainTextEdit,
    QHBoxLayout, QLineEdit, QInputDialog, QStatusBar, QToolBar, QAction, QSizePolicy
)
from PyQt5.QtGui import QColor, QPainter, QFont, QTextFormat, QSyntaxHighlighter, QTextCharFormat, QTextCursor, QIcon
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

        self.bracket_format = QTextCharFormat()
        self.bracket_format.setForeground(QColor("#E2C044"))  # yellow

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

        # String patterns
        self.double_quote_pattern = QRegExp(r'"(?:\\.|[^"\\])*"')
        self.single_quote_pattern = QRegExp(r"'(?:\\.|[^'\\])*'")

        # The order is critical - we'll process strings and comments first
        self.string_patterns = [
            self.double_quote_pattern,
            self.single_quote_pattern
        ]

        # Then other highlighting rules
        self.highlighting_rules = [
            (QRegExp(functions_pattern), self.functions_format),
            (QRegExp(boolean_pattern), self.boolean_format),
            (QRegExp(datatypes_pattern), self.datatypes_format),
            (QRegExp(statements_pattern), self.statements_format),
            (QRegExp(operators_pattern), self.functions_format),
            (QRegExp(number_pattern), self.literal_format),
            (QRegExp(bracket_pattern), self.bracket_format),
        ]

    def highlightBlock(self, text):
        # Clear any previous formatting
        self.setCurrentBlockState(0)

        # First, find all string regions to exclude them from other highlighting
        string_regions = []
        for pattern in self.string_patterns:
            index = 0
            while index >= 0:
                index = pattern.indexIn(text, index)
                if index >= 0:
                    length = pattern.matchedLength()
                    string_regions.append((index, index + length))
                    self.setFormat(index, length, self.literal_format)
                    index += length

        # Handle single-line comments
        comment_start = text.find("//")
        if comment_start >= 0:
            self.setFormat(comment_start, len(text) - comment_start, self.comment_format)
            # Add comment region to exclusion list
            string_regions.append((comment_start, len(text)))
        
        # Handle multiline comments (/* ... */)
        in_multiline = self.previousBlockState() == 1
        if in_multiline:
            start_index = 0
            end_index = self.comment_end.indexIn(text)
            
            if end_index == -1:
                # Comment continues to next line
                self.setFormat(0, len(text), self.comment_format)
                self.setCurrentBlockState(1)
                return  # Skip other highlighting
            else:
                # End of multiline comment in this block
                comment_length = end_index + self.comment_end.matchedLength()
                self.setFormat(0, comment_length, self.comment_format)
                string_regions.append((0, comment_length))
        else:
            # Check for new multiline comment start
            start_index = self.comment_start.indexIn(text)
            if start_index >= 0:
                # Check if comment ends in this line
                end_index = self.comment_end.indexIn(text, start_index)
                if end_index == -1:
                    # Comment continues to next line
                    self.setFormat(start_index, len(text) - start_index, self.comment_format)
                    self.setCurrentBlockState(1)
                    string_regions.append((start_index, len(text)))
                else:
                    # Comment ends in this line
                    comment_length = end_index - start_index + self.comment_end.matchedLength()
                    self.setFormat(start_index, comment_length, self.comment_format)
                    string_regions.append((start_index, start_index + comment_length))

        # Now apply other rules, but only to non-string and non-comment regions
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = 0
            while index >= 0:
                index = expression.indexIn(text, index)
                if index >= 0:
                    length = expression.matchedLength()
                    
                    # Check if this match is within a string or comment region
                    is_in_excluded_region = False
                    for start, end in string_regions:
                        if index >= start and index < end:
                            is_in_excluded_region = True
                            break
                    
                    if not is_in_excluded_region:
                        self.setFormat(index, length, format)
                        
                    index += length

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("background: #202020; color: #888888;")

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor("#202020"))

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#888888"))
                painter.setFont(QFont("Consolas", 10))
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
        self.setFont(QFont("Consolas", 12))
        self.setPlaceholderText("")
        self.setStyleSheet("""
            QPlainTextEdit {
                background: #202020;
                color: #D4D4D4;
                border: none;
                padding-left: 1px; /* Reserve space for line numbers */
                selection-background-color: #264F78;
            }
            QScrollBar:vertical {
                background: #202020;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #616161;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                background: #202020;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #424242;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #616161;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                border: none;
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width()
        self.highlighter = SyntaxHighlighter(self)
        self.bracket_pairs = {"{": "}", "(": ")", "[": "]", '"': '"', "'": "'"}
        self.bracket_state = {}  # Track bracket positions

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        
        if event.key() == Qt.Key_Tab:
            cursor.insertText("    ")  # Indent with 4 spaces
        elif event.key() == Qt.Key_Backspace:
            # Get current position and the character before it
            position = cursor.position()
            if position > 0:
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                current_char = cursor.selectedText()
                
                # Reset the cursor position
                cursor.setPosition(position)
                
                # Check if we're between a pair of brackets
                if position > 0 and position < self.document().characterCount():
                    cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                    left_char = cursor.selectedText()
                    cursor.setPosition(position)
                    
                    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                    right_char = cursor.selectedText()
                    cursor.setPosition(position)
                    
                    # If deleting an opening bracket with its closing bracket right after it
                    if left_char in self.bracket_pairs and right_char == self.bracket_pairs[left_char]:
                        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                        cursor.removeSelectedText()
                        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                        cursor.removeSelectedText()
                        return
            
            # Default backspace behavior
            super().keyPressEvent(event)
            
        elif event.key() in (Qt.Key_BraceLeft, Qt.Key_ParenLeft, Qt.Key_BracketLeft, 
                            Qt.Key_QuoteDbl, Qt.Key_Apostrophe):
            char = event.text()
            if char in self.bracket_pairs:
                # Insert the pair and position cursor between them
                cursor.insertText(char + self.bracket_pairs[char])
                cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
                self.setTextCursor(cursor)
        elif event.key() in (Qt.Key_BraceRight, Qt.Key_ParenRight, Qt.Key_BracketRight,
                            Qt.Key_QuoteDbl, Qt.Key_Apostrophe):
            # Check if we're typing a closing bracket that already exists
            char = event.text()
            position = cursor.position()
            
            if position < self.document().characterCount():
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                next_char = cursor.selectedText()
                cursor.setPosition(position)  # Reset cursor
                
                # If the next character is the same as what we're typing, just move cursor
                if next_char == char:
                    cursor.movePosition(QTextCursor.Right)
                    self.setTextCursor(cursor)
                    return
            
            # If not skipping, insert normally
            super().keyPressEvent(event)
        elif event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            current_line = cursor.block().text()
            position_in_block = cursor.positionInBlock()

            # Determine current indentation (number of leading spaces)
            indent = len(current_line) - len(current_line.lstrip())

            # Text before the cursor in the current line
            text_before_cursor = current_line[:position_in_block].rstrip()

            if text_before_cursor.endswith('{'):
                # If the line ends with '{' before the cursor
                cursor.insertText('\n' + ' ' * (indent + 4))  # New line + increased indent
                cursor.insertText('\n' + ' ' * indent)  # New line + closing brace
                cursor.movePosition(QTextCursor.Up)
                cursor.movePosition(QTextCursor.EndOfLine)
                self.setTextCursor(cursor)
            else:
                # Normal behavior: just continue indenting as the current line
                cursor.insertText('\n' + ' ' * indent)
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
        self.setStyleSheet("background-color: #202020;")

        # Create toolbar for buttons at the top
        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(16, 16))
        self.toolbar.setStyleSheet("""
            QToolBar {
                background:#1c1c1c;
                border: none;
                padding: 10px;
                spacing: 10px;
            }
            QToolButton {
                color: white;
                font-weight: bold;
                border-radius: 3px;
                padding: 5px 10px;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.addToolBar(self.toolbar)

        # Create buttons instead of actions
        self.analyze_button = QPushButton("▶ Lexical Analysis")
        self.analyze_button.clicked.connect(self.lexical_analyzer)
        self.analyze_button.setStyleSheet("""
            background: #393939;
            color: white;
            font-weight: bold;
            border-radius: 3px;
            padding: 5px 10px;
        """)
        self.toolbar.addWidget(self.analyze_button)
        
        self.syntax_button = QPushButton("⚙ Syntax Analyzer")
        self.syntax_button.clicked.connect(self.syntax_button_clicked)
        self.syntax_button.setEnabled(False)
        self.syntax_button.setStyleSheet("""
            background: #393939;
            color: white;
            font-weight: bold;
            border-radius: 3px;
            padding: 5px 10px;
        """)
        self.toolbar.addWidget(self.syntax_button)
        
        self.semantic_button = QPushButton("📄 Semantic Analyzer")
        self.semantic_button.clicked.connect(self.semantic_button_clicked)
        self.semantic_button.setEnabled(False)
        self.semantic_button.setStyleSheet("""
            background: #393939;
            color: white;
            font-weight: bold;
            border-radius: 3px;
            padding: 5px 10px;
        """)
        self.toolbar.addWidget(self.semantic_button)

        # Spacer to push next button (Run) to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer.setStyleSheet("""
            background: #1c1c1c;
        """)
        self.toolbar.addWidget(spacer)
        
        self.run_button = QPushButton("▶ Run")
        self.run_button.clicked.connect(self.run_botton_clicked)
        self.run_button.setStyleSheet("""
            background: #254460;
            color: white;
            font-weight: bold;
            border-radius: 3px;
            padding: 5px 20px;
            margin-right:2px;
        """)
        self.toolbar.addWidget(self.run_button)
        
        
        # Add actions to toolbar
        # self.toolbar.addAction(self.analyze_action)
        # self.toolbar.addAction(self.syntax_action)
        # self.toolbar.addAction(self.semantic_action)
        # self.toolbar.addAction(self.run_action)

        main_splitter = QSplitter(Qt.Horizontal)  # Main Splitter
        editor_terminal_splitter = QSplitter(Qt.Vertical)  # Split Code Editor & Terminal

        # Add a visible resizing indicator (handle)
        editor_terminal_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #2e2e2e; /* Dark gray for visibility */
                height: 1px; /* Thinner VSCode-like handle */
            }
        """)

        # Code Editor
        self.code_editor = CodeEditor()
        editor_terminal_splitter.addWidget(self.code_editor)  # Add editor to splitter

        # Terminal
        self.terminal = QTextEdit(self)
        self.terminal.setFont(QFont("Consolas", 11))
        self.terminal.setReadOnly(True)
        self.terminal.document().setMaximumBlockCount(5000)  # Increase line limit
        self.terminal.setStyleSheet("""
            QTextEdit {
                background: #202020;
                color: #CCCCCC;
                border: 1px solid #3C3C3C;
                padding: 5px;
                selection-background-color: #264F78;
            }
            QScrollBar:vertical {
                background: #202020;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #616161;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        terminal_label = QLabel("TERMINAL")
        terminal_label.setStyleSheet("color: #CCCCCC; font-weight: bold; padding: 3px; font-size: 11px; background: #252526;")
        
        # Add Text Field below terminal
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.submit_user_input)  # Allow Enter key submission
        self.input_field.setFixedHeight(30)
        self.input_field.setFont(QFont("Consolas", 11))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background: #202020;
                color: #FFFFFF;
                border: 1px solid #3C3C3C;
                border-radius: 0px;
                padding: 5px;
                selection-background-color: #264F78;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
        """)
        self.input_field.setPlaceholderText("Enter input here...")
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_user_input)
        self.submit_button.setEnabled(False)  # Initially disabled
        self.submit_button.setStyleSheet("""
            QPushButton {
                background: #0E639C;
                color: white;
                font-weight: bold;
                border-radius: 2px;
                padding: 5px 10px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #1177BB;
            }
            QPushButton:pressed {
                background: #0D5086;
            }
            QPushButton:disabled {
                background: #333333;
                color: #666666;
            }
        """)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(2)

        terminal_container = QWidget()
        terminal_layout = QVBoxLayout()
        terminal_layout.addWidget(terminal_label)
        terminal_layout.addWidget(self.terminal)
        terminal_layout.addLayout(input_layout)  # Add the input field below terminal
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(1)
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
                font-size: 11px;
                font-family: 'Consolas';
            }
            QHeaderView::section {
                background: #333;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
            }
            QTableWidget::item {
                padding: 3px;
            }
            QTableWidget QTableCornerButton::section {  /* Style the top-left corner */
                background: #333;
                border: none;
            }
            QScrollBar:vertical {
                background: #202020;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #424242;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #616161;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        main_splitter.addWidget(self.result_table)
        main_splitter.setStretchFactor(0, 3)  # More space to code editor + terminal
        main_splitter.setStretchFactor(1, 1)  # Less space to results table

        # Create status bar (VSCode-like)
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("""
            QStatusBar {
                background: #054C7B;
                color: white;
            }
        """)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Set main widget
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_splitter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_button_action(self, text, icon_path=""):
        action = QAction(text, self)
        if icon_path:
            action.setIcon(QIcon(icon_path))
        
        # Style the action button VSCode style
        if "Lexical" in text:
            action.setStyleSheet("""
                background: #007ACC;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
            """)
        elif "Syntax" in text:
            action.setStyleSheet("""
                background: #F55D3E;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
            """)
        elif "Semantic" in text:
            action.setStyleSheet("""
                background: #4CAF50;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
            """)
        elif "Run" in text:
            action.setStyleSheet("""
                background: #9C27B0;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
            """)
        
        return action
    
    # Signal handler methods
    def update_terminal(self, text):
        self.terminal.append(text)
        # Ensure cursor is at the end and visible
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()
    
    def display_error(self, error_text):
        self.terminal.append(f"<span style='color:#FF6B6B;'>Error: {error_text}</span>")
    
    def request_input(self, prompt):
        self.terminal.append(f"<span style='color:#4FC3F7;'>{prompt}</span>")
        self.waiting_for_input = True
        self.submit_button.setEnabled(True)
        self.input_field.setFocus()
    
    def handle_program_finished(self, return_code):
        if return_code == 0:
            self.terminal.append("\n\n\n\n<span style='color:#81C784;'>✅ Program completed successfully.</span>")
            self.statusBar.showMessage("Program execution completed", 3000)
        else:
            self.terminal.append(f"\n\n\n\n<span style='color:#81C784;'>✅ Program completed successfully.</span>")
            self.statusBar.showMessage(f"Program execution completed", 3000)

    def submit_user_input(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return  # Do nothing if input is empty
        
        # Echo the input in the terminal
        self.terminal.append(f"<span style='color:#FFCC80;'>> {user_input}</span>")
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
                self.terminal.append(f"<span style='color:#FF6B6B;'>⚠ Failed to send input: {e}</span>")
                import traceback
                self.terminal.append(f"<span style='color:#FF6B6B;'>{traceback.format_exc()}</span>")

    def lexical_analyzer(self):
        self.terminal.clear()
        self.analyzer.errors.clear()
        self.tokens = []
        self.statusBar.showMessage("Running lexical analysis...", 2000)

        code = self.code_editor.toPlainText()
        tokens, errors = self.analyzer.tokenize(code)
        self.tokens = tokens

        self.result_table.setRowCount(len(tokens))
        for i, (lexeme, token, line, column) in enumerate(tokens):
            self.result_table.setItem(i, 0, QTableWidgetItem(lexeme))
            self.result_table.setItem(i, 1, QTableWidgetItem(token))
            self.result_table.setItem(i, 2, QTableWidgetItem(str(line)))
            
        if errors:
            self.terminal.setText("<span style='color:#FF6B6B;'>" + "<br>".join(errors) + "</span>")
            self.syntax_button.setEnabled(False)  # Changed from self.syntax_action
            self.semantic_button.setEnabled(False)  # Changed from self.semantic_action
            self.statusBar.showMessage("Lexical analysis completed with errors", 3000)
        else:
            self.terminal.setText("<span style='color:#81C784;'>✅ No lexical errors found.</span>")
            self.syntax_button.setEnabled(True)  # Changed from self.syntax_action
            self.statusBar.showMessage("Lexical analysis completed successfully", 3000)

    def syntax_button_clicked(self):
        self.run_syntax_analysis()

    def run_syntax_analysis(self):
        self.terminal.clear()
        self.statusBar.showMessage("Running syntax analysis...", 2000)

        if not self.tokens:
            self.terminal.setText("<span style='color:#FF6B6B;'>⚠ No tokens available. Please run lexical analysis first.</span>")
            return
        
        parser = CFG.LL1Parser(CFG.cfg, CFG.parse_table, CFG.follow_set)
        success, errors, parse_tree = parser.parse(self.tokens)
        parser.print_errors()
        
        if success:
            self.terminal.setText("<span style='color:#81C784;'>✅ Syntax analysis completed successfully.</span>")
            self.semantic_button.setEnabled(True)
            self.statusBar.showMessage("Syntax analysis completed successfully", 3000)
        else:
            self.terminal.setText("<span style='color:#FF6B6B;'>" + "<br>".join(errors) + "</span>")
            self.semantic_button.setEnabled(False)
            self.statusBar.showMessage("Syntax analysis completed with errors", 3000)

    def semantic_button_clicked(self):
        self.run_semantic_analysis()

    def run_semantic_analysis(self):
        self.terminal.clear()
        self.statusBar.showMessage("Running semantic analysis...", 2000)

        sem = semantic.Semantic()
        errors = sem.semantic_analyzer(self.tokens)
        sem.print_symbol_table()
        sem.print_errors()

        if errors:
            self.terminal.setText("<span style='color:#FF6B6B;'>" + "<br>".join(errors) + "</span>")
            self.statusBar.showMessage("Semantic analysis completed with errors", 3000)
        else:
            self.terminal.setText("<span style='color:#81C784;'>✅ No Semantic errors found.</span>")
            self.statusBar.showMessage("Semantic analysis completed successfully", 3000)

    def run_botton_clicked(self):
        self.terminal.clear()
        self.statusBar.showMessage("Running full compilation and execution...", 2000)

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

    def run_code_generation(self):
        self.terminal.clear()
        self.statusBar.showMessage("Generating and executing code...", 2000)

        if not self.tokens:
            self.terminal.setText("<span style='color:#FF6B6B;'>⚠ No tokens available for code generation.</span>")
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
        
        # self.terminal.append("<span style='color:#BBDEFB;'>Compiling code...</span>")
        print("Generated Code: " + generated_code)  # Debug: Print generated code
        
        try:
            # Create temporary file for the C code
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
                self.terminal.setText("<span style='color:#FF6B6B;'>❌ Compilation failed:</span>\n" + compile_process.stderr)
                self.statusBar.showMessage("Compilation failed", 3000)
                return
            
            self.statusBar.showMessage("Running program...", 3000)
            
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

                    # Process remaining events to keep UI responsive
                    QApplication.processEvents()
                    
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
            self.terminal.setText(f"<span style='color:#FF6B6B;'>⚠ Error running generated code:</span>\n{str(e)}")
            import traceback
            self.terminal.append(f"<span style='color:#FF6B6B;'>{traceback.format_exc()}</span>")
            self.statusBar.showMessage("Error running program", 3000)
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