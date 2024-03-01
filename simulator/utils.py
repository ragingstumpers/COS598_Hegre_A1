from collections import defaultdict
import csv
import defs
import random
from typing import Any, Type, TypeVar

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
    ) -> set[defs.VariableEnum]:
    return {
        var
        for var, deps in dependency_registry.items()
        if not deps
    }


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




def _get_sym_psd_matrix(num_entries: int) -> list[list[float]]:
    import numpy as np
    A = np.random.rand(num_entries, num_entries)
    B = np.dot(A, A.transpose())
    return B

def _sample_covariance_matrix(cov_matrix_necessary_variables: set[defs.VariableEnum]) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    num_entries = len(cov_matrix_necessary_variables)
    sym_psd_matrix = _get_sym_psd_matrix(num_entries)
    index_to_variable = {
        i: var
        for i, var in enumerate(cov_matrix_necessary_variables)
    }
    return {
        index_to_variable[row]: {
            index_to_variable[col]: sym_psd_matrix[row][col] / 10.0
            for col in range(num_entries)
        }
        for row in range(num_entries)
    }


def _extract_possible_varname(raw_possible_varname: str) -> str:
    return raw_possible_varname.split('.')[-1].split(':')[-1]


def _process_covariance_matrix_csv(filepath: str, name_map: dict[str, defs.VariableEnum]) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    with open(filepath, newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        cov = {}
        name_values_set = set(name_map.values())
        for row in reader:
            row_iter = iter(row.items())
            _, raw_possible_row_varname = next(row_iter)
            possible_row_varname = _extract_possible_varname(raw_possible_row_varname)
            if possible_row_varname not in name_map:
                continue
            row_variable = name_map[possible_row_varname]
            cur_row_map = {}
            cov[row_variable] = cur_row_map
            for raw_possible_col_varname, val in row_iter:
                # there were leading : or . at times, therefore remove them
                possible_col_varname =_extract_possible_varname(raw_possible_col_varname)
                if possible_col_varname in name_map:
                    cur_row_map[name_map[possible_col_varname]] = val
            assert(set(cur_row_map) == name_values_set)
        # SHOULD PROBABLY ADD A CHECK THAT IT IS PSD
        assert(set(cov) == name_values_set)
        return cov

def process_major_covariance_matrix_csv(filepath: str) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    # return _sample_covariance_matrix(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR.values()))
    return _process_covariance_matrix_csv(filepath, defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR)

def process_minor_covariance_matrix_csv(filepath: str) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    # return _sample_covariance_matrix(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR.values()))
    return _process_covariance_matrix_csv(filepath, defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR)




def _sample_coefficients(coeffs_necessary_variables: set[defs.VariableEnum]) -> dict[defs.VariableEnum, float]:
    return {
        var: random.random()*2*(-1 if random.random() < 0.2 else 1)
        for var in coeffs_necessary_variables
    }


def _process_coeffs_matrix_csv(filepath: str, name_map: dict[str, defs.VariableEnum]) ->  dict[defs.VariableEnum, float]:
    with open(filepath, newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        reader_iter = iter(reader)
        row = next(reader_iter)
        try:
            next(reader_iter)
            raise Exception("There should only be one row in the coeffs csv")
        except StopIteration:
            pass
        coeffs = {}
        for raw_possible_varname, val in row.items():
            # there were leading : or . at times, therefore remove them
            possible_varname = _extract_possible_varname(raw_possible_varname)
            if possible_varname in name_map:
                coeffs[name_map[possible_varname]] = val
        assert(set(coeffs) == set(name_map.values()))
        return coeffs


def process_major_coeffs_matrix_csv(filepath: str) ->  dict[defs.VariableEnum, float]:
    # return _sample_coefficients(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR.values()))
    return _process_coeffs_matrix_csv(filepath, defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR)

def process_minor_coeffs_matrix_csv(filepath: str) ->  dict[defs.VariableEnum, float]:
    # return _sample_coefficients(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR.values()))
    return _process_coeffs_matrix_csv(filepath, defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR)



_SAMPLE_COUNTRIES = {
    'USA',
    'CANADA',
    'MEXICO'
}


def _sample_neighbors() -> dict[str, list[str]]:
    return {
        country: []
        for country in _SAMPLE_COUNTRIES
    }

def _process_neighbor_countries_csv(filepath: str) -> dict[str, list[str]]:
    country_to_region = _process_region_by_country(filepath)
    region_to_countries_set = defaultdict(lambda: set)
    for country, region in country_to_region.items():
        region_to_countries_set[region].add(country)
    return {
        country: list(countries - {country})
        for countries in region_to_countries_set.values()
        for country in countries
    }


def process_neighbor_countries_csv(filepath: str) -> dict[str, list[str]]:
    # return _sample_neighbors()
    return _process_neighbor_countries_csv(filepath)




def _sample_regions() -> dict[defs.VariableEnum, dict[str, int]]:
    return {
        var: {
            country: 0
            for country in _SAMPLE_COUNTRIES
        }
        for var in defs.REGION_NECESSARY_VARIABLES
    }

def _process_region_by_country(filepath: str) -> dict[str, int]:
    with open(filepath, newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        region_by_country = {}
        for row in reader:
            country = row['statename']
            region = _convert_type_with_default(row['region'], int, 0)
            region_by_country[country] = region

        return region_by_country

def _process_regional_information_csv(filepath: str) -> dict[defs.VariableEnum, dict[str, float]]:
    country_to_region = _process_region_by_country(filepath)
    return {
        var: {
            country: processor(region)
        }
       for country, region in country_to_region.items()
       for var, processor in defs.REGION_NECESSARY_VARIABLES_PROCESSORS
    }


def process_regional_information_csv(filepath: str) -> dict[defs.VariableEnum, dict[str, int]]:
    # return _sample_regions()
    return _process_regional_information_csv(filepath)





def _convert_type_with_default(raw: str, convert_to: Type[S], default: S) -> S:
    try:
        return convert_to(raw)
    except Exception:
        return default


def _process_exogenous_projections_csv(start_year: int, end_year: int, filepath: str, name_map: dict[str, defs.VariableEnum]) -> dict[defs.VariableEnum, dict[int, dict[str, Any]]]:
    with open(filepath, newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        # {Variable: {Year: {Country: Val}}}
        proj_by_var_by_year_by_country = defaultdict(lambda: defaultdict(lambda: {}))
        for row in reader:
            year = int(row['year'])
            if year < start_year or year > end_year:
                continue
            country = row['statename']
            for raw_possible_varname, val in row.items():
                # there were leading : or . at times, therefore remove them
                possible_varname =_extract_possible_varname(raw_possible_varname)
                if possible_varname in name_map:
                    variable = name_map[possible_varname]
                    proj_by_var_by_year_by_country[variable][year][country] = _convert_type_with_default(val, float, 0.0)

        assert(set(proj_by_var_by_year_by_country) == set(name_map.values()))
        return proj_by_var_by_year_by_country

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
    # values_by_variable_by_year_by_country = _sample_exo(start_year, end_year)
    values_by_variable_by_year_by_country = _process_exogenous_projections_csv(start_year, end_year, filepath, defs.MAP_EXOGENOUS_PROJECTIONS_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS)
    for years_to_values_by_country in values_by_variable_by_year_by_country.values():
        assert start_year == min(years_to_values_by_country)
        assert end_year == max(years_to_values_by_country)
    return values_by_variable_by_year_by_country




def _sample_non_projected() -> dict[defs.VariableEnum, dict[str, float]]:
    return {
        var: {
            country: random.choice([0,0,0,0,0,1,1,2])
            for country in _SAMPLE_COUNTRIES
        }
        for var in defs.NON_PROJECTED_NECESSARY_VARIABLES
    }

def _process_conflict_history_by_country_csv(start_year: int, filepath: str) -> dict[str, list[int]]:
    with open(filepath, newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        # {Variable: {Year: {Country: Val}}}
        conflict_level_history_by_country = defaultdict(lambda: [])
        for row in reader:
            year = int(row['year'])
            if year >= start_year:
                continue
            country = row['statename']
            # CHECK WITH FUMIYA WHAT THE KEY SHOULD BE
            conflict_level = _convert_type_with_default(row['conflict'], int, 0)
            conflict_level_history_by_country[country].append(conflict_level)

        return conflict_level_history_by_country

def _process_non_projected_base_variables_csv(start_year: int, filepath: str) -> dict[defs.VariableEnum, dict[str, float]]:
    conflict_history_by_country = _process_conflict_history_by_country_csv(start_year, filepath)
    return {
        var: {
            country: processor(history)
        }
       for country, history in conflict_history_by_country.items()
       for var, processor in defs.NON_PROJECTED_NECESSARY_VARIABLES_HISTORY_PROCESSORS
    }

def process_non_projected_base_variables_csv(start_year: int, filepath: str) -> dict[defs.VariableEnum, dict[str, dict[int, Any]]]:
    # return _sample_non_projected()
    return _process_non_projected_base_variables_csv(start_year, filepath)


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
    ) -> dict[defs.VariableEnum, Any]:

    assert start_year <= end_year
    return {
        defs.VariableEnum.covariance_matrix_minor_by_variable: process_minor_covariance_matrix_csv(minor_covariance_matrix_filepath),
        defs.VariableEnum.average_coefficients_minor_by_variable: process_minor_coeffs_matrix_csv(minor_coefficients_filepath),
        defs.VariableEnum.covariance_matrix_major_by_variable: process_major_covariance_matrix_csv(major_covariance_matrix_filepath),
        defs.VariableEnum.average_coefficients_major_by_variable: process_major_coeffs_matrix_csv(major_coefficients_filepath),
        **process_exogenous_projections_csv(start_year, end_year, exogenous_projections_filepath),
        **process_non_projected_base_variables_csv(start_year, country_init_filepath),
        **process_regional_information_csv(regions_filepath),
        defs.VariableEnum.country_to_neighbors: process_neighbor_countries_csv(neighbors_filepath),
        defs.VariableEnum.current_year: start_year,
        defs.VariableEnum.end_year: end_year,
        defs.VariableEnum.should_stop_simulation: end_year < start_year,
        defs.VariableEnum.minor_constant: 1,  # this is one since it will be multiplied by the coefficient drawn
        defs.VariableEnum.major_constant: 1,  # this is one since it will be multiplied by the coefficient drawn
    }
