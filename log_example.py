# import logging
#
# # create a file handler
# handler = logging.FileHandler('hello.log')
# # handler.setLevel(logging.INFO)
#
# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)
#
# logger.info('aaa')
# logger.debug('hehe')

from osresmorning import mylog

mylog.set_config({
    'level':'DEBUG'
})

logger = mylog.get_log(__name__)

logger.debug('debug')
logger.info('info')