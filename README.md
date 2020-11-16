TimeMe is a small python pacakge to time the execution of functions and methods and help you manage
your experiments involving measuring runtime of code


The goal of TimeMe is to make it easier for you to time/profile your code without writing repetitive code to record times, manage the results of these time/profile experiments in a single place, and make it easy to compare the execution time of functions and methods.


To Do:
Make Doxygen documentation/manual pages
Fixing the parallel processing code in the decorator. This feature allows for multiple trials of a single function to run at once, speeding up testing for larger functions



Warnings:
While I am working on adding parallel processing, setting the 'parrallelize' parameter to True in the decorator when overriding the function call will cause the calling code to break.

General disclaimer: this project is still in its infancy, so expect to run into problems.
Check out the examples folder to see it in action. Runtimes can be recorded in just a few lines and accessed with just a few more. Hopefully this helps out your project.

Feel free to reach out at: rohin.dasari@gmail.com


