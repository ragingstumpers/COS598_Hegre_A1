from defs import ResolverBase, VariableEnum
from typing import Any
from .resolution_utils import draw_result_from_probability_matrix, compute_logistic_probability


class CurrentConflictLevelByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_conflict_level_by_country
    dependencies = [
        VariableEnum.conflict_exponent_minor_by_country,
        VariableEnum.conflict_exponent_major_by_country
    ]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        conflict_level_by_country = {}
        minor_exps_by_country = current_values[VariableEnum.conflict_exponent_minor_by_country]
        major_exps_by_country = current_values[VariableEnum.conflict_exponent_minor_by_country]
        for country in current_values[VariableEnum.conflict_exponent_minor_by_country]:
            result_to_exponent = {
                0: 0,
                1: minor_exps_by_country[country],
                2: major_exps_by_country[country],
            }
            transition_probability_matrix = compute_logistic_probability(result_to_exponent)
            conflict_level = draw_result_from_probability_matrix(transition_probability_matrix)
            conflict_level_by_country[country] = conflict_level
        return conflict_level_by_country
