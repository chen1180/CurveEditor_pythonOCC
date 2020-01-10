import enum


class Sketch_GeometryType:
    PointSketchObject = 0
    LineSketchObject = 1
    CircleSketchObject = 2
    ArcSketchObject = 3
    CurveSketchObject = 4


class Sketch_ObjectType:
    MainSketchType = 0
    AuxiliarySketchType = 1


class Sketch_ObjectTypeOfMethod:
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


class TangentType:
    NothingTangent = 0
    Line_FirstPnt = 1
    Line_SecondPnt = 2
    Circle_CenterPnt = 3


class Sketcher_SnapType:
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
