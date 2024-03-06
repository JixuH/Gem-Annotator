#!/usr/bin/python3

"""
# -*- coding: utf-8 -*-

# @Time     : 2024/03/06
# @File     : defaults.py

"""

from .config import CfgNode as CN


_C = CN()

_C.FIX_SEED = 0

_C.WINDOW = CN()
_C.WINDOW.CONFIG = CN()
_C.WINDOW.CONFIG.REGISTER = CN()
_C.WINDOW.CONFIG.REGISTER.FILE_FOLDER = '/path/to/file_folder/'
_C.WINDOW.CONFIG.REGISTER.ANNOTATOR_FOLDER = '/path/to/annotator_folder/'
_C.WINDOW.CONTROL = CN()
_C.WINDOW.CONTROL.AUTO_SAVE = CN()
_C.WINDOW.CONTROL.AUTO_SAVE.ENABLE = True

_C.REQUEST_PROTOCOL = CN()
_C.REQUEST_PROTOCOL.IMAGE_SUFFIX = ['png', 'jpg', 'jpeg', 'bmp']

_C.LOG = CN()
_C.LOG.LEVEL = 'INFO'
_C.LOG.FILE_PATH = 'logs/logs.log'

