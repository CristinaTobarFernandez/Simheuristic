from enum import Enum

class MethodsEnum(Enum):
    EXACT_DETERMINISTIC = "Exact Deterministic"
    DETERMINISTIC = "Deterministic"
    EXACT_MULTI_SCENARIO = "Exact Multi-scenario"
    MULTI_SCENARIO = "Multi-scenario"
    EXACT_KNN_MULTI_SCENARIO = "Exact KNN Multi-scenario"
    KNN_MULTI_SCENARIO = "KNN Multi-scenario"
    EXACT_MACHINE_LEARNING = "Exact Machine Learning"
    MACHINE_LEARNING = "Machine Learning"