# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets

class VisualWire():
    def __init__(self, interface1, interface2):
        self.interface1 = interface1
        self.interface2 = interface2
        self.device1 = interface1.router
        self.device2 = interface2.router

class VisualInterface():
    def __init__(self, source, mask, destination, router = None):
        self.source = source
        self.mask = mask
        self.destination = destination
        self.router = router
        self.wire = None

class SimulationController(QtWidgets.QWidget):
    def __init__(self):
        self.currentSelection = None
        self.elementEditor = None
        self.wires = []
        self.interfaceMap = {}

    def _updateInterfaceConnection(self, src):
        dest = self.interfaceMap[src].destination

        if dest == '' or dest not in self.interfaceMap:
            return

        if src == self.interfaceMap[dest].destination:
            wire1 = self.interfaceMap[src].wire
            wire2 = self.interfaceMap[dest].wire
            if wire1 is None and wire2 is None:
                self.wires.append(VisualWire(self.interfaceMap[src], self.interfaceMap[dest]))
            else:
                if wire1 is not None:
                    if wire1.interface1.source == self.interfaceMap[src].source:
                        wire1.interface2.wire = None
                        wire1.interface2 = self.interfaceMap[dest]
                    elif wire1.interface2.source == self.interfaceMap[src].source:
                        wire1.interface1.wire = None
                        wire1.interface1 = self.interfaceMap[dest]
                elif wire2 is not None:
                    if wire2.interface1.source == self.interfaceMap[src].source:
                        wire2.interface2.wire =  None
                        wire2.interface2 = self.interfaceMap[dest]
                    elif wire2.interface2.source == self.interfaceMap[src].source:
                        wire2.interface1.wire =  None
                        wire2.interface1 = self.interfaceMap[dest]
            self.drawWidget._updateWireNetwork()


    def setElementEditor(self, editor):
        self.elementEditor = editor

    def setDrawWidget(self, drawWidget):
        self.drawWidget = drawWidget

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
                prevValue = getattr(property, subkey)
                setattr(property, subkey, updatedValue)

                if key == "interfaces":
                    if subkey == "source":
                        if len(prevValue) > 0:
                            self.interfaceMap.pop(prevValue)
                        self.interfaceMap[updatedValue] = property
                        self._updateInterfaceConnection(updatedValue)
                    elif subkey == "destination":
                        self._updateInterfaceConnection(property.source)

    def getWires(self) :
        return self.wires

    def setWires(self, wires) :
        self.wires = wires
