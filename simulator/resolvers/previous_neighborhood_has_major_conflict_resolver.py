from defs import ResolverBase, VariableEnum
from typing import Any


class PreviousNeighborhoodHasMajorConflictResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.previous_neighborhood_has_major_conflict_by_country
    dependencies = [VariableEnum.country_to_neighbors, VariableEnum.previous_year_conflict_level_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        country_to_neighbors = current_values[VariableEnum.country_to_neighbors]
        previous_conflict_by_country = current_values[VariableEnum.previous_year_conflict_level_by_country]
        previous_neighborhood_has_major_conflict = {}
        for country in previous_conflict_by_country.keys():
            neighbors = country_to_neighbors[country]
            previous_neighborhood_has_major_conflict[country] = sum((1 if (previous_conflict_by_country[neighbor] > 0 and neighbor != country) else 0 for neighbor in neighbors))
        return previous_neighborhood_has_major_conflict
