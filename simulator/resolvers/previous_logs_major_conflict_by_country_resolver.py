from defs import ResolverBase, VariableEnum
from typing import Any


class PreviousLogsMajorConflictByCountryResolver(ResolverBase[float]):

    variable = VariableEnum.previous_logs_major_conflict_by_country
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> float:
        return current_values[VariableEnum.previous_logs_major_conflict_by_country]
