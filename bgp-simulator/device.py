# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtQuick
from PySide6 import QtGui
import random


class Device(QtWidgets.QLabel):
    def __init__(self, parent, x, y, pixmap):
        super().__init__(parent)
        self.iconSize = 80
        self.borderWidth = 2
        self.deviceSize = self.iconSize + self.borderWidth
        self.properties = { "name": "Router", "as_id": "AS" + str(random.randint(1, 500))}
        self.setMinimumSize(self.deviceSize, self.deviceSize)
        self.setPixmap(pixmap)
        self.move(x,y)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.activeStyle = ".Device { border: 2px solid #1DDC80; border-radius: 10px; background: transparent; }"
        self.inactiveStyle = ".Device { border: 2px solid #483059; border-radius: 10px; background: transparent; }"
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setStyleSheet(self.inactiveStyle);

    @classmethod
    def fromDropEvent(self, parent, x, y, pixmap, properties):
        droppedDevice = Device(parent, x, y, pixmap)
        if len(properties) > 0:
            droppedDevice.properties = properties
        return droppedDevice

    def getProp(self, key):
        return self.properties[key]

    def setSelected(self, isSelected):
        if isSelected :
            self.setStyleSheet(self.activeStyle);
        else :
            self.setStyleSheet(self.inactiveStyle);


