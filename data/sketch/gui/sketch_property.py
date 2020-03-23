from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from OCC.Core.Aspect import *
from OCC.Core.Prs3d import *
from OCC.Core.Quantity import *
from OCC.Core.gp import *
from OCC.Core.AIS import *
from OCC.Core.BRepBuilderAPI import *
from OCC.Core.TCollection import *
from data.sketch.sketch_object import Sketch_Object
from view.sketchProperty import Ui_SketchProperty
from data.sketch.sketch_utils import *
from data.node import *


class Sketch_Property(QWidget):
    def __init__(self, parent, name, fl):
        super(Sketch_Property, self).__init__(parent)
        self.StartCoord = "["
        self.MidCoord = ","
        self.EndCoord = "]"
        self.NumberExpr = "[^0-9.-]"
        self.firstPnt2d = gp_Pnt2d()
        self.tempPnt2d = gp_Pnt2d()
        self.isPointWindow = False
        # UI initialization
        self.ui = Ui_SketchProperty()
        self.ui.setupUi(self)
        self.setMinimumSize(QSize(400, 600))
        self.setWindowModality(Qt.ApplicationModal)
        # color palette
        self.uiPalette = self.ui.PushButtonColor.palette()
        self.uiPalette.setColor(QPalette.Window, Qt.red)
        self.ui.PushButtonColor.setPalette(self.uiPalette)
        self.ui.PushButtonColor.setAutoFillBackground(True)
        self.ui.PushButtonColor.clicked.connect(self.openColorDialog)
        if not name:
            self.setObjectName("Sketch_Property")
        # self.resize(400, 400)
        # self.setMaximumSize(QSize(400, 400))
        self.setWindowTitle("Property")

        self.ui.PushButtonOK.clicked.connect(self.onOK)
        self.ui.PushButtonCancel.clicked.connect(self.close)
        self.ui.PushButtonApply.clicked.connect(self.onApply)

        myIcon = QIcon(QPixmap(":/settings.png"))
        self.setWindowIcon(myIcon)

        self.myColor = Quantity_NOC_YELLOW
        self.myObjectStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0

    def openColorDialog(self):
        color:QColor = QColorDialog.getColor()
        if color.isValid():
            self.ui.PushButtonColor.setStyleSheet("background-color:{};".format(color.name()))
            self.ui.PushButtonColor.setText(str(color.getRgb()))
            self.myColor=color.getRgbF()

    def SetContext(self, theContext):
        self.myContext = theContext

    def SetAx3(self, theAx3):
        self.myCoordinateSystem = theAx3

    def SetObject(self, CurObject: Sketch_Geometry):
        self.mySObject: Sketch_Geometry = CurObject
        self.myAIS_Object = self.mySObject.GetAIS_Object()
        self.myID = self.mySObject.GetName()
        self.myColor = self.mySObject.GetColor()
        self.myObjectType = self.mySObject.GetType()
        self.myWidth = self.mySObject.GetWidth()
        if not self.isPointWindow:
            self.myObjectStyle = self.mySObject.GetStyle()
            self.SetObjectStyle()


        self.SetID()
        self.SetColor()
        self.SetWidth()
        self.SetGeometry()
        self.show()

    def onOK(self):
        if self.CheckGeometry():
            if self.GetGeometry():
                self.GetAttributies()
            else:
                self.CheckAttributies()
            self.GetName()
            self.mySObject.SetAIS_Object(self.myAIS_Object)
            self.myContext.Display(self.myAIS_Object, True)
            self.close()

    def onApply(self):
        if self.CheckGeometry():
            if self.GetGeometry():
                self.GetAttributies()
                self.mySObject.SetAIS_Object(self.myAIS_Object)
                self.myContext.Display(self.myAIS_Object, True)
            else:
                self.CheckAttributies()
            self.GetName()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        button = a0.key()
        if button == Qt.Key_Escape:
            self.close()

    def SetID(self):
        self.ui.LineEditID.setText(self.myID)

    def GetID(self):
        return self.ui.LineEditID.text()

    def SetCoord(self, le: QLineEdit, p):
        NumName = self.StartCoord + str(round(p.X(), 1)) + self.MidCoord + str(round(p.Y(), 1)) + self.EndCoord
        le.setText(NumName)

    def CheckCoord(self, le: QLineEdit, p: gp_Pnt2d):
        NumName = le.text()
        if NumName[0] == self.StartCoord and NumName[-1] == self.EndCoord:
            NumName = NumName.strip("[]")
            NumName = NumName.split(",")
            x = NumName[0]
            y = NumName[1]
            try:
                x = float(x)
                y = float(y)
                p.SetCoord(x, y)
                return True
            except Exception as e:
                print(e)
        le.selectAll()
        return False

    def CheckAttributies(self):
        if self.myColor != self.GetColor() or self.myObjectStyle != self.GetObjectStyle() or self.myWidth != self.GetWidth():
            self.GetAttributies()
            self.myContext.Redisplay(self.mySObject.GetAIS_Object(), True)

    def GetAttributies(self):
        self.myColor = self.GetColor()
        self.mySObject.SetColor(self.myColor)

        self.myWidth = self.GetWidth()
        self.mySObject.SetWidth(self.myWidth)

        if self.isPointWindow:
            pass
        else:
            self.myObjectStyle = self.GetObjectStyle()

            self.mySObject.SetStyle(self.myObjectStyle)


    def GetName(self):
        tempID = self.GetID()
        if self.myID != tempID:
            self.myID = tempID
            self.mySObject.SetObjectName(self.myID)

    def SetColor(self):
        color=Quantity_Color(self.myColor).Values(Quantity_TOC_RGB)
        color=tuple([int(i*255) for i in color])
        self.ui.PushButtonColor.setText(str(color))
        self.ui.PushButtonColor.setStyleSheet("background-color: rgb{};".format(color))

    def GetColor(self):
        color=self.ui.PushButtonColor.text().replace("(","").replace(")","").split(",")
        r=float(color[0].strip())/255.0
        g=float(color[1].strip())/255.0
        b=float(color[2].strip())/255.0
        return Quantity_Color().Name(r,g,b)

    def SetObjectStyle(self):
        self.ui.ComboBoxStyle.setCurrentIndex(self.myObjectStyle)

    def GetObjectStyle(self):
        if self.isPointWindow:
            return Aspect_TOL_SOLID
        else:
            return self.ui.ComboBoxStyle.currentIndex()

    def SetWidth(self):
        self.ui.ComboBoxWidth.setCurrentIndex(int(self.myWidth) - 1)

    def GetWidth(self):
        return self.ui.ComboBoxWidth.currentIndex() + 1


if __name__ == '__main__':
    application = QApplication([])
    window = Sketch_Property(None, "test", True)  # Opengl window creation
    window.show()
    application.exec_()
