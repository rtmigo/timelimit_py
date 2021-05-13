# [timelimit](https://github.com/rtmigo/timelimited_py#readme)

Unified way to call time-limited functions in parallel threads or processes.

Tested with Python 3.6-3.9 on macOS, Ubuntu and Windows.

# Install

``` bash
pip3 install timelimit
```

# Use

``` python3
from timelimit import limit_thread, limit_process, LimitedTimeOut

def sluggish(a, b):
  ...
  return a+b

# will run sluggish(1, 2) in parallel thread no more than 5 seconds
a_plus_b = limit_thread(sluggish, (1, 2), timeout=5)

# will run sluggish(1, 2) in parallel process no more than 5 seconds
a_plus_b = limit_process(sluggish, (1, 2), timeout=5)
```

## If the time is up

If the function did not complete its work within the specified time, a 
`LimitedTimeOut` exception is thrown.

``` python3
try:
    limit_thread(sluggish, (1, 2), timeout=5)
    
except LimitedTimeOut:
    print("Oops!")  
```

If `default` is set to something other than `LimitedTimeOut`, no exception is 
thrown, but the `default` is returned.

``` python3
result = limit_thread(sluggish, (1, 2), timeout=5, default=-1)

if result == -1:
    print("Oops!")
```
