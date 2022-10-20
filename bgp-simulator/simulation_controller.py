# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets


class SimulationController(QtWidgets.QWidget):
    def __init__(self):
        self.currentSelection = None

    def setCurrentSelection(self, device):
        if self.currentSelection is not device :
            if self.currentSelection is not None:
                self.currentSelection.setSelected(False)
            self.currentSelection = device
            if self.currentSelection is not None:
                self.currentSelection.setSelected(True)
