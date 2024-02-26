from defs import ResolverBase, VariableEnum
from typing import Any


class PreviousLogsMinorConflictByCountryResolver(ResolverBase[float]):

    variable = VariableEnum.previous_logs_minor_conflict_by_country
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> float:
        return current_values[VariableEnum.previous_logs_minor_conflict_by_country]
