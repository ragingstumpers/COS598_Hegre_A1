import defs
import math
import random
from typing import Any, TypeVar

S = TypeVar('S')

def draw_result_from_probability_matrix(
        transition_probabilities_by_outcome: dict[S, float],
    ) -> S:
    # dependency here is the transiation probability matrix
    #print(transition_probabilities_by_outcome)
    total_prob = sum((prob for prob in transition_probabilities_by_outcome.values()))
    #print(total_prob)
    # rounding issues can creep up, therefore not exactly one
    assert 1.0000001 > total_prob > 0.999999, f"total prob: {total_prob} does not sum to one"

    rand_val = random.random()
    sampled_outcome = None
    previous = 0.0
    for outcome, transition_prob in transition_probabilities_by_outcome.items():
        current_prob = previous + transition_prob
        if rand_val < current_prob:
            sampled_outcome = outcome
            break
        previous = current_prob
    
    assert sampled_outcome is not None
    return sampled_outcome

def get_variable_values_for_specific_country(country: str, variables_by_country: dict[defs.VariableEnum, Any]) -> dict[defs.VariableEnum, Any]:
    # should move the whitelist to a constant, do a set operation on the dict keys to make this more efficient
    return {
        var: values_for_all_countries[country]
        for var, values_for_all_countries in variables_by_country.items()
        if var in defs.COUNTRY_SPECIFIC_VARIABLES
    }


def dot_product(d1: dict[defs.VariableEnum, S], d2: dict[defs.VariableEnum, S]) -> S:
    assert(set(d1) == set(d2)), f"same keys not present in dot product:\n{set(d1).difference(set(d2))}\n{set(d2).difference(set(d1))}"
    #for var, el in d1.items():
    #    print(f"var: {var}        coeff: {el}           val: {d2[var]}\n")
    x = sum((
        v1*d2[var]
        for var, v1 in d1.items()
    ))
    #print(x)
    #raise Exception
    return x

def compute_logistic_probability(outcome_to_exponent: dict[S, list[float]]) -> dict[S, float]:
    #print(outcome_to_exponent)
    individual_exponentiated = {
        outcome: math.e**exponent
        for outcome, exponent in outcome_to_exponent.items()
    }
    #print(individual_exponentiated)
    denominator = sum((v for v in individual_exponentiated.values()))
    return {
        outcome: exponentiated / denominator
        for outcome, exponentiated in individual_exponentiated.items()
    }
