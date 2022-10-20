# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui

class TextFieldWithLabel(QtWidgets.QWidget):
    def __init__(self, label, parent, element):
        super().__init__(parent)
        self.widget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)

        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QtCore.QRect(0, 30, 371, 31))
        self.textEdit.setStyleSheet(u"background: #eeeeee; max-height: 24px;")
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.label = QtWidgets.QLabel()
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(0, 0, 63, 20))

        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setText(label)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: #eeeeee")

        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.textEdit)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
    def setFieldValue(self, value):
        self.textEdit.setText(value)

class ElementEditor(QtWidgets.QWidget):
    def __init__(self, parent, layout, controller):
        super().__init__(parent)
        self.controller = controller
        self.inputMap = {}
        self.properties=["name","as_id"]

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#        sizePolicy.setHorizontalStretch(1)
#        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

#        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        for x in self.properties:
           textField = TextFieldWithLabel(x, self, controller.currentSelection)
           self.inputMap[x] = textField
           layout.addWidget(textField)

#        textField2 = TextFieldWithLabel("Test", self)
#        self.verticalLayout.addWidget(textField2)
    def updateSelection(self):
        self.controller.configureCurrentSelection()
    def updateDisplay(self, device):
        if device is not None:
            for key in self.properties:
                self.inputMap[key].setFieldValue(device.getProp(key))

