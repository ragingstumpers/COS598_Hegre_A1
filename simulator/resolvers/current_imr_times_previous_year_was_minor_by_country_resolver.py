from defs import ResolverBase, VariableEnum
from typing import Any


class CurrentIMRTimesPreviousYearWasMinorByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_imr_times_previous_year_was_minor_by_country
    dependencies = [VariableEnum.current_imr_level_by_country, VariableEnum.previous_year_was_minor_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        current_imr_levels_by_country = current_values[VariableEnum.current_imr_level_by_country]
        previous_year_was_minor_by_country = current_values[VariableEnum.previous_year_was_minor_by_country]
        return {
            country: current_imr_levels_by_country[country] * previous_year_was_minor_by_country[country]
            for country in current_imr_levels_by_country.keys()
        }
