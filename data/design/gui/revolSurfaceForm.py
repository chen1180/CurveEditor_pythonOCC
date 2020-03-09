from view import createRevolSurfaceForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from OCC.Core.AIS import *
from data.model import SceneGraphModel
from data.sketch.geometry import *
from data.sketch.sketch_type import *
from data.node import *


class RevolSurfaceForm(QWidget):
    def __init__(self, parent=None):
        super(RevolSurfaceForm, self).__init__()
        self.ui = createRevolSurfaceForm.Ui_Form()
        self.ui.setupUi(self)
        self.parent = parent
        self.myProfile = None
        self.myAxis = None
        self.myAngle = 360
        self.myGeomSurface = None
        self.ui.uiChangeProfile.clicked.connect(self.SelectProfile)
        self.ui.uiChangeAxis.clicked.connect(self.SelectAxis)
        self.ui.uiPreview.clicked.connect(self.PreviewSurface)
        self.ui.uiOk.clicked.connect(self.ApplyChange)
        self.selectProfile = False
        self.selectAxis = False

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
                    self.ui.uiProfile.setText(myCurObject.GetName())
                    self.myProfile = myCurObject

    def SelectAxis(self):
        self.parent.Hide()
        self.ui.uiChangeAxis.setText("Selecting")
        self.selectAxis = True

    def SetAxis(self):
        self.parent.Show()
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.uiAxis.setText(myCurObject.GetName())
                    self.myAxis = myCurObject

    def CheckType(self):
        if self.myProfile:
            if self.myProfile.GetTypeOfMethod() is Sketch_ObjectTypeOfMethod.Line2P_Method:
                raise TypeError("Profile must be a curve")
        else:
            raise ValueError("Please select a profile curve!")
        if self.myAxis:
            if self.myAxis.GetTypeOfMethod() is not Sketch_ObjectTypeOfMethod.Line2P_Method:
                raise TypeError("Axis must be a line")
        else:
            raise ValueError("Please select a revolve axis!")
        return True

    def PreviewSurface(self):
        if self.myGeomSurface:
            self.myGeomSurface.RemoveDisplay()
            del self.myGeomSurface
        if self.CheckType():
            self.myGeomSurface = Surface_Revolved(self.myContext)
            self.myGeomSurface.SetCurves(self.myProfile)
            self.myGeomSurface.SetRevolveAxis(self.myAxis)
            self.myGeomSurface.SetAngle(self.ui.uiDegree.value())
            self.myGeomSurface.Compute()

    def ApplyChange(self):
        if self.myGeomSurface:
            root = self.myModel.getNode(QModelIndex())
            self.revolveSurfaceNode = RevolvedSurfaceNode(self.myGeomSurface.GetName(), root)
            self.revolveSurfaceNode.setSketchObject(self.myGeomSurface)
            self.myModel.layoutChanged.emit()


# -----------------------------Debugging-----------------------------------#
if __name__ == '__main__':
    application = QApplication([])
    window = RevolSurfaceForm()  # Opengl window creation
    window.show()
    application.exec_()
