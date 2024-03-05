from defs import ResolverBase, VariableEnum
from typing import Any

class PreviousYearConflictLevelByCountryResolver(ResolverBase[dict[str, int]]):

    variable = VariableEnum.previous_year_conflict_level_by_country
    dependencies = [VariableEnum.conflict_level_history_by_country__earlier_to_later, VariableEnum.conflict_history_lookback]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        lookback = current_values[VariableEnum.conflict_history_lookback]
        return {
            # we toggle btwn -1 and -2 due to uncertainty in definitions
            country: history[lookback]
            for country, history in current_values[VariableEnum.conflict_level_history_by_country__earlier_to_later].items()
        }
