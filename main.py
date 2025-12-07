import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from view.main_window import Ui_NETman
from view.request_widget_logic import RequestWidget
import qdarktheme

class MainWindow(QMainWindow, Ui_NETman):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.actionNew_Tab.triggered.connect(self.add_new_tab)
        self.mainTabWidget.tabCloseRequested.connect(self.close_tab)

        self.add_new_tab()

    def add_new_tab(self):
        new_tab = RequestWidget()
        self.mainTabWidget.addTab(new_tab, "New Request")
        self.mainTabWidget.setCurrentWidget(new_tab)

    def close_tab(self, index):
        widget = self.mainTabWidget.widget(index)
        if widget:
            widget.deleteLater()
        self.mainTabWidget.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    qdarktheme.setup_theme()
    app.exec()

    