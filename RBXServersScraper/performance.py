import time

def measure_performance(f:function):
    def wrapper(*args,**kwargs):
        timeNow = time.perf_counter()
        result = f(*args,**kwargs)
        timeEnd = time.perf_counter()
        time_took = timeEnd-timeNow
        print(f"{f.__name__} took {time_took}s to execute")
        return result
    return wrapper
