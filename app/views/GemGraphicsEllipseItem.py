from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem


class GemGraphicsEllipseItem(QGraphicsEllipseItem):

    def __init__(self, parent=None):
        super().__init__(parent)
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(2.0)
        self.setPen(pen)
        self.pix = self.setRect(0, 0, 10, 10)
        self.width = 10
        self.height = 10
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # update selected node and its edge
        # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()