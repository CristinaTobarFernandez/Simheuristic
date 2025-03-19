from enum import Enum

class MethodsEnum(Enum):
    EXACT_DETERMINISTIC = "Exact Deterministic"
    DETERMINISTIC = "Deterministic"
    MULTI_SCENARIO = "Multi-scenario"
    KNN_MULTI_SCENARIO = "KNN Multi-scenario"
    MACHINE_LEARNING = "Machine Learning"