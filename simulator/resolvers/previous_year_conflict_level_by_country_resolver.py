from defs import ResolverBase, VariableEnum
from typing import Any


class PreviousYearConflictLevelByCountryResolver(ResolverBase[dict[str, int]]):

    variable = VariableEnum.previous_year_conflict_level_by_country
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        return current_values[cls.variable]
