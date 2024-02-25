from defs import ResolverBase, VariableEnum
from typing import Any


class CurrentEthnicDominanceProjectionByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_ethnic_dominance_projection_by_country
    dependencies = [VariableEnum.current_year, VariableEnum.projections_ethnic_dominance_all_years_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        current_ethnic_dominance_projection_by_country = current_values[VariableEnum.projections_oil_level_by_country][current_values[VariableEnum.current_year]]
        return {**current_ethnic_dominance_projection_by_country}
