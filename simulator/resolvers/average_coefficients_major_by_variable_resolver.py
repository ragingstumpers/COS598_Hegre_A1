from defs import ResolverBase, VariableEnum
from typing import Any


class AverageCoefficientsMajorByVariableResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.average_coefficients_major_by_variable
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[VariableEnum, float]:
        return current_values[VariableEnum.average_coefficients_major_by_variable]
