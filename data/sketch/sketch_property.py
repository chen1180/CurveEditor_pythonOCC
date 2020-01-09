from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout,QGridLayout,QComboBox,QGroupBox,QLabel,QLineEdit,QPushButton,QWidget

class Sketch_Property(QWidget):
    def __init__(self,parent,name,fl):
        super(Sketch_Property, self).__init__(parent,name,fl)
        self.StartCoord="["
        self.MidCoord=","
        self.EndCoord="]"
        self.NumberExpr="[^0-9.-]"

        

    def SetContext(self,theContext):
        pass
    def SetAx3(self,theAx3):
        pass
    def SetSketch_Object(self,CurObject):
        pass


