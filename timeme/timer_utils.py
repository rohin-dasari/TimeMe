"""
Author: Rohin Dasari


This module provides a series of helper functions that are used by the Timer module


"""



import time
from dataclasses import dataclass




@dataclass
class Record:
    data: list
    metadata: dict
    aggregate: dict = None


def profileme(func, *args, **kwargs):
    profiler = cProfile.Profile()
    profiler.enable()
    value = func(*args, **kwargs)
    profiler.disable()
    return profiler.getstats(), value


def profileme_par(args):
    return profileme(args[0], *args[1], **args[2])


def timeme(func, *args, **kwargs):
    start_time = time.time()
    value = func(*args, **kwargs)
    return time.time()-start_time, value


def timeme_par(args):
    return timeme(args[0], *args[1], **args[2])


def parmap(f, iterable, nprocs, pbar=None):
    times = []
    result = None
    with mp.Pool(processes=nprocs) as p:
        for data in p.imap_unordered(f, iterable):
            times.append(data[0])
            result = data[1]
            if pbar is not None:
                pbar.update()
        if pbar is not None:
            pbar.close()
    return result, times
