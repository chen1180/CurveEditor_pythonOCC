from PyQt5.QtWidgets import QMainWindow, QDockWidget,QWidget
from PyQt5.QtCore import Qt
from data.design.gui.bezierSurfaceForm import BezierSurfaceForm
from data.design.part_type import *


class Part_QTGUI(object):
    def __init__(self, parent: QMainWindow):
        self.dockWidget = QDockWidget("Tool", parent)
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        parent.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.form_createBezierSurface = BezierSurfaceForm()
        self.dockWidget.hide()

    def SetGui(self, theActionType: Part_ObjectTypeOfMethod):
        if theActionType==Part_ObjectTypeOfMethod.BezierSurface_Method:
            self.dockWidget.setWidget(self.form_createBezierSurface)
        elif theActionType==Part_ObjectTypeOfMethod.Nothing_Method:
            self.dockWidget.hide()
        self.dockWidget.show()
    def Hide(self):
        self.dockWidget.hide()