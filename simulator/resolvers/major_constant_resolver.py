from defs import ResolverBase, VariableEnum
from typing import Any


class MajorConstantResolver(ResolverBase[float]):

    variable = VariableEnum.major_constant
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> float:
        assert current_values[VariableEnum.major_constant] == 1, "constant value must be 1 to multiply by coefficient drawn"
        return current_values[VariableEnum.major_constant]
