from OpenGL.GL import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from data.curve import *
class DrawController(QObject):
    DRAWING_START=0
    DRAWING_END=1
    CURVE_BEZIER=10
    CURVE_NURBS=11
    CURVE_NURBS_CIRCLE = 12
    CURVE_FREEFORM=13
    SURFACE_BEZIER=14
    SURFACE_NURBS=15
    def __init__(self):
        self.screenPos=[]
        self._currentPoint=None
        self._drawStatus=None
        self._drawType=None
        self._scribbling=False
    def setStatus(self,status):
        self._drawStatus=status
    def setType(self,type):
        self._drawType=type
    def startDraw(self,type):
        self.setStatus(self.DRAWING_START)
        self.setType(type)
    def endDraw(self):
        self.setStatus(self.DRAWING_END)
    def clearDrawType(self):
        self._drawType=None
    def setupMatrix(self,View,Projection):
        self.View=View
        self.Projection=Projection
    def setupViewport(self,x,y,width,height):
        self.Viewport=QRect(x,y,width,height)
        self.width=width
        self.height=height
    def mouseClick(self, pos):
        if self._drawStatus==self.DRAWING_START:
            self.screenPos.append(pos)
            if self._drawType==self.CURVE_FREEFORM:
                self._scribbling=True
    def mouseMove(self,pos):
        if self._drawStatus == self.DRAWING_START:
            self._currentPoint=pos

    def mouseRelease(self,pos):
        if self._drawStatus == self.DRAWING_START:
            self._currentPoint=None
            if self._drawType==self.CURVE_FREEFORM and self._scribbling==True:
                self._scribbling=False
    def drawPoints(self,painter:QPainter):
        for vertices in self.screenPos:
            painter.drawEllipse(vertices,5,5)
        for i in range(len(self.screenPos)-1):
            painter.drawLine(QLine(self.screenPos[i],self.screenPos[i+1]))
        if self._currentPoint:
            painter.drawEllipse(self._currentPoint, 5, 5)
            if self.screenPos:
                painter.drawLine(QLine(self.screenPos[-1], self._currentPoint))
    def drawCircles(self,painter:QPainter):
        if self._currentPoint:
            if len(self.screenPos)==1:
                radius=QLineF(self._currentPoint, self.screenPos[0]).length()
                painter.drawEllipse(self.screenPos[0],radius,radius)
            elif len(self.screenPos)>=2:
                radius = QLineF(self.screenPos[0], self.screenPos[1]).length()
                painter.drawEllipse(self.screenPos[0], radius, radius)
    def drawLineTo(self,painter:QPainter):
        if self.screenPos and self._currentPoint:
            for i in range(len(self.screenPos)-1):
                painter.drawLine(self.screenPos[i],self.screenPos[i+1])
            painter.drawLine(self.screenPos[-1], self._currentPoint)
            self.screenPos.append(self._currentPoint)
    def drawShapeOnScreen(self, painter:QPainter):
        if self._drawStatus == self.DRAWING_START:
            if self._drawType==self.CURVE_NURBS_CIRCLE:
                self.drawCircles(painter)
            elif self._drawType==self.CURVE_FREEFORM:
                self.drawLineTo(painter)
            else:
                self.drawPoints(painter)

    def ToBezierCurve(self):
        if self._drawStatus==self.DRAWING_END:
            if self.screenPos:
                worldPos=[self.screenPosToWorldPos(vertices) for vertices in self.screenPos]

                item = BezierCurve("Beizer")
                item.setVertices(worldPos)
                self.screenPos.clear()
                return item
    def ToNurbsCurve(self):
        if self._drawStatus==self.DRAWING_END:
            if self.screenPos:
                worldPos=[self.screenPosToWorldPos(vertices) for vertices in self.screenPos]
                item = Nurbs("Nurbs")
                nPoints=len(worldPos)
                order=3
                knots=Nurbs_API.generateKnots(nPoints,order)
                weights=Nurbs_API.generateWeights(nPoints)
                item.setParams(knots,weights)
                item.setVertices(worldPos)
                item.setOrder(order)
                self.screenPos.clear()
                return item
    def ToNurbsCircle(self):
        if self._drawStatus == self.DRAWING_END:
            if self.screenPos:
                radius = QLineF(self.screenPos[0], self.screenPos[1]).length()
                center:QPointF = self.screenPos[0]
                squarePos=[]
                # calculate the 8 vertices of square that can enclose circle
                #top
                squarePos.append(QPointF(center.x(),center.y()+radius))
                # right top
                squarePos.append(QPointF(center.x() + radius, center.y() + radius))
                # right
                squarePos.append(QPointF(center.x() + radius, center.y()))
                # right bottom
                squarePos.append(QPointF(center.x() + radius, center.y() - radius))
                #bottom
                squarePos.append(QPointF(center.x(), center.y()-radius))
                # left bottom
                squarePos.append(QPointF(center.x() - radius, center.y() - radius))
                #left
                squarePos.append(QPointF(center.x()- radius, center.y() ))
                # left top
                squarePos.append(QPointF(center.x() - radius, center.y() + radius))
                # top
                squarePos.append(QPointF(center.x(), center.y() + radius))

                worldPos=[self.screenPosToWorldPos(vertices) for vertices in squarePos]
                knots=Nurbs_API.generateKnots_fullcircle()
                weights=Nurbs_API.generateWeights_fullcircle()
                item = Nurbs("Nurbs Circle")
                item.setVertices(worldPos)
                item.setParams(knots,weights)
                self.screenPos.clear()
                return item
    def To3DShape(self):
        item=None
        if self._drawType==self.CURVE_BEZIER:
            item=self.ToBezierCurve()
        elif self._drawType==self.CURVE_NURBS:
            item=self.ToNurbsCurve()
        elif self._drawType==self.CURVE_NURBS_CIRCLE:
            item=self.ToNurbsCircle()
        self._drawType=None
        self._drawStatus=None
        return item
    def screenPosToWorldPos(self,pos:QPointF):
        #Calculate Z depth value in the worold
        Z = QVector3D(0, 0, 0)
        Z = Z.project(self.View, self.Projection, self.Viewport)
        screenPos = pos
        #Use the Z depth value to convert 2D point on Screent to Wolrd pos
        wolrdPosition = QVector3D(screenPos.x(), self.height - screenPos.y(), Z.z()).unproject(self.View,
                                                                                               self.Projection,
                                                                                               self.Viewport)
        print("screen position:",screenPos.x(), screenPos.y(),Z.z(),"World position:",wolrdPosition)
        return wolrdPosition
#For debug purpose
if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook
    application=QApplication([])
    # The follow format can set up the OPENGL context
    window = SceneDockWidget() #Opengl window creation
    window.addItem(Bezier(window,"asd",[QVector3D(0,0,0),QVector3D(0,0,2)]))
    window.show()
    application.exec_()