from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import QRegularExpression


class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

        self.format_key = QTextCharFormat()
        self.format_key.setForeground(QColor("#2f00ff"))

        self.format_string = QTextCharFormat()
        self.format_string.setForeground(QColor("#178229"))

        self.format_number = QTextCharFormat()
        self.format_number.setForeground(QColor("#333333"))

        self.format_boolean = QTextCharFormat()
        self.format_boolean.setForeground(QColor("#05008f"))

        self.format_null = QTextCharFormat()
        self.format_null.setForeground(QColor("#808080"))

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
