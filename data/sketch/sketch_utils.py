from OCC.Core.TColgp import TColgp_Array1OfPnt2d, TColgp_Array1OfPnt
from OCC.Core.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
from OCC.Core.ElCLib import elclib


def Pnt2dToPnt(pnt2d, theAxis):
    return elclib.To3d(theAxis.Ax2(), pnt2d)

def TColgp_Array1OfPnt2d_to_point_list(li):
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


def setQuasiUniformKnots(poles_size: int, degree: int):
    # total knots vector size
    knots_size = poles_size + degree + 1
    # calculate number of vectors in the middle of knots vector
    middle_size = knots_size - 2 * (degree + 1)
    multipicities = []
    if middle_size > 0:
        multipicities = [degree + 1]
        for i in range(middle_size):
            multipicities.append(1)
        multipicities += [degree + 1]
    else:
        first_point_multiplicities = knots_size - (degree + 1)
        if first_point_multiplicities > 0:
            multipicities = [degree + 1]
            for i in range(first_point_multiplicities):
                multipicities.append(1)
        else:
            for i in range(knots_size):
                multipicities.append(1)
    knots = []
    for i in range(len(multipicities)):
        knots.append(float(i))
    return (multipicities, knots)


def setUniformKnots(poles_size: int, degree: int):
    # total knots vector size
    knots_size = poles_size + degree + 1
    # calculate number of vectors in the middle of knots vector
    middle_size = knots_size - 2 * (degree + 1)
    multipicities = []
    knots = [float(i) for i in range(knots_size)]
    multipicities = [1] * knots_size
    return (multipicities, knots)


def setPiecewiseBezierKnots(poles_size: int, degree: int):
    # total knots vector size
    knots_size = poles_size + degree + 1
    # calculate number of vectors in the middle of knots vector
    middle_size = knots_size - 2 * (degree + 1)
    multipicities = [degree + 1]
    for i in range(middle_size // degree):
        multipicities.append(degree)
    remainder=middle_size%degree
    if remainder!=0:
        multipicities.append(remainder)
    multipicities += [degree + 1]
    knots = []
    for i in range(len(multipicities)):
        knots.append(float(i))
    return (multipicities, knots)
