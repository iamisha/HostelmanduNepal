"""kanilog - """

__version__ = '0.1.9'
__author__ = 'fx-kirin <fx.kirin@gmail.com>'
__all__ = []

import logging
import sys
from pathlib import Path

import logzero

DEFAULT_DATE_FORMAT = '%(color)s[%(levelname)1.1s|%(process)s|%(asctime)s.%(msecs)03d %(name)s:%(threadName)s:%(module)s:%(lineno)d]%(end_color)s %(message)s'


def setup_logger(*args, **kwargs):
    if 'level' in kwargs:
        level = kwargs['level']
    else:
        level = logging.INFO

    if 'file_log_level' in kwargs:
        file_log_level = kwargs['file_log_level']
        del kwargs['file_log_level']
    else:
        file_log_level = logging.DEBUG

    if 'maxBytes' not in kwargs:
        kwargs['maxBytes'] = 10000000

    if 'backupCount' not in kwargs:
        kwargs['backupCount'] = 30

    if 'stdout_logging' in kwargs:
        stdout_logging = kwargs['stdout_logging']
        assert isinstance(stdout_logging, bool)
        del kwargs['stdout_logging']
    else:
        stdout_logging = True

    if 'stderr_logging' in kwargs:
        stderr_logging = kwargs['stderr_logging']
        assert isinstance(stderr_logging, bool)
        del kwargs['stderr_logging']
    else:
        stderr_logging = True

    if 'name' in kwargs:
        name = kwargs['name']
        assert isinstance(stdout_logging, bool)
    else:
        logzero.__name__ = ''
        kwargs['name'] = ''

    root_log_level = file_log_level if file_log_level < level else level
    kwargs['level'] = root_log_level

    if 'formatter' in kwargs:
        formatter = kwargs['formatter']
    else:
        formatter = logzero.LogFormatter(fmt=DEFAULT_DATE_FORMAT)

    kwargs['formatter'] = logzero.LogFormatter(fmt=formatter._fmt)
    kwargs['formatter']._fmt = formatter._fmt.replace('%(color)s', '').replace('%(end_color)s', '')

    logger = logzero.setup_logger(disableStderrLogger=True, *args, **kwargs)

    if stdout_logging:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if stderr_logging:
        stderr_logger = logging.getLogger('STDERR')
        stderr_logger.propagate = False

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(level)
        stderr_handler.setFormatter(formatter)
        stderr_logger.addHandler(stderr_handler)

        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setLevel(file_log_level)
                stderr_logger.addHandler(handler)
    return logger


def get_stderr_logger():
    return logging.getLogger('STDERR')


def log_anywhere(*args, **kwargs):
    logger = logzero.setup_logger('log_anywhere', logfile='/tmp/log_anywhere.log', disableStderrLogger=True, level=logging.DEBUG)
    logger.info(*args, **kwargs)


def get_module_logger(file_path, parent_index):
    module_path = Path(file_path)
    if parent_index == 0:
        logger_name = module_path.stem
    else:
        logger_name = str(module_path.parent.relative_to(module_path.parents[parent_index])).replace('/', '.') + '.' + module_path.stem
    return logging.getLogger(logger_name)
