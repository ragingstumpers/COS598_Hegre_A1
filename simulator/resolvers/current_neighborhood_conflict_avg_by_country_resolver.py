from defs import ResolverBase, VariableEnum
from typing import Any


class CurrentNeighborhoodConflictAvgByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_neighborhood_conflict_avg_by_country
    dependencies = [VariableEnum.country_to_neighbors, VariableEnum.tentative_conflict_value_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, float]:
        country_to_neighbors = current_values[VariableEnum.country_to_neighbors]
        tentative_conflict_by_country = current_values[VariableEnum.tentative_conflict_value_by_country]
        current_conflict_neighbor_averages_by_country = {}
        for country in tentative_conflict_by_country.keys():
            neighbors = country_to_neighbors[country]
            current_conflict_neighbor_averages_by_country[country] = (sum((current_conflict_neighbor_averages_by_country[neighbor] for neighbor in neighbors))*1.0) / len(neighbors)
        return current_conflict_neighbor_averages_by_country
