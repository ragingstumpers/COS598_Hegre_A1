from defs import ResolverBase, VariableEnum
from typing import Any


class MinorConstantResolver(ResolverBase[float]):

    variable = VariableEnum.minor_constant
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> float:
        return current_values[VariableEnum.minor_constant]
