import sys
import argparse

from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QApplication

from app.core.main_window import MainWindow
from app.config.config import get_cfg

# init logger
from app.utils import gem_logger

from loguru import logger
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", default="configs/sample.yml", metavar="FILE", help="path to config file")
    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()
    return args

def setup_logger_cfg(cfg):
    gem_logger.setup_file_logger(cfg.LOG.FILE_PATH, cfg.LOG.LEVEL)


def get_runtime_cfg(args):
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    return cfg


if __name__ == "__main__":

    args = parse_args()
    cfg_node = get_runtime_cfg(args)
    setup_logger_cfg(cfg_node)

    # 防止软件多开
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        serverName = 'AppServer'
        socket = QLocalSocket()
        socket.connectToServer(serverName)
        # 判定应用服务是否正常链接，如正常则证明程序实例已经在运行
        if socket.waitForConnected(500):
            app.quit()
        # 如果没有实例运行，则创建应用服务器并监听服务
        else:
            localServer = QLocalServer()
            localServer.listen(serverName)
            # 原始处理逻辑
            window = MainWindow(cfg=cfg_node)
            window.show()
            sys.exit(app.exec_())
    except Exception as e:
        logger.error('程序启动异常：{}'.format(e))
