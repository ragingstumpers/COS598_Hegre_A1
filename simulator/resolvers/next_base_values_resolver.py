from defs import ResolverBase, VariableEnum
from typing import Any


class NextBaseValuesResolver(ResolverBase[dict[str, float]]):

    variable = VariableEnum.next_base_values
    dependencies = [
        VariableEnum.current_conflict_value_by_country,
        # ADD MORE, MOST OF THEM WILL MAP TO THEMSELVES, SOME OTHERS WONT
    ]

    @classmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> int:
        return {
            VariableEnum.previous_year_conflict_level_by_country: current_values[VariableEnum.current_conflict_value_by_country],
            # AND SO ON
        }
