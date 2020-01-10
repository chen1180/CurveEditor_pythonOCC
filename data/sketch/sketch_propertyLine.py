from data.sketch.sketch_property import *
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_Line
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.ElCLib import *
from data.sketch.geometry.geom2d_edge import Geom2d_Edge


class Sketch_PropertyLine(Sketch_Property):
    def __init__(self, parent, name, fl):
        super(Sketch_PropertyLine, self).__init__(parent, name, fl)
        if not name:
            self.setObjectName("Property Lines")
        self.secondPnt2d=gp_Pnt2d()
        self.temp2Pnt2d = gp_Pnt2d()
        self.ui.TextLabelPoint1.setText("Point 1")
        self.TextLabelPoint2 = QLabel(self.ui.GroupBoxGP)
        self.TextLabelPoint2.setText("Point 2")
        self.LineEditPoint2 = QLineEdit(self.ui.GroupBoxGP)
        self.ui.GroupBoxGPLayout.addWidget(self.TextLabelPoint2, 1, 0)
        self.ui.GroupBoxGPLayout.addWidget(self.LineEditPoint2, 1, 1)

        self.TextLabelLength = QLabel(self.ui.GroupBoxAttributes)
        self.TextLabelLength.setText("Length")
        self.LineEditLength = QLineEdit(self.ui.GroupBoxAttributes)
        self.LineEditLength.setEnabled(False)

        self.ui.GroupBoxAttributesLayout.addWidget(self.TextLabelLength, 4, 0)
        self.ui.GroupBoxAttributesLayout.addWidget(self.LineEditLength, 4, 1)

    def SetGeometry(self, *__args):
        self.curGeom2d_Edge: Geom2d_Edge = self.mySObject.GetGeometry()
        self.firstPnt2d = self.curGeom2d_Edge.GetStart_Pnt()
        self.secondPnt2d = self.curGeom2d_Edge.GetEnd_Pnt()
        self.SetCoord(self.ui.LineEditPoint1, self.firstPnt2d)
        self.SetCoord(self.LineEditPoint2, self.secondPnt2d)
        self.SetLineLength()

    def CheckGeometry(self):
        if self.CheckCoord(self.ui.LineEditPoint1, self.tempPnt2d):
            return self.CheckCoord(self.LineEditPoint2, self.temp2Pnt2d)
        else:
            return False

    def GetGeometry(self):
        if (not self.firstPnt2d.IsEqual(self.tempPnt2d, 1.0e-8)) or ( not self.secondPnt2d.IsEqual(self.temp2Pnt2d, 1.0e-8)):
            if self.curGeom2d_Edge.SetPoints(self.tempPnt2d, self.temp2Pnt2d):
                self.firstPnt2d = self.tempPnt2d
                self.secondPnt2d = self.temp2Pnt2d
                Geom_Point1 = Geom_CartesianPoint(elclib.To3d(self.myCoordinateSystem.Ax2(), self.firstPnt2d))
                Geom_Point2 = Geom_CartesianPoint(elclib.To3d(self.myCoordinateSystem.Ax2(), self.secondPnt2d))
                myAIS_Line = AIS_Line(Geom_Point1, Geom_Point2)
                # edge = BRepBuilderAPI_MakeEdge(Geom_Point1.Pnt(), Geom_Point2.Pnt())
                # myAIS_Line = AIS_Shape(edge.Shape())
                self.myContext.Remove(self.myAIS_Object, True)
                self.myAIS_Object = myAIS_Line
                self.SetLineLength()
                return True
        return False

    def SetLineLength(self):
        length = ((self.firstPnt2d.X() - self.secondPnt2d.X()) ** 2 + (
                self.firstPnt2d.Y() - self.secondPnt2d.Y()) ** 2) ** 0.5
        length=round(length,1)
        self.LineEditLength.setText(str(length))