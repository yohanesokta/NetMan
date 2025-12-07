from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import QRegularExpression


class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

        self.format_key = QTextCharFormat()
        self.format_key.setForeground(QColor("#66d9ef")) # Cyan for keys

        self.format_string = QTextCharFormat()
        self.format_string.setForeground(QColor("#a6e22e")) # Bright green for strings

        self.format_number = QTextCharFormat()
        self.format_number.setForeground(QColor("#fd971f")) # Orange for numbers

        self.format_boolean = QTextCharFormat()
        self.format_boolean.setForeground(QColor("#ae81ff")) # Purple for booleans

        self.format_null = QTextCharFormat()
        self.format_null.setForeground(QColor("#75715e")) # Gray for null

        self.rules.append(
            (QRegularExpression(r"\".*?\"(?=\s*:)"), self.format_key)
        )  # key
        self.rules.append(
            (QRegularExpression(r":\s*\".*?\""), self.format_string)
        )  # string value
        self.rules.append(
            (QRegularExpression(r"\b\d+(\.\d+)?\b"), self.format_number)
        )  # number
        self.rules.append(
            (QRegularExpression(r"\btrue\b|\bfalse\b"), self.format_boolean)
        )
        self.rules.append((QRegularExpression(r"\bnull\b"), self.format_null))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            match_iter = pattern.globalMatch(text)
            while match_iter.hasNext():
                match = match_iter.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
