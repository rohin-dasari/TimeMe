# TimeMe

A small python pacakge to time the execution of functions, organize the results,
and manage larger experiments involving runtime and profiling of code.

## Download

```
pip install Please-TimeMe==0.0.1
```

Check the pypi page here: https://pypi.org/project/Please-TimeMe/0.0.1/


## Why TimeMe?

Ever want to test out how fast your function really is? Maybe you want to test
and compare multiple functions. You used to have to write a quick block of code
to time the execution of your function, and in some cases, even write your own
decorator. You might then store the results in some array, compute some stats,
then plot it. How many times will you do the same thing over and over again?

For example:
 
Say you have a function like this:

```python

def foo():
    for i in range(10):
        print(i)

```


Now, if you want to time it, you have to do something like this:

```python

import time

start = time.time()
foo()
runtime = time.time() - start

print(runtime)
```

Where do you store the runtime of the function? How do you make sure it is
associated with the funciton `foo` with the particular parameters passed to it?
Also what happens if you want to run multiple trials and take the average
runtime?

You used to have to write all this logic yourself, but here's how it looks with
TimeMe:

```python

from timeme import Timer

@Timer(name='foo_experiment', trials=100)
def foo():
    for i in range(10):
        print(i)
        
        
foo(timeme=true)
runtime_data = Timer.records['foo_experiment']

```

TimeMe automatically tracks the runtime of your function as it executes, so you
don't have to write any additional code. It also overrides your function
parameters and adds an additional keyword argument, `timeme`. This allows you to
toggle whether or not you want the runtime to be recorded. You can even run
multiple trials. TimeMe will automatically store the data from each run and
compute basic stats such as the mean and standard deviation of the trials.

The data can be retrieved in the Timer object. Want to export it as a CSV or do
even more analytics?

TimeMe can export the data as a pandas dataframe so you can do as much data
analysis as your heart desires.


TimeMe is a tool that will make sure you never have to write annoying
boilerplate code to evaluate the runtime of your code.

## Examples

Clone the repo and run the examples to see how TimeMe works for yourself.

To build the project from github, clone the repo and run the following at the
root of the project directory

```
pip install -e .
```

Then navigate to the examples directory and take a look around.

Run `python compare.py` to get a basic assessment between bubble sort and merge
sort. The code will run 100 trials on each function, record the runtime, and
report the mean and standard deviations.

Run `python varying_input.py` to see the same functions but with varying inputs.
This example will also graph the runtime of each function according to the
input size. Make sure you have `matplotlib` installed for this example.


## Questions?

Feel free to reach out at: rohin.dasari@gmail.com


