from PyQt6.QtCore import QThread, pyqtSignal
from lib.http_adapter import HttpAdapter

class request_worker(QThread):
    progress = pyqtSignal(object)
    url = ""
    method = ""
    headers = None
    body = None
    body_type = None

    def run(self):
        adapter = HttpAdapter()
        result = adapter.fetch(self.url, self.method, self.headers, self.body, self.body_type)
        self.progress.emit(result)
