from defs import COUNTRY_TO_NEIGHBORS, ResolverBase, VariableEnum
from typing import Any


class CurrentNeighborhoodIMRAvgByCountryResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.current_neighborhood_imr_avg_by_country
    dependencies = [VariableEnum.current_imr_level_by_country]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        current_imr_by_country = current_values[VariableEnum.current_imr_level_by_country]
        current_imr_neighbor_averages_by_country = {}
        for country in current_imr_by_country.keys():
            neighbors = COUNTRY_TO_NEIGHBORS[country]
            current_imr_neighbor_averages_by_country[country] = (sum((current_imr_by_country[neighbor] for neighbor in neighbors))*1.0) / len(neighbors)
        return current_imr_neighbor_averages_by_country
