import resources.icon.icon
import resources.shaders.shaders
import numpy as np
from data.node import *
from data.model import *
class SceneObject(object):
    def __init__(self):
        self._mesh=MeshNode()
        self._transform=TransformNode()
        self._material=MaterialNode()
class Curve(object):
    def __init__(self, name, parent=None):
        super(Curve, self).__init__(name, parent)
        self._vertices=np.array([],dtype="float32")
        self._size=0
        self._order=2
        self._clamped=True
        self._subdivision = 20
class BezierCurve(Curve):
    def __init__(self, name, parent=None):
        super(BezierCurve, self).__init__(name, parent)
    def resource(self):
        return ":/bezier.png"
    def initializeShader(self):
        self._shader.InitShader(":/bezier.vert", ":/bezier.frag", None, ":/bezier.tese", None)
        self._shader.BindShader()
        self._shader.InitBuffer(self._vertices, self._size)
        self._shaderDirty=False
    def runShader(self):
        self._shader.DrawBezierCurve(self._subdivision, self._vertices.shape[0] // 3)


