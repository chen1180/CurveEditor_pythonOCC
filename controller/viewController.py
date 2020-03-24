from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ViewController(QObject):

    def __init__(self, parent=None):
        super(ViewController, self).__init__(parent)
        self._display = parent._glWindow._display
        self.actions = []
        self.createActions()

    def createActions(self):

        # self._action_transform = QAction(QIcon(":/move.png"), "Transform", self,
        #                                  statusTip="Transform a object",
        #                                  triggered=self._display.View.SetFront)
        # self.actions.append(self._action_transform)
        self._action_fitAll = QAction(QIcon(":/fitContent.png"), "Fit all", self,
                                      statusTip="Fit all shapes on screen",
                                      triggered=self._display.FitAll)
        self.actions.append(self._action_fitAll)

        def setView(a0):
            if a0 == True:
                self._display.SetPerspectiveProjection()
                self._action_setView.setText("Perspective")
            else:
                self._display.SetOrthographicProjection()
                self._action_setView.setText("Ortho")
            self._display.Repaint()

        icon = QIcon()
        icon.addPixmap(QPixmap(":/orthorgraphic.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/perspective.png"), QIcon.Normal, QIcon.On)
        self._action_setView = QAction(icon, "Ortho", self,
                                       statusTip="set view type",
                                       triggered=setView)
        self._action_setView.setCheckable(True)
        self.actions.append(self._action_setView)
        self._action_viewIso = QAction(QIcon(":/viewIso.png"), "View ISO", self,
                                       statusTip="Change view point",
                                       triggered=self._display.View_Iso)
        self.actions.append(self._action_viewIso)

        def switchDisplayMode(state):
            if state:
                self._display.SetModeWireFrame()
                self._action_switchDisplayMode.setText("Wireframe")
            else:
                self._display.SetModeShaded()
                self._action_switchDisplayMode.setText("Shading")

        icon = QIcon()
        icon.addPixmap(QPixmap(":/shading.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/wireframe.png"), QIcon.Normal, QIcon.On)
        self._action_switchDisplayMode = QAction(icon, "Shading", self,
                                                 statusTip="Wireframe mode",
                                                 triggered=switchDisplayMode, checkable=True)
        self.actions.append(self._action_switchDisplayMode)


class CustomTreeViewController(QTreeView):
    def __init__(self, parent=None):
        super(CustomTreeViewController, self).__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def openMenu(self, position):
        indexes = self.selectedIndexes()
        level = 0
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        menu = QMenu()
        menu.addAction(QAction(QIcon(), "Delete", self,
                               statusTip="Delete selected node",
                               triggered=self.deleteTreeItem))
        if level == 0:
            menu.addAction(QAction(QIcon(), "Delete all", self,
                                   statusTip="Delete all objects in the scene",
                                   triggered=self.deleteAllTreeItem))
        elif level == 1:
            # menu.addAction(self.tr("Edit object/container"))
            pass
        elif level == 2:
            # menu.addAction(self.tr("Edit object"))
            pass
        menu.exec_(self.viewport().mapToGlobal(position))

    def deleteAllTreeItem(self):
        """
        Delete all object on the tree
        @return:
        """
        index = self.currentIndex()
        parent = index.parent()
        self.model().removeRows(0, self.model().rowCount(QModelIndex()))

    def deleteTreeItem(self):
        """
        Delete current selected object on the tree
        @return:
        """
        index = self.currentIndex()
        parent = index.parent()
        self.model().removeRows(index.row(), 1, parent)

    def updateIndex(self, node):
        if node:
            row = self._rootNode.childCount()
            column = node.childCount()
            index = self._model.index(row - 1, column, QModelIndex())
            self._uiTreeView.setCurrentIndex(index.child(index.column() - 1, 0))
            self._uiTreeView.updateEditorData()
            self._uiTreeView.expandAll()
