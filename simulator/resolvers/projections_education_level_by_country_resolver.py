from defs import ResolverBase, VariableEnum
from typing import Any


class ProjectionsEducationLevelByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.projections_education_level_by_country
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        return current_values[VariableEnum.projections_education_level_by_country]
