# coding:utf8
"""
该日志类可以把不同级别的日志输出到不同的日志文件中
日志级别： debug < info < warning < error < critical
"""

import logging

log_level = logging.INFO
# log_format = '%(asctime)-20s %(filename)-40s %(funcName)-20s - %(levelname)-8s (line %(lineno)4d): %(message)s'
log_format = '%(pathname)-s:%(lineno)-d %(funcName)-s() - %(levelname)s: %(message)s'

logging.basicConfig(level=log_level, format=log_format)
logger = logging.getLogger(__name__)
