# autonomous_vehicle_flocking
Attempting to integrate flocking behavior into autonomous vehicle navigation to make it more efficient

This code implements a very simple simulation of city traffic to allow me to analyze the effects of incorporating
flocking behavior into an autonomous vehicle's navigation methods.

To run the code, simply run `$ python vehicle_sim.py`.  A window should pop up which will run the simulation after a few
seconds.

To change between the normal vehicle navigation method and the flocking-augmented one, go into `constants.py` and set
the `method` variable to be either `"normal"` or `"flocking"`, whichever you wish to run.  You may also change some of
the other parameters here.
