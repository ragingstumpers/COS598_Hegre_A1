
from defs import ResolverBase, VariableEnum
import numpy
from typing import Any


class DrawnCoefficientMinorByVariableResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.drawn_coefficients_minor_by_variable
    dependencies = [VariableEnum.average_coefficients_minor_by_variable, VariableEnum.covariance_matrix_minor_by_variable]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[VariableEnum, float]:
        avg_coeffs_by_variable = current_values[VariableEnum.average_coefficients_minor_by_variable]
        covariance_matrix_by_variable = current_values[VariableEnum.covariance_matrix_minor_by_variable]

        variable_list = list(avg_coeffs_by_variable.keys())

        avg_coeffs_list = [
            avg_coeffs_by_variable[var]
            for var in variable_list
        ]

        covariance_matrix = [
            [
                covariance_matrix_by_variable[row][col]
                for col in variable_list
            ]
            for row in variable_list
        ]
        
        coeffs = numpy.random.default_rng().multivariate_normal(avg_coeffs_list, covariance_matrix)
        return {
            var: coeffs[i]
            for i, var in enumerate(variable_list)
        }
