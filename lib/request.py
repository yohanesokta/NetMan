import requests
from PyQt6.QtCore import QThread, pyqtSignal

class request_worker(QThread):
    progress = pyqtSignal(list)
    url = ""
    method = ""
    def run(self):
        try:
            result = requests.get(self.url)
            self.progress.emit(result.json())
        except Exception as error:
            print("Error : ", error)
            self.progress.emit([{"Errors":"Failed Request","Errors Details" : str(error.__str__())}])
