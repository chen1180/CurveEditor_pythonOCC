from data.sketch.gui.sketch_property import *
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BSplineCurve
from OCC.Core.Geom import Geom_CartesianPoint, Geom_BezierCurve
from OCC.Core.ElCLib import *
from view.basisFunctionPlot import BasisFunctionWindow
from itertools import groupby
class Sketch_PropertyBspline(Sketch_Property):
    def __init__(self, parent, name, fl):
        super(Sketch_PropertyBspline, self).__init__(parent, name, fl)
        if not name:
            self.setObjectName("Property bezier curve")
        self.geometry_dict = {}
        self.knots_distribution_dict = {0: "NonUniform ", 1: "Uniform", 2: "QuasiUniform ", 3: "PiecewiseBezier"}
        self.ui_initialized = False
        self.mySObject: Sketch_Bspline = None
        self.canvas = BasisFunctionWindow()
        self.canvas.PlotUpdated.connect(self.UpdateBasisFunction)

        # ui
        self.ui.TextLabelPoint1.close()
        self.ui.LineEditPoint1.close()

    def SetGeometry(self, *__args):
        self.curGeom2d_Bspline: Geom2d_BSplineCurve = self.mySObject.GetGeometry2d()
        # save data and create gui
        poles = TColgp_Array1OfPnt2d_to_point_list(self.curGeom2d_Bspline.Poles())
        weights = self.mySObject.myWeights
        knots = TColStd_Array1OfNumber_to_list(self.curGeom2d_Bspline.Knots())
        multiplicity = TColStd_Array1OfNumber_to_list(self.curGeom2d_Bspline.Multiplicities())

        nbPoles = self.curGeom2d_Bspline.NbPoles()
        degree = self.curGeom2d_Bspline.Degree()
        closed_flag = self.curGeom2d_Bspline.IsClosed()
        periodic_flag = self.curGeom2d_Bspline.IsPeriodic()
        rational_flag = self.curGeom2d_Bspline.IsRational()
        knots_distribution = self.knots_distribution_dict[self.curGeom2d_Bspline.KnotDistribution()]
        continuity = self.curGeom2d_Bspline.Continuity()
        knots_sequence = TColStd_Array1OfNumber_to_list(self.curGeom2d_Bspline.KnotSequence())
        self.geometry_dict = {"poles": poles,
                              "weights": weights,
                              "knots": knots,
                              "multiplicity": multiplicity,
                              "knots_sequence": knots_sequence,
                              "knots_distribution": knots_distribution,
                              "periodic": periodic_flag,
                              "degree": degree,
                              "closed": closed_flag,
                              "rational": rational_flag,
                              "continuity": continuity,
                              "nbPoles": nbPoles}
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
            if weight_value != self.geometry_dict["weights"][idx]:
                needUpdate = True
                self.mySObject.ChangeWeights(index=idx, weight=weight_value)
        for idx in range(self.multiplicity.childCount()):
            multiplicity = self.multiplicity.child(idx)
            multi_splinbox: QSpinBox = self.tree.itemWidget(multiplicity, 1)
            multi_value = multi_splinbox.value()
            if multi_value != self.geometry_dict["multiplicity"][idx]:
                needUpdate = True
                self.mySObject.ChangeMulties(idx, multi_value)
                self.mySObject.IncreaseMultiplicity(idx, multi_value)
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
        self.button_degreeElevation = QPushButton()
        self.button_degreeElevation.setText("Increase degree")
        self.button_degreeElevation.clicked.connect(self.degreeElevation)
        self.tree.setItemWidget(self.degree, 2, self.button_degreeElevation)

        self.periodic = QTreeWidgetItem(self.tree, ["Is periodic", str(self.geometry_dict["periodic"])])
        self.button_setPeriodic = QPushButton()
        self.button_setPeriodic.setText("Set Periodic")
        self.button_setPeriodic.clicked.connect(self.setPeriodic)
        self.tree.setItemWidget(self.periodic, 2, self.button_setPeriodic)

        self.closed = QTreeWidgetItem(self.tree, ["Is closed", str(self.geometry_dict["closed"])])
        self.rational = QTreeWidgetItem(self.tree, ["Is rational", str(self.geometry_dict["rational"])])
        self.continuity = QTreeWidgetItem(self.tree, ["Continuity", str(self.geometry_dict["continuity"])])
        self.knots_distribution = QTreeWidgetItem(self.tree,
                                                  ["Knots distribution", str(self.geometry_dict["knots_distribution"])])
        self.comboBox_knots_distribution = QComboBox()
        self.comboBox_knots_distribution.addItems(["NonUniform", "Uniform", "QuasiUniform ", "PiecewiseBezier"])
        self.comboBox_knots_distribution.setCurrentText(self.geometry_dict["knots_distribution"])
        self.comboBox_knots_distribution.currentIndexChanged.connect(self.changeKnotsType)
        self.tree.setItemWidget(self.knots_distribution, 2, self.comboBox_knots_distribution)

        self.knots_sequence = QTreeWidgetItem(self.tree, ["Knots sequence", str(self.geometry_dict["knots_sequence"])])
        self.button_plotKnots = QPushButton()
        self.button_plotKnots.setText("Plot")
        self.button_plotKnots.clicked.connect(self.plotBasisFunction)
        self.tree.setItemWidget(self.knots_sequence, 2, self.button_plotKnots)

        self.poles = QTreeWidgetItem(self.tree, ["poles", str(self.geometry_dict["nbPoles"])])
        # self.poles.setData(0, Qt.UserRole, self.geometry_dict["poles"])
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

        knots = self.geometry_dict["knots"]
        self.knots = QTreeWidgetItem(self.tree, ["knots", str(knots)])
        for idx, value in enumerate(knots):
            knots_children = QTreeWidgetItem(self.knots)
            knots_children.setText(0, str(idx))
            widget = QDoubleSpinBox()
            widget.setSingleStep(0.1)
            widget.setValue(value)
            self.tree.setItemWidget(knots_children, 1, widget)
        multiplicity = self.geometry_dict["multiplicity"]
        self.multiplicity = QTreeWidgetItem(self.tree, ["multiplicity", str(multiplicity)])
        for idx, value in enumerate(multiplicity):
            multiplicity_children = QTreeWidgetItem(self.multiplicity)
            multiplicity_children.setText(0, str(idx))
            widget = QSpinBox()
            widget.setRange(1, self.geometry_dict["degree"] + 1)
            widget.setValue(value)
            self.tree.setItemWidget(multiplicity_children, 1, widget)
        # for i in range(3):
        #     self.tree.resizeColumnToContents(i)
        # self.ui.GroupBoxGPLayout.addWidget(self.canvas)

    def degreeElevation(self):
        self.mySObject.IncreaseDegree(self.geometry_dict["degree"] + 1)
        self.SetGeometry()
        self.updateUI()

    def changeKnotsType(self, currentIndex):
        self.knots_distribution.setText(1, self.knots_distribution_dict[currentIndex])
        self.mySObject.SetKnotsType(currentIndex)
        self.SetGeometry()
        self.updateUI()

    def setPeriodic(self):
        self.mySObject.SetPeriodic()
        self.SetGeometry()
        self.updateUI()
    def plotBasisFunction(self):
        self.canvas.setBasisFunction(self.geometry_dict["knots_sequence"],self.geometry_dict["degree"])
        self.canvas.show()

    def updateUI(self):
        degree = self.curGeom2d_Bspline.Degree()
        closed_flag = self.curGeom2d_Bspline.IsClosed()
        periodic_flag = self.curGeom2d_Bspline.IsPeriodic()
        rational_flag = self.curGeom2d_Bspline.IsRational()
        knots_distribution = self.knots_distribution_dict[self.curGeom2d_Bspline.KnotDistribution()]
        continuity = self.curGeom2d_Bspline.Continuity()
        knots_sequence = TColStd_Array1OfNumber_to_list(self.curGeom2d_Bspline.KnotSequence())

        self.degree.setText(1, str(degree))
        self.closed.setText(1, str(closed_flag))
        self.periodic.setText(1, str(periodic_flag))
        self.rational.setText(1, str(rational_flag))
        self.knots_distribution.setText(1, knots_distribution)
        self.continuity.setText(1, str(continuity))
        self.knots_sequence.setText(1, str(knots_sequence))
    def UpdateBasisFunction(self,knots,degree):
        knots_no_duplicates=sorted(list(set(knots)))
        multiplicities=[knots.count(x) for x in knots_no_duplicates]
        self.mySObject.SetKnots(knots_no_duplicates)
        self.mySObject.SetMultiplicities(multiplicities)
        self.mySObject.SetDegree(degree)
        self.mySObject.Compute()