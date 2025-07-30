import timeit
from functools import partial

def runtime(func, *args, **kwargs):
    myfunc = partial(func, *args, **kwargs)
    return f"{(timeit.timeit(myfunc, number=1000) / 1000) * 10**6:.4f}"
