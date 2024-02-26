import defs
import math
import random
from typing import Any, TypeVar

S = TypeVar('S')

def draw_result_from_probability_matrix(
        transition_probabilities: dict[S, float],
    ) -> S:
    # dependency here is the transiation probability matrix
    rand_val = random.random()
    sampled_outcome = None
    previous = 0.0
    for outcome, transition_prob in transition_probabilities.items():
        current_prob = previous + transition_prob
        if rand_val < current_prob:
            sampled_outcome = outcome
            break
        previous = current_prob
    
    assert sampled_outcome is not None
    return sampled_outcome


def get_variable_values_for_specific_country(country: str, variables_by_country: dict[defs.VariableEnum, dict[str, Any]]) -> dict[defs.VariableEnum, Any]:
    return {
        var: values_for_all_countries[country]
        for var, values_for_all_countries in variables_by_country.items()
    }


def dot_product(d1: dict[defs.VariableEnum, S], d2: dict[defs.VariableEnum, S]) -> list[S]:
    return [
        v1*d2[var]
        for var, v1 in d1.values()
    ]

def compute_logistic_probability(outcome_to_exponents: dict[S, list[float]]) -> dict[S, float]:
    individual_exponentiated = {
        outcome: math.e**exponent
        for outcome, exponent in outcome_to_exponents.items()
    }
    denominator = sum((v for v in individual_exponentiated.values()))
    return {
        outcome: exponentiated / denominator
        for outcome, exponentiated in individual_exponentiated.items()
    }
