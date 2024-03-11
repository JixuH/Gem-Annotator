from app.views.GemGraphicsPathItem import GemGraphicsPathItem


class GemEdge:
    '''
    线条的包装类
    '''

    def __init__(self, scene, start_item, end_item, labelText=''):
        super().__init__()
        # 参数分别为场景、开始图元、结束图元
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item
        self.labelText = labelText

        # 线条图形在此创建
        self.gr_edge = GemGraphicsPathItem(self)
        # add edge on graphic scene  一旦创建就添加进scene
        self.scene.add_edge(self.gr_edge)

        if self.start_item is not None:
            self.update_positions()

    def store(self):
        self.scene.add_edge(self.gr_edge)

    def update_positions(self):
        patch = self.start_item.width / 2  # 想让线条从图元的中心位置开始，让他们都加上偏移
        src_pos = self.start_item.pos()
        self.gr_edge.set_src(src_pos.x()+patch, src_pos.y()+patch)
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            self.gr_edge.set_dst(end_pos.x()+patch, end_pos.y()+patch)
        else:
            self.gr_edge.set_dst(src_pos.x()+patch, src_pos.y()+patch)
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        self.gr_edge = None