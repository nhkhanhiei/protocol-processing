# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QSizePolicy

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
from drag_widget import DragWidget, DragBar
from simulation_controller import SimulationController
from element_editor import ElementEditor

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

    controller = SimulationController()
    elementEditor = ElementEditor(ex.scrollAreaWidgetContents,ex.verticalLayout_2, controller)
    controller.setElementEditor(elementEditor)

    drawWidget = DragWidget(ex.groupBox, controller)
    drawBar = DragBar(ex.groupBox, controller)

    ex.verticalLayout.replaceWidget(ex.widget_3, drawWidget)
    ex.verticalLayout.replaceWidget(ex.widget_4, drawBar)

    w.show()
    sys.exit(app.exec())
