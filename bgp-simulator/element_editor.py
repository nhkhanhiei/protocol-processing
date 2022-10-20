# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui

class TextFieldWithLabel(QtWidgets.QWidget):
    def __init__(self, label, parent):
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

class ElementEditor(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background: #ee0000;")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        for x in range(2):
            textField = TextFieldWithLabel("Test", self)
            self.verticalLayout.addWidget(textField)
#        textField2 = TextFieldWithLabel("Test", self)
#        self.verticalLayout.addWidget(textField2)

