from defs import ResolverBase, VariableEnum
from typing import Any


class PreviousNeighborhoodConflictAvgTimesPreviousLogsNoConflictByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.previous_neighborhood_conflict_avg_times_previous_logs_no_conflict_by_country
    dependencies = [VariableEnum.previous_neighborhood_conflict_avg_by_country, VariableEnum.previous_logs_no_conflict_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        previous_neighborhood_conflict_avg_by_country = current_values[VariableEnum.previous_neighborhood_conflict_avg_by_country]
        previous_logs_no_conflict_by_country = current_values[VariableEnum.previous_logs_no_conflict_by_country]
        return {
            country: previous_neighborhood_conflict_avg_by_country[country] * previous_logs_no_conflict_by_country[country]
            for country in previous_neighborhood_conflict_avg_by_country.keys()
        }
