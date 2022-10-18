# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QSizePolicy

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from drag_widget import DragWidget, DragBar

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QMainWindow()
    ex.setupUi(w)

    drawWidget = DragWidget(ex.groupBox)
    drawBar = DragBar(ex.groupBox)
    ex.verticalLayout.replaceWidget(ex.widget_3, drawWidget)
    ex.verticalLayout.replaceWidget(ex.widget_4, drawBar)


    w.show()
    sys.exit(app.exec())
