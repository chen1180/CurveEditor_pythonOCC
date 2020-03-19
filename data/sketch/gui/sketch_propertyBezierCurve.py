from data.sketch.gui.sketch_property import *
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BezierCurve
from OCC.Core.Geom import Geom_CartesianPoint, Geom_BezierCurve
from OCC.Core.ElCLib import *
from view.basisFunctionPlot import BezierBasisFunctionWindow
from functools import lru_cache
import math


class Sketch_PropertyBezierCurve(Sketch_Property):
    def __init__(self, parent, name, fl):
        super(Sketch_PropertyBezierCurve, self).__init__(parent, name, fl)
        if not name:
            self.setObjectName("Property bezier curve")
        self.geometry_dict = {}
        self.ui_initialized = False
        self.mySObject: Sketch_BezierCurve = None
        self.canvas = BezierBasisFunctionWindow(self)
        self.ui.PushButtonPlot.clicked.connect(self.plotBasisFunction)
        self.ui.PushButtonAnimate.clicked.connect(self.animateCurveConstruction)
        self.animatedGeometry=[]
        # ui
        self.ui.TextLabelPoint1.close()
        self.ui.LineEditPoint1.close()

    def SetGeometry(self, *__args):
        self.curGeom2d_BezierCurve: Geom2d_BezierCurve = self.mySObject.GetGeometry2d()
        # save data and create gui
        poles = [pole.GetGeometry2d().Pnt2d() for pole in self.mySObject.GetPoles()]
        weights = self.mySObject.myWeights
        nbPoles = self.curGeom2d_BezierCurve.NbPoles()
        degree = self.curGeom2d_BezierCurve.Degree()
        closed_flag = self.curGeom2d_BezierCurve.IsClosed()
        rational_flag = self.curGeom2d_BezierCurve.IsRational()
        continuity = self.curGeom2d_BezierCurve.Continuity()
        self.geometry_dict = {"poles": poles, "weights": weights, "degree": degree, "closed": closed_flag,
                              "rational": rational_flag,
                              "continuity": continuity, "nbPoles": nbPoles}
        self.setupUI()

    def CheckGeometry(self):
        return True

    def GetGeometry(self):
        needUpdate = False
        for idx in range(self.poles.childCount()):
            pole = self.poles.child(idx)
            x = pole.child(0)
            y = pole.child(1)
            coordinate_x: QDoubleSpinBox = self.tree.itemWidget(x, 1)
            coordinate_y: QDoubleSpinBox = self.tree.itemWidget(y, 1)
            new_pole2d = gp_Pnt2d(coordinate_x.value(), coordinate_y.value())
            # original pole coordinate
            old_pole2d = self.geometry_dict["poles"][idx]
            if not new_pole2d.IsEqual(old_pole2d, 1.0e-6):
                needUpdate = True
                # update old poles interactive points
                self.mySObject.GetPoles()[idx].DragTo(new_pole2d)

        for idx in range(self.weights.childCount()):
            weights = self.weights.child(idx)
            weight_spinbox: QDoubleSpinBox = self.tree.itemWidget(weights, 1)
            weight_value = weight_spinbox.value()
            self.mySObject.ChangeWeights(index=idx, weight=weight_value)
        # check if the geometry of curve (coordinate of poles) has changed.
        if needUpdate:
            self.mySObject.Recompute()
            self.updateUI()
            return True
        return False

    def setupUI(self):
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['Key', 'Value', 'Action'])
        self.ui.GroupBoxGPLayout.addWidget(self.tree, 1, 0, 1, 3)
        self.degree = QTreeWidgetItem(self.tree, ["degree", str(self.geometry_dict["degree"])])
        self.button = QPushButton()
        self.button.setText("Increase degree")
        self.button.clicked.connect(self.degreeElevation)
        self.tree.setItemWidget(self.degree, 2, self.button)
        self.closed = QTreeWidgetItem(self.tree, ["Is closed", str(self.geometry_dict["closed"])])
        self.rational = QTreeWidgetItem(self.tree, ["Is rational", str(self.geometry_dict["rational"])])
        self.continuity = QTreeWidgetItem(self.tree, ["Continuity", str(self.geometry_dict["continuity"])])
        self.poles = QTreeWidgetItem(self.tree, ["poles", str(self.geometry_dict["nbPoles"])])
        self.poles.setData(0, Qt.UserRole, self.geometry_dict["poles"])
        for k, v in enumerate(self.geometry_dict["poles"]):
            poles_children = QTreeWidgetItem(self.poles, [str(k), str((round(v.X(), 2), round(v.Y(), 2)))])
            coordinate_x = QTreeWidgetItem()
            coordinate_x.setText(0, "x")
            coordinate_y = QTreeWidgetItem()
            coordinate_y.setText(0, "y")
            x_widget = QDoubleSpinBox()
            x_widget.setRange(-10000, 10000)
            x_widget.setValue(v.X())
            y_widget = QDoubleSpinBox()
            y_widget.setRange(-10000, 10000)
            y_widget.setValue(v.Y())
            poles_children.addChild(coordinate_x)
            poles_children.addChild(coordinate_y)
            self.tree.setItemWidget(coordinate_x, 1, x_widget)
            self.tree.setItemWidget(coordinate_y, 1, y_widget)
        weights = self.geometry_dict["weights"]
        if weights is None:
            weights = [1.0] * self.geometry_dict["nbPoles"]
        self.weights = QTreeWidgetItem(self.tree, ["weights", str(weights)])
        for idx, value in enumerate(weights):
            weights_children = QTreeWidgetItem(self.weights)
            weights_children.setText(0, str(idx))
            widget = QDoubleSpinBox()
            widget.setRange(0.1, 1.0)
            widget.setSingleStep(0.1)
            widget.setValue(value)
            self.tree.setItemWidget(weights_children, 1, widget)

        self.tree.addTopLevelItem(self.poles)

    def degreeElevation(self):
        self.mySObject.IncreaseDegree(self.geometry_dict["degree"] + 1)
        self.SetGeometry()
        self.updateUI()

    def updateUI(self):
        degree = self.curGeom2d_BezierCurve.Degree()
        closed_flag = self.curGeom2d_BezierCurve.IsClosed()
        rational_flag = self.curGeom2d_BezierCurve.IsRational()
        continuity = self.curGeom2d_BezierCurve.Continuity()
        self.degree.setText(1, str(degree))
        self.closed.setText(1, str(closed_flag))
        self.rational.setText(1, str(rational_flag))
        self.continuity.setText(1, str(continuity))

    def plotBasisFunction(self):
        self.canvas.setBasisFunction(self.geometry_dict["nbPoles"])
        self.canvas.plot()
        self.canvas.show()

    def lerp(self, pnt2d_1, pn2d_2, t):
        s = 1 - t
        return gp_Pnt2d(pnt2d_1.X() * s + pn2d_2.X() * t, pnt2d_1.Y() * s + pn2d_2.Y() * t)

    @lru_cache(1000)
    def DeCastlejau(self, coorArr, i, j, t):
        if j == 0:
            return coorArr[i]
        return self.DeCastlejau(coorArr, i, j - 1, t) * (1 - t) + self.DeCastlejau(coorArr, i + 1, j - 1, t) * t

    def binomial(self, i, n):
        """Binomial coefficient"""
        return math.factorial(n) / float(
            math.factorial(i) * math.factorial(n - i))

    def bernstein(self, t, i, n):
        """Bernstein polynom"""
        return self.binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))

    def animateCurveConstruction(self):
        # remove the last animation shape first
        if self.animatedGeometry:
            for _ in self.animatedGeometry:
                _.RemoveDisplay()
        poles = self.geometry_dict["poles"]
        x_poles = tuple([i.X() for i in poles])
        y_poles = tuple([i.Y() for i in poles])
        degree = len(poles) - 1
        points_list = []
        for i in range(1, degree + 1):
            points_list.append(poles[0:(len(poles) - i)])
        bezier_point = Sketch_Point(self.myContext, self.myCoordinateSystem)
        bezier_point.Compute(poles[0])
        bezier_point.SetStyle(Aspect_TOM_O_PLUS)
        bezier_point.SetColor(Quantity_Color(Quantity_NOC_RED1))
        self.animatedGeometry.append(bezier_point)
        line_list = []
        for _ in points_list:
            if len(_) >= 2:
                lines = []
                for idx in range(len(_) - 1):
                    line = Sketch_Line(self.myContext, self.myCoordinateSystem)
                    line.AddPoints(_[idx])
                    line.AddPoints(_[idx + 1])
                    line.Compute()
                    line.SetColor(Quantity_Color(1, i / degree, 1, 0))
                    lines.append(line)
                    self.animatedGeometry.append(line)
                line_list.append(lines)
        # aCubeTrsf = gp_Trsf2d()
        # tA = time.time()
        # for t in np.linspace(0, 1, 10):
        #     for i in range(len(points_list)):
        #         computed_point = []
        #         for idx in range(len(points_list[i])):
        #             new_point = gp_Pnt2d(self.B(x_poles, idx, i + 1, t), self.B(y_poles, idx, i + 1, t))
        #             points_list[i][idx].DragTo(new_point)
        #             computed_point.append(new_point)
        #         if i < len(points_list) - 1:
        #             for j in range(len(computed_point) - 1):
        #                 line_list[i][j].DragTo(0, computed_point[j])
        #                 line_list[i][j].DragTo(1, computed_point[j + 1])
        #         self.myContext.UpdateCurrentViewer()

        # start_pnt = gp_Trsf()
        # start_pnt.SetTranslation(points_list[0][0].GetGeometry().Pnt(),points_list[0][0].GetGeometry().Pnt())
        # end_pnt = gp_Trsf()
        # end_pnt.SetTranslation(points_list[0][0].GetGeometry().Pnt(),points_list[0][1].GetGeometry().Pnt())

        # animation_obj = AIS_AnimationObject(TCollection_AsciiString("obj1"), self.myContext, points_list[0][0].GetAIS_Object(), start_pnt,
        #                                     end_pnt)
        # animation_obj.SetOwnDuration(3)
        # animation_obj.SetStartPts(0)
        # animation.Add(animation_obj)
        animation = AIS_Animation(TCollection_AsciiString("obj1"))
        animation.SetOwnDuration(4.0)
        animation.StartTimer(0, 1.0, True)
        duration = animation.Duration()
        while not animation.IsStopped():
            t = animation.ElapsedTime() / duration
            if t > 1.0:
                t = 1.0
            for i in range(len(points_list)):
                if i < len(points_list) - 1:
                    for idx in range(len(points_list[i]) - 1):
                        new_point1 = gp_Pnt2d(self.DeCastlejau(x_poles, idx, i + 1, t),
                                              self.DeCastlejau(y_poles, idx, i + 1, t))
                        new_point2 = gp_Pnt2d(self.DeCastlejau(x_poles, idx + 1, i + 1, t),
                                              self.DeCastlejau(y_poles, idx + 1, i + 1, t))
                        line_list[i][idx].DragTo(0, new_point1)
                        line_list[i][idx].DragTo(1, new_point2)
            currentPnt2d = self.mySObject.GetGeometry2d().Value(t)
            bezier_point.DragTo(currentPnt2d)
            animation.UpdateTimer()
            self.myContext.UpdateCurrentViewer()
            if t >= self.ui.doubleSpinBoxAnimationValue.value():
                break

    def closeEvent(self, QCloseEvent):
        super(Sketch_PropertyBezierCurve, self).closeEvent(QCloseEvent)
        # remove the last animation shape first
        if self.animatedGeometry:
            for _ in self.animatedGeometry:
                _.RemoveDisplay()
