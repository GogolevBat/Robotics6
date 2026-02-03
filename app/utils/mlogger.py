from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from datetime import datetime
class Logger:
    def __init__(self, log_field: QTextEdit):
        self.log_field = log_field
        self.logs = {}
        self.index = 0

    def _set(self, message: str, level="INFO"):
        dt = datetime.now().strftime("%d/%m/%Y, %H:%M:%S.%f")
        print(f"[{dt}][{level}] - {message}")
        self.log_field.insertHtml(f"<span style='color: #000000'>[{dt}][{level}] - {message}</span>")
        self.log_field.insertPlainText("\n")
        self.log_field.moveCursor(QTextCursor.End)
        self.index += 1
        self.logs[self.index] = (dt, level, message)
        if len(self.logs) > 1000: 
            del self.logs[self.index-1000]
    
    def info(self, *args):
        self._set(" ".join(map(str, args)), "INFO")
    def warning(self, *args):
        self._set(" ".join(map(str, args)), "WARNING")
    def debug(self, *args):
        self._set(" ".join(map(str, args)), "DEBUG")
    def error(self, *args):
        self._set(" ".join(map(str, args)), "ERROR")
