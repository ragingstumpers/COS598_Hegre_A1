import argparse
from defs import VariableEnum
from utils import create_initial_base_variables
from simulator import Simulator

def _main():
    sim_cli = argparse.ArgumentParser(description="A program to run conflict data simulations. See Hegre 2013")
    sim_cli.add_argument(
        "-min_cov", "--minor_covariance_matrix",
        type=str, help="filepath to CSV file for minor outcome covariance matrix", required=True,
    )
    sim_cli.add_argument(
        "-min_coeff", "--minor_coefficients",
        type=str, help="filepath to CSV file for minor outcome coefficients matrix", required=True,
    )
    sim_cli.add_argument(
        "-maj_cov", "--major_covariance_matrix",
        type=str, help="filepath to CSV file for major outcome covariance matrix", required=True,
    )
    sim_cli.add_argument(
        "-maj_coeff", "--major_coefficients",
        type=str, help="filepath to CSV file for major outcome coefficients matrix", required=True,
    )
    sim_cli.add_argument(
        "-exo", "--exogenous_projections",
        type=str, help="filepath to CSV file for exogenous variable projections by country", required=True,
    )
    sim_cli.add_argument(
        "-init", "--country_init",
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
        "-r", "--regions",
        type=str, help="filepath to CSV file mapping country to regional information", required=True,
    )
    sim_cli.add_argument(
        "-n", "--neighbors",
        type=str, help="filepath to CSV file mapping country to its neighbors", required=True,
    )
    sim_cli.add_argument(
        "-conc", "--concurrent_simulations",
        type=int, help="the number of concurrent simulations to run and then choose majority", default=10,
    )

    args = sim_cli.parse_args()
    initial_base_variables = create_initial_base_variables(
        args.minor_covariance_matrix,
        args.minor_coefficients,
        args.major_covariance_matrix,
        args.major_coefficients,
        args.exogenous_projections,
        args.country_init,
        args.start_year,
        args.end_year,
        args.regions,
        args.neighbors,
    )

    sim = Simulator(initial_base_variables, args.concurrent_simulations)
    results = sim.run()
    print(results)


if __name__ == '__main__':
   _main()