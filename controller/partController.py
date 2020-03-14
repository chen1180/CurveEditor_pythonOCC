from PyQt5.QtCore import QModelIndex, QObject, pyqtSignal
from PyQt5.QtWidgets import QAction, QStatusBar
from PyQt5.QtGui import QIcon
from data.design.part import Part
from data.design.part_type import *
from data.node import *
from data.model import SceneGraphModel
from data.design.gui import part_qtgui


class PartController(QObject):
    modelUpdated = pyqtSignal(object)

    def __init__(self, display, parent=None):
        super(PartController, self).__init__(parent)
        self._display = display
        self._statusBar: QStatusBar = parent.statusBar()
        self.partGUI = part_qtgui.Part_QTGUI(parent)
        self.part = Part(self._display, self._statusBar, self.partGUI)
        self.parent = parent
        self.model: SceneGraphModel = None
        self.currentSketchNode: SketchObjectNode = None
        self.actions = []
        self.createActions()

    def highlightCurrentNode(self, current: QModelIndex, old: QModelIndex):
        node: SketchObjectNode = current.internalPointer()
        if isinstance(node, SketchNode):
            self.selectSketchNode(node)
        elif isinstance(node, SketchObjectNode):
            self._display.Context.SetSelected(node.sketchObject.myAIS_InteractiveObject, True)

    def createActions(self):
        self.action_addBezierSurface = QAction(QIcon(":/bezier_surface.png"), "Bezier Surface",
                                               self,
                                               statusTip="Create from two Bezier curve",
                                               triggered=self.partBezierSurface)
        self.actions.append(self.action_addBezierSurface)
        self.action_revolutedSurface = QAction(QIcon(":/revolve.png"), "Revolve", self,
                                               statusTip="Create surface of revolution based on a selected shape",
                                               triggered=self.partRevolveSurface)
        self.actions.append(self.action_revolutedSurface)
        self.action_extrudedSurface = QAction(QIcon(":/extrude.png"), "Extrude", self,
                                              statusTip="Create extruded surface based on a selected shape",
                                              triggered=self.partExtrudedSurface)
        self.actions.append(self.action_extrudedSurface)
        self.action_sweptSurface = QAction(QIcon(":/sweep.png"), "Sweep", self,
                                           statusTip="Select a profile and a path to create sweep surface",
                                           triggered=self.partSweptSurface)
        self.actions.append(self.action_sweptSurface)

    def setModel(self, model):
        self.model = model
        self.part.SetModel(self.model)

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

    def editGeometry(self):
        self.part.ViewProperties()

    def OnCancel(self):
        self.part.OnCancel()

    def DeleteSelectedObject(self):
        root: Node = self.model.getNode(QModelIndex())
        index = 0
        while index < root.childCount():
            child = root.child(index)
            if isinstance(child, BezierSurfaceNode) or isinstance(child, SweepSurfaceNode) or isinstance(child,
                                                                                                         ExtrudedSurfaceNode) or isinstance(
                    child, RevolvedSurfaceNode):
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self._display.Context.IsSelected(myCurObject.GetAIS_Object()):
                    myCurObject.RemoveDisplay()
                    self.model.removeRow(index, QModelIndex())
                else:
                    index += 1
            else:
                index += 1
        # inform model to update
        self.model.layoutChanged.emit()
