# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets

class VisualWire():
    def __init__(self, device1, device2, interface1 = None, interface2 = None):
        self.device1 = device1
        self.device2 = device2
        self.interface1 = interface1
        self.interface2 = interface2

class VisualInterface():
    def __init__(self, source, mask, destination, router = None):
        self.source = source
        self.mask = mask
        self.destination = destination
        self.router = router

class SimulationController(QtWidgets.QWidget):
    def __init__(self):
        self.currentSelection = None
        self.elementEditor = None
        self.wires = []
        self.interfaceMap = {}


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

    def configureCurrentSelection(self, key, updatedValue, index = None, subkey = None):

        if self.currentSelection is not None:
            if index is None and subkey is None:
                self.currentSelection.properties[key] = updatedValue
            else :
                property = self.currentSelection.properties[key][index]

                setattr(property, subkey, updatedValue)


    def getWires(self) :
        return self.wires

    def setWires(self, wires) :
        self.wires = wires
