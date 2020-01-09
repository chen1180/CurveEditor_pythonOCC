import enum


class Sketch_GeometryType(enum.Enum):
    PointSketcherObject = 0
    LineSketcherObject = 1
    CircleSketcherObject = 2
    ArcSketcherObject = 3
    CurveSketcherObject = 3


class Sketch_ObjectType(enum.Enum):
    MainSketcherType = 0
    AuxiliarySketcherType = 1


class Sketch_ObjectTypeOfMethod(enum.Enum):
    Nothing_Method = 0
    Point_Method = 1
    Line2P_Method = 2
    CircleCenterRadius_Method = 3
    Circle3P_Method = 4
    Circle2PTan_Method = 5
    CircleP2Tan_Method = 6
    Circle3Tan_Method = 7
    Arc3P_Method = 8

    ArcCenter2P_Method = 9
    BezierCurve_Method = 10
    Trim_Method = 11
    BSpline_Method=12
    PointsToBSpline_Method = 13


class TangentType(enum.Enum):
    NothingTangent = 0
    Line_FirstPnt = 1
    Line_SecondPnt = 2
    Circle_CenterPnt = 3


class Sketcher_SnapType(enum.Enum):
    SnapNothing = 0
    SnapEnd = 1
    SnapMiddle = 2
    SnapCenter = 3
    SnapNearest = 4
    SnapIntersection = 5
    SnapTangent = 6
    SnapParallel = 7
    SnapPerpendicular = 8
    SnapAnalyse = 9
