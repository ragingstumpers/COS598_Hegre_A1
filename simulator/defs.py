import abc
from enum import Enum
import math
from typing import Any, Generic, TypeVar

S = TypeVar('S')
T = TypeVar('T')


# neighborhood conflict seems like the last weird one
class VariableEnum(Enum):

    # BASE, done
    conflict_level_history_by_country__earlier_to_later = 'conflict_level_history_by_country__earlier_to_later'

    previous_year_conflict_level_by_country = 'previous_year_conflict_level_by_country'
    # C1_{t-1} DERIVED done
    previous_year_was_minor_by_country = 'previous_year_was_minor_by_country'
    # C2_{t-1} DERIVEd done
    previous_year_was_major_by_country = 'previous_year_was_major_by_country'

    # ln(t_0) BASE done
    previous_logs_no_conflict_by_country = 'previous_logs_no_conflict_by_country'
    # ln(t_1) BASE done
    previous_logs_minor_conflict_by_country = 'previous_logs_minor_conflict_by_country'
    # ln(t_2) BASE done
    previous_logs_major_conflict_by_country = 'previous_logs_major_conflict_by_country'

    # Oil BASE done
    projections_oil_level_by_country = 'projections_oil_level_by_country'
    # Oil DERIVED done
    current_oil_level_by_country = 'current_oil_level_by_country'
    # Oil * C1_{t-1} DERIVED done
    current_oil_times_previous_year_was_minor_by_country = 'current_oil_times_previous_year_was_minor_by_country'
    # Oil * C2_{t-1} DERIVED done
    current_oil_times_previous_year_was_major_by_country = 'current_oil_times_previous_year_was_major_by_country'
    # Oil * ln(t_1) DERIVED done
    current_oil_times_previous_logs_no_conflict_by_country = 'current_oil_times_previous_logs_no_conflict_by_country'
    
    # Ethn. dom PROJ BASE done
    projections_ethnic_dominance_all_years_by_country = 'projections_ethnic_dominance_all_years_by_country'
    # Ethn. dom DERIVED done
    current_ethnic_dominance_projection_by_country = 'current_ethnic_dominance_projection_by_country'
    # Ethn. dom * C1_{t-1} DERIVED done
    current_ethnic_dominance_projection_times_previous_year_was_minor_by_country = 'current_ethnic_dominance_projection_times_previous_year_was_minor_by_country'
    # Ethn. dom * C2_{t-1} DERIVED done
    current_ethnic_dominance_projection_times_previous_year_was_major_by_country = 'current_ethnic_dominance_projection_times_previous_year_was_major_by_country'
    # Ethn. dom *ln(t_1) DERIVED done
    current_ethnic_dominance_projection_times_previous_logs_no_conflict_by_country = 'current_ethnic_dominance_projection_times_previous_logs_no_conflict_by_country'
    
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
    current_imr_times_previous_logs_no_conflict_by_country = 'current_imr_times_previous_logs_no_conflict_by_country'
    

    # YOUTH BASE done
    projections_youth_level_by_country = 'projections_youth_level_by_country'
    # YOUTH DERIVED done
    current_youth_level_by_country = 'current_youth_level_by_country'
    # YOUTH * C1_{t-1} DERIVED done
    current_youth_times_previous_year_was_minor_by_country = 'current_youth_times_previous_year_was_minor_by_country'
    # YOUTH * C2_{t-1} DERIVED done
    current_youth_times_previous_year_was_major_by_country = 'current_youth_times_previous_year_was_major_by_country'
    # YOUTH * ln(t_1) DERIVED done
    current_youth_times_previous_logs_no_conflict_by_country = 'current_youth_times_previous_logs_no_conflict_by_country'


    # POPULATION BASE done
    projections_population_level_by_country = 'projections_population_level_by_country'
    # POPULATION DERIVED done
    current_population_level_by_country = 'current_population_level_by_country'
    # POPULATION * C1_{t-1} DERIVED done
    current_population_times_previous_year_was_minor_by_country = 'current_population_times_previous_year_was_minor_by_country'
    # POPULATION * C2_{t-1} DERIVED done
    current_population_times_previous_year_was_major_by_country = 'current_population_times_previous_year_was_major_by_country'
    # POPULATION * ln(t_1) DERIVED done
    current_population_times_previous_logs_no_conflict_by_country = 'current_population_times_previous_logs_no_conflict_by_country'
    

    # EDUCATION BASE done
    projections_education_level_by_country = 'projections_education_level_by_country'
    # EDUCATION DERIVED done
    current_education_level_by_country = 'current_education_level_by_country'
    # EDUCATION * C1_{t-1} DERIVED done
    current_education_times_previous_year_was_minor_by_country = 'current_education_times_previous_year_was_minor_by_country'
    # EDUCATION * C2_{t-1} DERIVED done
    current_education_times_previous_year_was_major_by_country = 'current_education_times_previous_year_was_major_by_country'
    # EDUCATION * ln(t_1) DERIVED done
    current_education_times_previous_logs_no_conflict_by_country = 'current_education_times_previous_logs_no_conflict_by_country'
    

    # neighborhood IMR DERIVED done
    current_neighborhood_imr_avg_by_country = 'current_neighborhood_imr_avg_by_country'
     # neighborhood education DERIVED done
    current_neighborhood_education_avg_by_country = 'current_neighborhood_education_avg_by_country'
    # neighborhood youth DERIVED done
    current_neighborhood_youth_avg_by_country = 'current_neighborhood_youth_avg_by_country'

    # done
    previous_neighborhood_has_minor_conflict_by_country = 'previous_neighborhood_has_minor_conflict_by_country'
    # done
    previous_neighborhood_has_minor_conflict_times_previous_year_was_minor_by_country = 'previous_neighborhood_has_minor_conflict_times_previous_year_was_minor_by_country'
    # done
    previous_neighborhood_has_minor_conflict_times_previous_year_was_major_by_country = 'previous_neighborhood_has_minor_conflict_times_previous_year_was_major_by_country'
    # done
    previous_neighborhood_has_minor_conflict_times_previous_logs_no_conflict_by_country = 'previous_neighborhood_has_minor_conflict_times_previous_logs_no_conflict_by_country'
    
    # done
    previous_neighborhood_has_major_conflict_by_country = 'previous_neighborhood_has_major_conflict_by_country'
    # done
    previous_neighborhood_has_major_conflict_times_previous_year_was_minor_by_country = 'previous_neighborhood_has_major_conflict_times_previous_year_was_minor_by_country'
    # done
    previous_neighborhood_has_major_conflict_times_previous_year_was_major_by_country = 'previous_neighborhood_has_major_conflict_times_previous_year_was_major_by_country'
    # done
    previous_neighborhood_has_major_conflict_times_previous_logs_no_conflict_by_country = 'previous_neighborhood_has_major_conflict_times_previous_logs_no_conflict_by_country'
    
    # done
    conflict_exponent_minor_by_country = 'conflict_exponent_minor_by_country'
    # done
    conflict_exponent_major_by_country = 'conflict_exponent_major_by_country'




    # no resolver
    previous_neighborhood_has_conflict_by_country = 'previous_neighborhood_has_conflict_by_country'
    # no resolver
    previous_neighborhood_has_conflict_times_previous_year_was_minor_by_country = 'previous_neighborhood_has_conflict_times_previous_year_was_minor_by_country'
    # no resolver
    previous_neighborhood_has_conflict_times_previous_year_was_major_by_country = 'previous_neighborhood_has_conflict_times_previous_year_was_major_by_country'
    # no resolver
    previous_neighborhood_has_conflict_times_previous_logs_no_conflict_by_country = 'previous_neighborhood_has_conflict_times_previous_logs_no_conflict_by_country'

    current_conflict_level_by_country = 'current_conflict_level_by_country'

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
    
    # BASE done
    current_year = 'current_year'


    # BASE done
    end_year = 'end_year'

    # BASE done
    average_coefficients_minor_by_variable = 'average_coefficients_minor_by_variable'
    # BASE done
    covariance_matrix_minor_by_variable = 'covariance_matrix_minor_by_variable'
    # DERIVED done
    drawn_coefficients_minor_by_variable = 'drawn_coefficients_minor_by_variable'
    # BASE done
    average_coefficients_major_by_variable = 'average_coefficients_major_by_variable'
    # BASE done
    covariance_matrix_major_by_variable = 'covariance_matrix_major_by_variable'
    # DERIVED done
    drawn_coefficients_major_by_variable = 'drawn_coefficients_major_by_variable'

    # DERIVED BUT BASE done
    should_stop_simulation = 'should_stop_simulation'


    # DERIVED done
    next_base_values = 'next_base_values'


COUNTRY_SPECIFIC_VARIABLES = {
    VariableEnum.previous_year_was_minor_by_country,
    VariableEnum.previous_year_was_major_by_country,
    VariableEnum.previous_logs_no_conflict_by_country,
    VariableEnum.previous_logs_minor_conflict_by_country,
    VariableEnum.previous_logs_major_conflict_by_country,
    VariableEnum.current_oil_level_by_country,
    VariableEnum.current_oil_times_previous_year_was_minor_by_country,
    VariableEnum.current_oil_times_previous_year_was_major_by_country,
    VariableEnum.current_oil_times_previous_logs_no_conflict_by_country,
    VariableEnum.current_ethnic_dominance_projection_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_minor_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_major_by_country,
    VariableEnum.current_ethnic_dominance_projection_times_previous_logs_no_conflict_by_country,
    VariableEnum.current_imr_level_by_country,
    VariableEnum.current_imr_times_previous_year_was_minor_by_country,
    VariableEnum.current_imr_times_previous_year_was_major_by_country,
    VariableEnum.current_imr_times_previous_logs_no_conflict_by_country,
    VariableEnum.current_youth_level_by_country,
    VariableEnum.current_youth_times_previous_year_was_minor_by_country,
    VariableEnum.current_youth_times_previous_year_was_major_by_country,
    VariableEnum.current_youth_times_previous_logs_no_conflict_by_country,
    VariableEnum.current_population_level_by_country,
    VariableEnum.current_population_times_previous_year_was_minor_by_country,
    VariableEnum.current_population_times_previous_year_was_major_by_country,
    VariableEnum.current_population_times_previous_logs_no_conflict_by_country,
    VariableEnum.current_education_level_by_country,
    VariableEnum.current_education_times_previous_year_was_minor_by_country,
    VariableEnum.current_education_times_previous_year_was_major_by_country,
    VariableEnum.current_education_times_previous_logs_no_conflict_by_country,
    
    VariableEnum.previous_neighborhood_has_minor_conflict_by_country,
    VariableEnum.previous_neighborhood_has_minor_conflict_times_previous_year_was_minor_by_country,
    VariableEnum.previous_neighborhood_has_minor_conflict_times_previous_year_was_major_by_country,
    VariableEnum.previous_neighborhood_has_minor_conflict_times_previous_logs_no_conflict_by_country,
    VariableEnum.previous_neighborhood_has_major_conflict_by_country,
    VariableEnum.previous_neighborhood_has_major_conflict_times_previous_year_was_minor_by_country,
    VariableEnum.previous_neighborhood_has_major_conflict_times_previous_year_was_major_by_country,
    VariableEnum.previous_neighborhood_has_major_conflict_times_previous_logs_no_conflict_by_country,

    VariableEnum.current_neighborhood_imr_avg_by_country,
    VariableEnum.current_neighborhood_education_avg_by_country,
    VariableEnum.current_neighborhood_youth_avg_by_country,
    VariableEnum.country_in_west_asia_north_africa_region_by_country,
    VariableEnum.country_in_west_africa_region_by_country,
    VariableEnum.country_in_south_africa_region_by_country,
}


MAP_EXOGENOUS_PROJECTIONS_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS = {
    'loi': VariableEnum.projections_oil_level_by_country,
    'let': VariableEnum.projections_ethnic_dominance_all_years_by_country,
    'lli': VariableEnum.projections_imr_level_by_country,
    'lyo': VariableEnum.projections_youth_level_by_country,
    'llpo': VariableEnum.projections_population_level_by_country,
    'led': VariableEnum.projections_education_level_by_country,
}
EXOGENOUS_PROJECTIONS_NECESSARY_VARIABLES = set(MAP_EXOGENOUS_PROJECTIONS_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS.values())


NON_PROJECTED_NECESSARY_VARIABLES = {
    VariableEnum.conflict_level_history_by_country__earlier_to_later
}

NEIGHBOR_NECESSARY_BASE_VARIABLES = {
    VariableEnum.country_to_neighbors,
}

REGION_NECESSARY_VARIABLES_PROCESSORS = {
    VariableEnum.country_in_west_asia_north_africa_region_by_country: lambda region: 1 if region == 4 else 0,
    VariableEnum.country_in_west_africa_region_by_country: lambda region: 1 if region == 6 else 0,
    VariableEnum.country_in_south_africa_region_by_country: lambda region: 1 if region == 7 else 0,
}

REGION_NECESSARY_VARIABLES = set(REGION_NECESSARY_VARIABLES_PROCESSORS)

CONSTANTS_NECESSARY_VARIABLES = {
    VariableEnum.minor_constant,
    VariableEnum.major_constant,
}

# probably should not be computed like this but rather from the utils func
BASE_VARIABLES = {
    VariableEnum.conflict_level_history_by_country__earlier_to_later,

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
    _resolver_registry = {}
    _dependency_registry = {}
    def __new__(mycls, name, bases, attrs):
        newcls = super().__new__(mycls, name, bases, attrs)
        if name not in ('AbstractResolverMeta', 'ResolverBase'):
                mycls._resolver_registry[attrs['variable']] = newcls
                mycls._dependency_registry[attrs['variable']] = attrs['dependencies']
        return newcls
            

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

_MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_BASE = {
    'lc1': VariableEnum.previous_year_was_minor_by_country,
    'lc2': VariableEnum.previous_year_was_major_by_country,
    'ltsc0': VariableEnum.previous_logs_no_conflict_by_country,

    'loi': VariableEnum.current_oil_level_by_country,
    'loic1': VariableEnum.current_oil_times_previous_year_was_minor_by_country,
    'loic2': VariableEnum.current_oil_times_previous_year_was_major_by_country,
    'lois0': VariableEnum.current_oil_times_previous_logs_no_conflict_by_country,

    'let': VariableEnum.current_ethnic_dominance_projection_by_country,
    'letc1': VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_minor_by_country,
    'letc2':  VariableEnum.current_ethnic_dominance_projection_times_previous_year_was_major_by_country,
    'lets0': VariableEnum.current_ethnic_dominance_projection_times_previous_logs_no_conflict_by_country,

    'lli': VariableEnum.current_imr_level_by_country,
    'limc1': VariableEnum.current_imr_times_previous_year_was_minor_by_country,
    'limc2': VariableEnum.current_imr_times_previous_year_was_major_by_country,
    'lims0': VariableEnum.current_imr_times_previous_logs_no_conflict_by_country,

    'lyo': VariableEnum.current_youth_level_by_country,
    'lyoc1': VariableEnum.current_youth_times_previous_year_was_minor_by_country,
    'lyoc2':  VariableEnum.current_youth_times_previous_year_was_major_by_country,
    'lyos0': VariableEnum.current_youth_times_previous_logs_no_conflict_by_country,

    'llpo': VariableEnum.current_population_level_by_country,
    'lpoc1': VariableEnum.current_population_times_previous_year_was_minor_by_country,
    'lpoc2': VariableEnum.current_population_times_previous_year_was_major_by_country,
    'lpos0': VariableEnum.current_population_times_previous_logs_no_conflict_by_country,

    'led': VariableEnum.current_education_level_by_country,
    'ledc1': VariableEnum.current_education_times_previous_year_was_minor_by_country,
    'ledc2': VariableEnum.current_education_times_previous_year_was_major_by_country,
    'leds0': VariableEnum.current_education_times_previous_logs_no_conflict_by_country,

    'llin': VariableEnum.current_neighborhood_imr_avg_by_country,
    'ledn': VariableEnum.current_neighborhood_education_avg_by_country,
    'lyon': VariableEnum.current_neighborhood_youth_avg_by_country,
    'lnc1': VariableEnum.previous_neighborhood_has_conflict_by_country,
    'lnc1c1': VariableEnum.previous_neighborhood_has_conflict_times_previous_year_was_minor_by_country,
    'lnc1c2': VariableEnum.previous_neighborhood_has_conflict_times_previous_year_was_major_by_country,
    'lnc1ts0': VariableEnum.previous_neighborhood_has_conflict_times_previous_logs_no_conflict_by_country,

    'r4': VariableEnum.country_in_west_asia_north_africa_region_by_country,
    'r6': VariableEnum.country_in_west_africa_region_by_country,
    'r7': VariableEnum.country_in_south_africa_region_by_country,

}


MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR = {
    **_MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_BASE,
    'ltsc1': VariableEnum.previous_logs_minor_conflict_by_country,
    '_cons': VariableEnum.minor_constant,
}

MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR = {
    **_MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_BASE,
    'ltsc2': VariableEnum.previous_logs_major_conflict_by_country,
    '_cons': VariableEnum.major_constant,
}


MINOR_COEFFICIENTS_NECESSARY_VARIABLES = set(MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MINOR.values())

MAJOR_COEFFICIENTS_NECESSARY_VARIABLES = set(MAP_CSV_NAME_TO_VARIABLE_ENUM_FOR_STATS_MAJOR.values())


MINOR_COVARIANCE_MATRIX_NECESSARY_VARIABLES = MINOR_COEFFICIENTS_NECESSARY_VARIABLES
MAJOR_COVARIANCE_MATRIX_NECESSARY_VARIABLES = MAJOR_COEFFICIENTS_NECESSARY_VARIABLES