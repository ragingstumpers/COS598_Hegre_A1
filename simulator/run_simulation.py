import argparse
from collections import namedtuple
from defs import VariableEnum
from json import loads
from multiprocessing import Pool
from simulator import Simulator
from utils import average_models, create_initial_base_variables, majority_results_outer, write_results, write_ratio_results

_Args = namedtuple("_Args", "cov coeff exo hist start end lvl_name conc use_c1c2")

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
        args.lvl_name,
        args.use_c1c2,
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
    sim_cli.add_argument(
        "-use_c1c2", "--use_c1c2_instead_of_lc1lc2",
        type=str, help="true if should use c1/c2 in computing histories instead of lc1/lc2 (false)", required=True,
    )

    args = sim_cli.parse_args()
    assert(len(args.covariance_matrix) == len(args.coefficients)), "number of coeff files doesn't match covariance files"
    
    if args.use_c1c2_instead_of_lc1lc2 not in ('true', 'false', 'True', 'False'):
        raise Exception(f"value for use_c1c2_instead_of_lc1lc2: {args.use_c1c2_instead_of_lc1lc2}, is not in ('true', 'false', 'True', 'False')")

    use_c1c2_instead_of_lc1lc2 = loads(args.use_c1c2_instead_of_lc1lc2)

    args_list = [
        _Args(
            cov,
            coeff,
            args.exogenous_projections,
            args.history,
            args.start_year,
            args.end_year,
            args.conflict_level_name,
            args.concurrent_simulations,
            use_c1c2_instead_of_lc1lc2,
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

# python run_simulation.py -cov ~/Desktop/Results/conf_v4/c/VarCov/m23.csv ~/Desktop/Results/conf_v4/c/VarCov/m43.csv ~/Desktop/Results/conf_v4/c/VarCov/m45.csv ~/Desktop/Results/conf_v4/c/VarCov/m48.csv ~/Desktop/Results/conf_v4/c/VarCov/m66.csv ~/Desktop/Results/conf_v4/c/VarCov/m67.csv ~/Desktop/Results/conf_v4/c/VarCov/m96.csv ~/Desktop/Results/conf_v4/c/VarCov/m97.csv ~/Desktop/Results/conf_v4/c/VarCov/m98.csv -coeff ~/Desktop/Results/conf_v4/c/Coefs/m23.csv ~/Desktop/Results/conf_v4/c/Coefs/m43.csv ~/Desktop/Results/conf_v4/c/Coefs/m45.csv ~/Desktop/Results/conf_v4/c/Coefs/m48.csv ~/Desktop/Results/conf_v4/c/Coefs/m66.csv ~/Desktop/Results/conf_v4/c/Coefs/m67.csv ~/Desktop/Results/conf_v4/c/Coefs/m96.csv ~/Desktop/Results/conf_v4/c/Coefs/m97.csv ~/Desktop/Results/conf_v4/c/Coefs/m98.csv -exo ~/Desktop/Results/conf_v4/c/projection.csv -hist ~/Desktop/Results/conf_v4/c/merged_conflict_1970_2008.csv -start 2009 -end 2020 -conc 100 -out ~/Desktop/Results/conf_v4/c/results_conflict.csv -lvl_name conflict -use_c1c2 true
