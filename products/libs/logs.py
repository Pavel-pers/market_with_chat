import logging
import functools

# set up logger
product_logger = logging.getLogger('products')
handler = logging.FileHandler('logs/root.log', mode='a')
formatter = logging.Formatter('[%(asctime)s](%(name)s)%(levelname)s:%(message)s', '%H:%M:%S')
handler.setFormatter(formatter)
product_logger.addHandler(handler)
product_logger.setLevel(logging.DEBUG)


def action_with_logging(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        product_logger.debug('start executing: {}'.format(func.__name__))
        response = await func(*args, **kwargs)
        product_logger.debug('end executing: {}'.format(func.__name__,))
        return response

    return wrapper
