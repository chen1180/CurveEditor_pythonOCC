import pickle
from data.node import *
from data.sketch.geometry import *
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
display, start_display, add_menu, add_function_to_menu = init_display()
class A(object):
    def __init__(self,a):
        self.a=a
        self.b= BRepPrimAPI_MakeBox(10., 10., 10.).Shape()

b=SketchObjectNode("Asd",None)
b.setSketchObject(Sketch_Point(display.Context,None))
c=Node("Asdas",None)
d=Node("Asd",c)
f=Node("Asdasdxzc",c)
dumps=pickle.dumps(c)
ob=pickle.loads(dumps)
print(ob)