from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPainterPath, QFont, QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsPathItem


class GemGraphicsPathItem(QGraphicsPathItem):

    def __init__(self, edge_wrap, parent=None):
        super().__init__(parent)
        self.edge_wrap = edge_wrap
        print(self.edge_wrap)
        self.width = 2.0
        self.pos_src = [0, 0]  # 线条起始坐标
        self.pos_dst = [0, 0]  # 线条结束坐标

        self._pen = QPen(QColor("#000"))  # 画线条的笔
        self._pen.setWidthF(self.width)

        self._pen_dragging = QPen(QColor("#000"))  # 画拖拽线条的笔
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self._mark_pen = QPen(Qt.green)
        self._mark_pen.setWidthF(self.width)
        self._mark_brush = QBrush()
        self._mark_brush.setColor(Qt.green)
        self._mark_brush.setStyle(Qt.SolidPattern)

        # self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)  # 让线条出现在所有图元的最下层

        # 标注信息
        self.information = {'coordinates':'', 'class':'', 'name':'', 'scale':'', 'owner':'', 'saliency':''}

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]

    def calc_path(self):  # 计算线条的路径
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
        path.lineTo(self.pos_dst[0], self.pos_src[1])
        path.lineTo(self.pos_dst[0], self.pos_dst[1])
        path.moveTo(self.pos_src[0], self.pos_src[1])
        path.lineTo(self.pos_src[0], self.pos_dst[1])
        path.lineTo(self.pos_dst[0], self.pos_dst[1])

        font = QFont("Helvetica [Cronyx]", 12)
        path.addText(self.pos_src[0], self.pos_src[1], font, self.edge_wrap.labelText)
        self.information['coordinates'] = str([self.pos_src[0], self.pos_src[1], self.pos_dst[0], self.pos_dst[1]])
        self.information['class'] = self.edge_wrap.labelText
        return path

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        return self.calc_path()

    def paint(self, painter, graphics_item, widget=None):
        self.setPath(self.calc_path())
        path = self.path()
        if self.edge_wrap.end_item is None:
            # 包装类中存储了线条开始和结束位置的图元
            # 刚开始拖拽线条时，并没有结束位置的图元，所以是None
            # 这个线条画的是拖拽路径，点线
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
            painter.setPen(self._pen)
            painter.drawPath(path)