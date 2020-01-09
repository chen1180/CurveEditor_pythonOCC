from view import mainWindow, customToolButton
from controller import editorController, openglWindowController, toolController
import resources.icon.icon
from PyQt5 import QtWidgets, QtCore, QtGui
from data.node import *
from data.model import *

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self._ui = mainWindow.Ui_MainWindow()
        self._ui.setupUi(self)
        # opengl window
        self._glWindow = openglWindowController.OpenGLEditor(self)
        self.setCentralWidget(self._glWindow)
        # setup tool bar
        self.createDrawActions()
        self.createViewActions()
        self.createModeActions()
        self.createPartActions()
        self.createToolBars()

        # setup data
        self._rootNode = Node("Scene")
        self._sketch = SketchNode("Sketch", self._rootNode)
        self._node = TransformNode("Transform", self._sketch)
        self._light = LightNode("Light", self._sketch)
        self._model = ModelNode("Model", self._sketch)
        self._model2 = ModelNode("Model2", self._model)
        # setup design
        self._model = SceneGraphModel(self._rootNode)
        self._glWindow.setScene(self._model)

        # """VIEW <------> PROXY MODEL <------> DATA MODEL"""
        self._proxyModel = QtCore.QSortFilterProxyModel()
        self._proxyModel.setSourceModel(self._model)

        self._proxyModel.setDynamicSortFilter(True)
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self._proxyModel.setSortRole(SceneGraphModel.sortRole)
        self._proxyModel.setFilterRole(SceneGraphModel.filterRole)

        # setup sceneGraph editor
        self._uiTreeView = QtWidgets.QTreeView()
        self._uiTreeView.setModel(self._proxyModel)
        self._uiTreeView.setSortingEnabled(True)

        # create sceneGraph dock widget
        self._sceneGraphDock = QtWidgets.QDockWidget("Scene", self)
        self._sceneGraphDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self._sceneGraphDock.setWidget(self._uiTreeView)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._sceneGraphDock)

        # setup property editor
        self._propEditor = editorController.PropertyEditor(self)
        self._propEditor.setModel(self._proxyModel)

        # create property dock widget
        self._propertyDock = QtWidgets.QDockWidget("Scene", self)
        self._propertyDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self._propertyDock.setWidget(self._propEditor)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._propertyDock)

        # create tool dock widget
        # self._toolBarDock = QtWidgets.QDockWidget("Tool", self)
        # self._toolBarDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        # set two vertical toolbar in the tool widget
        self._toolBarLayout = QtWidgets.QVBoxLayout()

        self._toolBarLayout.setMenuBar(self._curveToolBar)
        # self._toolBarLayout.setMenuBar(self._surfaceToolBar)

        self._toolBarContainer = QtWidgets.QWidget()
        self._toolBarContainer.setLayout(self._toolBarLayout)

        # self._toolBarDock.setWidget(self._toolBarContainer)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._toolBarDock)

        # sceneGraph and property synchronization
        self._uiTreeView.selectionModel().currentChanged.connect(self._propEditor.setSelection)
        self._glWindow.modelUpdated.connect(self.updateModel)

    def updateModel(self, item):
        '''

        Args:
            item: Mesh node (usually represent shape node)

        Returns:

        '''
        self._model.insertNode(item, 0, 1)

    def createToolBars(self):
        # Curve tool bar
        self._curveToolBar = QtWidgets.QToolBar("Curve")
        self._curveToolBar.setOrientation(QtCore.Qt.Vertical)
        # self._curveToolBar.addAction(self._action_sketchMode_addBezierCurve)
        # self._curveToolBar.addAction(self._action_sketchMode_addBSpline)
        # self._curveToolBar.addAction(self._action_sketchMode_addNurbs)
        # Surface tool bar
        self._surfaceToolBar = QtWidgets.QToolBar("Surface")
        self._surfaceToolBar.setOrientation(QtCore.Qt.Vertical)
        # View tool bar
        self._viewToolBar = QtWidgets.QToolBar("View")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self._viewToolBar)
        self._viewToolBar.setOrientation(QtCore.Qt.Horizontal)
        self._viewToolBar.addAction(self._action_transform)
        self._viewToolBar.addAction(self._action_fitAll)
        self._viewToolBar.addAction(self._action_setView)
        self._viewToolBar.addAction(self._action_viewTop)
        self._viewToolBar.addAction(self._action_viewBot)
        self._viewToolBar.addAction(self._action_viewFront)
        self._viewToolBar.addAction(self._action_viewRear)
        self._viewToolBar.addAction(self._action_viewLeft)
        self._viewToolBar.addAction(self._action_viewRight)
        self._viewToolBar.addAction(self._action_viewIso)
        self._viewToolBar.addSeparator()
        self._swithModeButton = customToolButton.CustomToolButton()
        self._switchModeMenu = QtWidgets.QMenu()
        self._switchModeMenu.addAction(self._action_switchViewMode)
        self._switchModeMenu.addAction(self._action_switchDesignMode)
        self._switchModeMenu.addAction(self._action_switchSketchMode)
        self._swithModeButton.setMenu(self._switchModeMenu)
        self._swithModeButton.setDefaultAction(self._action_switchViewMode)
        self._viewToolBar.addWidget(self._swithModeButton)
        # Toolbar for different modes
        self.createSketchToolBar()

    def createSketchToolBar(self):
        self._sketchToolBar = QtWidgets.QToolBar("Sketch")
        self._sketchToolBar.addAction(self._action_sketchMode_createNewSketch)
        self._sketchToolBar.addAction(self._action_sketchMode_addPoint)
        self._sketchToolBar.addAction(self._action_sketchMode_addLine)
        self._sketchToolBar.addAction(self._action_sketchMode_addBezierCurve)
        self._sketchToolBar.addAction(self._action_sketchMode_addBSpline)
        self._sketchToolBar.addAction(self._action_sketchMode_pointsToBSpline)
        self._sketchToolBar.addAction(self._action_sketchMode_addArc)
        self._sketchToolBar.addAction(self._action_sketchMode_addCircle)
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self._sketchToolBar)

        self._viewToolBar = QtWidgets.QToolBar("View")
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self._viewToolBar)
        self._designToolBar = QtWidgets.QToolBar("Design")
        self.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        self._designToolBar.addAction(self._action_partMode_addBezierSurface)
        self._designToolBar.addAction(self._action_partMode_revolutedSurface)
        self._designToolBar.addAction(self._action_partMode_extrudedSurface)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self._designToolBar)
        self._sketchToolBar.setVisible(False)
        self._designToolBar.setVisible(False)

    def createViewActions(self):
        def setView(a0):
            if a0 == True:
                self._glWindow._display.SetPerspectiveProjection()
            else:
                self._glWindow._display.SetOrthographicProjection()
            self._glWindow._display.Repaint()

        self._action_transform = QtWidgets.QAction(QtGui.QIcon(""), "Transform", self,
                                                   statusTip="Transform a object",
                                                   triggered=self._glWindow.viewManager.setActive)
        self._action_fitAll = QtWidgets.QAction(QtGui.QIcon(""), "Fit all shape on screen", self,
                                                statusTip="Fit all shapes on screen",
                                                triggered=self._glWindow._display.FitAll)

        self._action_setView = QtWidgets.QAction(QtGui.QIcon(""), "Projective/Orthor", self,
                                                 statusTip="set view type",
                                                 triggered=setView)
        self._action_setView.setCheckable(True)
        self._action_viewTop = QtWidgets.QAction(QtGui.QIcon(""), "View Top", self,
                                                 statusTip="Change view point",
                                                 triggered=self._glWindow._display.View_Top)
        self._action_viewBot = QtWidgets.QAction(QtGui.QIcon(""), "View Bottom", self,
                                                 statusTip="Change view point",
                                                 triggered=self._glWindow._display.View_Bottom)
        self._action_viewFront = QtWidgets.QAction(QtGui.QIcon(""), "View Front", self,
                                                   statusTip="Change view point",
                                                   triggered=self._glWindow._display.View_Front)
        self._action_viewRear = QtWidgets.QAction(QtGui.QIcon(), "View Rear", self,
                                                  statusTip="Change view point",
                                                  triggered=self._glWindow._display.View_Rear)
        self._action_viewLeft = QtWidgets.QAction(QtGui.QIcon(), "View Left", self,
                                                  statusTip="Change view point",
                                                  triggered=self._glWindow._display.View_Left)
        self._action_viewRight = QtWidgets.QAction(QtGui.QIcon(), "View Right", self,
                                                   statusTip="Change view point",
                                                   triggered=self._glWindow._display.View_Right)
        self._action_viewIso = QtWidgets.QAction(QtGui.QIcon(), "View ISO", self,
                                                 statusTip="Change view point",
                                                 triggered=self._glWindow._display.View_Iso)

    def createDrawActions(self):
        # self.deleteItem_action = QtWidgets.QAction(QtGui.QIcon(":images/delete.png"), "Delete a selection", self,
        #                               statusTip="Delete an item",
        #                               triggered=self.deleteItem)
        self._action_sketchMode_createNewSketch = QtWidgets.QAction(QtGui.QIcon(""), "create a new sketch", self,
                                                                    statusTip="create a new sketch",
                                                                    triggered=self._glWindow.createNewSketch)
        self._action_sketchMode_addPoint = QtWidgets.QAction(QtGui.QIcon(""), "add points", self,
                                                             statusTip="add points on sketch",
                                                             triggered=self._glWindow.sketchPoint)
        self._action_sketchMode_addLine = QtWidgets.QAction(QtGui.QIcon(""), "add lines", self,
                                                            statusTip="add a line",
                                                            triggered=self._glWindow.sketchLine)
        self._action_sketchMode_addBezierCurve = QtWidgets.QAction(QtGui.QIcon(""), "Add Bezier Curve", self,
                                                                   statusTip="Add a cubic Bezier curve",
                                                                   triggered=self._glWindow.sketchBezier)
        self._action_sketchMode_addBSpline = QtWidgets.QAction(QtGui.QIcon(""), "Add BSpline Curve", self,
                                                               statusTip="Add a B Spline curve",
                                                               triggered=self._glWindow.sketchBSpline)
        self._action_sketchMode_pointsToBSpline = QtWidgets.QAction(QtGui.QIcon(""), "Interpolate BSpline", self,
                                                                    statusTip="Interpolate points with BSpline",
                                                                    triggered=self._glWindow.sketchPointsToBSpline)
        self._action_sketchMode_addArc = QtWidgets.QAction(QtGui.QIcon(""), "Add Arc", self,
                                                           statusTip="Add an arc",
                                                           triggered=self._glWindow.sketchArc3P)
        self._action_sketchMode_addCircle = QtWidgets.QAction(QtGui.QIcon(""), "Add Circle", self,
                                                              statusTip="Add a circle",
                                                              triggered=self._glWindow.sketchCircleCenterRadius)

        # self.addBezierPatch = QtWidgets.QAction(QtGui.QIcon(":images/bezier_patch.png"),"Add Bezier patch", self,
        #                               statusTip="Add a cubic Bezier patch",
        #                               triggered=self.drawBezierPatch)
        # self.addNurbsPatch = QtWidgets.QAction(QtGui.QIcon(":images/nurbs_patch.png"), "Add a NURB patch", self,
        #                         statusTip="Add a Nurb patch",
        #                         triggered=self.drawNurbsPatch)

    def createPartActions(self):
        self._action_partMode_addBezierSurface = QtWidgets.QAction(QtGui.QIcon(""), "Construct a Bezier Surface",
                                                                   self,
                                                                   statusTip="Create from two Bezier curve",
                                                                   triggered=self._glWindow.sketchCircleCenterRadius)
        self._action_partMode_revolutedSurface = QtWidgets.QAction(QtGui.QIcon(""), "revolve a shape", self,
                                                                   statusTip="Create surface of revolution based on a selected shape",
                                                                   triggered=self._glWindow.partRevolveSurface)
        self._action_partMode_extrudedSurface = QtWidgets.QAction(QtGui.QIcon(""), "extrude a shape", self,
                                                                  statusTip="Create extruded surface based on a selected shape",
                                                                  triggered=self._glWindow.partExtrudedSurface)

    def createModeActions(self):
        self._action_switchViewMode = QtWidgets.QAction(QtGui.QIcon(""), "View", self,
                                                        statusTip="The tools set will change to view mode",
                                                        triggered=lambda state,
                                                                         x=self._glWindow.MODE_VIEW: self.setState(x))
        self._action_switchSketchMode = QtWidgets.QAction(QtGui.QIcon(""), "Sketch", self,
                                                          statusTip="The tools set will change to sketch mode",
                                                          triggered=lambda
                                                              state, x=self._glWindow.MODE_SKETCH: self.setState(x))
        self._action_switchDesignMode = QtWidgets.QAction(QtGui.QIcon(""), "Design", self,
                                                          statusTip="The tools set will change to design mode",
                                                          triggered=lambda
                                                              state, x=self._glWindow.MODE_DESIGN: self.setState(x))

    def setState(self, gl_state):
        self._glWindow.setState(gl_state)
        if gl_state == self._glWindow.MODE_DESIGN:
            self._designToolBar.setVisible(True)
            self._sketchToolBar.setVisible(False)
            self._viewToolBar.setVisible(False)
        elif gl_state == self._glWindow.MODE_SKETCH:
            self._designToolBar.setVisible(False)
            self._sketchToolBar.setVisible(True)
            self._viewToolBar.setVisible(False)
        elif gl_state == self._glWindow.MODE_VIEW:
            self._designToolBar.setVisible(False)
            self._sketchToolBar.setVisible(False)
            self._viewToolBar.setVisible(True)
