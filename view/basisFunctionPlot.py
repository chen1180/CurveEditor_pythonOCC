from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-
"""Python/Numpy implementation of Bspline basis functions via Cox - de Boor algorithm."""

from functools import partial
import numpy as np
import matplotlib.cm
import matplotlib.colors
import matplotlib.pyplot as plt


class memoize(object):
    """Cache the return value of a method.
       This class is meant to be used as a decorator of methods. The return value
       from a given method invocation will be cached on the instance whose method
       was invoked. All arguments passed to a method decorated with memoize must
       be hashable.
       If a memoized method is invoked directly on its class the result will not
       be cached. Instead the method will be invoked like a static method:
       class Obj(object):
           @memoize
           def add_to(self, arg):
               return self + arg
       Obj.add_to(1) # not enough arguments
       Obj.add_to(1, 2) # returns 3, result is not cached
       Script borrowed from here:
       MIT Licensed, attributed to Daniel Miller, Wed, 3 Nov 2010
       http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)

    def __call__(self, *args, **kw):
        obj = args[0]
        try:
            cache = obj.__cache
        except AttributeError:
            cache = obj.__cache = {}
        key = (self.func, args[1:], frozenset(kw.items()))
        try:
            res = cache[key]
        except KeyError:
            res = cache[key] = self.func(*args, **kw)
        return res


class Bspline:
    """Numpy implementation of Cox - de Boor algorithm in 1D."""

    def __init__(self, knot_vector, order):
        """Create a Bspline object.
        Parameters:
            knot_vector: Python list or rank-1 Numpy array containing knot vector
                         entries
            order: Order of interpolation, e.g. 0 -> piecewise constant between
                   knots, 1 -> piecewise linear between knots, etc.
        Returns:
            Bspline object, callable to evaluate basis functions at given
            values of `x` inside the knot span.
        """
        kv = np.atleast_1d(knot_vector)
        if kv.ndim > 1:
            raise ValueError("knot_vector must be Python list or rank-1 array, but got rank = %d" % (kv.ndim))
        self.knot_vector = kv

        order = int(order)
        if order < 0:
            raise ValueError("order must be integer >= 0, but got %d" % (order))

        self.p = order

        # Dummy calls to the functions for memory storage
        self.__call__(0.0)
        self.d(0.0)
        self.x = None
        self.y = None
        self.plt = []

    def GetBasis(self):
        nt_per_interval = 16

        epsrel = 1e-10
        epsabs = epsrel * (self.knot_vector[-1] - self.knot_vector[0])

        xxs = []
        for I in zip(self.knot_vector[:-1], self.knot_vector[1:]):
            t_i = I[0]
            t_ip1 = I[1] - epsabs
            if t_ip1 - t_i > 0.:  # accept only intervals of length > 0 (to skip higher-multiplicity knots in the interior)
                xxs.append(np.linspace(t_i, t_ip1, nt_per_interval))
        yys = []
        for i, xx in enumerate(xxs):
            yy = np.array([self(x) for x in xx])
            yys.append(yy)

        return xxs, yys

    def __basis0(self, xi):
        """Order zero basis (for internal use)."""
        return np.where(np.all([self.knot_vector[:-1] <= xi,
                                xi < self.knot_vector[1:]], axis=0), 1.0, 0.0)

    def __basis(self, xi, p, compute_derivatives=False):
        """Recursive Cox - de Boor function (for internal use).
        Compute basis functions and optionally their first derivatives.
        """

        if p == 0:
            return self.__basis0(xi)
        else:
            basis_p_minus_1 = self.__basis(xi, p - 1)

        first_term_numerator = xi - self.knot_vector[:-p]
        first_term_denominator = self.knot_vector[p:] - self.knot_vector[:-p]

        second_term_numerator = self.knot_vector[(p + 1):] - xi
        second_term_denominator = (self.knot_vector[(p + 1):] -
                                   self.knot_vector[1:-p])

        # Change numerator in last recursion if derivatives are desired
        if compute_derivatives and p == self.p:
            first_term_numerator = p
            second_term_numerator = -p

        # Disable divide by zero error because we check for it
        with np.errstate(divide='ignore', invalid='ignore'):
            first_term = np.where(first_term_denominator != 0.0,
                                  (first_term_numerator /
                                   first_term_denominator), 0.0)
            second_term = np.where(second_term_denominator != 0.0,
                                   (second_term_numerator /
                                    second_term_denominator), 0.0)

        return (first_term[:-1] * basis_p_minus_1[:-1] +
                second_term * basis_p_minus_1[1:])

    @memoize
    def __call__(self, xi):
        """Convenience function to make the object callable.  Also 'memoized' for speed."""
        return self.__basis(xi, self.p, compute_derivatives=False)

    @memoize
    def d(self, xi):
        """Convenience function to compute first derivative of basis functions. 'Memoized' for speed."""
        return self.__basis(xi, self.p, compute_derivatives=True)

    def plot(self, plt):
        """Plot basis functions over full range of knots.
        Convenience function. Requires matplotlib.
        """

        # try:
        #     import matplotlib.pyplot as plt
        # except ImportError:
        #     from sys import stderr
        #     print("ERROR: matplotlib.pyplot not found, matplotlib must be installed to use this function", file=stderr)
        #     raise

        x_min = np.min(self.knot_vector)
        x_max = np.max(self.knot_vector)
        x = np.linspace(x_min, x_max, num=100)
        N = np.array([self(i) for i in x]).T
        self.x = x
        self.y = N
        for i, n in enumerate(N):
            tmp, = plt.plot(x, n[i], picker=True, label="Knots {}".format(i))
            self.plt.append(tmp)
        plt.legend(loc="upper right")

    def dplot(self):
        """Plot first derivatives of basis functions over full range of knots.
        Convenience function. Requires matplotlib.
        """

        try:
            import matplotlib.pyplot as plt
        except ImportError:
            from sys import stderr
            print("ERROR: matplotlib.pyplot not found, matplotlib must be installed to use this function", file=stderr)
            raise

        x_min = np.min(self.knot_vector)
        x_max = np.max(self.knot_vector)

        x = np.linspace(x_min, x_max, num=1000)

        N = np.array([self.d(i) for i in x]).T

        for n in N:
            plt.plot(x, n)

        return plt.show()

    def __diff_internal(self):
        """Differentiate a B-spline once, and return the resulting coefficients and Bspline objects.
This preserves the Bspline object nature of the data, enabling recursive implementation
of higher-order differentiation (see `diff`).
The value of the first derivative of `B` at a point `x` can be obtained as::
    def diff1(B, x):
        terms = B.__diff_internal()
        return sum( ci*Bi(x) for ci,Bi in terms )
Returns:
    tuple of tuples, where each item is (coefficient, Bspline object).
See:
    `diff`: differentiation of any order >= 0
"""
        assert self.p > 0, "order of Bspline must be > 0"  # we already handle the other case in diff()

        # https://www.cs.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/B-spline/bspline-derv.html
        #
        t = self.knot_vector
        p = self.p
        Bi = Bspline(t[:-1], p - 1)
        Bip1 = Bspline(t[1:], p - 1)

        numer1 = +p
        numer2 = -p
        denom1 = t[p:-1] - t[:-(p + 1)]
        denom2 = t[(p + 1):] - t[1:-p]

        with np.errstate(divide='ignore', invalid='ignore'):
            ci = np.where(denom1 != 0., (numer1 / denom1), 0.)
            cip1 = np.where(denom2 != 0., (numer2 / denom2), 0.)

        return ((ci, Bi), (cip1, Bip1))

    def diff(self, order=1):
        """Differentiate a B-spline `order` number of times.
Parameters:
    order:
        int, >= 0
Returns:
    **lambda** `x`: ... that evaluates the `order`-th derivative of `B` at the point `x`.
                    The returned function internally uses __call__, which is 'memoized' for speed.
"""
        order = int(order)
        if order < 0:
            raise ValueError("order must be >= 0, got %d" % (order))

        if order == 0:
            return self.__call__

        if order > self.p:  # identically zero, but force the same output format as in the general case
            dummy = self.__call__(0.)  # get number of basis functions and output dtype
            nbasis = dummy.shape[0]
            return lambda x: np.zeros((nbasis,), dtype=dummy.dtype)  # accept but ignore input x

        # At each differentiation, each term maps into two new terms.
        # The number of terms in the result will be 2**order.
        #
        # This will cause an exponential explosion in the number of terms for high derivative orders,
        # but for the first few orders (practical usage; >3 is rarely needed) the approach works.
        #
        terms = [(1., self)]
        for k in range(order):
            tmp = []
            for Ci, Bi in terms:
                tmp.extend((Ci * cn, Bn) for cn, Bn in Bi.__diff_internal())  # NOTE: also propagate Ci
            terms = tmp

        # perform final summation at call time
        return lambda x: sum(ci * Bi(x) for ci, Bi in terms)

    def collmat(self, tau, deriv_order=0):
        """Compute collocation matrix.
Parameters:
    tau:
        Python list or rank-1 array, collocation sites
    deriv_order:
        int, >=0, order of derivative for which to compute the collocation matrix.
        The default is 0, which means the function value itself.
Returns:
    A:
        if len(tau) > 1, rank-2 array such that
            A[i,j] = D**deriv_order B_j(tau[i])
        where
            D**k  = kth derivative (0 for function value itself)
        if len(tau) == 1, rank-1 array such that
            A[j]   = D**deriv_order B_j(tau)
Example:
    If the coefficients of a spline function are given in the vector c, then::
        np.sum( A*c, axis=-1 )
    will give a rank-1 array of function values at the sites tau[i] that were supplied
    to `collmat`.
    Similarly for derivatives (if the supplied `deriv_order`> 0).
"""
        # get number of basis functions and output dtype
        dummy = self.__call__(0.)
        nbasis = dummy.shape[0]

        tau = np.atleast_1d(tau)
        if tau.ndim > 1:
            raise ValueError("tau must be a list or a rank-1 array")

        A = np.empty((tau.shape[0], nbasis), dtype=dummy.dtype)
        f = self.diff(order=deriv_order)
        for i, taui in enumerate(tau):
            A[i, :] = f(taui)

        return np.squeeze(A)


import math


class Bezier:
    def binomial(self, i, n):
        """Binomial coefficient"""
        return math.factorial(n) / float(
            math.factorial(i) * math.factorial(n - i))

    def bernstein(self, t, i, n):
        """Bernstein polynom"""
        return self.binomial(i, n) * (t ** i) * ((1 - t) ** (n - i))

    def bezier(self, t, points):
        """Calculate coordinate of a point in the bezier curve"""
        n = len(points) - 1
        x = y = 0
        for i, pos in enumerate(points):
            bern = self.bernstein(t, i, n)
            x += pos[0] * bern
            y += pos[1] * bern
        return x, y

    def bezier_curve_range(self, n, points):
        """Range of points in a curve bezier"""
        for i in range(n):
            t = i / float(n - 1)
            yield self.bezier(t, points)


class BsplineBasisFunctionWindow(QDialog):
    epsilon = 20
    PlotUpdated = pyqtSignal(object, int)

    def __init__(self, parent=None):
        super(BsplineBasisFunctionWindow, self).__init__(parent)
        # a figure instance to plot on
        self.figure = plt.figure()
        self.setWindowTitle("Basis function plot")

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.setModal(Qt.WindowModal)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.plotButton = QPushButton('Plot')
        self.plotButton.clicked.connect(self.plot)
        self.resetButton = QPushButton('Reset')
        self.resetButton.clicked.connect(self.resetPlot)

        # degreeLabel = QLabel("Degree")
        # self.degreeLineEdit = QLineEdit()
        # degreeLabel.setBuddy(self.degreeLineEdit)

        # set the layout
        layout = QGridLayout()
        # layout.addWidget(degreeLabel, 0, 0, 1, 2)
        # layout.addWidget(self.degreeLineEdit, 0, 1, 1, 2)
        layout.addWidget(self.toolbar, 0, 0, 1, 4)
        layout.addWidget(self.canvas, 1, 0, 1, 4)
        layout.addWidget(self.plotButton, 2, 0, 1, 4)
        layout.addWidget(self.resetButton, 3, 0, 1, 4)

        self.setLayout(layout)
        self._ind = None
        self.canvas.mpl_connect('button_press_event', self.button_press_callback)
        self.canvas.mpl_connect('button_release_event', self.button_release_callback)
        self.canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.knots_vector = []
        self.degree = None
        self.original_knots = []
        self.original_degree = None

    # def closeEvent(self, QCloseEvent):
    #     super(BsplineBasisFunctionWindow, self).closeEvent(QCloseEvent)
    #     if (QMessageBox.question(self, "Close this window?"), "Close this window?", QWidget.QMessageBox.Yes,
    #         QWidget.QMessageBox.QMessageBox.No) == QWidget.QMessageBox.QMessageBox.Yes:
    #         self.close()

    def setBasisFunction(self, knots, degree):
        self.knots_vector = knots
        self.max_knot = max(self.knots_vector)
        self.min_knot = min(self.knots_vector)
        self.degree = degree
        self.original_degree = degree
        self.original_knots = knots

    def get_ind_under_point(self, event):
        xy = np.asarray(self.scatter.get_offsets())
        xyt = self.ax.transData.transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]

        d = np.sqrt((xt - event.x) ** 2 + (yt - event.y) ** 2)
        ind = d.argmin()

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def button_press_callback(self, event):
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)

    def button_release_callback(self, event):
        if event.button != 1:
            return
        self._ind = None

    def motion_notify_callback(self, event):
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata
        if x < self.min_knot:
            x = self.min_knot
        if x > self.max_knot:
            x = self.max_knot
        y = 1.0
        xy = np.asarray(self.scatter.get_offsets())
        xy[self._ind] = np.array([x, y])
        self.scatter.set_offsets(xy)
        self.knots_vector = sorted([scatter[0] for scatter in self.scatter.get_offsets()])
        self.updatePlot()
        self.canvas.draw_idle()

    def updatePlot(self):
        for curve in self.curves:
            curve.remove()
        del self.curves
        basis = Bspline(self.knots_vector, self.degree)
        xxs, yys = basis.GetBasis()
        nrBasis = len(basis(0.0))
        # setting
        NUM_COLORS = nrBasis
        cm = plt.get_cmap('gist_rainbow')
        cNorm = matplotlib.colors.Normalize(vmin=0, vmax=NUM_COLORS - 1)
        scalarMap = matplotlib.cm.ScalarMappable(norm=cNorm, cmap=cm)
        colors = [scalarMap.to_rgba(i) for i in range(NUM_COLORS)]
        settings = {"linestyle": 'solid',
                    "linewidth": 1.0}
        self.curves = []
        for idx, xx in enumerate(xxs):
            yy = yys[idx]
            for i in range(nrBasis):
                # plt, = self.ax.plot(xx, yy[:,i], label="N{},{}".format(i, self.degree))
                settings["color"] = colors[i]
                ax, = self.ax.plot(xx, yy[:, i], **settings)
                self.curves.append(ax)
        self.PlotUpdated.emit(self.knots_vector, self.degree)

    def plot(self):
        ''' plot some random stuff '''
        self.figure.clear()

        # create an axis
        self.ax = self.figure.add_subplot(111)

        # plot data
        self.scatter = self.ax.scatter(self.knots_vector, [1] * len(self.knots_vector), picker=True, marker='x')
        basis = Bspline(self.knots_vector, self.degree)
        nrBasis = len(basis(0.0))
        x, N = basis.GetBasis()
        # setting
        NUM_COLORS = nrBasis
        cm = plt.get_cmap('gist_rainbow')
        cNorm = matplotlib.colors.Normalize(vmin=0, vmax=NUM_COLORS - 1)
        scalarMap = matplotlib.cm.ScalarMappable(norm=cNorm, cmap=cm)
        colors = [scalarMap.to_rgba(i) for i in range(NUM_COLORS)]
        settings = {"linestyle": 'solid',
                    "linewidth": 1.0}
        self.curves = []
        for idx, xx in enumerate(x):
            yy = N[idx]
            for i in range(nrBasis):
                # plt, = self.ax.plot(xx, yy[:,i], label="N{},{}".format(i, self.degree))
                settings["color"] = colors[i]
                ax, = self.ax.plot(xx, yy[:, i], **settings)
                self.curves.append(ax)
        self.canvas.draw()

    def resetPlot(self):
        self.degree = self.original_degree
        self.knots_vector = self.original_knots
        self.plot()
        self.PlotUpdated.emit(self.knots_vector, self.degree)


class BezierBasisFunctionWindow(QDialog):

    def __init__(self, parent=None):
        super(BezierBasisFunctionWindow, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()
        self.setWindowTitle("Bezier Basis function plot")

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.setModal(Qt.WindowModal)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.bezier = Bezier()

        # Just some button connected to `plot` method
        self.plotButton = QPushButton('Plot')
        self.plotButton.clicked.connect(self.plot)

        # set the layout
        layout = QGridLayout()
        layout.addWidget(self.toolbar, 1, 0, 1, 4)
        layout.addWidget(self.canvas, 2, 0, 1, 4)
        layout.addWidget(self.plotButton, 3, 0, 1, 4)
        self.setLayout(layout)

        self.knots_vector = []
        self.degree = None

    def setBasisFunction(self, numPoints):
        self.numPoints = numPoints
        self.degree = self.numPoints - 1

    def plot(self):
        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        self.ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        x = np.linspace(0, 1, 100)
        for j in range(self.numPoints):
            y = [self.bezier.bernstein(i, j, self.degree) for i in x]
            self.ax.plot(x, y, label="B{},{}".format(j, self.degree))
        self.ax.legend()
        # refresh canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # main = BezierBasisFunctionWindow()
    # main.setBasisFunction( 5)
    main = BsplineBasisFunctionWindow()
    main.setBasisFunction([0, 1, 2, 3, 4], 2)
    main.plot()
    main.show()

    sys.exit(app.exec_())
