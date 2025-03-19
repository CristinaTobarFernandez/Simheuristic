from utils import MethodsEnum, MultiScenarioMethod, MachineLearningEnum
import algorithms.exact_optimization as exact
import algorithms.meta_optimization as meta
from algorithms.structure.InstancePCTSP import InstancePCTSP

class Algorithm:
    def __init__(self, problem, method: MethodsEnum = MethodsEnum.DETERMINISTIC, num_scenarios: int = 30, alpha: float = 0.95, 
                 ms_method: MultiScenarioMethod = MultiScenarioMethod.MAXIMUM_EXPECTATION, 
                 ml_model: MachineLearningEnum = MachineLearningEnum.LINEAR_REGRESSION
                 ):
        self.problem = problem
        self.method = method
        self.ml_model = ml_model
        self.num_scenarios = num_scenarios
        self.alpha = alpha
        self.ms_method = ms_method

    def solve(self):
        instance = InstancePCTSP(self.problem)
        if self.method in [MethodsEnum.MULTI_SCENARIO, MethodsEnum.EXACT_MULTI_SCENARIO, MethodsEnum.KNN_MULTI_SCENARIO, MethodsEnum.EXACT_KNN_MULTI_SCENARIO]:
            instance.set_num_scenarios(self.num_scenarios)
            if self.method in [MethodsEnum.KNN_MULTI_SCENARIO, MethodsEnum.EXACT_KNN_MULTI_SCENARIO]:
                instance.set_progressive_demand_scenario_probabilities()
                for customer in instance.customers_list:
                    customer.set_demand_scenarios_knn(self.num_scenarios)
                    customer.set_demand_prediction(self.ml_model)
            else:
                instance.set_equiprobable_demand_scenario_probabilities()
                for customer in instance.customers_list:
                    customer.set_demand_scenarios_lognormal(self.num_scenarios)
                    customer.set_demand_mean()
        elif self.method in [MethodsEnum.DETERMINISTIC, MethodsEnum.EXACT_DETERMINISTIC]:
            for customer in instance.customers_list:
                customer.set_real_demand()
        elif self.method in [MethodsEnum.MACHINE_LEARNING, MethodsEnum.EXACT_MACHINE_LEARNING]:
            for customer in instance.customers_list:
                customer.set_demand_prediction(self.ml_model)



        if self.method in [MethodsEnum.DETERMINISTIC, MethodsEnum.MACHINE_LEARNING]:
            return meta.Deterministic(instance).solve()
        elif self.method in [MethodsEnum.EXACT_DETERMINISTIC, MethodsEnum.EXACT_MACHINE_LEARNING]:
            return exact.Deterministic(instance).solve()
        
        elif self.method in [MethodsEnum.EXACT_MULTI_SCENARIO, MethodsEnum.EXACT_KNN_MULTI_SCENARIO]:
            return exact.MultiScenario(instance, self.ms_method, self.num_scenarios, self.alpha).solve()
        elif self.method in [MethodsEnum.MULTI_SCENARIO, MethodsEnum.KNN_MULTI_SCENARIO]:
            return meta.MultiScenario(instance, self.ms_method, self.num_scenarios, self.alpha).solve()
