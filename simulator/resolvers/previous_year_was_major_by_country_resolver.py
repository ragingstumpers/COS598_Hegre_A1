from defs import ResolverBase, VariableEnum
from typing import Any


class PreviousYearWasMajorByCountryResolver(ResolverBase[dict[str, int]]):

    variable = VariableEnum.previous_year_was_major_by_country
    dependencies = [VariableEnum.previous_year_conflict_level_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        prev_conflict_level_by_country = current_values[VariableEnum.previous_year_conflict_level_by_country]
        return {
            country: 1 if level == 1 else 0
            for country, level in prev_conflict_level_by_country.items()
        }
