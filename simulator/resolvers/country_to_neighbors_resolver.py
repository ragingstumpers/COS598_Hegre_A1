from defs import ResolverBase, VariableEnum
from typing import Any


class CountryToNeighborsResolver(ResolverBase[dict[str, list[str]]]):

    variable = VariableEnum.country_to_neighbors
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, list[str]]:
        return current_values[VariableEnum.country_to_neighbors]
