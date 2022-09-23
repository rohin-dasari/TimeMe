# TimeMe

A small python pacakge to time the execution of functions, organize the results,
and manage larger experiments involving runtime and profiling of code.

## Why TimeMe?

Ever want to test out how fast your function really is? Maybe you want to test
and compare multiple functions. You used to have to write a quick block of code
to time the execution of your function, and in some cases, even write your own
decorator. You might then store the results in some array, compute some stats,
then plot it. How many times will you do the same thing over and over again?

For example:
 
I have a function like this:

```python

def foo():
    for i in range(10):
        print(i)

```


Now, if I want to time it, I have to do something like this:

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

## Questions?

Feel free to reach out at: rohin.dasari@gmail.com


