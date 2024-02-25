import defs
import utils
from typing import Any

# NEED TO ADD PREVIOUS CONFLICT LEVEL ENDOGENOUS, NEIGHBORING AVGS FOR EXOGENOUS AS ENDOGENOUS

class Simulator:

    def __init__(
            self, 
            # should make the matrix an array but too lazy to better parse stata data, copy and paste will be 2d array
            variable_names: list[str],
            avg_coefficients: list[float],
            covariance_matrix: list[list[float]],
            # maybe this should be oriented another way
            exogenous_variables_by_country: dict[str, list[float]],
            endogenous_variables_base: list[float],
            num_years: int=10,
            countries: set[str]=None,
            neighbors: set[str]=None,
        ):

            # add some asserts to ensure that all variables accounted for in covariance matrix
            # ensure enough exogenous variable data
            # ensure there is data for all countries passed in
            # ensure endogenous order unique
            # assert all variable names accounted for
        pass

    def _simulate_years(
            self,
            initial_base_values: dict[defs.VariableEnum, Any]
        ) -> dict[int, dict[str, int]]:
        # these cannot be shared by the entire class
        conflict_levels_by_year = {}
        current_base_values = initial_base_values
        while not current_base_values.get(defs.VariableEnum.should_stop_simulation):
            updated_values = utils.resolve(
                defs.ResolverBase._resolver_registry,
                defs.ResolverBase._dependency_registry,
                current_base_values
            )
            conflict_levels_by_year[current_base_values[defs.VariableEnum.current_year]] = updated_values[defs.VariableEnum.current_conflict_value_by_country]
            current_base_values = updated_values[defs.VariableEnum.next_base_values]
        return conflict_levels_by_year

    
    def run(self, concurrent_simulations=25):
        # do some multiprocoessing shit
        pass
          
