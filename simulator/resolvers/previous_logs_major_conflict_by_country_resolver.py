from defs import ResolverBase, VariableEnum
from .resolution_utils import safe_log_previous_consecutive
from typing import Any


class PreviousLogsMajorConflictByCountryResolver(ResolverBase[float]):

    variable = VariableEnum.previous_logs_major_conflict_by_country
    dependencies = [VariableEnum.conflict_level_history_by_country__earlier_to_later]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> float:
        # currently ignoring this value as I think that is what is intended by the paper
        return {
            country: 0 #safe_log_previous_consecutive(2, history)
            for country, history in current_values[VariableEnum.conflict_level_history_by_country__earlier_to_later].items()
        }