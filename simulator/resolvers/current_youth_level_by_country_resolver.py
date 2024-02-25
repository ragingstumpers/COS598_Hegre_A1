from defs import ResolverBase, VariableEnum
from typing import Any


class CurrentYouthLevelByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_youth_level_by_country
    dependencies = [VariableEnum.current_year, VariableEnum.projections_youth_level_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        projected_youth_level_by_country_for_year = current_values[VariableEnum.projections_youth_level_by_country][current_values[VariableEnum.current_year]]
        return {**projected_youth_level_by_country_for_year}
