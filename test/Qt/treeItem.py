import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt


class pointsTreeWidgetItem(QTreeWidgetItem):
    def __init__(self):
        super(pointsTreeWidgetItem, self).__init__()

    def setData(self, p_int, p_int_1, Any):
        pass

    def data(self, p_int, p_int_1):
        pass


class TreeWidgetDemo(QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidgetDemo, self).__init__(parent)
        self.setWindowTitle('TreeWidget 例子')

        self.tree = QTreeWidget()
        # 设置列数
        self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        self.tree.setHeaderLabels(['Key', 'Value'])
        data = {"poles": [[0.0, 0.0], [1.1, 1.1], [2, 2]], "knots": [1, 2, 3, 4, 5],
                "weights": [1.0, 1.0, 1.0, 1.0, 1.0], "degree": 3}
        # 设置根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, "Key")
        root.setText(1, "Value")

        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 150)

        # 设置子节点1
        self.poles = QTreeWidgetItem(root, ["poles", str(data["poles"])])
        self.poles.setData(0, Qt.UserRole, data["poles"])
        for k, v in enumerate(data["poles"]):
            poles_children = QTreeWidgetItem(self.poles, [str(k), str(v)])
            # poles_children.setData(1,Qt.UserRole,v)
            coordinate_x = QTreeWidgetItem()
            coordinate_x.setText(0, "x")
            # coordinate_x.setText(1, str(v[0]))
            coordinate_y = QTreeWidgetItem()
            coordinate_y.setText(0, "y")
            # coordinate_y.setText(1, str(v[1]))
            x_widget = QDoubleSpinBox()
            x_widget.setValue(v[0])
            y_widget = QDoubleSpinBox()
            y_widget.setValue(v[1])
            poles_children.addChild(coordinate_x)
            poles_children.addChild(coordinate_y)
            self.tree.setItemWidget(coordinate_x, 1, x_widget)
            self.tree.setItemWidget(coordinate_y, 1, y_widget)
        self.weights = QTreeWidgetItem()
        self.weights.setText(0, "weights")
        self.weights.setText(1, str(data["weights"]))
        for k, v in enumerate(data["weights"]):
            widget = QDoubleSpinBox()
            widget.setValue(v)
            widget.setRange(0, 1.0)
            widget.setSingleStep(0.1)
            children = QTreeWidgetItem()
            children.setText(0, str(k))
            self.weights.addChild(children)
            self.tree.setItemWidget(children, 1, widget)
        root.addChild(self.weights)
        # 加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(root)

        # TODO 优化3 给节点添加响应事件
        self.tree.clicked.connect(self.onClicked)

        # 节点全部展开
        # self.tree.expandAll()
        self.setCentralWidget(self.tree)

    def onClicked(self, qmodeLindex):
        item = self.tree.currentItem()
        print('Key=%s,value=%s' % (item.text(0), item.text(1)))
        print(self.poles.data(0, Qt.UserRole))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = TreeWidgetDemo()
    tree.show()
    sys.exit(app.exec_())
