from defs import MAJOR_COEFFICIENTS_NECESSARY_VARIABLES, MINOR_COEFFICIENTS_NECESSARY_VARIABLES, ResolverBase, VariableEnum
from typing import Any
from .resolution_utils import dot_product, draw_result_from_probability_matrix, get_variable_values_for_specific_country, compute_logistic_probability


class TentativeConflictValueByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.tentative_conflict_value_by_country
    dependencies = [
        VariableEnum.drawn_coefficients_minor_by_variable,
        VariableEnum.drawn_coefficients_major_by_variable,

        # SHOULD PROBABLY DEFINE A NEW CONSTANT FOR THESE
        VariableEnum.previous_year_was_minor_by_country,
        VariableEnum.previous_year_was_major_by_country,
        VariableEnum.previous_logs_no_conflict_by_country,
        VariableEnum.previous_logs_minor_conflict_by_country,
        VariableEnum.projections_oil_level_by_country,
        VariableEnum.current_oil_level_by_country,
        VariableEnum.current_oil_times_previous_year_was_minor_by_country,
        VariableEnum.current_oil_times_previous_year_was_major_by_country,
        VariableEnum.current_oil_times_previous_logs_minor_conflict_by_country,
        VariableEnum.projections_ethnic_dominance_all_years_by_country,
        VariableEnum.current_ethnic_dominance_projection_by_country,
        VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_minor_by_country,
        VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_major_by_country,
        VariableEnum.current_ethnic_dominance_projection_times_previous_logs_minor_conflict_by_country,
        VariableEnum.projections_imr_level_by_country,
        VariableEnum.current_imr_level_by_country,
        VariableEnum.current_imr_times_previous_year_was_minor_by_country,
        VariableEnum.current_imr_times_previous_year_was_major_by_country,
        VariableEnum.current_imr_times_previous_logs_minor_conflict_by_country,
        VariableEnum.projections_youth_level_by_country,
        VariableEnum.current_youth_level_by_country,
        VariableEnum.current_youth_times_previous_year_was_minor_by_country,
        VariableEnum.current_youth_times_previous_year_was_major_by_country,
        VariableEnum.current_youth_times_previous_logs_minor_conflict_by_country,
        VariableEnum.projections_population_level_by_country,
        VariableEnum.current_population_level_by_country,
        VariableEnum.current_population_times_previous_year_was_minor_by_country,
        VariableEnum.current_population_times_previous_year_was_major_by_country,
        VariableEnum.current_population_times_previous_logs_minor_conflict_by_country,
        VariableEnum.projections_education_level_by_country,
        VariableEnum.current_education_level_by_country,
        VariableEnum.current_education_times_previous_year_was_minor_by_country,
        VariableEnum.current_education_times_previous_year_was_major_by_country,
        VariableEnum.current_education_times_previous_logs_minor_conflict_by_country,
        VariableEnum.current_neighborhood_imr_avg_by_country,
        VariableEnum.current_neighborhood_education_avg_by_country,
        VariableEnum.current_neighborhood_youth_avg_by_country,

        VariableEnum.previous_neighborhood_conflict_avg_by_country,
        VariableEnum.previous_neighborhood_conflict_avg_times_previous_year_was_minor_by_country,
        VariableEnum.previous_neighborhood_conflict_avg_times_previous_year_was_major_by_country,
        VariableEnum.previous_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country,
        
        VariableEnum.country_in_west_asia_north_africa_region_by_country,
        VariableEnum.country_in_west_africa_region_by_country,
        VariableEnum.country_in_south_africa_region_by_country,
        VariableEnum.minor_constant,
        VariableEnum.major_constant,
    ]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        minor_coeffs_by_variable = current_values[VariableEnum.drawn_coefficients_minor_by_variable]
        major_coeffs_by_variable = current_values[VariableEnum.drawn_coefficients_major_by_variable]
        variables_by_country = {
            dep: current_values[dep]
            for dep in cls.dependencies
            if dep not in {
                VariableEnum.drawn_coefficients_minor_by_variable,
                VariableEnum.drawn_coefficients_major_by_variable,
                }
        }
        conflict_level_by_country = {}
        for country in current_values[VariableEnum.previous_logs_minor_conflict_by_country].keys():
            variable_values = get_variable_values_for_specific_country(country, variables_by_country)
            shared_overrides = {
                VariableEnum.current_neighborhood_conflict_avg_by_country: variable_values[VariableEnum.previous_neighborhood_conflict_avg_by_country],
                VariableEnum.current_neighborhood_conflict_avg_times_previous_year_was_minor_by_country: variable_values[VariableEnum.previous_neighborhood_conflict_avg_times_previous_year_was_minor_by_country],
                VariableEnum.current_neighborhood_conflict_avg_times_previous_year_was_major_by_country: variable_values[VariableEnum.previous_neighborhood_conflict_avg_times_previous_year_was_major_by_country],
                VariableEnum.current_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country: variable_values[VariableEnum.previous_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country],
            }
            minor_variable_values = {**variable_values, **shared_overrides, VariableEnum.minor_constant: current_values[VariableEnum.minor_constant]}
            major_variable_values = {**variable_values, **shared_overrides, VariableEnum.major_constant: current_values[VariableEnum.major_constant]}
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
