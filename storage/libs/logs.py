import logging
import functools

# set up logger
storage_logger = logging.getLogger('storage')
handler = logging.FileHandler('logs/root.log', mode='a')
formatter = logging.Formatter('[%(asctime)s](%(name)s)%(levelname)s:%(message)s', '%H:%M:%S')
handler.setFormatter(formatter)
storage_logger.addHandler(handler)
storage_logger.setLevel(logging.DEBUG)


def action_with_logging(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        storage_logger.debug('start executing: {}'.format(func.__name__))
        response = await func(*args, **kwargs)
        storage_logger.debug('end executing: {}'.format(func.__name__,))
        return response

    return wrapper
