from PyQt5.QtCore import QModelIndex, QObject, pyqtSignal
from PyQt5.QtWidgets import QAction, QStatusBar
from PyQt5.QtGui import QIcon
from data.design.part import Part
from data.design.part_type import *
from data.node import *
from data.model import SceneGraphModel


class PartController(QObject):
    modelUpdated = pyqtSignal(object)

    def __init__(self, display, parent=None):
        super(PartController, self).__init__(parent)
        self._display = display
        self._statusBar: QStatusBar = parent.statusBar()

        self.part = Part(self._display, self._statusBar)
        self.model: SceneGraphModel = None
        self.currentSketchNode: SketchObjectNode = None
        self.createActions()

    def highlightCurrentNode(self, current: QModelIndex, old: QModelIndex):
        node: SketchObjectNode = current.internalPointer()
        if isinstance(node, SketchNode):
            self.selectSketchNode(node)
        elif isinstance(node, SketchObjectNode):
            self._display.Context.SetSelected(node.sketchObject.myAIS_InteractiveObject, True)

    def createActions(self):
        self.action_addBezierSurface = QAction(QIcon(""), "Construct a Bezier Surface",
                                               self,
                                               statusTip="Create from two Bezier curve",
                                               triggered=self.partBezierSurface)
        self.action_revolutedSurface = QAction(QIcon(""), "revolve a shape", self,
                                               statusTip="Create surface of revolution based on a selected shape",
                                               triggered=self.partRevolveSurface)
        self.action_extrudedSurface = QAction(QIcon(""), "Extrude a curve", self,
                                              statusTip="Create extruded surface based on a selected shape",
                                              triggered=self.partExtrudedSurface)
        self.action_sweptSurface = QAction(QIcon(""), "Sweep a curve", self,
                                           statusTip="Select a profile and a path to create sweep surface",
                                           triggered=self.partSweptSurface)

    def setModel(self, model):
        self.model = model

    def setRootNode(self, root):
        self.rootNode: Node = root
        self.part.SetRootNode(self.rootNode)

    def partBezierSurface(self):
        self.part.ObjectAction(Part_ObjectTypeOfMethod.BezierSurface_Method)

    def partRevolveSurface(self):
        self.part.ObjectAction(Part_ObjectTypeOfMethod.RevolvedSurface_Method)

    def partExtrudedSurface(self):
        self.part.ObjectAction(Part_ObjectTypeOfMethod.ExtrudedSurface_Method)

    def partSweptSurface(self):
        self.part.ObjectAction(Part_ObjectTypeOfMethod.SweptSurface_Method)

    def OnMouseInputEvent(self, *kargs):
        self.part.OnMouseInputEvent(*kargs)

    def OnMouseMoveEvent(self, *kargs):
        self.part.OnMouseMoveEvent(*kargs)
        self.model.layoutChanged.emit()

    def editGeometry(self):
        self.part.ViewProperties()

    def OnCancel(self):
        self.part.OnCancel()

    def DeleteSelectedObject(self):
        self.part.DeleteSelectedObject()
