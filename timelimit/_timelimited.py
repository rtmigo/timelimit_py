# SPDX-FileCopyrightText: (c) 2020 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from multiprocessing.pool import Pool as BasePool
from typing import *

T = TypeVar("T")


class TimeLimitExceeded(Exception):
    # there are already:
    # - TimeoutError(OSError) in builtins.py
    # - TimeoutError in multiprocessing.context
    #
    # Not sure if it is correct to throw the first one (this is an OSError).
    # The second one causes confusion in names.
    pass


INF = float('inf')


def _limit(pool: BasePool, func: Callable[..., T], args,
           timeout: float,
           default: Union[T, TimeLimitExceeded]):
    if timeout is None:
        if args is not None:
            return func(*args)
        else:
            return func()

    from multiprocessing.context import TimeoutError as MpTimeoutError
    try:
        with pool:
            if args is not None:
                async_result = pool.apply_async(func, args=args)
            else:
                async_result = pool.apply_async(func)
            assert timeout is not None
            return async_result.get(timeout=timeout if timeout != INF else None)
    except MpTimeoutError:

        if default == TimeLimitExceeded:
            raise TimeLimitExceeded
        else:
            return default


def limit_thread(func: Callable[..., T], args=None, timeout: Optional[float] = INF,
                 default: Union[T, TimeLimitExceeded] = TimeLimitExceeded) -> T:
    """
    Runs the `func` in a parallel thread and waits for the result.

    :param func: The function to be run.
    :param args: Arguments to the function.
    :param timeout: Timeout in seconds.
    :param default: The value to return if the function does not complete
    in time.
    :return: The result of the function, if it has completed the work on time.
    The `default` value otherwise.
    """

    from multiprocessing.pool import ThreadPool
    return _limit(ThreadPool(), func, args, timeout, default)


def limit_process(func: Callable[..., T], args=None,
                  timeout: Optional[float] = INF,
                  default: Union[
                      T, TimeLimitExceeded] = TimeLimitExceeded) -> T:
    """
    Runs the `func` in a parallel process and waits for the result.

    :param func: The function to be run.
    :param args: Arguments to the function.
    :param timeout: Timeout in seconds.
    :param default: The value to return if the function does not complete
    in time.
    :return: The result of the function, if it has completed the work on time.
    The `default` value otherwise.
    """

    from multiprocessing import Pool as ProcessPool
    return _limit(ProcessPool(), func, args, timeout, default)
