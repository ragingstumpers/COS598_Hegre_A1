PLEASE NOTE that there is a ton of ambiguities in their paper and so the results of this simulator
unfortunately does not match theirs on the same data, sometimes it is quite close and sometimes varies wildly....

INSTRUCTIONS ON HOW TO USE SIMULATOR, GIVEN THAT YOU HAVE STATA MODELS COEFFICIENTS/COVARIANCE INFO ALREADY COMPUTED.

1) Use requirements.txt to set up venv
2) Enter venv
3) Invoke CLI, please use: python simulator/run_simulation.py --help    to get info on how to run

To offer a rough summary of what this does/how it works:
- takes in CSVs describing data to run the simulation - projections, historical state, constants and covariance matrix from STATA for various models
- given that information and the year range inputted, the column to use for conflict history, and if we should use c1c2 or lc1/lc2 the simulator does the following:
    1) Creates a pool of processes
    2) Extracts info about projections, history, and models from the various CSVs
    2) Then, for each ensemble, runs the simulation for each sub-model of the ensemble for all countries for the year range
        - for each year compute the independent variables
            -- this is done in DAG order, since some are multiplicative
        - draw new coefficients using the STATA information (draw from gaussian using OG coefficients as avg, covariance matrix)
        - compute logistic probability at that time step by computing dot products of coefficients and independent variables determined for that time step
        - draw a conflict level
        - compile the base state for the next iteration
        - NOTE: this is done for all countries at once
    3) merge all of the concurrent simulation results into one averaging the results from all models, writing it to a CSV

    EXAMPLE MINIMAL INVOCATION

    python simulator/run_simulation.py -cov ~/Desktop/Results/conf_v4/lc/VarCov/m23.csv [ADD MORE FILES, ENSURING ORDER MATCHES] -coeff ~/Desktop/Results/conf_v4/lc/Coefs/m23.csv [ADD MORE FILES, ENSURING ORDER MATCHES] -exo ~/Desktop/Results/conf_v4/lc/projection.csv -hist ~/Desktop/Results/conf_v4/lc/merged_conflict_1970_2008.csv -start 2009 -end 2020 -conc 100 -out ~/Desktop/Results/conf_v4/lc/results_conflict.csv -lvl_name conflict -use_c1c2 false
