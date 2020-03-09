from view import createBezierSurfaceForm
from PyQt5.QtWidgets import QWidget, QApplication, QAbstractItemView
from PyQt5.QtCore import QModelIndex, Qt
from OCC.Core.AIS import *
from data.model import SceneGraphModel
from data.sketch.geometry import *
from data.sketch.sketch_type import *
from data.node import *


class BezierSurfaceForm(QWidget):
    def __init__(self, parent=None):
        super(BezierSurfaceForm, self).__init__()
        self.ui = createBezierSurfaceForm.Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox.setItemData(0, "the style with the flattest patches", Qt.ToolTipRole)
        self.ui.comboBox.setItemData(1, "a rounded style of patch with less depth than those of Curved", Qt.ToolTipRole)
        self.ui.comboBox.setItemData(2, " the style with the most rounded patches", Qt.ToolTipRole)
        self.ui.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.uiAddCurve.clicked.connect(self.AddCurve)
        self.ui.uiDeleteCurve.clicked.connect(self.DeleteCurve)
        self.ui.uiPreview.clicked.connect(self.PreviewSurface)
        self.ui.uiOk.clicked.connect(self.ApplyChange)
        self.myCurves = []
        self.myGeomSurface=None

    def SetContext(self, theContext):
        self.myContext: AIS_InteractiveContext = theContext

    def SetModel(self, theModel):
        self.myModel: SceneGraphModel = theModel

    def AddCurve(self):
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.listWidget.addItem(myCurObject.GetName())
                    self.myCurves.append(myCurObject)

    def DeleteCurve(self):
        items = self.ui.listWidget.selectedItems()
        for i, item in enumerate(items):
            row = self.ui.listWidget.row(item)
            self.ui.listWidget.takeItem(row)
            self.myCurves.pop(row)

    def CheckCurveType(self):
        if self.myCurves:
            for curve in self.myCurves:
                if curve.GetTypeOfMethod() is not Sketch_ObjectTypeOfMethod.BezierCurve_Method:
                    raise TypeError("Selections must be BezierCurve. Pls remove the other types of geometry")
            return True

    def PreviewSurface(self):
        if self.myGeomSurface:
            self.myGeomSurface.RemoveDisplay()
            del self.myGeomSurface
        if self.CheckCurveType():
            self.myGeomSurface = Surface_Bezier(self.myContext)
            self.myGeomSurface.SetCurves([curve.GetGeometry() for curve in self.myCurves])
            self.myGeomSurface.SetStyle(self.ui.comboBox.currentIndex())
            self.myGeomSurface.Compute()

    def ApplyChange(self):
        if self.myGeomSurface:
            root = self.myModel.getNode(QModelIndex())
            self.bezierSurfaceNode = BezierSurfaceNode(self.myGeomSurface.GetName(), root)
            self.bezierSurfaceNode.setSketchObject(self.myGeomSurface)
            self.myModel.layoutChanged.emit()


# -----------------------------Debugging-----------------------------------#
if __name__ == '__main__':
    application = QApplication([])
    window = BezierSurfaceForm()  # Opengl window creation
    window.show()
    application.exec_()
