from defs import ResolverBase, VariableEnum
from typing import Any


class CountryInWestAfricaByCountryResolver(ResolverBase[dict[str, int]]):

    variable = VariableEnum.country_in_west_africa_region_by_country
    dependencies = []

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> dict[str, int]:
        return current_values[VariableEnum.country_in_west_africa_region_by_country]
