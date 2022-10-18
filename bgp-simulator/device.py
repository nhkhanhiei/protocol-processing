# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtQuick
from PySide6 import QtGui


class Device(QtWidgets.QLabel):
    def __init__(self, parent, x, y, pixmap):
        super().__init__(parent)
        iconSize = 80
        borderWidth = 2
        self.setMinimumSize(iconSize + borderWidth, iconSize + borderWidth)
        self.setPixmap(pixmap)
        self.move(x,y)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.activeStyle = ".Device { border: 2px solid #1DDC80; border-radius: 10px; background: transparent; }"
        self.inactiveStyle = ".Device { border: 2px solid #483059; border-radius: 10px; background: transparent; }"
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setStyleSheet(self.inactiveStyle);
    def setSelected(self, isSelected):
        if isSelected :
            self.setStyleSheet(self.activeStyle);
        else :
            self.setStyleSheet(self.inactiveStyle);


