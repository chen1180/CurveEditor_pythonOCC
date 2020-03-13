import numpy as np
import matplotlib.pyplot as plt


class DraggableScatter():

    epsilon = 5

    def __init__(self, scatter):

        self.scatter = scatter
        self._ind = None
        self.ax = scatter.axes
        self.canvas = self.ax.figure.canvas
        self.canvas.mpl_connect('button_press_event', self.button_press_callback)
        self.canvas.mpl_connect('button_release_event', self.button_release_callback)
        self.canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        plt.show()


    def get_ind_under_point(self, event):
        xy = np.asarray(self.scatter.get_offsets())
        xyt = self.ax.transData.transform(xy)
        xt, yt = xyt[:, 0], xyt[:, 1]

        d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)
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
        xy = np.asarray(self.scatter.get_offsets())
        xy[self._ind] = np.array([x, y])
        self.scatter.set_offsets(xy)
        self.canvas.draw_idle()

fig, ax = plt.subplots(1, 1)
scatter = ax.scatter(np.random.rand(10), np.random.rand(10), marker='o')

DraggableScatter(scatter)