import pickle
from data.node import *
from data.sketch.geometry import *
from OCC.Display.SimpleGui import init_display
display, start_display, add_menu, add_function_to_menu = init_display()
class A:
    def __init__(self,a):
        self.a=a
a=A(5)


b=SketchObjectNode("Asd",None)
b.setSketchObject(Sketch_Point(display.Context,None))
c=Node("Asdas",b)
print(pickle.dumps(a))
print(pickle.dumps(c))