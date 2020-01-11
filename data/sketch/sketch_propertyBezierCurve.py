from data.sketch.sketch_property import *
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_Line, Geom2d_BezierCurve
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.ElCLib import *
from OCC.Core.TColgp import TColgp_Array1OfPnt2d
from OCC.Core.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal


def TColgp_Array1OfPnt2d_to_point_list(li: TColgp_Array1OfPnt2d):
    pts =[]
    for i in range(li.Length()):
        point:gp_Pnt2d=li.Value(i+1)
        pts.append([point.X(),point.Y()])
    return pts
def TColStd_Array1OfNumber_to_list(li):
    pts = []
    for i in range(li.Length()):
        num = li.Value(i + 1)
        pts.append(num)
    return pts

class Sketch_PropertyBezierCurve(Sketch_Property):
    def __init__(self, parent, name, fl):
        super(Sketch_PropertyBezierCurve, self).__init__(parent, name, fl)
        if not name:
            self.setObjectName("Property bezier curve")
        self.secondPnt2d = gp_Pnt2d()
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
        self.curGeom2d_Edge: Geom2d_BezierCurve = self.mySObject.GetGeometry()
        poles=TColgp_Array1OfPnt2d_to_point_list(self.curGeom2d_Edge.Poles())
        # weights=TColStd_Array1OfNumber_to_list(self.curGeom2d_Edge.Weights())
        degree=self.curGeom2d_Edge.Degree()
        print(poles,degree)

    def CheckGeometry(self):
        if self.CheckCoord(self.ui.LineEditPoint1, self.tempPnt2d):
            if self.CheckCoord(self.LineEditPoint2, self.temp2Pnt2d):
                return True
        else:
            return False

    def GetGeometry(self):
        if (not self.firstPnt2d.IsEqual(self.tempPnt2d, 1.0e-6)) or (
                not self.secondPnt2d.IsEqual(self.temp2Pnt2d, 1.0e-6)):
            if self.curGeom2d_Edge.SetPoints(self.tempPnt2d, self.temp2Pnt2d):
                self.firstPnt2d.SetX(self.tempPnt2d.X())
                self.firstPnt2d.SetY(self.tempPnt2d.Y())
                self.secondPnt2d.SetX(self.temp2Pnt2d.X())
                self.secondPnt2d.SetY(self.temp2Pnt2d.Y())
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
