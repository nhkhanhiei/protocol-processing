# This Python file uses the following encoding: utf-8
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QDataStream, QIODevice, QByteArray, QMimeData)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QDrag,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPicture, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QScrollArea, QSizePolicy,
    QStatusBar, QTextEdit, QWidget, QFrame)
from device import Device


class DragWidget(QFrame):
    def _createIcon(self, x, y, image, parent) :
        newPixmap = QPixmap(image)
        newIcon = Device(parent, x, y, newPixmap)
        newIcon.show()
        return newIcon

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.draggedProperties = {}
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setAcceptDrops(True)
        self._createIcon(10, 10, 'images/pc.png', self)

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
            dataStream >> pixmap >> offset

            newPoint = event.position().toPoint() - offset
            newIcon = Device.fromDropEvent(self, newPoint.x(), newPoint.y(), pixmap, properties)
            self.controller.setCurrentSelection(newIcon)
            newIcon.show()

            if event.source() == self :
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else :
                event.acceptProposedAction()
        else :
            event.ignore()
    def mousePressEvent(self, event):
        child = self.childAt(event.position().toPoint())

        self.controller.setCurrentSelection(child)

        if not child or not child.pixmap() :
            return
        pixmap = child.pixmap()
        itemData = QByteArray()
        self.draggedProperties = child.properties

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
            child.close()
        else :
            child.show()
            child.setPixmap(pixmap)

class DragBar(DragWidget) :

    def __init__(self, parent, controller) :
        super().__init__(parent, controller)
        self.setMinimumSize(80,100)
        self.setStyleSheet(u"background: rgb(145, 155, 155)")
        self.setAcceptDrops(False)
        self._createIcon(10, 10, 'images/pc.png', self)
        self._createIcon(120, 10, 'images/router.png', self)

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
