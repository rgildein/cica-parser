import logging
from functools import wraps
from typing import Callable, Optional

logger = logging.getLogger(__name__)


def tries(f: Optional[Callable] = None, try_count: int = 3):
    """tries run more times"""
    def real_decorator(func):
        @wraps(func)
        def decorator(*args, count: int = 0, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                logger.error(error)
                if count + 1 < try_count:
                    return decorator(*args, count=count+1, **kwargs)
                else:
                    raise error

        return decorator

    return real_decorator(f) if callable(f) else real_decorator
