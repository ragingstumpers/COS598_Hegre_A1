import abc
import defs
from enum import Enum
from functools import reduce
from multiprocessing import Pool
import numpy
import random
from typing import Any, Generic, Type, TypeVar, Union

S = TypeVar('S')
T = TypeVar('T')


# neighborhood conflict seems like the last weird one
class VariableEnum(Enum):

    # BASE, done
    previous_year_conflict_level_by_country = 'previous_year_conflict_level_by_country'
    # C1_{t-1} DERIVED done
    previous_year_was_minor_by_country = 'previous_year_was_minor_by_country'
    # C2_{t-1} DERIVEd done
    previous_year_was_major_by_country = 'previous_year_was_major_by_country'

    # ln(t_0) BASE done
    previous_logs_no_conflict_by_country = 'previous_logs_no_conflict_by_country'
    # ln(t_1) BASE done
    previous_logs_minor_conflict_by_country = 'previous_logs_minor_conflict_by_country'

    # Oil BASE done
    projections_oil_level_by_country = 'projections_oil_level_by_country'
    # Oil DERIVED done
    current_oil_level_by_country = 'current_oil_level_by_country'
    # Oil * C1_{t-1} DERIVED done
    current_oil_times_previous_year_was_minor_by_country = 'current_oil_times_previous_year_was_minor_by_country'
    # Oil * C2_{t-1} DERIVED done
    current_oil_times_previous_year_was_major_by_country = 'current_oil_times_previous_year_was_major_by_country'
    # Oil * ln(t_1) DERIVED done
    current_oil_times_previous_logs_minor_conflict_by_country = 'current_oil_times_previous_logs_minor_conflict_by_country'
    
    # Ethn. dom PROJ BASE done
    projections_ethnic_dominance_all_years_by_country = 'projections_ethnic_dominance_all_years_by_country'
    # Ethn. dom DERIVED done
    current_ethnic_dominance_projection_by_country = 'current_ethnic_dominance_projection_by_country'
    # Ethn. dom * C1_{t-1} DERIVED done
    current_ethnic_dominance_projection_times_previous_year_was_minor_by_country = 'current_ethnic_dominance_projection_times_previous_year_was_minor_by_country'
    # Ethn. dom * C2_{t-1} DERIVED done
    current_ethnic_dominance_projection_times_previous_year_was_major_by_country = 'current_ethnic_dominance_projection_times_previous_year_was_major_by_country'
    # Ethn. dom *ln(t_1) DERIVED done
    current_ethnic_dominance_projection_times_previous_logs_minor_conflict_by_country = 'current_ethnic_dominance_projection_times_previous_logs_minor_conflict_by_country'
    
    # IF HAVE TIME CHANGE VARNAME TO BE LN IN FRONT
    # IMR BASE done
    projections_imr_level_by_country = 'projections_imr_level_by_country'
    # IMR DERIVED done
    current_imr_level_by_country = 'current_imr_level_by_country'
    # IMR * C1_{t-1} DERIVED done
    current_imr_times_previous_year_was_minor_by_country = 'current_imr_times_previous_year_was_minor_by_country'
    # IMR * C2_{t-1} DERIVED done
    current_imr_times_previous_year_was_major_by_country = 'current_imr_times_previous_year_was_major_by_country'
    # IMR * ln(t_1) DERIVED done
    current_imr_times_previous_logs_minor_conflict_by_country = 'current_imr_times_previous_logs_minor_conflict_by_country'
    

    # YOUTH BASE done
    projections_youth_level_by_country = 'projections_youth_level_by_country'
    # YOUTH DERIVED done
    current_youth_level_by_country = 'current_youth_level_by_country'
    # YOUTH * C1_{t-1} DERIVED done
    current_youth_times_previous_year_was_minor_by_country = 'current_youth_times_previous_year_was_minor_by_country'
    # YOUTH * C2_{t-1} DERIVED done
    current_youth_times_previous_year_was_major_by_country = 'current_youth_times_previous_year_was_major_by_country'
    # YOUTH * ln(t_1) DERIVED done
    current_youth_times_previous_logs_minor_conflict_by_country = 'current_youth_times_previous_logs_minor_conflict_by_country'


    # POPULATION BASE done
    projections_population_level_by_country = 'projections_population_level_by_country'
    # POPULATION DERIVED done
    current_population_level_by_country = 'current_population_level_by_country'
    # POPULATION * C1_{t-1} DERIVED done
    current_population_times_previous_year_was_minor_by_country = 'current_population_times_previous_year_was_minor_by_country'
    # POPULATION * C2_{t-1} DERIVED done
    current_population_times_previous_year_was_major_by_country = 'current_population_times_previous_year_was_major_by_country'
    # POPULATION * ln(t_1) DERIVED done
    current_population_times_previous_logs_minor_conflict_by_country = 'current_population_times_previous_logs_minor_conflict_by_country'
    

    # EDUCATION BASE done
    projections_education_level_by_country = 'projections_education_level_by_country'
    # EDUCATION DERIVED done
    current_education_level_by_country = 'current_education_level_by_country'
    # EDUCATION * C1_{t-1} DERIVED done
    current_education_times_previous_year_was_minor_by_country = 'current_education_times_previous_year_was_minor_by_country'
    # EDUCATION * C2_{t-1} DERIVED done
    current_education_times_previous_year_was_major_by_country = 'current_education_times_previous_year_was_major_by_country'
    # EDUCATION * ln(t_1) DERIVED done
    current_education_times_previous_logs_minor_conflict_by_country = 'current_education_times_previous_logs_minor_conflict_by_country'
    

    # neighborhood IMR DERIVED done
    current_neighborhood_imr_avg_by_country = 'current_neighborhood_imr_avg_by_country'
     # neighborhood education DERIVED done
    current_neighborhood_education_avg_by_country = 'current_neighborhood_education_avg_by_country'
    # neighborhood youth DERIVED done
    current_neighborhood_youth_avg_by_country = 'current_neighborhood_youth_avg_by_country'

    # previous neighborhood youth DERIVED done
    previous_neighborhood_conflict_avg_by_country = 'previous_neighborhood_conflict_avg_by_country'
    # previous neighborhood youth * C1_{t-1} DERIVED done
    previous_neighborhood_conflict_avg_times_previous_year_was_minor_by_country = 'previous_neighborhood_conflict_avg_times_previous_year_was_minor_by_country'
    # previous neighborhood youth * C2_{t-1} DERIVED done
    previous_neighborhood_conflict_avg_times_previous_year_was_major_by_country = 'previous_neighborhood_conflict_avg_times_previous_year_was_major_by_country'
    # previous neighborhood youth * ln(t_1) DERIVED done
    previous_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country = 'previous_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country'
    # DERIVED done
    tentative_conflict_value_by_country = 'tentative_conflict_value_by_country'

    # current neighborhood youth DERIVED done
    current_neighborhood_conflict_avg_by_country = 'current_neighborhood_conflict_avg_by_country'
    # current neighborhood youth * C1_{t-1} DERIVED done
    current_neighborhood_conflict_avg_times_previous_year_was_minor_by_country = 'current_neighborhood_conflict_avg_times_previous_year_was_minor_by_country'
    # current neighborhood youth * C2_{t-1} DERIVED done
    current_neighborhood_conflict_avg_times_previous_year_was_major_by_country = 'current_neighborhood_conflict_avg_times_previous_year_was_major_by_country'
    # current neighborhood youth * ln(t_1) DERIVED done
    current_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country = 'current_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country'
    # DERIVED done
    current_conflict_value_by_country = 'current_conflict_value_by_country'

    # BASE done
    country_to_neighbors = 'country_to_neighbors'


    # country specific ones
    # BASE W Asia N Africa done
    country_in_west_asia_north_africa_region_by_country = 'country_in_west_asia_north_africa_region_by_country'
    # BASE w africa done
    country_in_west_africa_region_by_country = 'country_in_west_africa_region_by_country'
    # BASE s africa done
    country_in_south_africa_region_by_country = 'country_in_south_africa_region_by_country'

    # CONSTANT IDK WHAT THIS MEANS
    # BASE done
    minor_constant = 'minor_constant'
    # BASE done
    major_constant = 'major_constant'

    # not resolved, set as minor or major when computing, but necessary to define
    # done
    constant = 'constant'
    
    # BASE done
    current_year = 'current_year'


    # BASE done
    end_year = 'end_year'

    # BASE done
    average_coefficients_minor_by_variable = 'average_coefficients'
    # BASE done
    covariance_matrix_minor_by_variable = 'covariance_matrix'
    # DERIVED done
    drawn_coefficients_minor_by_variable = 'drawn_coefficients_by_variable'
    # BASE done
    average_coefficients_major_by_variable = 'average_coefficients'
    # BASE done
    covariance_matrix_major_by_variable = 'covariance_matrix'
    # DERIVED done
    drawn_coefficients_major_by_variable = 'drawn_coefficients_by_variable'

    # DERIVED BUT BASE done
    should_stop_simulaton = 'should_stop_simulation'


    # DERIVED done
    next_base_values = 'next_base_values'


MINOR_COEFFICIENTS_NECESSARY_VARIABLES = {
    VariableEnum.previous_year_was_minor_by_country,
    VariableEnum.previous_year_was_major_by_country,
    VariableEnum.previous_logs_no_conflict_by_country,
    VariableEnum.previous_logs_minor_conflict_by_country,
    VariableEnum.projections_oil_level_by_country,
    VariableEnum.current_oil_level_by_country,
    VariableEnum.current_oil_times_previous_year_was_minor_by_country,
    VariableEnum.current_oil_times_previous_year_was_major_by_country,
    VariableEnum.current_oil_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_ethnic_dominance_all_years_by_country,
    VariableEnum.current_ethnic_dominance_projection_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_minor_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_major_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_imr_level_by_country,
    VariableEnum.current_imr_level_by_country,
    VariableEnum.current_imr_times_previous_year_was_minor_by_country,
    VariableEnum.current_imr_times_previous_year_was_major_by_country,
    VariableEnum.current_imr_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_youth_level_by_country,
    VariableEnum.current_youth_level_by_country,
    VariableEnum.current_youth_times_previous_year_was_minor_by_country,
    VariableEnum.current_youth_times_previous_year_was_major_by_country,
    VariableEnum.current_youth_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_population_level_by_country,
    VariableEnum.current_population_level_by_country,
    VariableEnum.current_population_times_previous_year_was_minor_by_country,
    VariableEnum.current_population_times_previous_year_was_major_by_country,
    VariableEnum.current_population_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_education_level_by_country,
    VariableEnum.current_education_level_by_country,
    VariableEnum.current_education_times_previous_year_was_minor_by_country,
    VariableEnum.current_education_times_previous_year_was_major_by_country,
    VariableEnum.current_education_times_previous_logs_minor_conflict_by_country,
    VariableEnum.current_neighborhood_imr_avg_by_country,
    VariableEnum.current_neighborhood_education_avg_by_country,
    VariableEnum.current_neighborhood_youth_avg_by_country,
    VariableEnum.current_neighborhood_conflict_avg_by_country,
    VariableEnum.current_neighborhood_conflict_avg_times_previous_year_was_minor_by_country,
    VariableEnum.current_neighborhood_conflict_avg_times_previous_year_was_major_by_country,
    VariableEnum.current_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country,
    VariableEnum.country_in_west_asia_north_africa_region_by_country,
    VariableEnum.country_in_west_africa_region_by_country,
    VariableEnum.country_in_south_africa_region_by_country,
    VariableEnum.minor_constant,
}

MAJOR_COEFFICIENTS_NECESSARY_VARIABLES = {
    VariableEnum.previous_year_was_minor_by_country,
    VariableEnum.previous_year_was_major_by_country,
    VariableEnum.previous_logs_no_conflict_by_country,
    VariableEnum.previous_logs_minor_conflict_by_country,
    VariableEnum.projections_oil_level_by_country,
    VariableEnum.current_oil_level_by_country,
    VariableEnum.current_oil_times_previous_year_was_minor_by_country,
    VariableEnum.current_oil_times_previous_year_was_major_by_country,
    VariableEnum.current_oil_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_ethnic_dominance_all_years_by_country,
    VariableEnum.current_ethnic_dominance_projection_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_minor_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_major_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_imr_level_by_country,
    VariableEnum.current_imr_level_by_country,
    VariableEnum.current_imr_times_previous_year_was_minor_by_country,
    VariableEnum.current_imr_times_previous_year_was_major_by_country,
    VariableEnum.current_imr_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_youth_level_by_country,
    VariableEnum.current_youth_level_by_country,
    VariableEnum.current_youth_times_previous_year_was_minor_by_country,
    VariableEnum.current_youth_times_previous_year_was_major_by_country,
    VariableEnum.current_youth_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_population_level_by_country,
    VariableEnum.current_population_level_by_country,
    VariableEnum.current_population_times_previous_year_was_minor_by_country,
    VariableEnum.current_population_times_previous_year_was_major_by_country,
    VariableEnum.current_population_times_previous_logs_minor_conflict_by_country,
    VariableEnum.projections_education_level_by_country,
    VariableEnum.current_education_level_by_country,
    VariableEnum.current_education_times_previous_year_was_minor_by_country,
    VariableEnum.current_education_times_previous_year_was_major_by_country,
    VariableEnum.current_education_times_previous_logs_minor_conflict_by_country,
    VariableEnum.current_neighborhood_imr_avg_by_country,
    VariableEnum.current_neighborhood_education_avg_by_country,
    VariableEnum.current_neighborhood_youth_avg_by_country,
    VariableEnum.current_neighborhood_conflict_avg_by_country,
    VariableEnum.current_neighborhood_conflict_avg_times_previous_year_was_minor_by_country,
    VariableEnum.current_neighborhood_conflict_avg_times_previous_year_was_major_by_country,
    VariableEnum.current_neighborhood_conflict_avg_times_previous_logs_minor_conflict_by_country,
    VariableEnum.country_in_west_asia_north_africa_region_by_country,
    VariableEnum.country_in_west_africa_region_by_country,
    VariableEnum.country_in_south_africa_region_by_country,
    VariableEnum.major_constant,
}


MINOR_COVARIANCE_MATRIX_NECESSARY_VARIABLES = MINOR_COEFFICIENTS_NECESSARY_VARIABLES
MAJOR_COVARIANCE_MATRIX_NECESSARY_VARIABLES = MAJOR_COEFFICIENTS_NECESSARY_VARIABLES


EXOGENOUS_PROJECTIONS_NECESSARY_VARIABLES = {
    VariableEnum.projections_oil_level_by_country,
    VariableEnum.projections_ethnic_dominance_all_years_by_country,
    VariableEnum.projections_imr_level_by_country,
    VariableEnum.projections_youth_level_by_country,
    VariableEnum.projections_population_level_by_country,
    VariableEnum.projections_education_level_by_country,
}


NON_PROJECTED_NECESSARY_VARIABLES = {
    VariableEnum.previous_year_conflict_level_by_country,
    VariableEnum.previous_year_was_minor_by_country,
    VariableEnum.previous_year_was_major_by_country,
    VariableEnum.previous_logs_no_conflict_by_country,
    VariableEnum.previous_logs_minor_conflict_by_country,
}

NEIGHBOR_NECESSARY_BASE_VARIABLES = {
    VariableEnum.country_to_neighbors,
}

REGION_NECESSARY_VARIABLES = {
    VariableEnum.country_in_west_asia_north_africa_region_by_country,
    VariableEnum.country_in_west_africa_region_by_country,
    VariableEnum.country_in_south_africa_region_by_country,
}

CONSTANTS_NECESSARY_VARIABLES = {
    VariableEnum.minor_constant,
    VariableEnum.major_constant,
}

BASE_VARIABLES = {
    VariableEnum.previous_year_conflict_level_by_country,
    VariableEnum.previous_logs_no_conflict_by_country,
    VariableEnum.previous_logs_minor_conflict_by_country,

    VariableEnum.projections_oil_level_by_country,
    VariableEnum.projections_ethnic_dominance_all_years_by_country,
    VariableEnum.projections_imr_level_by_country,
    VariableEnum.projections_youth_level_by_country,
    VariableEnum.projections_population_level_by_country,
    VariableEnum.projections_education_level_by_country,

    VariableEnum.current_year,
    VariableEnum.end_year,

    VariableEnum.minor_constant,
    VariableEnum.major_constant,
    VariableEnum.country_to_neighbors,

    VariableEnum.country_in_west_africa_region_by_country,
    VariableEnum.country_in_south_africa_region_by_country,
    VariableEnum.country_in_west_asia_north_africa_region_by_country,

    VariableEnum.average_coefficients_minor_by_variable,
    VariableEnum.covariance_matrix_minor_by_variable,
    VariableEnum.average_coefficients_major_by_variable,
    VariableEnum.covariance_matrix_major_by_variable,
}


class ResolverMeta(type):
    def __init__(mycls, name, bases, attrs):
        if name != 'GenericResolverMeta':
            if 'resolver_registry' not in attrs:
                attrs['_resolver_registry'] = {}

            if 'dependency_registry' not in attrs:
                attrs['_dependency_registry'] = {}

            if name != 'ResolverBase':
                attrs['_resolver_registry'][attrs['variable']] = mycls
                attrs['_dependency_registry'][attrs['variable']] = attrs['dependencies']

        super().__init__(name, bases, attrs)
            

class AbstractResolverMeta(ResolverMeta, abc.ABC):
    pass


class ResolverBase(Generic[S], metaclass=AbstractResolverMeta):

    @abc.abstractproperty
    def variable(self) -> VariableEnum:
        pass

    @abc.abstractproperty
    def dependencies(self) -> list[VariableEnum]:
        pass
    
    @classmethod
    @abc.abstractmethod
    def resolve(cls, current_values: dict[VariableEnum, Any]) -> S:
        raise NotImplementedError
    


def _construct_countries_to_neighbors_dict(csv_filepath: str) -> dict[str, set[str]]:
    pass



COUNTRIES_TO_NEIGHBORS = _construct_countries_to_neighbors_dict("filepath")
