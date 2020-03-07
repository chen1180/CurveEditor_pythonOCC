from view import createBezierSurfaceForm
from PyQt5.QtWidgets import QWidget,QApplication

class BezierSurfaceForm(QWidget):
    def __init__(self, parent=None):
        super(BezierSurfaceForm, self).__init__()
        self.ui = createBezierSurfaceForm.Ui_Form()
        self.ui.setupUi(self)
        self.ui.uiAddCurve.clicked.connect(self.addCurve)
    def addCurve(self):
        self.ui.listWidget.addItem("Item 1")

# -----------------------------Debugging-----------------------------------#
if __name__ == '__main__':
    application = QApplication([])
    window = BezierSurfaceForm()  # Opengl window creation
    window.show()
    application.exec_()