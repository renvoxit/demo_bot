
import logging
from functools import wraps


def async_log_function_call(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logging.info(f"CALL: {func.__name__}")
        return await func(*args, **kwargs)
    return wrapper
