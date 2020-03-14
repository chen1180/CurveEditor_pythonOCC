from PyQt5 import QtGui, QtWidgets, QtCore
import sys
from data.node import *


class SceneGraphModel(QtCore.QAbstractItemModel):
    sortRole = QtCore.Qt.UserRole
    filterRole = QtCore.Qt.UserRole + 1

    def __init__(self, root=None, parent=None):
        '''

        Args:
            root: take a Node as input
            parent: pointer to the start of the sceneGraph
        '''
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode: Node = root

    def rowCount(self, parent) -> int:
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()

    def columnCount(self, parent) -> int:
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.data(index.column())
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = node.resource()
                return QtGui.QIcon(QtGui.QPixmap(resource))
        if role == SceneGraphModel.sortRole:
            return node.typeInfo()
        if role == SceneGraphModel.filterRole:
            return node.typeInfo()

    def setData(self, index, value, role=QtCore.Qt.EditRole) -> bool:
        if index.isValid():
            node = index.internalPointer()
            if role == QtCore.Qt.EditRole:
                node.setData(index.column(), value)
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Scene"
            else:
                return "TypeInfo"

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def parent(self, index: QtCore.QModelIndex):
        '''

        Args:
            index: given QModelIndex

        Returns: the parent of the node with the given index

        '''
        node: Node = self.getNode(index)
        parentNode: Node = node.parent()
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):

        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()) -> bool:
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()

        return success

    def insertNode(self, node, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = node
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()) -> bool:
        parentNode = self.getNode(parent)
        if parentNode==None:
            return False
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)
        self.endRemoveRows()
        return success

class ListModel(QtCore.QAbstractListModel):
    def __init__(self,array:[],title="",parent=None):
        super(ListModel, self).__init__(parent)
        self._array=array
        self._title=title
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int):
        if role==QtCore.Qt.DisplayRole:
            if orientation==QtCore.Qt.Horizontal:
                return self._title
            else:
                return "{}".format(section)
    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        return QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable

    def setData(self, index: QtCore.QModelIndex, value: str, role: int=QtCore.Qt.EditRole) -> bool:
        if role==QtCore.Qt.EditRole:
            row=index.row()
            new_value=value
            if type(new_value)==float:
                self._array[row]=new_value
                self.dataChanged.emit(index,index)
                return True
        return False
    def data(self, index:QtCore.QModelIndex, role):
        if role==QtCore.Qt.EditRole:
            return round(self._array[index.row()],2)
        if role==QtCore.Qt.DisplayRole:
            row=index.row()
            value=self._array[row]
            return round(value,2)
    def rowCount(self, parent) -> int:
        return len(self._array)
if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    app.setStyle("cleanlooks")
    #data
    model=ListModel([0.12,2.5,2.333333333333],"Knots")
    #list view
    list_view=QtWidgets.QTableView()
    list_view.setModel(model)
    list_view.show()
    sys.exit(app.exec_())