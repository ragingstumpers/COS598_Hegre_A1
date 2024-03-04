PLEASE NOTE that there is a ton of ambiguities in their paper and so the results of this simulator
unforatunately does not match theirs on the same data, sometimes it is quite close and sometimes varies wildly....

1) Use requirements.txt to set up venv
2) Wrote a CLI, please use: python simulator/run_simulation.py --help    to get info on how to run
To offer a rough summary of what this does/how it works:
- takes in CSVs describing data to run the simulation - projections, current state, constants and covariance matrix from STATA
- given that information and the year range inputted, the simulator does the following:
    1) Creates a pool of processes
    2) In each one, runs the simulation for all countries for the year range
        - for each year compute the independent variables
            -- this is done in DAG order, since some are multiplicative
        - draw new coefficients using the STATA information (draw from gaussian using OG coefficients as avg, covariance matrix)
        - compute logistic probability at that time step by computing dot products of coefficients and independent variables determined for that time step
        - draw a conflict level
        - compile the base state for the next iteration
        - NOTE: this is done for all countries at once
    3) merge all of the concurrent simulation results into one averaging the results from all models, writing it to a CSV