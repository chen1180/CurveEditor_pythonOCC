from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OCC.Extend.DataExchange import read_stl_file, read_step_file, read_iges_file, write_stl_file, \
    read_step_file_with_names_colors
from OCC.Core.TopoDS import *
from data.design.part_utilities import *
from data.design.geometry import *
from data.node import *
import os
import pickle


class MenuBarController(QObject):

    def __init__(self, parent=None):
        super(MenuBarController, self).__init__(parent)
        self.parent = parent
        self.glWindow = self.parent._glWindow
        self._display = parent._glWindow._display
        self.menuBar: QMenuBar = self.parent._ui.menuBar
        self.actions = []
        self.createMenuBars()

    def createMenuBars(self):
        menu = self.menuBar.addMenu("&File")
        menu.addAction(QAction(QIcon(""), "Load", self,
                               statusTip="Load existing file",
                               triggered=self.load))
        menu.addAction(QAction(QIcon(""), "Save as", self,
                               statusTip="Save this scene into computer",
                               triggered=self.saveAs))
        menu.addAction(QAction(QIcon(""), "Import", self,
                               statusTip="Import *step *stl *iges file",
                               triggered=self.importFile))
        menu.addAction(QAction(QIcon(""), "Quit", self, statusTip="Quit application",
                               triggered=self.quit))
        menu.addAction(QAction(QIcon(":/newPlane.png"), "ScreenShot", self,
                               statusTip="Export current view as picture",
                               triggered=self.export_to_PNG))

    def load(self):
        dlg = QFileDialog()
        fileFilter = ["Supported format(*.cred)"]
        dlg.setNameFilters(fileFilter)
        dlg.selectNameFilter(fileFilter[0])
        if dlg.exec_():
            path = dlg.selectedFiles()[0]
            with open(path, 'rb') as infile:
                objects = pickle.load(infile, encoding='bytes')
            # reset root node to the saved scene
            if self.parent._model._rootNode.childCount() > 0:
                self.parent._uiTreeView.deleteAllTreeItem()
            self.parent._model._rootNode = objects
            self.parent.sketchController.setRootNode(objects)
            self.parent.partController.setRootNode(objects)
            self.parent._model.layoutChanged.emit()
            # update sketch object from the loading node
            for object in objects.children():
                if isinstance(object, SketchObjectNode):
                    surface_geometry = shape_to_geometry(object.shapeObject)
                    if object.typeInfo() == NodeType.BezierSurfaceNode:
                        sketch = Surface_Bezier(self._display.Context)
                    elif object.typeInfo() == NodeType.BsplineSurfaceNode:
                        sketch = Surface_Bspline(self._display.Context)
                    elif object.typeInfo() == NodeType.ExtrudedSurfaceNode:
                        sketch = Surface_LinearExtrusion(self._display.Context)
                    elif object.typeInfo() == NodeType.RevolvedSurfaceNode:
                        sketch = Surface_Revolved(self._display.Context)
                    elif object.typeInfo() == NodeType.SweepSurfaceNode:
                        sketch = Surface_Sweep(self._display.Context)
                    elif object.typeInfo() == NodeType.ImportedSurfaceNode:
                        sketch = Surface_ImportedShape(object.name(),self._display.Context)
                    sketch.FromShape(surface_geometry, object.shapeObject)
                    object.setSketchObject(sketch)
                elif isinstance(object, SketchNode):
                    plane = shape_to_geometry(object.shapeObject)
                    sketch = Sketch_Plane(self._display, plane.Position())
                    sketch.Compute()
                    object.setSketchPlane(sketch)
                    for child in object.children():
                        sketch_geometry = shape_to_geometry(child.shapeObject)
                        if child.typeInfo() == NodeType.PointNode:
                            sketch = Sketch_Point(self._display.Context, plane.Position())
                        elif child.typeInfo() == NodeType.LineNode:
                            sketch = Sketch_Line(self._display.Context, plane.Position())
                        elif child.typeInfo() == NodeType.BsplineNode:
                            sketch = Sketch_Bspline(self._display.Context, plane.Position())
                        elif child.typeInfo() == NodeType.BezierNode:
                            sketch = Sketch_BezierCurve(self._display.Context, plane.Position())
                        sketch.FromShape(sketch_geometry, child.shapeObject)
                        child.setSketchObject(sketch)

    def saveAs(self):
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        path = dlg.getSaveFileName(self.parent, "Save a file", "", "Supported format(*.cred)")
        # Swig object can't be pickled. So create a copy of tree with no swig variable
        with open(path[0], "wb") as f:
            object = []
            root = Node(self.parent._model._rootNode.name(), None)
            for child in self.parent._model._rootNode.children():
                if isinstance(child, SketchObjectNode):
                    if child.typeInfo() == NodeType.BezierSurfaceNode:
                        node = BezierSurfaceNode(child.name(), root)
                    elif child.typeInfo() == NodeType.BsplineSurfaceNode:
                        node = BsplineSurfaceNode(child.name(), root)
                    elif child.typeInfo() == NodeType.ExtrudedSurfaceNode:
                        node = ExtrudedSurfaceNode(child.name(), root)
                    elif child.typeInfo() == NodeType.RevolvedSurfaceNode:
                        node = RevolvedSurfaceNode(child.name(), root)
                    elif child.typeInfo() == NodeType.SweepSurfaceNode:
                        node = SweepSurfaceNode(child.name(), root)
                    elif child.typeInfo() == NodeType.ImportedSurfaceNode:
                        node = ImportedSurfaceNode(child.name(), root)
                    node.shapeObject = child.getSketchObject().GetAIS_Object().Shape()
                    object.append(child.getSketchObject().GetAIS_Object().Shape())
                elif isinstance(child, SketchNode):
                    curNode = SketchNode(child.name(), root)
                    curNode.shapeObject = child.getSketchPlane().GetShape()
                    for subChild in child.children():
                        if subChild.typeInfo() == NodeType.PointNode:
                            node = PointNode(subChild.name(), curNode)
                        elif subChild.typeInfo() == NodeType.LineNode:
                            node = LineNode(subChild.name(), curNode)
                        elif subChild.typeInfo() == NodeType.BsplineNode:
                            node = BsplineNode(subChild.name(), curNode)
                        elif subChild.typeInfo() == NodeType.BezierNode:
                            node = BezierNode(subChild.name(), curNode)
                        node.shapeObject = subChild.getSketchObject().GetAIS_Object().Shape()
                        object.append(subChild.getSketchObject().GetAIS_Object().Shape())
            pickle.dump(root, f)

    def importFile(self):
        dlg = QFileDialog()
        fileFilter = ["Supported format(*.iges *.igs *.stl *.step)", "IGES format(*.iges *.igs)", "STL mesh (*.stl)",
                      "STEP (*.step)"]
        dlg.setNameFilters(fileFilter)
        dlg.selectNameFilter(fileFilter[0])
        if dlg.exec_():
            path = dlg.selectedFiles()[0]
            fileName = os.path.basename(path)
            baseName, postfix = fileName.split(".")
            if postfix == "iges" or postfix == "igs":
                shape = self.import_to_IGES(path)
            elif postfix == "stl":
                shape = self.import_to_STL(path)
            elif postfix == "step":
                shape = self.import_to_STEP(path)
            else:
                raise TypeError("Such type of a file can't be imported.")
            if shape:
                imported_surface = Surface_ImportedShape(baseName, self._display.Context)
                imported_surface.SetGeometry(shape)
                imported_surface.Compute()
                importedNode = ImportedSurfaceNode(imported_surface.GetName(), self.parent._model._rootNode)
                importedNode.setSketchObject(imported_surface)
                self.parent._model.layoutChanged.emit()

    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            return filenames[0]

    def import_to_STL(self, fileName):
        stl_shp = read_stl_file(fileName)
        return stl_shp

    def import_to_STEP(self, fileName):
        step_shp = read_step_file(fileName)
        return step_shp

    def import_to_IGES(self, fileName):
        iges_shp = read_iges_file(fileName)
        return iges_shp

    def quit(self):
        self.parent.close()

    def export_to_PNG(self):
        self.glWindow.view.Dump('./capture_png.png')
