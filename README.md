# [timelimit](https://github.com/rtmigo/timelimit_py#readme)

Sets the time limit for slow-running functions.
Runs functions in parallel threads or processes.

Tested with Python 3.6-3.9 on macOS, Ubuntu and Windows.

# Install

``` bash
pip3 install timelimit
```

# Use

``` python3
from timelimit import limit_thread, limit_process, TimeLimitExceeded

def sluggish(a, b):
  ...
  return a + b

# will run sluggish(1, 2) in parallel thread no more than 5 seconds
a_plus_b = limit_thread(sluggish, (1, 2), timeout=5)

# will run sluggish(1, 2) in parallel process no more than 5 seconds
a_plus_b = limit_process(sluggish, (1, 2), timeout=5)
```

## If the time is up

If the function did not complete its work within the specified time, a 
`TimeLimitExceeded` exception is thrown.

``` python3
try:
    limit_thread(sluggish, (1, 2), timeout=5)
    
except TimeLimitExceeded:
    print("Oops!")  
```

If you set the `default` argument (at least to `None`), the default value 
is returned instead of an exception.

``` python3
result = limit_thread(sluggish, (1, 2), timeout=5, default=-1)

if result == -1:
    print("Oops!")
```

## If time doesn't matter

If the `timeout` parameter is `None`, the function will run in the same way, but without time limits.

``` python3
result = limit_thread(sluggish, (1, 2), 
                      timeout = 5 if in_hurry else None)
```