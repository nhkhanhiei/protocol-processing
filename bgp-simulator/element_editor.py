# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
from device import DeviceProperty

class TextFieldWithLabel(QtWidgets.QWidget):
    def __init__(self, label, parent, element, onChange):
        super().__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setObjectName(u"textEdit")
        self.lineEdit.setGeometry(QtCore.QRect(0, 30, 371, 31))
        self.lineEdit.setStyleSheet(u"background: #eeeeee; max-height: 24px;")
        self.lineEdit.textEdited.connect(lambda newText: onChange(label, newText))

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

class ElementEditor(QtWidgets.QWidget):
    def __init__(self, parent, layout, controller):
        super().__init__(parent)
        self.controller = controller
        self.formElements = {}
        self.properties = [ DeviceProperty("Name", "name", "text"),
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
           textField = TextFieldWithLabel(propKey, self.splitter, controller.currentSelection, self.updateSelection)
           self.formElements[propKey] = textField
           self.splitter.addWidget(textField)

        self.splitter.addWidget(QtWidgets.QWidget())
        layout.addWidget(self.splitter)

    def updateSelection(self, key, newText):
        if self.formElements.get(key) is not None :
            self.controller.configureCurrentSelection(key, newText)

    def updateDisplay(self, device):
        if device is not None:
            for prop in self.properties:
                propKey = prop.key
                self.formElements[propKey].setFieldValue(device.getProp(propKey))

