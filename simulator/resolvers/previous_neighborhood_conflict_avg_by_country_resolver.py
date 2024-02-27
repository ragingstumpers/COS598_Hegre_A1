from defs import ResolverBase, VariableEnum
from typing import Any


class PreviousNeighborhoodConflictAvgByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.previous_neighborhood_conflict_avg_by_country
    dependencies = [VariableEnum.country_to_neighbors, VariableEnum.previous_year_conflict_level_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        country_to_neighbors = current_values[VariableEnum.country_to_neighbors]
        previous_conflict_by_country = current_values[VariableEnum.previous_year_conflict_level_by_country]
        previous_conflict_neighbor_averages_by_country = {}
        for country in previous_conflict_by_country.keys():
            neighbors = country_to_neighbors[country]
            previous_conflict_neighbor_averages_by_country[country] = (sum((previous_conflict_by_country[neighbor] for neighbor in neighbors))*1.0) / len(neighbors) if neighbors else 0
        return previous_conflict_neighbor_averages_by_country
