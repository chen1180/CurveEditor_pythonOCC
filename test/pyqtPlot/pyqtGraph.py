import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph.dockarea import *

# I use Qt Designer, below I just cut generated code to minimum
class Ui_StartForm(object):
    def setupUi(self, StartForm):
        StartForm.setObjectName("StartForm")
        StartForm.resize(1507, 968)
        self.GraphLayout = QtWidgets.QGridLayout(StartForm)


class MyPlotWidget(pg.PlotWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.scene() is a pyqtgraph.GraphicsScene.GraphicsScene.GraphicsScene
        self.scene().sigMouseClicked.connect(self.mouse_clicked)


    def mouse_clicked(self, mouseClickEvent):
        # mouseClickEvent is a pyqtgraph.GraphicsScene.mouseEvents.MouseClickEvent
        print('clicked plot 0x{:x}, event: {}'.format(id(self), mouseClickEvent))



# my application
class AppWindow(QtWidgets.QWidget, Ui_StartForm):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.setupUi(self)

        self.dock_area_main = DockArea()
        self.GraphLayout.addWidget(self.dock_area_main)

        # Best to use lower case for variables and upper case for types, so I
        # renamed self.Dock1 to self.dock1.

        self.dock1 = Dock("Dock 1", size=(1, 1))
        self.dock_area_main.addDock(self.dock1, 'left')

        self.dock2 = Dock("Dock 2", size=(1, 1))
        self.dock_area_main.addDock(self.dock2, 'right')

        self.GraphViewList = []

        self.pl1 = MyPlotWidget()
        self.pl2 = MyPlotWidget()

        self.dock1.addWidget(self.pl1)
        self.dock2.addWidget(self.pl2)



app = QtWidgets.QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())