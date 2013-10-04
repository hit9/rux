# coding=utf8

"""
    rux.logger
    ~~~~~~~~~~

    rux's colorful logger.
"""

from datetime import datetime
import logging
from logging import Formatter
from logging import getLogger
from logging import StreamHandler
import sys

from utils import colored


class ColoredFormatter(Formatter):
    """colored text output formatter"""

    def format(self, record):
        message = record.getMessage()
        mapping = {
            'CRITICAL': 'bgred',
            'ERROR': 'red',
            'WARNING': 'yellow',
            'SUCCESS': 'green',
            'INFO': 'cyan',
            'DEBUG': 'bggrey',
        }
        color = mapping.get(record.levelname, 'white')
        level = colored('%-8s' % record.levelname, color)
        time = colored(datetime.now().strftime("(%H:%M:%S)"), 'magenta')
        return " ".join([level, time, message])


logger = getLogger('rux')
logging.SUCCESS = 25  # WARNING(30) > SUCCESS(25) > INFO(20)
logging.addLevelName(logging.SUCCESS, 'SUCCESS')
logger.success = lambda msg, *args, **kwargs: logger.log(logging.SUCCESS, msg, *args, **kwargs)

# add colored handler
handler = StreamHandler(sys.stdout)
formatter = ColoredFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__':
    """Test all levels out"""
    logger.setLevel(logging.DEBUG)
    logger.info('info')
    logger.success('success')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
