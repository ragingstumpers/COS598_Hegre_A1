from collections import defaultdict
import defs
import random
from typing import Any, TypeVar

S = TypeVar('S')
T = TypeVar('T')


def compute_dag_order(
        dependency_registry: dict[defs.VariableEnum, list[defs.VariableEnum]]
    ) -> list[defs.VariableEnum]:
    stack = []
    order = []

    def _process_dependencies(dependencies):
        for dep_variable in dependencies:
            _process_variable(dep_variable)

    def _process_variable(variable_name):
        if variable_name in order:
            return
        if variable_name in stack:
            raise Exception("not a dag")
        stack.append(variable_name)
        _process_dependencies(dependency_registry[variable_name])
        assert stack.pop() == variable_name
        order.append(variable_name)

    for variable_name in dependency_registry.keys():
        _process_variable(variable_name)
    
    assert not stack
    assert len(order) == len(dependency_registry)
    return order


def compute_base_variables(
        dependency_registry: dict[defs.VariableEnum, list[defs.VariableEnum]]
    ) -> list[defs.VariableEnum]:
    [
        var
        for var, deps in dependency_registry.values()
        if not deps
    ]


def resolve(
        resolver_registry: dict[defs.VariableEnum, defs.ResolverBase],
        dependency_registry: dict[defs.VariableEnum, list[defs.VariableEnum]],
        base_values: dict[defs.VariableEnum, Any],
    ) -> dict[defs.VariableEnum, Any]:
    current_values = {**base_values}
    for variable in compute_dag_order(dependency_registry):
        resolver = resolver_registry[variable]
        current_values[variable] = resolver.resolve(current_values)
    return current_values


def majority_results(sim_results: list[dict[int, dict[str, int]]]) -> dict[int, dict[str, int]]:
    # {USA: {year: {1: #}}}
    country_to_year_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    # aggregage
    for sim_result in sim_results:
        for year, conflict_by_country in sim_result.items():
            for country, conflict_level in conflict_by_country.items():
                country_to_year_counts[country][year][conflict_level] += 1
    # choose maximal
    return {
        country: {
            year: max(conflict_counts.items(), key=lambda a: a[1])[0]
            for year, conflict_counts in conflict_counts_by_year.items()
        }
        for country, conflict_counts_by_year in country_to_year_counts.items()
    }




def _get_top_row_of_psd_matrix(num_entries: int) -> list[float]:
    import numpy as np
    A = np.random.rand(num_entries, num_entries)
    B = np.dot(A, A.transpose())
    return B[0]

def _sample_covariance_matrix(cov_matrix_necessary_variables: set[defs.VariableEnum]) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    top_row_psd = [x / 10.0 for x in _get_top_row_of_psd_matrix(len(cov_matrix_necessary_variables))]
    initial = {
        var: top_row_psd[i]
        for i, var in enumerate(cov_matrix_necessary_variables)
    }
    return {
        row: {
            col: initial[col]
            for col in sorted(initial, key=lambda x: x.value)
        }
        for row in sorted(initial, key=lambda x: x.value)
    }

def process_major_covariance_matrix_csv(filepath: str) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    return _sample_covariance_matrix(defs.MAJOR_COVARIANCE_MATRIX_NECESSARY_VARIABLES)

def process_minor_covariance_matrix_csv(filepath: str) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    return _sample_covariance_matrix(defs.MINOR_COVARIANCE_MATRIX_NECESSARY_VARIABLES)




def _sample_coefficients(coeffs_necessary_variables: set[defs.VariableEnum]) -> dict[defs.VariableEnum, float]:
    return {
        var: random.random()*2*(-1 if random.random() < 0.2 else 1)
        for var in coeffs_necessary_variables
    }

def process_major_coeffs_matrix_csv(filepath: str) ->  dict[defs.VariableEnum, float]:
    return _sample_coefficients(defs.MAJOR_COEFFICIENTS_NECESSARY_VARIABLES)

def process_minor_coeffs_matrix_csv(filepath: str) ->  dict[defs.VariableEnum, float]:
    return _sample_coefficients(defs.MINOR_COEFFICIENTS_NECESSARY_VARIABLES)


_SAMPLE_COUNTRIES = {
    'USA',
    'CANADA',
    'MEXICO'
}


def _sample_neighbors() -> dict[defs.VariableEnum, dict[str, list[str]]]:
    return {
        defs.VariableEnum.country_to_neighbors: {
            country: []
            for country in _SAMPLE_COUNTRIES
        }
    }

def process_neighbor_countries_csv(filepath: str) -> dict[defs.VariableEnum, dict[str, list[str]]]:
    return _sample_neighbors()





def _sample_regions() -> dict[defs.VariableEnum, dict[str, int]]:
    return {
        var: {
            country: 0
            for country in _SAMPLE_COUNTRIES
        }
        for var in defs.REGION_NECESSARY_VARIABLES
    }

def process_regional_information_csv(filepath: str) -> dict[defs.VariableEnum, dict[str, int]]:
    return _sample_regions()




def _sample_exo(start_year: int, end_year: int) -> dict[defs.VariableEnum, dict[int, dict[str, Any]]]:
    # should pass in start and end and validate that there is an entry for each in the projections
    return {
        var: {
            year: {
                country: random.random()*3
                for country in _SAMPLE_COUNTRIES
            }
            for year in range(start_year, end_year+1)
        }
        for var in defs.EXOGENOUS_PROJECTIONS_NECESSARY_VARIABLES
    }

def process_exogenous_projections_csv(start_year: int, end_year: int, filepath: str) -> dict[defs.VariableEnum, dict[int, dict[str, Any]]]:
    values_by_variable_by_year_by_country = _sample_exo(start_year, end_year)
    for years_to_values_by_country in values_by_variable_by_year_by_country.values():
        assert start_year == min(years_to_values_by_country)
        assert end_year == max(years_to_values_by_country)
    return values_by_variable_by_year_by_country




def _sample_non_projected() -> dict[defs.VariableEnum, dict[str, dict[int, Any]]]:
    return {
        var: {
            country: 2
            for country in _SAMPLE_COUNTRIES
        }
        for var in defs.NON_PROJECTED_NECESSARY_VARIABLES
    }

def process_non_projected_base_variables_csv(filepath: str) -> dict[defs.VariableEnum, dict[str, dict[int, Any]]]:
    return _sample_non_projected()


def create_initial_base_variables(
        minor_covariance_matrix_filepath: str,
        minor_coefficients_filepath: str,
        major_covariance_matrix_filepath: str,
        major_coefficients_filepath: str,
        exogenous_projections_filepath: str,
        country_init_filepath: str,
        start_year: int,
        end_year: int,
        regions_filepath: str,
        neighbors_filepath: str,
        minor_constant: float,
        major_constant: float,
    ) -> dict[defs.VariableEnum, Any]:

    assert start_year <= end_year
    return {
        defs.VariableEnum.covariance_matrix_minor_by_variable: process_minor_covariance_matrix_csv(minor_covariance_matrix_filepath),
        defs.VariableEnum.average_coefficients_minor_by_variable: process_minor_coeffs_matrix_csv(minor_coefficients_filepath),
        defs.VariableEnum.covariance_matrix_major_by_variable: process_major_covariance_matrix_csv(major_covariance_matrix_filepath),
        defs.VariableEnum.average_coefficients_major_by_variable: process_major_coeffs_matrix_csv(major_coefficients_filepath),
        **process_exogenous_projections_csv(start_year, end_year, exogenous_projections_filepath),
        **process_non_projected_base_variables_csv(country_init_filepath),
        **process_regional_information_csv(regions_filepath),
        **process_neighbor_countries_csv(neighbors_filepath),
        defs.VariableEnum.current_year: start_year,
        defs.VariableEnum.end_year: end_year,
        defs.VariableEnum.should_stop_simulation: end_year < start_year,
        defs.VariableEnum.minor_constant: minor_constant,
        defs.VariableEnum.major_constant: major_constant,
    }
