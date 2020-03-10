from view import createExtrudedSurfaceForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from OCC.Core.AIS import *
from data.model import SceneGraphModel
from data.sketch.geometry import *
from data.sketch.sketch_type import *
from data.node import *


class ExtrudedSurfaceForm(QWidget):
    def __init__(self, parent=None):
        super(ExtrudedSurfaceForm, self).__init__()
        self.ui = createExtrudedSurfaceForm.Ui_Form()
        self.ui.setupUi(self)
        self.ui.uiAlongNormal.setChecked(True)
        self.EnableEdgeWidgets(False)
        self.ui.uiAlongEdge.toggled.connect(self.EnableEdgeWidgets)
        self.ui.uiSelectButton.clicked.connect(self.SelectProfile)
        self.ui.uiSelectEdgeButton.clicked.connect(self.SelectDirection)
        self.ui.uiPreview.clicked.connect(self.PreviewSurface)
        self.ui.uiOk.clicked.connect(self.ApplyChange)
        self.parent = parent
        self.myProfile = None
        self.myDirection = None
        self.myGeomSurface = None
        self.selectProfile = False
        self.selectDirection = False

    def EnableEdgeWidgets(self, checked):
        self.ui.uiEdgeLineEdit.setEnabled(checked)
        self.ui.uiSelectEdgeButton.setEnabled(checked)

    def SetContext(self, theContext):
        self.myContext: AIS_InteractiveContext = theContext

    def SetModel(self, theModel):
        self.myModel: SceneGraphModel = theModel

    def SelectProfile(self):
        self.parent.Hide()
        self.selectProfile = True

    def SetProfile(self):
        self.parent.Show()
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.uiProfileLineEdit.setText(myCurObject.GetName())
                    self.myProfile = myCurObject
                    self.myNormalAxis = planeNode.getSketchPlane().Axis()

    def SelectDirection(self):
        self.parent.Hide()
        self.ui.uiSelectEdgeButton.setText("Selecting")
        self.selectDirection = True

    def SetDirections(self):
        self.parent.Show()
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.uiEdgeLineEdit.setText(myCurObject.GetName())
                    self.myDirection = myCurObject

    def CheckType(self):
        if self.myProfile:
            if self.myProfile.GetTypeOfMethod() is Sketch_ObjectTypeOfMethod.Line2P_Method:
                raise TypeError("Profile must be a curve")
        else:
            raise ValueError("Please select a profile curve!")
        if self.ui.uiAlongEdge.isChecked():
            if self.myDirection:
                if self.myDirection.GetTypeOfMethod() is not Sketch_ObjectTypeOfMethod.Line2P_Method:
                    raise TypeError("Axis must be a line")
            else:
                raise ValueError("Please select a edge!")
        return True

    def PreviewSurface(self):
        if self.myGeomSurface:
            self.myGeomSurface.RemoveDisplay()
            del self.myGeomSurface
        if self.CheckType():
            self.myGeomSurface = Surface_LinearExtrusion(self.myContext)
            if self.ui.uiAlongNormal.isChecked():
                axis = gp_Vec(self.myNormalAxis.Direction())
            if self.ui.uiAlongEdge.isChecked():
                axis=gp_Vec(self.myDirection.GetGeometry().Position().Direction())
            self.myGeomSurface.SetCurves(self.myProfile.GetGeometry())
            self.myGeomSurface.SetDirection(axis)
            self.myGeomSurface.SetLength(self.ui.uiLength.value())
            self.myGeomSurface.Compute()

    def ApplyChange(self):
        if self.myGeomSurface:
            root = self.myModel.getNode(QModelIndex())
            extrudedSurfaceNode = ExtrudedSurfaceNode(self.myGeomSurface.GetName(), root)
            extrudedSurfaceNode.setSketchObject(self.myGeomSurface)
            self.myModel.layoutChanged.emit()
        self.Finish()
    def Finish(self):
        self.myGeomSurface=None
        self.parent.Hide()


# -----------------------------Debugging-----------------------------------#
if __name__ == '__main__':
    application = QApplication([])
    window = ExtrudedSurfaceForm()  # Opengl window creation
    window.show()
    application.exec_()
