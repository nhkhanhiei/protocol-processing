# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets

class VisualWire() :
    def __init__(self, device1, device2):
        self.device1 = device1
        self.device2 = device2

class SimulationController(QtWidgets.QWidget):
    def __init__(self):
        self.currentSelection = None
        self.elementEditor = None
        self.wires = []

    def setElementEditor(self, editor):
        self.elementEditor = editor

    def setCurrentSelection(self, device):
        if self.currentSelection is not device :
            if self.currentSelection is not None:
                self.currentSelection.setSelected(False)
            self.currentSelection = device
            if self.currentSelection is not None:
                self.currentSelection.setSelected(True)
            self.elementEditor.updateDisplay(device)

    def configureCurrentSelection(self, key, updatedValue):
        if self.currentSelection is not None:
            self.currentSelection.properties[key] = updatedValue

    def getWires(self) :
        return self.wires

    def setWires(self, wires) :
        self.wires = wires
