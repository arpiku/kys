
## First commit
- The goal of the program is simple, to allow users to convert their keyboards into full macro keyboards.


Goals for v0.1
~~- A command line tool that lists all the available input devices and allow user to select the ones they wish
to use for macros.~~ 

~~- Generating config (a file containing individual function for each available key press) file for each device.~~  

This was done. Moving on, the current code is completely in one file, and a lot of things are uneccessarily mixing
the primary goal here is to write a generic piece of code that when receiving a certain command results in 
certain action..

Here I do not need to depend on evdev. I just need an event producer, which evdev is, but I need to overlay it 
with some code that sends some particular signal..

Generators !!!

- New goals:
  Make a generator that yields something when a certain event is observed.

Note: As of right now I am attempting to make everything functional and break them into very small chunks 
in order to remove dependency issues, and let's see if I have learned at least some functional programming..

Gonna start adding more structure to these notes:
  - April 13th 09:44
   - Side Project, a service to better prepare the documentation as I write the code.

  - April 29th 17:45
   - Was busy doing some leetcode, anyways back to work, heading forward on nixxy will require a lot of things to be done,
  right now gonna just complete kys enough to allow custom shortcuts based on any sort input device.






  
