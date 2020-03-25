from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OCC.Extend.DataExchange import read_stl_file, read_step_file, read_iges_file, write_stl_file, \
    read_step_file_with_names_colors
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
        menu.addAction(QAction(QIcon(":/newPlane.png"), "ScreenShot", self,
                               statusTip="Export current view as picture",
                               triggered=self.export_to_PNG))

    def load(self):
        file = self.getfiles()

    def saveAs(self):
        # # set the directory where to output the
        # stl_output_dir = os.path.abspath(os.path.join("..", "assets", "models"))
        #
        # # make sure the path exists otherwise OCE get confused
        # if not os.path.isdir(stl_output_dir):
        #     raise AssertionError("wrong path provided")
        # stl_low_resolution_file = os.path.join(stl_output_dir, "torus_default_resolution.stl")
        # write_stl_file(my_torus, stl_low_resolution_file)
        #
        # # then we change the mesh resolution, and export as binary
        # stl_high_resolution_file = os.path.join(stl_output_dir, "torus_high_resolution.stl")
        # # we set the format to binary
        # write_stl_file(my_torus, stl_low_resolution_file, mode="binary", linear_deflection=0.5, angular_deflection=0.3)
        # Create shape
        # iterate node
        output=[]
        for child in self.parent._rootNode.children():
            if isinstance(child, SketchObjectNode):
                output.append(pickle.dumps(child.getSketchObject().GetAIS_Object().Shape()))
            elif isinstance(child, SketchNode):
                for subChild in child.children():
                    output.append(pickle.dumps(subChild.getSketchObject().GetAIS_Object().Shape()))
                    print(pickle.dumps(subChild.getSketchObject().GetAIS_Object().Shape()))
                    print(pickle.dumps(subChild))

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
                importedNode = ImportedSurfaceNode(imported_surface.GetName(), self.parent._rootNode)
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

    def export_to_PNG(self):
        self.glWindow.view.Dump('./capture_png.png')
