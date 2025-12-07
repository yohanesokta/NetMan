import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem ,QHeaderView
from PyQt6.QtCore import Qt
from lib.formatter import JsonHighlighter
from lib.request import request_worker
import json
from view.main_window import Ui_NETman
from lib.controllers import get_table_data, queryAppend, to_dict
import qdarktheme


class MainWindow(QMainWindow, Ui_NETman):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.request_worker = request_worker()
        self.request_worker.progress.connect(self.RequestParse)
        self.sendButton.clicked.connect(self.RequestAction)
        self.higlighter = JsonHighlighter(self.responseText.document())
        self.actionExit.triggered.connect(self.close)
        self.paramsAddButton.clicked.connect(
            lambda: self.addTable(self.paramsTableWidget)
        )
        for i in range(5):
            self.addTable(self.headersTableWidget)
            self.addTable(self.paramsTableWidget)
            if (i < 4):
                self.addTable(self.bodyTableWidget)
        self.paramsRemoveButton.clicked.connect(
            lambda: self.removeTable(self.paramsTableWidget)
        )
        self.headersAddButton.clicked.connect(
            lambda: self.addTable(self.headersTableWidget)
        )
        self.headersRemoveButton.clicked.connect(
            lambda: self.removeTable(self.headersTableWidget)
        )

        self.inputUrl.editingFinished.connect(lambda : print("Url Editing Finishing"))

        self.paramsTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.paramsTableWidget.cellChanged.connect(self.RequestParamsEditor)
        self.headersTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bodyTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def addTable(self, TableWigetVars):
        row_position = TableWigetVars.rowCount()
        TableWigetVars.insertRow(row_position)
        TableWigetVars.setItem(row_position, 0, QTableWidgetItem(""))
        TableWigetVars.setItem(row_position, 1, QTableWidgetItem(""))

    def removeTable(self, TableWigetVars):
        row_position = TableWigetVars.rowCount()
        if row_position > 0:
            TableWigetVars.removeRow(row_position - 1)

    def RequestParamsEditor(self):
        list_params = get_table_data(self.paramsTableWidget)
        new_url = queryAppend(self.inputUrl.text(),list_params)
        self.inputUrl.setText(new_url)

    def RequestAction(self):
        method = self.inputMethod.currentText()
        url = self.inputUrl.text()
        headers = to_dict(get_table_data(self.headersTableWidget))
        
        body = None
        body_type = None

        # Check which body type is selected
        if self.tabWidget_2.currentIndex() == 0: # Form Data
            body = to_dict(get_table_data(self.bodyTableWidget))
            body_type = 'form'
        elif self.tabWidget_2.currentIndex() == 1: # Raw JSON
            try:
                body = json.loads(self.textEdit.toPlainText())
                body_type = 'json'
            except json.JSONDecodeError:
                self.responseText.setPlainText("Invalid JSON in body")
                return

        if method and url:
            self.sendButton.setDisabled(True)
            self.responseText.setPlainText('Waiting Response Server!')
            self.request_worker.method = method
            self.request_worker.url = url
            self.request_worker.headers = headers
            self.request_worker.body = body
            self.request_worker.body_type = body_type
            self.request_worker.start()



    def RequestParse(self,result):
        self.sendButton.setDisabled(False)
        if isinstance(result, dict):
            self.responseText.setPlainText(
                json.dumps(result, indent=4, ensure_ascii=False)
            )
        elif isinstance(result, list):
            self.responseText.setPlainText(str(result))
        else:
            self.responseText.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    qdarktheme.setup_theme()
    from PyQt6.QtWidgets import QStyleFactory
    print(QStyleFactory.keys())
    app.exec()
    