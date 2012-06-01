3Dtracker
=========

To run the program:
1.) Open ipython
2.) type 'imort tracker_runs_v2 as tracker'
3.) 'tracker.run()'
4.) Enter the event number that you want to look at.
5.) Admire the glorious plots and fits
//NOTE: each time you run the program it does generate an ouput file with title 'output#.txt' where # is the event number//

Group members
* Ben - Data I/0
* Robert - Data analysis / track separation
* Kyle - Fitting algorithm
* Kelsi - Visualization
* Royce  - Team Lead, Debugger
 
The goal of our project is to analyze and describe partical trajectories.

Our basic outline is to 

* Format data - separate incoming data into a rectilinear format that will then be section off into linear arrays
* Filter - create a filter that will sort through the data using smaller groupings of local data to identify clusters with limited hardware footprint
* Calculate - mathematically describe the clusters of data, at this time we are unsure of what the best algorithm would be to compliment those already existing
* Visualize - create a visual representation that will allow interested parties to have a straightforward interpretation the data
