from app.config.config import CfgNode
import time

from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QTextEdit, QFileDialog, QMessageBox, QDockWidget
from PyQt5 import QtCore, QtWidgets

from app.views.GemGraphicsView import GemGraphicsView
from app.views.GemListWidget import GemListWidget


class MainWindow(QMainWindow):
    def __init__(self, cfg: CfgNode = None):
        super().__init__()

        self.cfg = cfg
        if cfg is None:
            raise ValueError(f"the cfg node is None.")

        # 布局弹簧
        self.vspacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.hspacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.window_title = "GEM Annotator"
        self.setWindowTitle(self.window_title)
        self.resize(1000, 700)

        self.textbox = QTextEdit()
        self.textbox.adjustSize()
        self.cursor = self.textbox.textCursor()
        self.cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        self.textbox.setTextCursor(self.cursor)

        self.draw()

    def draw(self):
        # 界面相关
        main_widget = QtWidgets.QWidget()

        gem_main = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(QtCore.Qt.AlignVCenter)
        self.middle_layout = QVBoxLayout()
        self.middle_layout.setAlignment(QtCore.Qt.AlignVCenter)
        self.right_layout = QVBoxLayout()
        self.middle_layout.setAlignment(QtCore.Qt.AlignVCenter)

        gem_main.addLayout(self.left_layout)
        gem_main.addLayout(self.middle_layout)
        gem_main.addLayout(self.right_layout)
        gem_main.addItem(self.vspacerItem)
        main_widget.setLayout(gem_main)

        self.setCentralWidget(main_widget)

        self._draw_input_widgets()

    def _draw_input_widgets(self):
        self.left_layout.addItem(self.hspacerItem)


        btn_load_single_file = QPushButton("选择文件")
        btn_load_single_file.setFixedWidth(100)
        # btn_load_single_file.clicked.connect()
        btn_load_files_folder = QPushButton("选择目录")
        btn_load_files_folder.setFixedWidth(100)
        # btn_load_files_folder.clicked.connect()

        btn_start_annotation = QPushButton("开始标注")
        btn_start_annotation.setFixedWidth(100)
        # btn_start_annotation.clicked.connect()

        self.left_layout.addWidget(btn_load_single_file)
        self.left_layout.addWidget(btn_load_files_folder)
        self.left_layout.addWidget(btn_start_annotation)

        self.graphics = GemGraphicsView()
        self.middle_layout.addWidget(self.graphics)


        self.uniqLabelList = GemListWidget()
        self.uniqLabelList.setToolTip(
            self.tr(
                "Select label to start annotating for it. "
                "Press 'Esc' to deselect."
            )
        )
        self.label_dock = QtWidgets.QDockWidget(self.tr("Label List"), self)
        self.label_dock.setObjectName("Label List")
        self.label_dock.setWidget(self.uniqLabelList)

        self.fileSearch = QtWidgets.QLineEdit()
        self.fileSearch.setPlaceholderText(self.tr("Search Filename"))
        # self.fileSearch.textChanged.connect()
        self.fileListWidget = QtWidgets.QListWidget()
        # self.fileListWidget.itemSelectionChanged.connect()
        fileListLayout = QtWidgets.QVBoxLayout()
        fileListLayout.setContentsMargins(0, 0, 0, 0)
        fileListLayout.setSpacing(0)
        fileListLayout.addWidget(self.fileSearch)
        fileListLayout.addWidget(self.fileListWidget)
        self.file_dock = QtWidgets.QDockWidget(self.tr("File List"), self)
        self.file_dock.setObjectName("Files")
        fileListWidget = QtWidgets.QWidget()
        fileListWidget.setLayout(fileListLayout)
        self.file_dock.setWidget(fileListWidget)

        self.right_layout.addWidget(self.label_dock)
        self.right_layout.addWidget(self.file_dock)

    def _select_directory(self, input_component, update_key):
        """
        打开文件对话框选择目录
        """
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setDirectory(self.input_adc_input_image_folder.text())

        if dlg.exec_():
            dir_paths = dlg.selectedFiles()
            selected_dir_path = dir_paths[0]
            input_component.setText(selected_dir_path)

            self.updated_config_recorder.update_adc_folder_configs(update_key, selected_dir_path)

    # def on_worker_signal_out(self, inspect_record: InspectRecord):
    #     # logger.info(f"on_worker_signal_out: {signal}")
    #     if inspect_record is not None:
    #         # save statisitcs
    #         self.save_inspect_record_to_statisitcs_file(inspect_record)
    #         # show inspect result
    #         aries_output = inspect_record.aries_output
    #         color = '#00FF00' if aries_output.ng_property_text == 'OK' else '#FF0000'
    #         self._draw_text(self.label_inspect_result, aries_output.ng_property_text, aries_output.cls_pred_class_str, color)
    #         # show images
    #         if self.cfg.WINDOW.CONTROL.DISPLAY_IMAGE.ENABLED:
    #             self._draw_image(self.label_output_img_0, inspect_record.current_image_list[0])
    #             self._draw_image(self.label_output_img_1, inspect_record.current_image_list[1])
    #             self._draw_image(self.label_output_img_2, inspect_record.current_image_list[2])
    #         else:
    #             self.label_output_img_0.setText("根据配置不显示图片")
    #             self.label_output_img_1.setText("根据配置不显示图片")
    #             self.label_output_img_2.setText("根据配置不显示图片")
    #         # 打印日志
    #         if inspect_record.inspect_result_type == InspectResultType.NORMAL:
    #             is_ng = self.inspect_worker.ng_property_text(aries_output.is_ng)
    #             if is_ng == 'NG':
    #                 self._logbox(f"| Infer | {inspect_record.id}: NG. Type: {aries_output.cls_pred_class_str}")
    #             elif is_ng == "OK":
    #                 self._logbox(f"| Infer | {inspect_record.id}: OK")
    #         elif inspect_record.inspect_result_type == InspectResultType.MISSING_IMAGE:
    #             self._logbox(f"| Infer | {inspect_record.id}: MISSING_IMAGE")
    #         # 添加统计信息并更新
    #         # 写入数据库
    #         if self.cfg.WINDOW.CONFIG.WRITE_TO_DATABASE.ENABLED:
    #             self.today_database_file_name = self._get_current_database_file_name(str(datetime.date.today()))
    #             if str(self.sqlite_connect_for_today) != self.today_database_file_name:
    #                 self.sqlite_connect_for_today.init_today_db_file(self.today_database_file_name)
    #             try:
    #                 self.sqlite_connect_for_today.insert_database(inspect_record)
    #             except Exception as e:
    #                 logger.warning(f"writing datebase failed: {e}")


    def _message_reminder_box(self, message: str):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提示")
        msg_box.setText(message)
        msg_box.exec()

    def _logbox(self, info):
        self.textbox.append(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} {info}")

    def _draw_image(self, label_output_img: QLabel, image_path: str):
        if image_path is None:
            label_output_img.setText("图像缺失")
            return
        # self.label_output_img.setGeometry(QtCore.QRect(0, 0, 400, 400))
        label_output_img.setText("")
        label_output_img.setPixmap(QPixmap(image_path))
        label_output_img.setScaledContents(True)
        # self.label_output_img.setObjectName("output image")

    def _draw_text(self, label_widget: QLabel, text: str, class_text: str, color: str):

        text_font_size = 30 if len(text) > 2 else 35
        class_text_font_size = 13

        label_widget.setText(f"<font style = 'font-size:{text_font_size}px; color:{color}; font-weight:bold;'> {text} </font>"
                              "<br/>"
                              "<br/>"
                             f"<font style = 'font-size:{class_text_font_size}px; color:{color};text-align:center'> {class_text} </font>") # ; font-weight:bold

    def _set_btn_enable_state(self):
        self.btn_load_model.setEnabled(not self.inspect_started)
        self.btn_start_inspect.setEnabled(not self.inspect_started)
        self.btn_stop_inspect.setEnabled(self.inspect_started)

