from defs import MAJOR_COEFFICIENTS_NECESSARY_VARIABLES, MINOR_COEFFICIENTS_NECESSARY_VARIABLES, ResolverBase, VariableEnum
from typing import Any
from .resolution_utils import dot_product, draw_result_from_probability_matrix, get_variable_values_for_specific_country, compute_logistic_probability


class CurrentConflictLevelByCountryResolver(ResolverBase[dict[str, int]]):

    variable = VariableEnum.current_conflict_level_by_country
    dependencies = [
        VariableEnum.drawn_coefficients_minor_by_variable,
        VariableEnum.drawn_coefficients_major_by_variable
    ] + list(set(el for els in (MINOR_COEFFICIENTS_NECESSARY_VARIABLES, MAJOR_COEFFICIENTS_NECESSARY_VARIABLES) for el in els))

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        minor_coeffs_by_variable = current_values[VariableEnum.drawn_coefficients_minor_by_variable]
        major_coeffs_by_variable = current_values[VariableEnum.drawn_coefficients_minor_by_variable]
        variables_by_country = {
            dep: current_values[dep]
            for dep in cls.dependencies
            if dep not in (VariableEnum.drawn_coefficients_minor_by_variable, VariableEnum.drawn_coefficients_majorby_variable)
        }
        conflict_level_by_country = {}
        for country in current_values[VariableEnum.previous_logs_minor_conflict_by_country].keys():
            variable_values = get_variable_values_for_specific_country(country, variables_by_country)
            print(variable_values[VariableEnum.current_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country])
            minor_variable_values = {**variable_values, VariableEnum.constant: VariableEnum.minor_constant}
            major_variable_values = {**variable_values, VariableEnum.constant: VariableEnum.major_constant}
            minor_vals = dot_product(minor_coeffs_by_variable, minor_variable_values)
            major_vals = dot_product(major_coeffs_by_variable, major_variable_values)
            result_to_exponent = {
                0: 0,
                1: minor_vals,
                2: major_vals
            }
            transition_probability_matrix = compute_logistic_probability(result_to_exponent)
            conflict_level = draw_result_from_probability_matrix(transition_probability_matrix)
            conflict_level_by_country[country] = conflict_level
        return conflict_level_by_country
