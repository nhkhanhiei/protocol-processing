# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
from device import DeviceProperty
from simulation_controller import VisualInterface

class TextFieldWithLabel(QtWidgets.QWidget):
    def __init__(self, label, key, parent, element, onChange, isArrayProp = False, index = None, arrayKey = None):
        super().__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setObjectName(u"textEdit")
        self.lineEdit.setGeometry(QtCore.QRect(0, 30, 371, 31))
        self.lineEdit.setStyleSheet(u"background: #eeeeee; max-height: 24px;")
        if isArrayProp:
            self.lineEdit.textEdited.connect(lambda newText: onChange(arrayKey, newText, index, key))
        else:
            self.lineEdit.textEdited.connect(lambda newText: onChange(key, newText))

        self.label = QtWidgets.QLabel()
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(0, 0, 63, 20))

        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setText(label)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: #eeeeee; max-height: 20px;")

        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.lineEdit)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

    def setFieldValue(self, value):
        self.lineEdit.setText(value)

class InterfaceEditor(QtWidgets.QWidget):
    def __init__(self, parent, controller, updateSelection):
        super().__init__(parent)

        self.parent = parent
        self.interfaceCount = 0
        self.controller = controller
        self.updateSelection = updateSelection

        self.splitter = QtWidgets.QSplitter(parent)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOpaqueResize(False)

        self.label = QtWidgets.QLabel()
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(0, 0, 63, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setText("Interfaces")
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: #eeeeee; max-height: 16px;")

        self._updateForm()

    def _getInterfaces(self):
        if self.controller.currentSelection is not None:
            return self.controller.currentSelection.properties['interfaces']
        else:
            return None

    def _addInterface(self):
        self.controller.currentSelection.addNewEmptyInterface()
        self.interfaceCount = len(self._getInterfaces())
        self._updateForm()

    def _updateForm(self):

        newSplitter = QtWidgets.QSplitter(self.splitter.parent())
        newSplitter.setObjectName(u"splitter")
        newSplitter.setOrientation(QtCore.Qt.Vertical)
        newSplitter.setChildrenCollapsible(False)
        newSplitter.setOpaqueResize(False)
        oldSplitter = self.splitter
        self.splitter = newSplitter
        oldSplitter.close()

        self.splitter.addWidget(self.label)

        interfaces = self._getInterfaces()

        if interfaces is not None:
            for index, interface in enumerate(interfaces, start=0):
                rowContainer = QtWidgets.QSplitter(self.splitter)
                rowContainer.setObjectName(u"rowContainer")
                rowContainer.setOrientation(QtCore.Qt.Horizontal)
                rowContainer.setChildrenCollapsible(False)
                rowContainer.setOpaqueResize(False)

                currentSelection = self.controller.currentSelection
                isArray = True
                textField1 = TextFieldWithLabel('Source IP', 'source', rowContainer, currentSelection, self.updateSelection, isArray, index, 'interfaces')
                textField2 = TextFieldWithLabel('Mask', 'mask', rowContainer, currentSelection, self.updateSelection, isArray, index, 'interfaces')
                textField3 = TextFieldWithLabel('Destination IP', 'destination', rowContainer, currentSelection, self.updateSelection, isArray, index, 'interfaces')
                textField1.setFieldValue(interface.source)
                textField2.setFieldValue(interface.mask)
                textField3.setFieldValue(interface.destination)
                rowContainer.addWidget(textField1)
                rowContainer.addWidget(textField2)
                rowContainer.addWidget(textField3)
                self.splitter.addWidget(rowContainer)

        button = QtWidgets.QPushButton('Add New Interface', self.splitter)
        button.setStyleSheet(u"background: rgb(145, 131, 155);")
        button.pressed.connect(lambda : self._addInterface())
        self.splitter.addWidget(button)
        self.parent.insertWidget(2, self.splitter)

    def setFields(self, interfaces):
        self.interfaceCount = len(interfaces)
        self._updateForm()

class ElementEditor(QtWidgets.QWidget):
    def __init__(self, parent, layout, controller):
        super().__init__(parent)
        self.controller = controller
        self.formElements = {}
        self.properties = [
                            DeviceProperty("Name", "name", "text"),
                            DeviceProperty("AS ID", "as_id", "text"),
                            DeviceProperty("Interfaces", "interfaces", "interface"),
                          ]

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.splitter = QtWidgets.QSplitter(parent)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOpaqueResize(False)

        for prop in self.properties:
           propKey = prop.key
           propLabel = prop.label
           if prop.type == "interface":
               interfaceEditor = InterfaceEditor(self.splitter, controller, self.updateSelectionPropArray)
               self.formElements[propKey] = interfaceEditor
               self.splitter.addWidget(interfaceEditor)
           else :
               textField = TextFieldWithLabel(propLabel, propKey, self.splitter, controller.currentSelection, self.updateSelection)
               self.formElements[propKey] = textField
               self.splitter.addWidget(textField)

        self.filler = QtWidgets.QWidget()
        self.splitter.addWidget(self.filler)
        layout.addWidget(self.splitter)

    def updateSelection(self, key, newText):
        if self.formElements.get(key) is not None :
            self.controller.configureCurrentSelection(key, newText)

    def updateSelectionPropArray(self, key, updatedValue, index, subkey):
        if self.formElements.get(key) is not None :
            self.controller.configureCurrentSelection(key, updatedValue, index, subkey)

    def updateDisplay(self, device):
        if device is not None:
            for prop in self.properties:
                propKey = prop.key
                if prop.type == "text" :
                    self.formElements[propKey].setFieldValue(device.getProp(propKey))
                elif prop.type == "interface" :
                    self.formElements[propKey].setFields(device.getProp(propKey))

