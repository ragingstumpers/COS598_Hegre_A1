from defs import ResolverBase, VariableEnum
from typing import Any

class ConflictLevelHistoryByCountryEarlierToLaterResolver(ResolverBase[dict[str, list[int]]]):

    variable = VariableEnum.conflict_level_history_by_country__earlier_to_later
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, list[int]]:
        return current_values[VariableEnum.conflict_level_history_by_country__earlier_to_later]
