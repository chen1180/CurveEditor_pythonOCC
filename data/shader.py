from OpenGL.GL import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
class Shader(object):
    def __init__(self):
        self._vao=0
        self._vbo=0

    def InitShader(self,vertShader,fragShader,tescShader=None,teseShader=None,geomShader=None):
        self._program = QOpenGLShaderProgram()
        self._program.addShaderFromSourceFile(QOpenGLShader.Vertex, vertShader)
        self._program.addShaderFromSourceFile(QOpenGLShader.Fragment, fragShader)
        if tescShader:
            self._program.addShaderFromSourceFile(QOpenGLShader.TessellationControl, tescShader)
        if teseShader:
            self._program.addShaderFromSourceFile(QOpenGLShader.TessellationEvaluation, teseShader)
        if geomShader:
            self._program.addShaderFromSourceFile(QOpenGLShader.Geometry, geomShader)
        self._program.link()
        if self._program.log():
            qDebug(self._program.log())
            return False
        return True

    def BindShader(self):
        self._program.bind()
    def InitBuffer(self,vertices,size):
        self._vao = QOpenGLVertexArrayObject()
        self._vao.create()
        self._vao.bind()
        # initiate all the VBO and VAO
        self._vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self._vbo.create()
        self._vbo.bind()
        self._vbo.setUsagePattern(QOpenGLBuffer.StaticDraw)
        self._vbo.allocate(vertices, size)
        self._program.enableAttributeArray(0)
        self._program.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        # release
        self._vbo.release()
        self._vao.release()
        self._program.release()
    def DrawBezierCurve(self,resolution,size):
        # Camera transformation
        Model = QMatrix4x4()
        self.MVP = Model
        self._program.bind()
        self._program.setDefaultOuterTessellationLevels([1, resolution])
        # Qpengl Tesselation Control Shader attribute
        self._program.setPatchVertexCount(size)  # Maximum patch vertices
        self._vbo.bind()
        self._program.setUniformValue("MVP", self.MVP)
        # Rencently add code for lighting
        # ------------------------------------------------------------------------------
        self._program.setUniformValue("objectColor", QVector3D(1, 1, 1))
        self._program.setUniformValue("lightColor", QVector3D(1, 1, 1))
        # ------------------------------------------------------------------------------
        # Draw primitives
        self._vao.bind()
        glDrawArrays(GL_PATCHES, 0, size)
        self._vao.release()
        self._program.release()
    def DrawNurbsCurve(self,resolution,size,knots,weights,clamped,order):
        # Camera transformation
        Model = QMatrix4x4()
        self.MVP = Model
        self._program.bind()
        self._program.setDefaultOuterTessellationLevels([1, resolution])
        # Qpengl Tesselation Control Shader attribute
        self._program.setPatchVertexCount(size)  # Maximum patch vertices
        self._vbo.bind()
        self._program.setUniformValue("MVP", self.MVP)
        # Rencently add code for lighting
        # ------------------------------------------------------------------------------
        self._program.setUniformValue("objectColor", QVector3D(1, 1, 1))
        self._program.setUniformValue("lightColor", QVector3D(1, 1, 1))
        for i in range(len(knots)):
            self._program.setUniformValue("knots[{}]".format(i), knots[i])
        for i in range(len(weights)):
            self._program.setUniformValue("weights[{}]".format(i), weights[i])
        self._program.setUniformValue("knots_size", len(knots))
        self._program.setUniformValue("clamped", clamped)
        self._program.setUniformValue("order", order)
        # ------------------------------------------------------------------------------
        # Draw primitives
        self._vao.bind()
        glDrawArrays(GL_PATCHES, 0, size)
        self._vao.release()
        self._program.release()