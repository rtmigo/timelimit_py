# SPDX-FileCopyrightText: (c) 2020 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


from typing import *

T = TypeVar("T")


class TimeLimitExceeded(Exception):
    # я предпочитаю выкидывать такое исключение, поскольку TimeoutError,
    # определенная в builtins.py, унаследована от OSError (я подозреваю, что
    # имеет специальное назначение). А TimeoutError, определенная в
    # multiprocessing.context, вообще вызывает путаницу в именах
    pass


def limit_thread(func: Callable[..., T], args=None, timeout: float = None,
                 default=TimeLimitExceeded) -> T:
    # запускает функцию func в параллельном потоке.
    #
    # Если func успевает вернуть результат за время timeout, возвращаем этот
    # результат. Иначе возвращаем значение default.

    from multiprocessing.pool import ThreadPool
    from multiprocessing.context import TimeoutError as MpTimeoutError

    try:
        with ThreadPool() as pool:
            if args is not None:
                asyncResult = pool.apply_async(func, args=args)
            else:
                asyncResult = pool.apply_async(func)
            return asyncResult.get(timeout=timeout)
    except MpTimeoutError:

        if default == TimeLimitExceeded:
            raise TimeLimitExceeded
        else:
            # возвращаем значение по умолчанию
            return default


def limit_process(func: Callable[..., T], args=None,
                  timeout: float = None,
                  default=TimeLimitExceeded) -> T:
    # запускает функцию func в параллельном процессе.
    #
    # Если func успевает вернуть результат за время timeout, возвращаем этот
    # результат. Иначе возвращаем значение default.

    from multiprocessing import Pool
    from multiprocessing.context import TimeoutError as MpTimeoutError

    try:
        with Pool() as pool:
            if args is not None:
                asyncResult = pool.apply_async(func, args=args)
            else:
                asyncResult = pool.apply_async(func)
            return asyncResult.get(timeout=timeout)
    except MpTimeoutError:
        # возвращаем значение по умолчанию
        if default == TimeLimitExceeded:
            raise TimeLimitExceeded
        else:
            return default
