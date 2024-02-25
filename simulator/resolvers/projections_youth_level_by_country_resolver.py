from defs import ResolverBase, VariableEnum
from typing import Any


class ProjectionsYouthLevelByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.projections_youth_level_by_country
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        return current_values[VariableEnum.projections_youth_level_by_country]
