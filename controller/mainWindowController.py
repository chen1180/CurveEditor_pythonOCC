from view import mainWindow
from controller import editorController,openglWindowController,toolController
from data.model import *
from data.node import *
from data.primitives import *
from PyQt5.QtCore import *
import resources.icon.icon
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self._ui = mainWindow.Ui_MainWindow()
        self._ui.setupUi(self)
        # opengl window
        self._glWindow = openglWindowController.OpenGLEditor()
        self.setCentralWidget(self._glWindow)
        # setup tool bar
        self.createDrawActions()
        self.createToolBars()
        # setup data
        self._rootNode = Node("Scene")
        # setup model
        self._model = SceneGraphModel(self._rootNode)

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
        self._toolBarDock = QtWidgets.QDockWidget("Tool", self)
        self._toolBarDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        # set two vertical toolbar in the tool widget
        self._toolBarLayout = QtWidgets.QHBoxLayout()
        self._toolBarContainer = QtWidgets.QWidget()
        self._toolBarLayout.addWidget(self._curveToolBar)
        self._toolBarLayout.addWidget(self._surfaceToolBar)

        self._toolBarContainer.setLayout(self._toolBarLayout)
        self._toolBarDock.setWidget(self._toolBarContainer)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._toolBarDock)

        # sceneGraph and property synchronization
        self._uiTreeView.selectionModel().currentChanged.connect(self._propEditor.setSelection)

    def updateModel(self,item):
        '''

        Args:
            item: Mesh node (usually represent shape node)

        Returns:

        '''
        self._model.insertMeshNode(item,0,1)

    def createToolBars(self):
        # Curve tool bar
        self._curveToolBar = QtWidgets.QToolBar("Curve")
        self._curveToolBar.setOrientation(QtCore.Qt.Vertical)
        self._curveToolBar.addAction(self.addBezierCurve)
        self._curveToolBar.addAction(self.addBSplineCurve)
        self._curveToolBar.addAction(self.addNurbs)
        # Surface tool bar
        self._surfaceToolBar = QtWidgets.QToolBar("Surface")
        self._surfaceToolBar.setOrientation(QtCore.Qt.Vertical)
    def createDrawActions(self):
        # self.deleteItem_action = QtWidgets.QAction(QtGui.QIcon(":images/delete.png"), "Delete a selection", self,
        #                               statusTip="Delete an item",
        #                               triggered=self.deleteItem)
        self.addBezierCurve = QtWidgets.QAction(QtGui.QIcon(":bezier.png"),"Add Bezier Curve", self,
                                      statusTip="Add a cubic Bezier curve",
                                      triggered=self._glWindow.shape_drawer.drawBezierCurve)
        self.addBSplineCurve = QtWidgets.QAction(QtGui.QIcon(":spline.png"),"Add B Spline Curve", self,
                                       statusTip="Add a B Spline curve",
                                       triggered=self._glWindow.shape_drawer.drawBSpline)
        self.addNurbs = QtWidgets.QAction(QtGui.QIcon(":nurbs.png"),"Add a NURB", self,
                                       statusTip="Add a Nurb curve",
                                       triggered=self._glWindow.shape_drawer.drawNurbs)

        # self.addBezierPatch = QtWidgets.QAction(QtGui.QIcon(":images/bezier_patch.png"),"Add Bezier patch", self,
        #                               statusTip="Add a cubic Bezier patch",
        #                               triggered=self.drawBezierPatch)
        # self.addNurbsPatch = QtWidgets.QAction(QtGui.QIcon(":images/nurbs_patch.png"), "Add a NURB patch", self,
        #                         statusTip="Add a Nurb patch",
        #                         triggered=self.drawNurbsPatch)
# Qt error message traceback
sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook
# Install qt debug message handler
def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
        mode = 'INFO'
    elif mode == QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (
          context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))
if __name__ == '__main__':
    qInstallMessageHandler(qt_message_handler)
    app = QtWidgets.QApplication([])
    mainWin = Window()
    mainWin.showMaximized()
    sys.exit(app.exec_())
