
from defs import ResolverBase, VariableEnum
from typing import Any


class CovarianceMatrixMinorByVariableResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.covariance_matrix_minor_by_variable
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[VariableEnum, dict[VariableEnum, float]]:
        return current_values[VariableEnum.covariance_matrix_minor_by_variable]
