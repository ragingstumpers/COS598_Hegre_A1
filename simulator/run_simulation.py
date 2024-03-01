import argparse
from defs import VariableEnum
from utils import create_initial_base_variables, write_results
from simulator import Simulator

def _main():
    sim_cli = argparse.ArgumentParser(description="A program to run conflict data simulations. See Hegre 2013")
    sim_cli.add_argument(
        "-cov", "--covariance_matrix",
        type=str, help="filepath to CSV file for entire covariance matrix", required=True,
    )
    sim_cli.add_argument(
        "-coeff", "--coefficients",
        type=str, help="filepath to CSV file for entire coefficients matrix", required=True,
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

    args = sim_cli.parse_args()
    initial_base_variables = create_initial_base_variables(
        args.covariance_matrix,
        args.coefficients,
        args.exogenous_projections,
        args.history,
        args.start_year,
        args.end_year,
    )

    sim = Simulator(initial_base_variables, args.concurrent_simulations)
    results = sim.run()
    write_results(args.output_destination, results)
    #print(len(results))
    #print(results)


if __name__ == '__main__':
   _main()