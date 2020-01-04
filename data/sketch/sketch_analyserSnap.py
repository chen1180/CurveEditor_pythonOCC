from OCC.Core.Geom import *
from OCC.Core.gp import *
from OCC.Core.V3d import *
from OCC.Core.AIS import *
from OCC.Core.BRepPrimAPI import *
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import *
from OCC.Core.StdSelect import *
from OCC.Core.BRepAdaptor import *
from OCC.Core.BRep import *
from OCC.Core.GeomAbs import *
from OCC.Core.GeomFill import *
from OCC.Core.Aspect import *
from OCC.Core.Prs3d import *
from OCC.Core.Quantity import *
from OCC.Core.TColStd import *
from OCC.Core.Geom2d import *
from OCC.Core.TCollection import *
from OCC.Core.Standard import Standard_Transient
from data.sketch.sketch_type import *
from data.sketch.sketch_snap import *


class Sketcher_AnalyserSnap(Standard_Transient):
    def __init__(self, theContext: AIS_InteractiveContext,
                 thedata: TColStd_HSequenceOfTransient,
                 theAx3: gp_Ax3):
        super(Sketcher_AnalyserSnap, self).__init__()
        self.curCoordinateSystem = gp_Ax3(gp.XOY())
        self.myContext = theContext
        self.data = thedata
        self.curCoordinateSystem = theAx3

        self.myCurrentSnap = Sketcher_SnapType.SnapNothing
        self.mySnapAnType = Sketcher_SnapType.SnapNothing
        self.myPnt2d = gp.Origin2d()

        self.minimumSnapDistance = MINIMUMSNAP
        self.bestDist = 0
        self.curDist = 0

        self.storedPnt2d = gp.Origin2d()
        self.storedTangentType = Sketcher_SnapType.NothingTangent
        self.isTangent = False
        self.isLine = False

        self.mySnaps = TColStd_HSequenceOfTransient()

    def SetContext(self,theContext):
        self.myContext=theContext
        for i,value in enumerate(self.mySnaps):
            CurSnap=Sketcher_Snap.DownCast(self.mySnaps.Value(i))
            CurSnap.SetContext(self.myContext)
