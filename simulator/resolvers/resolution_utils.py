import defs
import random
from typing import TypeVar

S = TypeVar('S')

def draw_conflict_level_by_country(
        transition_probabilities_by_country: dict[str, list[list[float]]],
        previous_conflict_level_by_country: dict[str, int]
) -> dict[str, int]:
    # dependency here is the transiation probability matrix
    rand_val = random.random()
    conflict_level_by_country = {}
    for country in defs.COUNTRIES_TO_NEIGHBORS.keys():
        prev_conflict_level = previous_conflict_level_by_country[country]
        transition_probs = transition_probabilities_by_country[country][prev_conflict_level]
        previous = None
        current_conflict_level = None

        for conflict_level, transition_prob in enumerate(transition_probs):
            current_prob = previous + transition_prob
            if rand_val < current_prob:
                current_conflict_level = conflict_level
            previous = current_prob
        
        assert current_conflict_level is not None
        conflict_level_by_country[country] = current_conflict_level
    return conflict_level_by_country


def dot_product(d1: dict[defs.VariableEnum, S], d2: dict[defs.VariableEnum, S]) -> list[S]:
    return [
        v1*d2[var]
        for var, v1 in d1.values()
    ]
