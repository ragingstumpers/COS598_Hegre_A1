from defs import ResolverBase, VariableEnum
from typing import Any
from .resolution_utils import dot_product, get_variable_values_for_specific_country


class ConflictExponentMinorByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.conflict_exponent_minor_by_country
    dependencies = [
        VariableEnum.drawn_coefficients_minor_by_variable,

        # SHOULD PROBABLY DEFINE A NEW CONSTANT FOR THESE
        VariableEnum.previous_year_was_minor_by_country,
        VariableEnum.previous_year_was_major_by_country,
        VariableEnum.previous_logs_no_conflict_by_country,
        VariableEnum.previous_logs_minor_conflict_by_country,
        VariableEnum.projections_oil_level_by_country,
        VariableEnum.current_oil_level_by_country,
        VariableEnum.current_oil_times_previous_year_was_minor_by_country,
        VariableEnum.current_oil_times_previous_year_was_major_by_country,
        VariableEnum.current_oil_times_previous_logs_no_conflict_by_country,
        VariableEnum.projections_ethnic_dominance_all_years_by_country,
        VariableEnum.current_ethnic_dominance_projection_by_country,
        VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_minor_by_country,
        VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_major_by_country,
        VariableEnum.current_ethnic_dominance_projection_times_previous_logs_no_conflict_by_country,
        VariableEnum.projections_imr_level_by_country,
        VariableEnum.current_imr_level_by_country,
        VariableEnum.current_imr_times_previous_year_was_minor_by_country,
        VariableEnum.current_imr_times_previous_year_was_major_by_country,
        VariableEnum.current_imr_times_previous_logs_no_conflict_by_country,
        VariableEnum.projections_youth_level_by_country,
        VariableEnum.current_youth_level_by_country,
        VariableEnum.current_youth_times_previous_year_was_minor_by_country,
        VariableEnum.current_youth_times_previous_year_was_major_by_country,
        VariableEnum.current_youth_times_previous_logs_no_conflict_by_country,
        VariableEnum.projections_population_level_by_country,
        VariableEnum.current_population_level_by_country,
        VariableEnum.current_population_times_previous_year_was_minor_by_country,
        VariableEnum.current_population_times_previous_year_was_major_by_country,
        VariableEnum.current_population_times_previous_logs_no_conflict_by_country,
        VariableEnum.projections_education_level_by_country,
        VariableEnum.current_education_level_by_country,
        VariableEnum.current_education_times_previous_year_was_minor_by_country,
        VariableEnum.current_education_times_previous_year_was_major_by_country,
        VariableEnum.current_education_times_previous_logs_no_conflict_by_country,
        VariableEnum.current_neighborhood_imr_avg_by_country,
        VariableEnum.current_neighborhood_education_avg_by_country,
        VariableEnum.current_neighborhood_youth_avg_by_country,

        VariableEnum.previous_neighborhood_has_minor_conflict_by_country,
        VariableEnum.previous_neighborhood_has_minor_conflict_times_previous_year_was_minor_by_country,
        VariableEnum.previous_neighborhood_has_minor_conflict_times_previous_year_was_major_by_country,
        VariableEnum.previous_neighborhood_has_minor_conflict_times_previous_logs_no_conflict_by_country,
        
        VariableEnum.country_in_west_asia_north_africa_region_by_country,
        VariableEnum.country_in_west_africa_region_by_country,
        VariableEnum.country_in_south_africa_region_by_country,
        VariableEnum.minor_constant,
    ]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        minor_coeffs_by_variable = current_values[VariableEnum.drawn_coefficients_minor_by_variable]
        variables_by_country = {
            dep: current_values[dep]
            for dep in cls.dependencies
            if dep not in {
                VariableEnum.drawn_coefficients_minor_by_variable,
                }
        }
        exponents_by_country = {}
        for country in current_values[VariableEnum.previous_logs_minor_conflict_by_country].keys():
            tentative_variable_values = get_variable_values_for_specific_country(country, variables_by_country)
            # replacing the previous ones with the variable names expected since this is the tentative case
            variable_values = {}
            for var, val in tentative_variable_values.items():
                if 'previous_neighborhood_has_minor' in var.value:
                    var = VariableEnum(var.value.replace('previous_neighborhood_has_minor', 'previous_neighborhood_has'))
                variable_values[var] = val
            # need to remove the variables that are per country but are specific to each one
            minor_variable_values = {**variable_values, VariableEnum.minor_constant: current_values[VariableEnum.minor_constant]}
            exponents_by_country[country] = dot_product(minor_coeffs_by_variable, minor_variable_values)
        return exponents_by_country
