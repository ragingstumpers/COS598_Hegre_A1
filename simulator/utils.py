from collections import defaultdict
import csv
import defs
from functools import reduce
import numpy
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


def majority_results(sim_results: list[dict[int, dict[str, int]]]) -> dict[str, dict[int, int]]:
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


def average_sims(sim_results: list[dict[int, dict[str, int]]]) -> dict[str, dict[int, dict[int, float]]]:
    # {USA: {year: {1: #}}}
    country_to_year_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    # aggregage
    for sim_result in sim_results:
        for year, conflict_by_country in sim_result.items():
            for country, conflict_level in conflict_by_country.items():
                country_to_year_counts[country][year][conflict_level] += 1
    # choose maximal
    num_sims = len(sim_results)
    return {
        country: {
            year: {
                lvl: (count*1.0) / num_sims
                for lvl, count in conflict_counts.items()
            }
            for year, conflict_counts in conflict_counts_by_year.items()
        }
        for country, conflict_counts_by_year in country_to_year_counts.items()
    }



def _get_sym_psd_matrix(num_entries: int) -> list[list[float]]:
    A = numpy.random.rand(num_entries, num_entries)
    B = numpy.dot(A, A.transpose())
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

def _prefix_split_col(prefix: str, val: str) -> str:
    # they sometimes have weird shit added after what should be the prefix...
    if prefix not in val:
        return val
    return val.split(prefix)[-1].split('.')[-1]

def _prefix_split_row(prefix: str, val: str) -> str:
    # they sometimes have weird shit added after what should be the prefix...
    return val.split(prefix)[-1].split('.')[-1]


def _process_covariance_matrix_csv(filepath: str, prefix: str, begin_after: str, end_after: str, name_map: dict[str, defs.VariableEnum]) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    with open(filepath, mode="r", newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        cov = {}
        name_values_set = set(name_map.values())

        reader_iter = iter(reader)

        # get to beginning
        for row in reader_iter:
            if row[""] == begin_after:
                break
    
        for row in reader_iter:
            row_iter = iter(row.items())
            _, raw_possible_row_varname = next(row_iter)
            possible_row_varname = _prefix_split_row(prefix, raw_possible_row_varname)
            if possible_row_varname not in name_map:
                continue
            row_variable = name_map[possible_row_varname]
            cur_row_map = {}
            cov[row_variable] = cur_row_map
            for raw_possible_col_varname, val in row_iter:
                # there were leading : or . at times, therefore remove them
                possible_col_varname = _prefix_split_col(prefix, raw_possible_col_varname)
                if possible_col_varname in name_map:
                    assert name_map[possible_col_varname] not in cur_row_map
                    # print(f"{possible_row_varname} --- {possible_col_varname} ---- {float(val)} --------- {val}")
                    cur_row_map[name_map[possible_col_varname]] = float(val)
            assert(set(cur_row_map) == name_values_set), f"the two sets differ:    {set(cur_row_map).difference(name_values_set)}\n {name_values_set.difference(set(cur_row_map))}\n"
            # if we process the ending row, then terminate
            if row[""] == end_after:
                break

        # SHOULD PROBABLY ADD A CHECK THAT IT IS PSD
        # currently asserting that in the draw_cov/coeff file since construct the entire matrix there
        assert(set(cov) == name_values_set),  f"the two sets differ:    {set(cov).difference(name_values_set)}\n {name_values_set.difference(set(cov))}\n"
        return cov
    
def _process_covariance_matrix_csv_two(filepath: str, prefix: str, begin_after: str, end_after: str, name_map: dict[str, defs.VariableEnum]) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    if begin_after == "1":
        offset = 1
    else:
        offset = 2
    row_offset = 1 + 41*offset
    col_offset = 40*offset-1
    with open(filepath, mode="r", newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        cov = {}
        name_values_set = set(name_map.values())

        reader_iter = iter(reader)

        # get to beginning
        for _ in reader_iter:
            row_offset -= 1
            if row_offset == 0:
                break
        meow = []
        for i, row in enumerate(reader_iter):
            row_iter = iter(row.items())
            _, raw_possible_row_varname = next(row_iter)
            possible_row_varname = _prefix_split_row(prefix, raw_possible_row_varname)
            if possible_row_varname not in name_map:
                continue
            row_variable = name_map[possible_row_varname]
            cur_row_map = {}
            cov[row_variable] = cur_row_map
            for j, (raw_possible_col_varname, val) in enumerate(row_iter):
                if j < col_offset:
                    continue
                # there were leading : or . at times, therefore remove them
                possible_col_varname = _prefix_split_col(prefix, raw_possible_col_varname)
                if possible_col_varname in name_map:
                    #print(f"{possible_row_varname} --- {possible_col_varname} ---- {float(val)} --------- {val}")
                    cur_row_map[name_map[possible_col_varname]] = float(val)
            assert(set(cur_row_map) == name_values_set), f"the two sets differ:    {set(cur_row_map).difference(name_values_set)}\n {name_values_set.difference(set(cur_row_map))}\n"
            # if we process the ending row, then terminate
            if row[""] == end_after:
                break

        # SHOULD PROBABLY ADD A CHECK THAT IT IS PSD
        # currently asserting that in the draw_cov/coeff file since construct the entire matrix there
        assert(set(cov) == name_values_set),  f"the two sets differ:    {set(cov).difference(name_values_set)}\n {name_values_set.difference(set(cov))}\n"
        return cov

def process_major_covariance_matrix_csv(filepath: str) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    # return _sample_covariance_matrix(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR.values()))
    return _process_covariance_matrix_csv(filepath, "2:", "2", "_cons", defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR)

def process_minor_covariance_matrix_csv(filepath: str) -> dict[defs.VariableEnum, dict[defs.VariableEnum, float]]:
    # return _sample_covariance_matrix(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR.values()))
    return _process_covariance_matrix_csv(filepath, "1:", "1", "_cons", defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR)




def _sample_coefficients(coeffs_necessary_variables: set[defs.VariableEnum]) -> dict[defs.VariableEnum, float]:
    return {
        var: random.random()*2*(-1 if random.random() < 0.2 else 1)
        for var in coeffs_necessary_variables
    }


def _process_coeffs_matrix_csv(filepath: str, prefix: str, name_map: dict[str, defs.VariableEnum]) ->  dict[defs.VariableEnum, float]:
    with open(filepath, mode="r", newline='') as csv_file:
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
            possible_varname = _prefix_split_col(prefix, raw_possible_varname)
            if possible_varname in name_map:
                coeffs[name_map[possible_varname]] = float(val)
        assert(set(coeffs) == set(name_map.values())),  f"the two sets differ:    {set(coeffs).difference(set(name_map.values()))}\n {set(name_map.values()).difference(set(coeffs))}\n"
        return coeffs


def process_major_coeffs_matrix_csv(filepath: str) ->  dict[defs.VariableEnum, float]:
    # return _sample_coefficients(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR.values()))
    return _process_coeffs_matrix_csv(filepath, "2:", defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR)

def process_minor_coeffs_matrix_csv(filepath: str) ->  dict[defs.VariableEnum, float]:
    # return _sample_coefficients(set(defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR.values()))
    return _process_coeffs_matrix_csv(filepath, "1:", defs.MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR)



_SAMPLE_COUNTRIES = {
    'USA',
    'CANADA',
    'MEXICO'
}


def _sample_neighbors() -> tuple[dict[str, list[str]], set[str]]:
    return {
        country: []
        for country in _SAMPLE_COUNTRIES
    }, _SAMPLE_COUNTRIES

def _process_neighbor_countries_csv(filepath: str) -> tuple[dict[str, list[str]], set[str]]:
    country_to_region = _process_region_by_country(filepath)
    region_to_countries_set = defaultdict(set)
    for country, region in country_to_region.items():
        region_to_countries_set[region].add(country)
    return {
        country: list(countries)
        for countries in region_to_countries_set.values()
        for country in countries
    }, set(country_to_region)


def process_neighbor_countries_csv(filepath: str) -> tuple[dict[defs.VariableEnum, dict[str, list[str]]], set[str]]:
    # return _sample_neighbors()
    country_to_neighbors, countries = _process_neighbor_countries_csv(filepath)
    return {defs.VariableEnum.country_to_neighbors: country_to_neighbors}, countries




def _sample_regions() -> tuple[dict[defs.VariableEnum, dict[str, float]], set[str]]:
    return {
        var: {
            country: 0
            for country in _SAMPLE_COUNTRIES
        }
        for var in defs.REGION_NECESSARY_VARIABLES
    }, set(_SAMPLE_COUNTRIES)

def _process_region_by_country(filepath: str) -> dict[str, int]:
    with open(filepath, mode="r", newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        region_by_country = {}
        for i, row in enumerate(reader):
            country = row['statename']
            # the default means it has no region so it shouldnt be paired with any other country, so we ensure default is different for each
            region = _convert_type_with_default(row['region'], int, 100+i)
            region_by_country[country] = region

        return region_by_country

def _process_regional_information_csv(filepath: str) -> tuple[dict[defs.VariableEnum, dict[str, float]], set[str]]:
    country_to_region = _process_region_by_country(filepath)
    return {
        var: {
            country: processor(region)
            for country, region in country_to_region.items()
        }
       for var, processor in defs.REGION_NECESSARY_VARIABLES_PROCESSORS.items()
    }, set(country_to_region)


def process_regional_information_csv(filepath: str) -> tuple[dict[defs.VariableEnum, dict[str, float]], set[str]]:
    # return _sample_regions()
    return _process_regional_information_csv(filepath)





def _convert_type_with_default(raw: str, convert_to: Type[S], default: S) -> S:
    try:
        return convert_to(raw)
    except Exception:
        return default


def _process_exogenous_projections_csv(start_year: int, end_year: int, filepath: str, name_map: dict[str, defs.VariableEnum]) -> tuple[dict[defs.VariableEnum, dict[int, dict[str, Any]]], set[str]]:
    # had to change encoding for some reason
    with open(filepath, mode="r", newline='', encoding='mac_roman') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        all_countries = set()
        # {Variable: {Year: {Country: Val}}}
        proj_by_var_by_year_by_country = defaultdict(lambda: defaultdict(dict))
        for row in reader:
            country = row['statename']
            all_countries.add(country)
    
            year = int(row['year'])
            if year < start_year or year > end_year:
                continue

            for possible_varname, val in row.items():
                if possible_varname in name_map:
                    variable = name_map[possible_varname]
                    value = _convert_type_with_default(val, float, 0.0)
                    proj_by_var_by_year_by_country[variable][year][country] = value

        # ensure that all countries have something for the exo variables, defaulting to 0
        # actually, we should probably raise an error if there is no data for one of the countries...
        for var, proj_by_year_by_country in proj_by_var_by_year_by_country.items():
            for year, proj_by_country in proj_by_year_by_country.items():
                for country in all_countries:
                    if country not in proj_by_country:
                        raise AssertionError(f"Country: {country} does not have projections for variable: {var.value} for year: {year}")
                        # proj_by_country[country] = 0

        assert(set(proj_by_var_by_year_by_country) == set(name_map.values())), f"the two sets differ:    {set(proj_by_var_by_year_by_country).difference(set(name_map.values()))}\n {set(name_map.values()).difference(set(proj_by_var_by_year_by_country))}\n"
        return proj_by_var_by_year_by_country, all_countries

def _sample_exo(start_year: int, end_year: int) -> tuple[dict[defs.VariableEnum, dict[int, dict[str, Any]]], set[str]]:
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
    }, set(_SAMPLE_COUNTRIES)

def process_exogenous_projections_csv(start_year: int, end_year: int, filepath: str) -> tuple[dict[defs.VariableEnum, dict[int, dict[str, Any]]], set[str]]:
    # values_by_variable_by_year_by_country = _sample_exo(start_year, end_year)
    values_by_variable_by_year_by_country, all_countries = _process_exogenous_projections_csv(start_year, end_year, filepath, defs.MAP_EXOGENOUS_PROJECTIONS_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS)
    for years_to_values_by_country in values_by_variable_by_year_by_country.values():
        assert start_year == min(years_to_values_by_country)
        assert end_year == max(years_to_values_by_country)
    return values_by_variable_by_year_by_country, all_countries




def _sample_non_projected() -> tuple[dict[defs.VariableEnum, dict[str, float]], set[str]]:
    return {
        defs.VariableEnum.conflict_level_history_by_country__earlier_to_later: {
            country: [0]
            for country in _SAMPLE_COUNTRIES
        }
    }, set(_SAMPLE_COUNTRIES)

def _process_conflict_history_by_country_csv(start_year: int, filepath: str, conflict_level_name: str) -> dict[str, list[int]]:
    with open(filepath, mode="r", newline='') as csv_file:
        # first row is interpreted as keys
        reader = csv.DictReader(csv_file)
        # {Variable: {Year: {Country: Val}}}
        conflict_level_history_by_country = defaultdict(lambda: [])  # some countries do not have sufficient history, therefore we default to one non-war year
        for row in reader:
            country = row['statename']
            conflict_level_history_by_country[country]  # just done to instantiate in case no years apply
            
            year = int(row['year'])
            if year >= start_year:
                continue

            # CHECK WITH FUMIYA WHAT THE KEY SHOULD BE
            conflict_level = _convert_type_with_default(row[conflict_level_name], int, 0)
            conflict_level_history_by_country[country].append(conflict_level)

        return conflict_level_history_by_country

def _process_non_projected_base_variables_csv(start_year: int, filepath: str, conflict_level_name: str) -> tuple[dict[defs.VariableEnum, dict[str, int]], set[str]]:
    conflict_history_by_country = _process_conflict_history_by_country_csv(start_year, filepath, conflict_level_name)
    return {defs.VariableEnum.conflict_level_history_by_country__earlier_to_later: conflict_history_by_country}, set(conflict_history_by_country)

def process_non_projected_base_variables_csv(start_year: int, filepath: str, conflict_level_name: str) -> tuple[dict[defs.VariableEnum, dict[str, int]], set[str]]:
    # return _sample_non_projected()
    return _process_non_projected_base_variables_csv(start_year, filepath, conflict_level_name)




def majority_results_outer(mult_sim_results: list[dict[str, dict[int, int]]]) -> dict[str, dict[int, int]]:
    # {USA: {year: {1: #}}}
    country_to_year_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    # aggregage
    for sim_result in mult_sim_results:
        for country, conflict_by_year in sim_result.items():
            for year, conflict_level in conflict_by_year.items():
                country_to_year_counts[country][year][conflict_level] += 1
    # choose maximal
    return {
        country: {
            year: max(conflict_counts.items(), key=lambda a: a[1])[0]
            for year, conflict_counts in conflict_counts_by_year.items()
        }
        for country, conflict_counts_by_year in country_to_year_counts.items()
    }

def average_models(mult_sim_results: list[dict[str, dict[int, int]]]) -> dict[str, dict[int, dict[int, float]]]:
   # {USA: {year: {1: #}}}
    num_models = len(mult_sim_results)
    country_to_year_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    # aggregage
    for sim_result in mult_sim_results:
        for country, conflict_lvl_ratio_by_year in sim_result.items():
            for year, conflict_lvl_ratio in conflict_lvl_ratio_by_year.items():
                for lvl, ratio in conflict_lvl_ratio.items():
                    country_to_year_counts[country][year][lvl] += (ratio*1.0) / num_models
    # choose maximal
    return country_to_year_counts



def write_ratio_results(write_file: str, avg_results: dict[str, dict[int, dict[int, float]]]) -> None:
    with open(write_file, "w+") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["COUNTRY", "YEAR", "NONE", "MINOR", "MAJOR", "EITHER"])
        for country in sorted(avg_results):
            country_results_by_year = avg_results[country]
            for year in sorted(country_results_by_year, key=lambda year_string: int(year_string)):
                percentages_by_lvl = country_results_by_year[year]
                writer.writerow([country, year, percentages_by_lvl[0], percentages_by_lvl[1], percentages_by_lvl[2], percentages_by_lvl[1] + percentages_by_lvl[2]])


def write_results(write_file: str, maj_results: dict[str, dict[int, int]]) -> None:
    with open(write_file, "w+") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["COUNTRY", "YEAR", "CONFLICT LEVEL"])
        for country in sorted(maj_results):
            country_results_by_year = maj_results[country]
            for year in sorted(country_results_by_year, key=lambda year_string: int(year_string)):
                writer.writerow([country, year, country_results_by_year[year]])


def create_initial_base_variables(
        covariance_matrix_filepath: str,
        coefficients_filepath: str,
        exogenous_projections_filepath: str,
        history_filpath: str,
        start_year: int,
        end_year: int,
        conflict_level_name: str,
    ) -> dict[defs.VariableEnum, Any]:

    assert start_year <= end_year

    def _intersection_sets(*sets: list[set[S]]) -> set[S]:
        return reduce(lambda a, b: a.intersection(b), sets)

    exo, exo_countries = process_exogenous_projections_csv(start_year, end_year, exogenous_projections_filepath)
    non_proj, np_countries = process_non_projected_base_variables_csv(start_year, history_filpath, conflict_level_name)
    reg, reg_countries = process_regional_information_csv(history_filpath)
    neighbors, n_countries = process_neighbor_countries_csv(history_filpath)

    countries = _intersection_sets(exo_countries, np_countries, reg_countries, n_countries)

    def _exo_for_present_countries(exo: dict[defs.VariableEnum, dict[int, dict[str, Any]]]) -> dict[defs.VariableEnum, dict[int, dict[str, Any]]]:
        return {
            var: {
                year: {
                    country: val
                    for country, val in proj_by_country.items()
                    if country in countries
                }
                for year, proj_by_country in proj_by_year.items()
            }
            for var, proj_by_year in exo.items()
    }

    def _not_exo_for_present_countries(not_exo: dict[defs.VariableEnum, dict[str, Any]], val_is_countries_list: bool=False) -> dict[defs.VariableEnum, dict[str, Any]]:
        return {
            var: {
                country: val if not val_is_countries_list else [c for c in val if c in countries]
                for country, val in val_by_country.items()
                if country in countries
            }
            for var, val_by_country in not_exo.items()
        }



    return {
        defs.VariableEnum.covariance_matrix_minor_by_variable: process_minor_covariance_matrix_csv(covariance_matrix_filepath),
        defs.VariableEnum.average_coefficients_minor_by_variable: process_minor_coeffs_matrix_csv(coefficients_filepath),
        defs.VariableEnum.covariance_matrix_major_by_variable: process_major_covariance_matrix_csv(covariance_matrix_filepath),
        defs.VariableEnum.average_coefficients_major_by_variable: process_major_coeffs_matrix_csv(coefficients_filepath),
        **_exo_for_present_countries(exo),
        **_not_exo_for_present_countries(non_proj),
        **_not_exo_for_present_countries(reg),
        **_not_exo_for_present_countries(neighbors, val_is_countries_list=True),
        defs.VariableEnum.current_year: start_year,
        defs.VariableEnum.end_year: end_year,
        defs.VariableEnum.should_stop_simulation: end_year < start_year,
        defs.VariableEnum.minor_constant: 1,  # this is one since it will be multiplied by the coefficient drawn
        defs.VariableEnum.major_constant: 1,  # this is one since it will be multiplied by the coefficient drawn
    }
