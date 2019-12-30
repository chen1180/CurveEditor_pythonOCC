from PyQt5 import  QtWidgets

class CustomToolButton(QtWidgets.QToolButton):
    def __init__(self,parent=None):
        super(CustomToolButton, self).__init__(parent)
        self.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.triggered.connect(self.setDefaultAction)