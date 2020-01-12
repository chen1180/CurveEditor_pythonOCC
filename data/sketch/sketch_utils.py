from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger


def TColgp_Array1OfPnt2d_to_point_list(li: TColgp_Array1OfPnt2d):
    pts = []
    for i in range(li.Length()):
        point = li.Value(i + 1)
        pts.append(point)
    return pts


def TColStd_Array1OfNumber_to_list(li):
    pts = []
    for i in range(li.Length()):
        num = li.Value(i + 1)
        pts.append(num)
    return pts


def point_list_to_TColgp_Array1OfPnt(li):
    pts = TColgp_Array1OfPnt(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts


def point_list_to_TColgp_Array1OfPnt2d(li):
    pts = TColgp_Array1OfPnt2d(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts


def int_list_to_TColStd_Array1OfInteger(li):
    pts = TColStd_Array1OfInteger(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts


def float_list_to_TColStd_Array1OfReal(li):
    pts = TColStd_Array1OfReal(1, len(li))
    for n, i in enumerate(li):
        pts.SetValue(n + 1, i)
    return pts
