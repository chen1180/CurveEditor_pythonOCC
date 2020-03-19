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
        self.ui = Ui_SketchProperty()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModal)


        if not name:
            self.setObjectName("Sketch_Property")
        self.resize(400, 400)
        self.setMaximumSize(QSize(400, 400))
        self.setWindowTitle("Property")

        self.ui.PushButtonOK.clicked.connect(self.onOK)
        self.ui.PushButtonCancel.clicked.connect(self.close)
        self.ui.PushButtonApply.clicked.connect(self.onApply)

        # fileName = "res"
        # fileName = fileName + "/" + "property.png"
        # myIcon = QIcon(QPixmap(fileName))
        # self.setWindowIcon(myIcon)

        self.myNameOfColor = Quantity_NOC_YELLOW
        self.myObjectStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0
        self.myPrs3dAspect = Prs3d_LineAspect(Quantity_Color(self.myNameOfColor), self.myObjectStyle, self.myWidth)
        self.myDrawer = Prs3d_Drawer()
        self.myDrawer.SetLineAspect(self.myPrs3dAspect)

    def SetContext(self, theContext):
        self.myContext = theContext

    def SetAx3(self, theAx3):
        self.myCoordinateSystem = theAx3

    def SetObject(self, CurObject: Sketch_Geometry):
        self.mySObject: Sketch_Geometry = CurObject
        self.myAIS_Object = self.mySObject.GetAIS_Object()
        self.myID = self.mySObject.GetName()
        self.myNameOfColor = self.mySObject.GetColor()
        self.myObjectType = self.mySObject.GetType()

        if not self.isPointWindow:
            self.myObjectStyle = self.mySObject.GetStyle()
            self.myWidth = self.mySObject.GetWidth()
            self.SetObjectStyle()
            self.SetWidth()

        self.SetID()
        self.SetColor()

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
        if self.myNameOfColor != self.GetColor() or self.myObjectStyle != self.GetObjectStyle() or self.myWidth != self.GetWidth():
            self.GetAttributies()
            self.myContext.Redisplay(self.myAIS_Object, True)

    def GetAttributies(self):
        self.myNameOfColor = self.GetColor()
        self.mySObject.SetColor(self.myNameOfColor)
        if self.isPointWindow:
            self.myAIS_Object.SetColor(Quantity_Color(self.myNameOfColor))
        else:
            self.myObjectStyle = self.GetObjectStyle()
            self.myWidth = self.GetWidth()
            self.mySObject.SetStyle(self.myObjectStyle)
            self.mySObject.SetWidth(self.myWidth)

            self.myPrs3dAspect.SetColor(Quantity_Color(self.myNameOfColor))
            self.myPrs3dAspect.SetTypeOfLine(self.myObjectStyle)
            self.myPrs3dAspect.SetWidth(self.myWidth)
            self.myDrawer.SetLineAspect(self.myPrs3dAspect)
            self.myAIS_Object.SetAttributes(self.myDrawer)

    def GetName(self):
        tempID = self.GetID()
        if self.myID != tempID:
            self.myID = tempID
            self.mySObject.SetObjectName(self.myID)

    def SetColor(self):
        if self.myNameOfColor == Quantity_NOC_BLACK:
            self.ui.ComboBoxColor.setCurrentIndex(0)

        elif self.myNameOfColor == Quantity_NOC_BROWN:
            self.ui.ComboBoxColor.setCurrentIndex(1)

        elif self.myNameOfColor == Quantity_NOC_RED:
            self.ui.ComboBoxColor.setCurrentIndex(2)

        elif self.myNameOfColor == Quantity_NOC_ORANGE:
            self.ui.ComboBoxColor.setCurrentIndex(3)

        elif self.myNameOfColor == Quantity_NOC_YELLOW:
            self.ui.ComboBoxColor.setCurrentIndex(4)

        elif self.myNameOfColor == Quantity_NOC_FORESTGREEN:
            self.ui.ComboBoxColor.setCurrentIndex(5)

        elif self.myNameOfColor == Quantity_NOC_GREEN:
            self.ui.ComboBoxColor.setCurrentIndex(6)

        elif self.myNameOfColor == Quantity_NOC_BLUE1:
            self.ui.ComboBoxColor.setCurrentIndex(7)

        elif self.myNameOfColor == Quantity_NOC_DEEPSKYBLUE1:
            self.ui.ComboBoxColor.setCurrentIndex(8)

        elif self.myNameOfColor == Quantity_NOC_LIGHTSKYBLUE:
            self.ui.ComboBoxColor.setCurrentIndex(9)

        elif self.myNameOfColor == Quantity_NOC_CYAN1:
            self.ui.ComboBoxColor.setCurrentIndex(10)

        elif self.myNameOfColor == Quantity_NOC_PURPLE:
            self.ui.ComboBoxColor.setCurrentIndex(11)

        elif self.myNameOfColor == Quantity_NOC_MAGENTA1:
            self.ui.ComboBoxColor.setCurrentIndex(12)

        elif self.myNameOfColor == Quantity_NOC_VIOLET:
            self.ui.ComboBoxColor.setCurrentIndex(13)

        elif self.myNameOfColor == Quantity_NOC_DEEPPINK:
            self.ui.ComboBoxColor.setCurrentIndex(14)

        elif self.myNameOfColor == Quantity_NOC_PINK:
            self.ui.ComboBoxColor.setCurrentIndex(15)

        elif self.myNameOfColor == Quantity_NOC_GRAY70:
            self.ui.ComboBoxColor.setCurrentIndex(16)

        elif self.myNameOfColor == Quantity_NOC_WHITE:
            self.ui.ComboBoxColor.setCurrentIndex(17)

        else:
            self.ui.ComboBoxColor.setCurrentIndex(4)

    def GetColor(self):
        index = self.ui.ComboBoxColor.currentIndex()
        if index == 0:
            return Quantity_NOC_BLACK

        elif index == 1:
            return Quantity_NOC_BROWN

        elif index == 2:
            return Quantity_NOC_RED

        elif index == 3:
            return Quantity_NOC_ORANGE

        elif index == 4:
            return Quantity_NOC_YELLOW

        elif index == 5:
            return Quantity_NOC_FORESTGREEN

        elif index == 6:
            return Quantity_NOC_GREEN

        elif index == 7:
            return Quantity_NOC_BLUE1

        elif index == 8:
            return Quantity_NOC_DEEPSKYBLUE1

        elif index == 9:
            return Quantity_NOC_LIGHTSKYBLUE

        elif index == 10:
            return Quantity_NOC_CYAN1

        elif index == 11:
            return Quantity_NOC_PURPLE

        elif index == 12:
            return Quantity_NOC_MAGENTA1

        elif index == 13:
            return Quantity_NOC_VIOLET

        elif index == 14:
            return Quantity_NOC_DEEPPINK

        elif index == 15:
            return Quantity_NOC_PINK

        elif index == 16:
            return Quantity_NOC_GRAY70

        elif index == 17:
            return Quantity_NOC_WHITE

        else:
            return Quantity_NOC_YELLOW

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
        if self.isPointWindow:
            return 1.0
        else:
            return self.ui.ComboBoxWidth.currentIndex() + 1


if __name__ == '__main__':
    application = QApplication([])
    window = Sketch_Property(None, "test", True)  # Opengl window creation
    window.show()
    application.exec_()
