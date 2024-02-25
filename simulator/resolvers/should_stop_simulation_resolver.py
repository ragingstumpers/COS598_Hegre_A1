from defs import ResolverBase, VariableEnum
from typing import Any


class ShouldStopSimulationResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.should_stop_simulation
    dependencies = [VariableEnum.current_year, VariableEnum.end_year]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> int:
        return current_values[VariableEnum.end_year] <= current_values[VariableEnum.current_year]
