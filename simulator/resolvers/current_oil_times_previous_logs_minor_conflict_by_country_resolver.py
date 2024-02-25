from defs import ResolverBase, VariableEnum
from typing import Any


class CurrentOilTimesPreviousLogsMinorConflictByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_oil_times_previous_year_was_major_by_country
    dependencies = [VariableEnum.current_oil_level_by_country, VariableEnum.previous_logs_minor_conflict_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        current_oil_levels_by_country = current_values[VariableEnum.current_oil_level_by_country]
        previous_logs_minor_conflict_by_country = current_values[VariableEnum.previous_logs_minor_conflict_by_country]
        return {
            country: current_oil_levels_by_country[country] * previous_logs_minor_conflict_by_country[country]
            for country in current_oil_levels_by_country.keys()
        }
