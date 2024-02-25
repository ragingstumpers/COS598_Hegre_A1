from defs import ResolverBase, VariableEnum
from typing import Any


class CurrentYearResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_year
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> int:
        return current_values[VariableEnum.current_year]
