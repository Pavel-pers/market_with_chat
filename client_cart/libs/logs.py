import logging
import functools

# set up logger
client_cart_logger = logging.getLogger('client_cart')
handler = logging.FileHandler('logs/root.log', mode='a')
formatter = logging.Formatter('[%(asctime)s](%(name)s)%(levelname)s:%(message)s', '%H:%M:%S')
handler.setFormatter(formatter)
client_cart_logger.addHandler(handler)
client_cart_logger.setLevel(logging.DEBUG)


def action_with_logging(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        client_cart_logger.debug('start executing: {}'.format(func.__name__))
        response = await func(*args, **kwargs)
        client_cart_logger.debug('end executing: {}'.format(func.__name__,))
        return response

    return wrapper
