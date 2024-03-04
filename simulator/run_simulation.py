import argparse
from collections import namedtuple
from defs import VariableEnum
from utils import average_models, create_initial_base_variables, majority_results_outer, write_results, write_ratio_results
from multiprocessing import Pool
from simulator import Simulator

_Args = namedtuple("_Args", "cov coeff exo hist start end lvl_name conc")

def _run_for_model(args: _Args) -> dict[str, dict[int, int]]:
    # lots of shit being done repeatedly, but thats fine for now
    print(args.coeff)
    initial_base_variables = create_initial_base_variables(
        args.cov,
        args.coeff,
        args.exo,
        args.hist,
        args.start,
        args.end,
        args.lvl_name
    )
    sim = Simulator(initial_base_variables, args.conc)
    return sim.run()

def _main():
    sim_cli = argparse.ArgumentParser(description="A program to run conflict data simulations. See Hegre 2013")
    sim_cli.add_argument(
        "-cov", "--covariance_matrix",
        nargs='*', type=str, help="filepaths to CSV files for entire covariance matrix. Make sure that they match with the coefficients filepaths order!", required=True,
    )
    sim_cli.add_argument(
        "-coeff", "--coefficients",
        nargs='*', type=str, help="filepath to CSV file for entire coefficients matrix. Make sure that they match with the covariance filepaths order!", required=True,
    )
    sim_cli.add_argument(
        "-exo", "--exogenous_projections",
        type=str, help="filepath to CSV file for exogenous variable projections by country", required=True,
    )
    sim_cli.add_argument(
        "-hist", "--history",
        type=str, help="filepath to CSV file for initializer variables for non-projected variables", required=True,
    )
    sim_cli.add_argument(
        "-start", "--start_year",
        type=int, help="Year to start the simulation", required=True,
    )
    sim_cli.add_argument(
        "-end", "--end_year",
        type=int, help="Year to end the simulation", required=True,
    )
    sim_cli.add_argument(
        "-conc", "--concurrent_simulations",
        type=int, help="the number of concurrent simulations to run and then choose majority", default=10,
    )
    sim_cli.add_argument(
        "-out", "--output_destination",
        type=str, help="filepath to write the results to in CSV format", required=True,
    )
    sim_cli.add_argument(
        "-lvl_name", "--conflict_level_name",
        type=str, help="name for the column that should be used as the conflict level (allows for different definitions to be processed)", required=True,
    )

    args = sim_cli.parse_args()
    assert(len(args.covariance_matrix) == len(args.coefficients)), "number of coeff files doesn't match covariance files"
    
    args_list = [
        _Args(
            cov,
            coeff,
            args.exogenous_projections,
            args.history,
            args.start_year,
            args.end_year,
            args.conflict_level_name,
            args.concurrent_simulations
        )
        for cov, coeff in zip(args.covariance_matrix, args.coefficients)
    ]

    results = list(map(_run_for_model, args_list))
    write_ratio_results(args.output_destination, average_models(results))
    return
    with Pool(5) as p:
        results = p.map(_run_for_model, args_list)
    write_results(args.output_destination, majority_results(results))
    #print(len(results))
    #print(results)


if __name__ == '__main__':
   _main()

# python run_simulation.py -cov ~/Desktop/original_models/m23_cov.csv ~/Desktop/original_models/m43_cov.csv ~/Desktop/original_models/m45_cov.csv ~/Desktop/original_models/m48_cov.csv ~/Desktop/original_models/m66_cov.csv ~/Desktop/original_models/m67_cov.csv ~/Desktop/original_models/m96_cov.csv ~/Desktop/original_models/m97_cov.csv ~/Desktop/original_models/m98_cov.csv -coeff ~/Desktop/original_models/m23_coeff.csv ~/Desktop/original_models/m43_coeff.csv ~/Desktop/original_models/m45_coeff.csv ~/Desktop/original_models/m48_coeff.csv ~/Desktop/original_models/m66_coeff.csv ~/Desktop/original_models/m67_coeff.csv ~/Desktop/original_models/m96_coeff.csv ~/Desktop/original_models/m97_coeff.csv ~/Desktop/original_models/m98_coeff.csv -exo ~/Desktop/original_models/projection.csv -hist ~/Desktop/original_models/merged_v2.csv -start 2009 -end 2020 -conc 100 -out ~/Desktop/original_models/results.csv -lvl_name intensity
