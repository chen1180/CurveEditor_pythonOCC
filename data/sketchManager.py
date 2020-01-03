import resources.icon.icon
from data.node import *

class SketchObject(object):
    def __init__(self):
        self._geometry=None
        self._interactivePoints=[]
    def setGeometry(self,geometry):
        self._geometry=geometry
    def setInteractivePoints(self,points):
        self._interactivePoints=points
    def compute(self):
        pass
    def draw(self):
        pass
class BezierSketch(SketchObject):
    def __init__(self):
        super(BezierSketch, self).__init__()






