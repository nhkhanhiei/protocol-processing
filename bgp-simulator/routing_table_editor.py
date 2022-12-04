# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtQuick
from PySide6 import QtGui
from textfield_with_label import TextFieldWithLabel

class RoutingTableEditor(QtWidgets.QWidget):

    def __init__(self, parent, controller, updateSelection):
        super().__init__(parent)

        self.parent = parent
        self.interfaceCount = 0
        self.controller = controller
        self.updateSelection = updateSelection

        self.splitter = QtWidgets.QSplitter(parent)
        self.splitter.setObjectName(u"routing_table_splitter")
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setOpaqueResize(False)

        self.label = QtWidgets.QLabel()
        self.label.setObjectName(u"routing_table_label")
        self.label.setGeometry(QtCore.QRect(0, 0, 63, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setText("Routing Table")
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: #eeeeee; max-height: 16px;")

        self._updateForm()

    def _getRoutingTableEntries(self):
        if self.controller.currentSelection is not None:
            return self.controller.currentSelection.properties['routing_table']
        else:
            return None

    def _addRoutingTableEntry(self):
        self.controller.currentSelection.addNewEmptyInterface()
        self.interfaceCount = len(self._getRoutingTableEntries())
        self._updateForm()

    def _updateForm(self):

        newSplitter = QtWidgets.QSplitter(self.splitter.parent())
        newSplitter.setObjectName(u"routing_table_splitter")
        newSplitter.setOrientation(QtCore.Qt.Vertical)
        newSplitter.setChildrenCollapsible(False)
        newSplitter.setOpaqueResize(False)
        oldSplitter = self.splitter
        self.splitter = newSplitter
        oldSplitter.close()

        self.splitter.addWidget(self.label)

        interfaces = self._getRoutingTableEntries()

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

        button = QtWidgets.QPushButton('Add New Entry', self.splitter)
        button.setStyleSheet(u"background: rgb(145, 131, 155); height: 32px; border-radius: 8px; margin: 0 4px;")
        button.pressed.connect(lambda : self._addRoutingTableEntry())
        self.splitter.addWidget(button)
        self.parent.insertWidget(2, self.splitter)

    def setFields(self, interfaces):
        self.interfaceCount = len(interfaces)
        self._updateForm()

