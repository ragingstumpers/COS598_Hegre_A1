import defs
import utils
from multiprocessing import Pool
# necessary to add all resolvers to registry for DAG
import resolvers
from typing import Any

# NEED TO ADD PREVIOUS CONFLICT LEVEL ENDOGENOUS, NEIGHBORING AVGS FOR EXOGENOUS AS ENDOGENOUS

class Simulator:

    def __init__(
            self, 
            # should make the matrix an array but too lazy to better parse stata data, copy and paste will be 2d array
            initial_base_variables: dict[defs.VariableEnum, Any],
            concurrent_simulations: int,
        ):
            self._initial_base_variables = initial_base_variables
            self._concurrent_simulations = concurrent_simulations

    def _simulate_years(
            self,
            _,
        ) -> dict[int, dict[str, int]]:
        # these cannot be shared by the entire class
        #return {1: {"USA": 1, "CANADA": 2}, 2: {"USA": 2, "CANADA": 3}, 3: {"USA": 3, "CANADA": 4}} if _%2 else {1: {"USA": 0, "CANADA": 1}, 2: {"USA": 1, "CANADA": 2}, 3: {"USA": 2, "CANADA": 3}}
        conflict_levels_by_year = {}
        current_base_values = self._initial_base_variables
        while not current_base_values.get(defs.VariableEnum.should_stop_simulation):
            updated_values = utils.resolve(
                defs.ResolverBase._resolver_registry,
                defs.ResolverBase._dependency_registry,
                current_base_values
            )
            print(updated_values)
            conflict_levels_by_year[current_base_values[defs.VariableEnum.current_year]] = updated_values[defs.VariableEnum.current_conflict_level_by_country]
            current_base_values = updated_values[defs.VariableEnum.next_base_values]
        return conflict_levels_by_year

    def run(self):
        # do some multiprocoessing shit
        with Pool(self._concurrent_simulations) as p:
            results = p.map(self._simulate_years, [_ for _ in range(self._concurrent_simulations)])
        return utils.majority_results(results)