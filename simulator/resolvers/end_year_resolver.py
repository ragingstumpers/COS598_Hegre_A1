from defs import ResolverBase, VariableEnum
from typing import Any


class EndYearResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.end_year
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> int:
        return current_values[VariableEnum.end_year]
