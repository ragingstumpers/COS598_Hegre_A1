from defs import ResolverBase, VariableEnum
from typing import Any
from utils import dot_product, draw_result_from_probability_matrix, get_variable_values_for_specific_country, compute_logistic_probability


class TentativeConflictValueByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.tentative_conflict_value_by_country
    dependencies = [
        VariableEnum.drawn_coefficients_minor_by_variable,
        VariableEnum.drawn_coefficients_majorby_variable,
        # AND SO ON FOR ALL OF THE VARIABLES THAT GO INTO THIS
        # THIS ONE HAS PREVIOUS NEIGHBOR AS ESTIMATES
        # will need to relabel the coefficients I think
        VariableEnum.previous_logs_minor_conflict_by_country
        ]

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
            minor_vals = dot_product(minor_coeffs_by_variable, variable_values)
            major_vals = dot_product(major_coeffs_by_variable, variable_values)
            result_to_exponent = {
                0: 0,
                1: minor_vals,
                2: major_vals
            }
            transition_probability_matrix = compute_logistic_probability(result_to_exponent)
            conflict_level = draw_result_from_probability_matrix(transition_probability_matrix)
            conflict_level_by_country[country] = conflict_level
        return conflict_level_by_country
