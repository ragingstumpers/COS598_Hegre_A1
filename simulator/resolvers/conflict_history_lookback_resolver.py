from defs import ResolverBase, VariableEnum
from typing import Any

class ConflictHistoryLookbackResolver(ResolverBase[int]):

    variable = VariableEnum.conflict_history_lookback
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> int:
        return current_values[VariableEnum.conflict_history_lookback]
