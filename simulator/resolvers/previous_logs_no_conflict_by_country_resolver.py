from defs import ResolverBase, VariableEnum
from .resolution_utils import safe_log_previous_consecutive
from typing import Any


class PreviousLogsNoConflictByCountryResolver(ResolverBase[float]):

    variable = VariableEnum.previous_logs_no_conflict_by_country
    dependencies = [VariableEnum.conflict_level_history_by_country__earlier_to_later]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> float:
        return {
            country: safe_log_previous_consecutive(0, history)
            for country, history in current_values[VariableEnum.conflict_level_history_by_country__earlier_to_later].items()
        }