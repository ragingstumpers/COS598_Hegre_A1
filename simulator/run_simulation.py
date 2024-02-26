import argparse
from utils import create_initial_base_variables
from simulator import Simulator

def _main():
    sim_cli = argparse.ArgumentParser(description="A program to run conflict data simulations. See Hegre 2013")
    sim_cli.add_argument(
        "-min_cov", "--minor_covariance_matrix",
        type=str, nargs=1, help="filepath to CSV file for minor outcome covariance matrix", required=True,
    )
    sim_cli.add_argument(
        "-min_coeff", "--minor_coefficients",
        type=str, nargs=1, help="filepath to CSV file for minor outcome coefficients matrix", required=True,
    )
    sim_cli.add_argument(
        "-maj_cov", "--major_covariance_matrix",
        type=str, nargs=1, help="filepath to CSV file for major outcome covariance matrix", required=True,
    )
    sim_cli.add_argument(
        "-maj_coeff", "--major_coefficients",
        type=str, nargs=1, help="filepath to CSV file for major outcome coefficients matrix", required=True,
    )
    sim_cli.add_argument(
        "-exo", "--exogenous_projections",
        type=str, nargs=1, help="filepath to CSV file for exogenous variable projections by country", required=True,
    )
    sim_cli.add_argument(
        "-init", "--country_init",
        type=str, nargs=1, help="filepath to CSV file for initializer variables for non-projected variables", required=True,
    )
    sim_cli.add_argument(
        "-start", "--start_year",
        type=IndentationError, nargs=1, help="Year to start the simulation", required=True,
    )
    sim_cli.add_argument(
        "-end", "--end_year",
        type=int, nargs=1, help="Year to end the simulation", required=True,
    )
    sim_cli.add_argument(
        "-r", "--regions",
        type=str, nargs=1, help="filepath to CSV file mapping country to regional information", required=True,
    )
    sim_cli.add_argument(
        "-n", "--neighbors",
        type=str, nargs=1, help="filepath to CSV file mapping country to its neighbors", required=True,
    )
    sim_cli.add_argument(
        "-min_c", "--minor_constant",
        type=float, nargs=1, help="the constant to be used in the minor case", required=True,
    )
    sim_cli.add_argument(
        "-maj_c", "--major_constant",
        type=float, nargs=1, help="the constant to be used in the major case", required=True,
    )
    sim_cli.add_argument(
        "-conc", "--concurrent_simulations",
        type=int, nargs=1, help="the number of concurrent simulations to run and then choose majority", default=10,
    )

    args = sim_cli.parse_args()
    initial_base_variables = create_initial_base_variables(
        args.min_cov,
        args.min_coeff,
        args.maj_cov,
        args.maj_coeff,
        args.exo,
        args.init,
        args.start,
        args.end,
        args.r,
        args.n,
        args.min_c,
        args.maj_c,
    )

    sim = Simulator(initial_base_variables, args.conc)
    results = sim.run()
    print(results)

# move this to run_simulator, make it a CLI
if __name__ == '__main__':
   _main()