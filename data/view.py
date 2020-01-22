from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import QMenu, QRubberBand
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from OCC.Core.V3d import V3d_View, V3d_Viewer
from OCC.Core.AIS import AIS_InteractiveContext
from OCC.Core.Graphic3d import Graphic3d_GraphicDriver
from enum import Enum


class CurrentAction3d(Enum):
    Nothing = 0
    DynamicZooming = 1
    WindowZooming = 2
    DynamicPanning = 3
    GlobalPanning = 4
    DynamicRotation = 5

def GetGraphicDriver():
    aGraphicDriver=Graphic3d_GraphicDriver()
    return aGraphicDriver
class OccView(QGLWidget):
    selectionChanged = pyqtSignal()

    def __init__(self, parent):
        super(OccView, self).__init__(parent)
        self.myCurrentMode=CurrentAction3d.DynamicRotation
        self.myDegenerateModeIsOn=True
        self.myRectBand=QRubberBand()

        self.myXmin=0
        self.myYmin=0
        self.myXmax=0
        self.myYmax=0

    def pan(self):
        pass

    def fitAll(self):
        pass

    def reset(self):
        pass

    def zoom(self):
        pass

    def rotate(self):
        pass

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        pass
