# SPDX-FileCopyrightText: (c) 2020 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from multiprocessing import Pool
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


def _limit(pool: Pool, func: Callable[..., T], args=None, timeout: float = None,
           default=TimeLimitExceeded):
    from multiprocessing.context import TimeoutError as MpTimeoutError
    try:
        with pool:
            if args is not None:
                async_result = pool.apply_async(func, args=args)
            else:
                async_result = pool.apply_async(func)
            return async_result.get(timeout=timeout)
    except MpTimeoutError:

        if default == TimeLimitExceeded:
            raise TimeLimitExceeded
        else:
            return default


def limit_thread(func: Callable[..., T], args=None, timeout: float = None,
                 default=TimeLimitExceeded) -> T:
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
                  timeout: float = None,
                  default=TimeLimitExceeded) -> T:
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
