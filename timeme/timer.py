"""
Author: Rohin Dasari



This module provides the main code behind the timeme module.

The Timer class is responsible for storing timing statistics for different functions

It also provides a decorator based interface to record timings of functions

"""


from collections import defaultdict
import statistics as stats
import multiprocessing as mp
from functools import wraps
from copy import copy

import pandas as pd
from tqdm import tqdm

from . import timer_utils as utils


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

    def _drop_from_dict(self, d, keys):
        """
        Safely remove a list of keys from a dictionary without modifying the
        dictionary outside of the scope of the function

        Parameters
        ----------
        d : dict
            dictionary to remove keys from
        key : list | str
            list of keys to remove from dict

        Returns
        -------
        dict
            A shallow copy of the original dictionary with the specefied keys
            removed

        """
        return {k: v for k, v in d.items() if k not in keys}

    def get_iterable(self):
        """
        Builds an iterable object based on whether or not the user wants a
        progress bar

        Returns
        -------
        range | tqdm.std.tqdm
            Either returns a regular range iterator or a tqdm iterator with a
            progress bar

        """
        if not self.pbar or self.parallelize:
            return range(self.trials)
        else:
            return tqdm(range(self.trials))

    def parallel_time_trials(self, func, *args, **kwargs):
        """
        Perform time trials of a function in parallel using the multiprocessing
        module

        Parameters
        ----------
        func : function
            The function that the user needs to time

        *args
            The arguments that the user passes to the function

        *kwargs
            The keyword arguments that the user passes to the function

        Returns
        -------
        return_val
            The expected return value of the function

        trial_runs
            data about the runtime or profiling of the code

        """
        iterable = self.get_iterable()
        iterable_args = [(func, args, kwargs) for i in iterable]
        pbar = tqdm(total=len(iterable)) if self.pbar else None
        return_val, trial_runs = utils.parmap(
                utils.timeme_par if not self.profile else utils.profileme_par,
                iterable_args,
                nprocs=self.nprocs,
                pbar=pbar)
        return return_val, trial_runs

    def time_trials(self, func, *args, **kwargs):
        """
        Perform time trials of a function sequentially

        Parameters
        ----------
        func : function
            The function that the user needs to time

        *args
            The arguments that the user passes to the function

        *kwargs
            The keyword arguments that the user passes to the function

        Returns
        -------
        return_val
            The expected return value of the function

        trial_runs
            data about the runtime or profiling of the code

        """
        trial_runs = []
        return_val = None
        iterable = self.get_iterable()
        f = utils.timeme if not self.profile else utils.profileme
        for _ in iterable:
            exec_time, return_val = f(func, *args, **kwargs)
            trial_runs.append(exec_time)
        return return_val, trial_runs

    def record_results(self, results, f_name, f_args, f_kwargs):
        """
        Compute basic stats about time trials and save the results in the main records dict

        Parameters
        ----------
        results : dict
            A dictionary containing the list of functions that have been
            evaluated using the time_trials or parallel_time_trials method

        f_name : str
            The function name

        f_args
            The arguments passed to the function

        f_kwargs
            The keyword arguments passed to the function

        """
        if f_name not in [*self.records[copy(self.name)].keys()]:
            self.records[self.name][f_name] = []

        record = utils.Record(
                data=results,
                metadata={'args': f_args, 'kwargs': f_kwargs},
                aggregate=None if self.profile is True else
                         {
                         'mean': stats.mean(results),
                         'std_dev': stats.pstdev(results)
                         }
                )
        self.records[self.name][f_name].append(record)

    def set_attributes(self, params):
        """
        Allow users to pass parameters to their functions to override the
        default behavior of the decorator they defined

        Parameters
        ----------
        params : dict
            A set of new parameters to override the original behavior of the Timer decorator

        Return
        ------
        dict
            The original set of attributes

        """
        if params.items() is None: return
        original_attrs = {}
        for k, v in params.items():
            original_attrs[k] = getattr(self, k)
            setattr(self, k, v)
        return original_attrs

    def __call__(self, func):
        """
        A decorator that allows the user to time whatever function that is decorated.
        Automatically provides an argument to the function that allows the user
        to bypass the timing logic if they don't want to time the function
        everytime.

        Parameters
        ----------
        func : function
            The function to be decorated

        Return
        -------
        wrapper : function
            return the wrapped version of the function
            The wrapped version will automatically time the function on
            execution and save the results in a dictionary along with some
            basic statistics

        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            timeme_args = ['timeme', 'timeme_params']
            kwargs_ = self._drop_from_dict(kwargs, timeme_args)
            original_attrs = {}
            if 'timeme_params' in kwargs:
                original_attrs = self.set_attributes(kwargs['timeme_params'])
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
            self.set_attributes(original_attrs)

            return return_val
        wrapper._original = func
        return wrapper
