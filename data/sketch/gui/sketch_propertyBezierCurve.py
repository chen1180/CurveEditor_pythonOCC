from data.sketch.gui.sketch_property import *
from OCC.Core.Geom2d import Geom2d_CartesianPoint, Geom2d_BezierCurve
from OCC.Core.Geom import Geom_CartesianPoint, Geom_BezierCurve
from OCC.Core.ElCLib import *


class Sketch_PropertyBezierCurve(Sketch_Property):
    def __init__(self, parent, name, fl):
        super(Sketch_PropertyBezierCurve, self).__init__(parent, name, fl)
        if not name:
            self.setObjectName("Property bezier curve")
        self.geometry_dict = {}
        self.ui_initialized = False
        self.mySObject: Sketch_BezierCurve = None
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
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Key', 'Value'])
        self.ui.GroupBoxGPLayout.addWidget(self.tree, 1, 0, 1, 3)
        self.degree = QTreeWidgetItem(self.tree, ["degree", str(self.geometry_dict["degree"])])
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

    def updateUI(self):
        degree = self.curGeom2d_BezierCurve.Degree()
        closed_flag = self.curGeom2d_BezierCurve.IsClosed()
        rational_flag = self.curGeom2d_BezierCurve.IsRational()
        continuity = self.curGeom2d_BezierCurve.Continuity()
        self.degree.setText(1, str(degree))
        self.closed.setText(1, str(closed_flag))
        self.rational.setText(1, str(rational_flag))
        self.continuity.setText(1, str(continuity))
