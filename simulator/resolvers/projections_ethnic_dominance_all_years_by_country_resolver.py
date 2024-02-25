from defs import ResolverBase, VariableEnum
from typing import Any


class ProjectionsEthnicDominanceAllYearsByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.projections_ethnic_dominance_all_years_by_country
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        return current_values[VariableEnum.projections_ethnic_dominance_all_years_by_country]
