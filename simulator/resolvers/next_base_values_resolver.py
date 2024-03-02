from defs import ResolverBase, VariableEnum
from typing import Any


class NextBaseValuesResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.next_base_values
    dependencies = [
        VariableEnum.current_conflict_level_by_country,
        # ADD MORE, MOST OF THEM WILL MAP TO THEMSELVES, SOME OTHERS WONT

        VariableEnum.conflict_level_history_by_country__earlier_to_later,

        VariableEnum.projections_oil_level_by_country,
        VariableEnum.projections_ethnic_dominance_all_years_by_country,
        VariableEnum.projections_imr_level_by_country,
        VariableEnum.projections_youth_level_by_country,
        VariableEnum.projections_population_level_by_country,
        VariableEnum.projections_education_level_by_country,

        VariableEnum.current_year,
        VariableEnum.end_year,
        VariableEnum.should_stop_simulation,

        VariableEnum.minor_constant,
        VariableEnum.major_constant,
        VariableEnum.country_to_neighbors,

        VariableEnum.country_in_west_africa_region_by_country,
        VariableEnum.country_in_south_africa_region_by_country,
        VariableEnum.country_in_west_asia_north_africa_region_by_country,

        VariableEnum.average_coefficients_minor_by_variable,
        VariableEnum.covariance_matrix_minor_by_variable,
        VariableEnum.average_coefficients_major_by_variable,
        VariableEnum.covariance_matrix_major_by_variable,
    ]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> int:


        return {
            # update this
            VariableEnum.conflict_level_history_by_country__earlier_to_later: {
                country: history + [current_values[VariableEnum.current_conflict_level_by_country][country]]
                for country, history in current_values[VariableEnum.conflict_level_history_by_country__earlier_to_later].items()
            },

            VariableEnum.projections_oil_level_by_country: current_values[VariableEnum.projections_oil_level_by_country],
            VariableEnum.projections_ethnic_dominance_all_years_by_country: current_values[VariableEnum.projections_ethnic_dominance_all_years_by_country],
            VariableEnum.projections_imr_level_by_country: current_values[VariableEnum.projections_imr_level_by_country],
            VariableEnum.projections_youth_level_by_country: current_values[VariableEnum.projections_youth_level_by_country],
            VariableEnum.projections_population_level_by_country: current_values[VariableEnum.projections_population_level_by_country],
            VariableEnum.projections_education_level_by_country: current_values[VariableEnum.projections_education_level_by_country],

            VariableEnum.current_year: current_values[VariableEnum.current_year]+1,
            VariableEnum.end_year: current_values[VariableEnum.end_year],
            VariableEnum.should_stop_simulation: current_values[VariableEnum.should_stop_simulation],

            VariableEnum.minor_constant: current_values[VariableEnum.minor_constant],
            VariableEnum.major_constant: current_values[VariableEnum.major_constant],
            VariableEnum.country_to_neighbors: current_values[VariableEnum.country_to_neighbors],

            VariableEnum.country_in_west_africa_region_by_country: current_values[VariableEnum.country_in_west_africa_region_by_country],
            VariableEnum.country_in_south_africa_region_by_country: current_values[VariableEnum.country_in_south_africa_region_by_country],
            VariableEnum.country_in_west_asia_north_africa_region_by_country: current_values[VariableEnum.country_in_west_asia_north_africa_region_by_country],

            VariableEnum.average_coefficients_minor_by_variable: current_values[VariableEnum.average_coefficients_minor_by_variable],
            VariableEnum.covariance_matrix_minor_by_variable: current_values[VariableEnum.covariance_matrix_minor_by_variable],
            VariableEnum.average_coefficients_major_by_variable: current_values[VariableEnum.average_coefficients_major_by_variable],
            VariableEnum.covariance_matrix_major_by_variable: current_values[VariableEnum.covariance_matrix_major_by_variable],
        }
