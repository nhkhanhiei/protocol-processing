from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtQuick
from PySide6 import QtGui

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
