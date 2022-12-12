# This Python file uses the following encoding: utf-8
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QDataStream, QIODevice, QByteArray, QMimeData)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QDrag,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPen, QPicture, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QScrollArea, QSizePolicy,
    QStatusBar, QTextEdit, QWidget, QFrame)
from device import Device
from simulation_controller import VisualWire


class DragWidget(QFrame):
    def _createDevice(self, x, y, image, parent) :
        newPixmap = QPixmap(image)
        newDevice = Device(parent, x, y, newPixmap)
        newDevice.show()
        return newDevice

    def _updateWireNetwork(self) :

        wires = self.controller.getWires()

        newPicture = QImage(self.parent.width(), self.parent.height(), QImage.Format_ARGB32)
        newPicture.fill(QColor(0,0,0,0))
        painter = QPainter()
        painter.begin(newPicture)
        painter.setPen(QPen(Qt.black, 2, Qt.DashDotLine, Qt.RoundCap));

        for wire in wires:
            if wire.interface1 is None or wire.interface2 is None:
                wires.remove(wire)
                del wire
                continue

            x1 = wire.device1.x + (wire.device1.width() / 2)
            y1 = wire.device1.y + (wire.device1.height() / 2)
            x2 = wire.device2.x + (wire.device2.width() / 2)
            y2 = wire.device2.y + (wire.device2.height() / 2)
            painter.drawLine(x1, y1, x2, y2)

            if wire.device1 is not None and wire.device2 is not None:
                x1 = wire.device1.x + (wire.device1.width() / 2)
                y1 = wire.device1.y + (wire.device1.height() / 2)
                x2 = wire.device2.x + (wire.device2.width() / 2)
                y2 = wire.device2.y + (wire.device2.height() / 2)
                painter.drawLine(x1, y1, x2, y2)

        painter.end()
        self.backgroundCanvas.setPixmap(QPixmap.fromImage(newPicture))
        self.backgroundCanvas.hide()
        self.backgroundCanvas.show()

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.backgroundCanvas = QLabel(self)
        self.backgroundCanvas.setMinimumSize(parent.height(), parent.width())

        self.controller = controller
        self.draggedProperties = {}
        self.draggedDevice = None
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        wires = []
        controller.setWires(wires)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-dnditemdata") :
            if event.source() == self :
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else :
                event.acceptProposedAction()
        else :
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-dnditemdata") :
            if event.source() == self :
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else :
                event.acceptProposedAction()
        else :
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasFormat("application/x-dnditemdata") :
            itemData = event.mimeData().data("application/x-dnditemdata")
            dataStream = QDataStream(itemData, QIODevice.ReadOnly)

            pixmap = QPixmap()
            offset = QPoint()

            properties = self.draggedProperties
            self.draggedProperties = {}

            device = self.draggedDevice
            self.draggedDevice = None

            dataStream >> pixmap >> offset

            newPoint = event.position().toPoint() - offset

            if device is not None :
                device.setPosition(newPoint.x(), newPoint.y())
            else :
                newDevice = Device.fromDropEvent(self, newPoint.x(), newPoint.y(), pixmap, properties)
                self.controller.setCurrentSelection(newDevice)
                self.controller.routers[ newDevice.properties['as_id'] ] = newDevice
                newDevice.show()

            self._updateWireNetwork()

            if event.source() == self :
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else :
                event.acceptProposedAction()
        else :
            event.ignore()

    def mousePressEvent(self, event):
        child = self.childAt(event.position().toPoint())
        if not child or not child.pixmap() or not hasattr(child, 'properties') :
            return
        self.controller.setCurrentSelection(child)
        pixmap = child.pixmap()
        itemData = QByteArray()
        self.draggedProperties = child.properties
        self.draggedDevice = child

        dataStream = QDataStream(itemData, QIODevice.WriteOnly)
        dataStream << pixmap << QPoint(event.position().toPoint() - child.pos())

        tempPixmap = QPixmap(pixmap)
        painter = QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127))
        painter.end()

        mimeData = QMimeData()
        mimeData.setData("application/x-dnditemdata", itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(tempPixmap)
        drag.setHotSpot(event.position().toPoint() - child.pos())

        if drag.exec(Qt.MoveAction) == Qt.MoveAction :
            child.show()
        else :
            child.show()
            child.setPixmap(pixmap)

class DragBar(QFrame) :

    def _createDevice(self, x, y, image, parent) :
        newPixmap = QPixmap(image)
        newDevice = Device(parent, x, y, newPixmap)
        newDevice.show()
        return newDevice

    def __init__(self, parent) :
        super().__init__(parent)
        self.setMinimumSize(80,100)
        self.setStyleSheet(u"background: rgb(145, 155, 155)")
        self.setAcceptDrops(False)
        self._createDevice(10, 10, 'images/pc.png', self)
        self._createDevice(120, 10, 'images/router.png', self)

    def mousePressEvent(self, event):
        child = self.childAt(event.position().toPoint())
        if not child or not child.pixmap() :
            return
        pixmap = child.pixmap()
        itemData = QByteArray()

        dataStream = QDataStream(itemData, QIODevice.WriteOnly)
        dataStream << pixmap << QPoint(event.position().toPoint() - child.pos())

        tempPixmap = QPixmap(pixmap)
        painter = QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QColor(127, 127, 127, 127))
        painter.end()

        mimeData = QMimeData()
        mimeData.setData("application/x-dnditemdata", itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(tempPixmap)
        drag.setHotSpot(event.position().toPoint() - child.pos())

        drag.exec(Qt.CopyAction)
