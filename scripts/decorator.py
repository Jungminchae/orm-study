import time
from typing import Any, Tuple


class TimeTrace:
    """
    :param func: 파이썬 함수
    :param *args: func's positional arguments
    :param **kwargs: func's keyword arguments
    :return: func's return value, func's executed time
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs) -> Tuple[Any, float]:
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()

        return result, end_time - start_time
