from utils import MethodsEnum, MultiScenarioMethod
from algorithms.math_optimization.deterministic import ExactDeterministic
from algorithms.meta_optimization.deterministic import Deterministic

class Algorithm:
    def __init__(self, problem, method: MethodsEnum = MethodsEnum.DETERMINISTIC, num_scenarios: int = 30, alpha: float = 0.95, 
                 ms_method: MultiScenarioMethod = MultiScenarioMethod.MAXIMUM_EXPECTATION,
                 knn_k: int = 5,
                 ):
        self.problem = problem
        self.method = method
        self.num_scenarios = num_scenarios
        self.alpha = alpha
        self.ms_method = ms_method
        self.k = knn_k

    def solve(self):
        if self.method == MethodsEnum.DETERMINISTIC:
            return Deterministic(self.problem).solve()
        elif self.method == MethodsEnum.EXACT_DETERMINISTIC:
            return ExactDeterministic(self.problem).solve()

