# [timelimit](https://github.com/rtmigo/timelimit_py#readme)

Sets the time limit for slow-running functions. Runs functions in parallel
threads or processes.

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

If you set the `default` argument (at least to `None`), the default value is
returned instead of an exception.

``` python3
result = limit_thread(sluggish, (1, 2), timeout=5, default=-1)

if result == -1:
    print("Oops!")
```

## If time doesn't matter

If you do not specify the `timeout` parameter it will default to `float('inf')`.
The `sluggish` function will run in a parallel thread or process, but without
time constraints.

``` python3
# both call run the function in parallel thread without time limits
limit_thread(sluggish, (1, 2))  
limit_thread(sluggish, (1, 2), timeout=float('inf')) 
```

If you specify the value `timeout = None`, then the `sluggish` function will be
executed like a regular function, without starting processes or threads.

``` python3
# the following calls are equivalent
sluggish(1, 2)
limit_thread(sluggish, (1, 2), timeout=None)
```

Thus, the limitation can be made optional and resource-saving.

``` python3
limit_thread(sluggish, (1, 2), 
             timeout = 5 if in_hurry else None)
```