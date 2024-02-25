from defs import ResolverBase, VariableEnum
from typing import Any


class CurrentEthnicDominanceProjectionTimesPreviousYearWasMinorByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_minor_by_country
    dependencies = [VariableEnum.current_ethnic_dominance_projection_by_country, VariableEnum.previous_logs_minor_conflict_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        current_ethnic_dominance_projection_by_country = current_values[VariableEnum.current_ethnic_dominance_projection_by_country]
        previous_logs_minor_conflict_by_country = current_values[VariableEnum.previous_logs_minor_conflict_by_country]
        return {
            country: current_ethnic_dominance_projection_by_country[country] * previous_logs_minor_conflict_by_country[country]
            for country in current_ethnic_dominance_projection_by_country.keys()
        }
