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
        def setView(a0):
            if a0 == True:
                self._display.SetPerspectiveProjection()
            else:
                self._display.SetOrthographicProjection()
            self._display.Repaint()

        self._action_transform = QAction(QIcon(""), "Transform", self,
                                         statusTip="Transform a object",
                                         triggered=self._display.View.SetFront)
        self.actions.append(self._action_transform)
        self._action_fitAll = QAction(QIcon(""), "Fit all shape on screen", self,
                                      statusTip="Fit all shapes on screen",
                                      triggered=self._display.FitAll)
        self.actions.append(self._action_fitAll)
        self._action_setView = QAction(QIcon(""), "Projective/Orthor", self,
                                       statusTip="set view type",
                                       triggered=setView)
        self._action_setView.setCheckable(True)
        self.actions.append(self._action_setView)
        self._action_viewIso = QAction(QIcon(), "View ISO", self,
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
