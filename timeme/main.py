import time
from collections import defaultdict
import statistics as stats
from tqdm import tqdm
import multiprocessing as mp
from functools import wraps
from copy import copy
import sys
import pandas as pd
import cProfile
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


class Timer:
    records = defaultdict(dict)

    def __init__(self,
                 name,
                 trials=1,
                 profile=False,
                 pbar=False,
                 parallelize=False,
                 nprocs=None):

        self.name = name
        self.trials = trials
        self.profile = profile
        self.pbar = pbar
        self.parallelize = parallelize
        if nprocs is None:
            self.nprocs = mp.cpu_count()-1
        else:
            self.nprocs = nprocs

    @classmethod
    def records_as_df(cls):
        """
        return data stored in records as dataframe
        """
        return pd.DataFrame(cls.records)
        pass

    def drop_from_dict(self, d, key):
        d_ = copy(d)
        if isinstance(key, str):
            key = [key]
        for k in key:
            if k in d_:
                del d_[k]
        return d_

    def get_iterable(self):
        if not self.pbar or self.parallelize:
            return range(self.trials)
        else:
            return tqdm(range(self.trials))

    def parallel_time_trials(self, func, *args, **kwargs):
        iterable = self.get_iterable()
        # get the original function
        f = getattr(sys.modules[__name__], func.__name__)
        iterable_args = [(f, args, kwargs) for i in iterable]
        pbar = tqdm(total=len(iterable)) if self.pbar else None
        return_val, trial_runs = parmap(
                timeme_par if not self.profile else profileme_par,
                iterable_args,
                nprocs=self.nprocs,
                pbar=pbar)
        return return_val, trial_runs

    def time_trials(self, func, *args, **kwargs):
        trial_runs = []
        return_val = None
        iterable = self.get_iterable()
        f = timeme if not self.profile else profileme
        for _ in iterable:
            exec_time, return_val = f(func, *args, **kwargs)
            trial_runs.append(exec_time)
        return return_val, trial_runs

    def record_results(self, results, f_name, f_args, f_kwargs):
        if len(self.records[self.name].keys()) == 0:
            self.records[self.name][f_name] = []
        record = Record(
                data=results,
                metadata={'args': f_args, 'kwargs': f_kwargs},
                aggregate=None if self.profile is None else
                         {
                         'mean': stats.mean(results),
                         'std_dev': stats.pstdev(results)
                         }
                )
        self.records[self.name][f_name].append(record)

    def override_defaults(self, params):
        """
        allow users to pass parameters to their functions to override
        the default behavior of the decorator they defined
        """
        for k, v in params.items():
            setattr(self, k, v)
        pass

    def __call__(self, func):
        # add cProfile capabilities
        @wraps(func)
        def wrapper(*args, **kwargs):
            timeme_args = ['timeme', 'timeme_params']
            kwargs_ = self.drop_from_dict(kwargs, timeme_args)
            if 'timeme_params' in kwargs:
                self.override_defaults(kwargs['timeme_params'])
            if 'timeme' not in kwargs or not kwargs['timeme']:
                return func(*args, **kwargs_)

            if not self.parallelize:
                return_val, trials = self.time_trials(
                        func,
                        *args,
                        **kwargs_)
            else:
                return_val, trials = self.parallel_time_trials(
                        func,
                        *args,
                        **kwargs_)
            self.record_results(trials, func.__name__, args, kwargs)

            return return_val
        return wrapper


@Timer('sample_experiment',
       trials=5,
       pbar=False,
       parallelize=True)
def test(a: int, b: int):
    return a+b


if __name__ == '__main__':
    thing = test(1, 2, timeme=True)
    print(thing)




