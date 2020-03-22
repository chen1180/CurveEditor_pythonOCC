from view import createSweepSurfaceForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from OCC.Core.AIS import *
from data.model import SceneGraphModel
from data.sketch.geometry import *
from data.sketch.sketch_type import *
from data.node import *


class SweepSurfaceForm(QWidget):
    def __init__(self, parent=None):
        super(SweepSurfaceForm, self).__init__()
        self.ui = createSweepSurfaceForm.Ui_Form()
        self.ui.setupUi(self)
        self.ui.uiCircularRadioButton.setChecked(True)
        self.EnableRadiusWidgets(True)
        self.EnableConstantSectionWidgets(False)
        self.EnableEvolvingSectionWidgets(False)
        self.ui.uiCircularRadioButton.toggled.connect(self.EnableRadiusWidgets)
        self.ui.uiConstantSectionRadioButton.toggled.connect(self.EnableConstantSectionWidgets)
        self.ui.uiEvolvingSectionRadioButton.toggled.connect(self.EnableEvolvingSectionWidgets)
        self.ui.uiPreview.clicked.connect(self.PreviewSurface)
        self.ui.uiOk.clicked.connect(self.ApplyChange)
        self.ui.uiSelectPathButton.clicked.connect(self.SelectPath)
        self.ui.uiSelectConstantSectionButton.clicked.connect(self.SelectConstantSection)
        self.ui.uiSelectFirstSectionButton.clicked.connect(self.SelectFirstSection)
        self.ui.uiSelectLastSectionButton.clicked.connect(self.SelectLastSection)
        self.parent = parent
        # flags
        self.selectPath = False
        self.selectConstantSection = False
        self.selectFirstSection = False
        self.selectLastSection = False
        # variables for surface generation
        self.myPath = None
        self.myConstantSection = None
        self.myFirstSection = None
        self.myLastSection = None
        self.myGeomSurface = None

    def EnableRadiusWidgets(self, checked):
        self.ui.uiRadiusLabel.setEnabled(checked)
        self.ui.uiRadiusSpinBox.setEnabled(checked)

    def EnableConstantSectionWidgets(self, checked):
        self.ui.uiConstantSectionLineEdit.setEnabled(checked)
        self.ui.uiSelectConstantSectionButton.setEnabled(checked)

    def EnableEvolvingSectionWidgets(self, checked):
        self.ui.uiFirstSectionLineEdit.setEnabled(checked)
        self.ui.uiSelectFirstSectionButton.setEnabled(checked)
        self.ui.uiLastSectionLineEdit.setEnabled(checked)
        self.ui.uiSelectLastSectionButton.setEnabled(checked)

    def SetContext(self, theContext):
        self.myContext: AIS_InteractiveContext = theContext

    def SetModel(self, theModel):
        self.myModel: SceneGraphModel = theModel

    def SelectPath(self):
        self.parent.Hide()
        self.selectPath = True

    def SelectConstantSection(self):
        self.parent.Hide()
        self.selectConstantSection = True

    def SelectFirstSection(self):
        self.parent.Hide()
        self.selectFirstSection = True

    def SelectLastSection(self):
        self.parent.Hide()
        self.selectLastSection = True

    def SetPath(self):
        self.parent.Show()
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.uiPathLineEdit.setText(myCurObject.GetName())
                    self.myPath = myCurObject

    def SetConstantSection(self):
        self.parent.Show()
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.uiConstantSectionLineEdit.setText(myCurObject.GetName())
                    self.myConstantSection = myCurObject

    def SetFirstSection(self):
        self.parent.Show()
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.uiFirstSectionLineEdit.setText(myCurObject.GetName())
                    self.myFirstSection = myCurObject

    def SetLastSection(self):
        self.parent.Show()
        root = self.myModel.getNode(QModelIndex())
        for i, planeNode in enumerate(root.children()):
            for child in planeNode.children():
                myCurObject: Sketch_Geometry = child.getSketchObject()
                if self.myContext.IsSelected(myCurObject.GetAIS_Object()):
                    self.ui.uiLastSectionLineEdit.setText(myCurObject.GetName())
                    self.myLastSection = myCurObject

    def CheckType(self):
        return True

    def PreviewSurface(self):
        if self.myGeomSurface:
            self.myGeomSurface.RemoveDisplay()
            del self.myGeomSurface
        if self.CheckType():
            self.myGeomSurface = Surface_Sweep(self.myContext)
            self.myGeomSurface.SetPath(self.myPath.GetGeometry())
            if self.ui.uiCircularRadioButton.isChecked():
                self.myGeomSurface.SetConstructionMethod(0)
                self.myGeomSurface.SetRadius(self.ui.uiRadiusSpinBox.value())
            elif self.ui.uiConstantSectionRadioButton.isChecked():
                self.myGeomSurface.SetConstructionMethod(1)
                self.myGeomSurface.SetSections([self.myConstantSection.GetGeometry()])
            elif self.ui.uiEvolvingSectionRadioButton.isChecked():
                self.myGeomSurface.SetConstructionMethod(2)
                self.myGeomSurface.SetSections([self.myFirstSection.GetGeometry(), self.myLastSection.GetGeometry()])
            self.myGeomSurface.Compute()

    def ApplyChange(self):
        if self.myGeomSurface:
            root = self.myModel.getNode(QModelIndex())
            sweepSurfaceNode = SweepSurfaceNode(self.myGeomSurface.GetName(), root)
            sweepSurfaceNode.setSketchObject(self.myGeomSurface)
            self.myModel.layoutChanged.emit()
        self.Finish()

    def Finish(self):
        self.myGeomSurface = None
        self.parent.Hide()


# -----------------------------Debugging-----------------------------------#
if __name__ == '__main__':
    application = QApplication([])
    window = SweepSurfaceForm()  # Opengl window creation
    window.show()
    application.exec_()
