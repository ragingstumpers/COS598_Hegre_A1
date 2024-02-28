PLEASE NOTE THAT THIS IS NOT YET DONE, I HAVE TO WRITE THE CSV INGEST CODE, BUT YOU ARE WELCOME TO EDIT THIS AS YOU SEE FIT

1) Use requirements.txt to set up venv
2) Wrote a CLI, please use `python run_simulation.py --help` to get info on how to run
    EXAMPLE INVOCATION (using meow for filenames):
    python run_simulation.py -min_cov meow -min_coeff meow -maj_cov meow -maj_coeff meow -exo meow -init meow -start 2000 -end 2010 -r meow -n meow -min_c 1 -maj_c 1 -conc 200

    EXAMPLE OUTPUT (current, will soon write to CSV):
    {'MEXICO': {2000: 2, 2001: 2, 2002: 1, 2003: 2, 2004: 2, 2005: 1, 2006: 2, 2007: 2, 2008: 2, 2009: 2, 2010: 2}, 'CANADA': {2000: 1, 2001: 2, 2002: 1, 2003: 2, 2004: 2, 2005: 2, 2006: 2, 2007: 2, 2008: 2, 2009: 1, 2010: 2}, 'USA': {2000: 1, 2001: 1, 2002: 1, 2003: 2, 2004: 1, 2005: 1, 2006: 2, 2007: 2, 2008: 2, 2009: 2, 2010: 2}}

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
    3) merge all of the concurrent simulation results into one by taking the majority conflict level for each country, year

STUFF LEFT TO DO:
- ingest CSVs, format correctly for use in the simulator (you can see how I expect to call it from utils.py where I generate random data)
- output a CSV of the results (currently just prints a dict)