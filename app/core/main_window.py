from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from PyQt5 import QtCore, QtWidgets

from app.config.config import CfgNode


class MainWindow(QMainWindow):
    def __init__(self, cfg: CfgNode = None):
        super().__init__()

        self.cfg = cfg
        if cfg is None:
            raise ValueError(f"the cfg node is None.")

        self.window_title = "Demo"
        self.setWindowTitle(self.window_title)
        self.resize(400, 150)
        self.draw()

    def draw(self):
        # 界面相关
        main_widget = QtWidgets.QWidget()

        main_div = QHBoxLayout(self)
        self.column = QVBoxLayout()

        main_div.addLayout(self.column)
        main_widget.setLayout(main_div)
        self.setCentralWidget(main_widget)

        self._draw_widgets()

    def _draw_widgets(self):

        line_machine_code_file_path = QHBoxLayout()
        label_machine_code_file_path = QLabel()
        label_machine_code_file_path.setText("空白窗口")
        label_machine_code_file_path.setFixedWidth(200)
        label_machine_code_file_path.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignVCenter)
        line_machine_code_file_path.addWidget(label_machine_code_file_path)
        self.column.addLayout(line_machine_code_file_path)

        self.btn_register = QPushButton("确定")
        self.btn_register.setFixedWidth(100)
        self.btn_exit = QPushButton("取消")
        self.btn_exit.setFixedWidth(100)
        line_btn = QHBoxLayout()
        line_btn.addWidget(self.btn_register)
        line_btn.addWidget(self.btn_exit)
        self.column.addLayout(line_btn)

