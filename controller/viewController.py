from PyQt5.QtCore import QObject, pyqtSignal, QModelIndex
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QAction, QStatusBar



class ViewController(QObject):

    def __init__(self, display, parent=None):
        super(ViewController, self).__init__(parent)
        self._display = display
        self.actions = []
        self.createActions()

    def createActions(self):

        self._action_transform = QAction(QIcon(":/move.png"), "Transform", self,
                                         statusTip="Transform a object",
                                         triggered=self._display.View.SetFront)
        self.actions.append(self._action_transform)
        self._action_fitAll = QAction(QIcon(":/fitContent.png"), "Fit all", self,
                                      statusTip="Fit all shapes on screen",
                                      triggered=self._display.FitAll)
        self.actions.append(self._action_fitAll)
        def setView(a0):
            if a0 == True:
                self._display.SetPerspectiveProjection()
                self._action_setView.setText("Perspective")
            else:
                self._display.SetOrthographicProjection()
                self._action_setView.setText("Ortho")
            self._display.Repaint()
        icon = QIcon()
        icon.addPixmap(QPixmap(":/orthorgraphic.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/perspective.png"), QIcon.Normal, QIcon.On)
        self._action_setView = QAction(icon, "Ortho", self,
                                       statusTip="set view type",
                                       triggered=setView)
        self._action_setView.setCheckable(True)
        self.actions.append(self._action_setView)
        self._action_viewIso = QAction(QIcon(":/viewIso.png"), "View ISO", self,
                                       statusTip="Change view point",
                                       triggered=self._display.View_Iso)
        self.actions.append(self._action_viewIso)
        def switchDisplayMode(state):
            if state:
                self._display.SetModeWireFrame()
                self._action_switchDisplayMode.setText("Wireframe")
            else:
                self._display.SetModeShaded()
                self._action_switchDisplayMode.setText("Shading")
        icon=QIcon()
        icon.addPixmap(QPixmap(":/shading.png"),QIcon.Normal,QIcon.Off)
        icon.addPixmap(QPixmap(":/wireframe.png"),QIcon.Normal,QIcon.On)
        self._action_switchDisplayMode = QAction(icon, "Shading", self,
                                                 statusTip="Wireframe mode",
                                                 triggered=switchDisplayMode, checkable=True)
        self.actions.append(self._action_switchDisplayMode)
