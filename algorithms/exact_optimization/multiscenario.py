import logging
import algorithms.exact_optimization.PCTSP as op
from models.outputs.Solution import Solution
import time 
from utils import MultiScenarioMethod
from algorithms.structure.InstancePCTSP import InstancePCTSP

class MultiScenario:
    def __init__(self, instance: InstancePCTSP, ms_method: MultiScenarioMethod, num_scenarios: int, alpha: float = 0.95):
        self.instance = instance
        self.ms_method = ms_method
        self.num_scenarios = num_scenarios
        self.alpha = alpha

    def solve(self):
        logging.info("Solving deterministic problem")
        codnodes, c, d, D= self.get_info_from_problem()
        logging.info('Running optimization...')
        start_time = time.time()
        model, _ = op.prize_collecting_TSP_multiscenario(n=self.instance.n_customers, c=c, d=d, D=D, 
                                                         num_scenarios=self.num_scenarios, 
                                                         probabilities=self.instance.p_scenarios,
                                                         method=self.ms_method.value,
                                                         alpha=self.alpha,
                                                         cost_per_km=self.instance.cost_per_km,
                                                         cost_per_no_del_demand=self.instance.cost_per_no_del_demand
                                                         )
        execution_time = time.time() - start_time
        _, y_sol, _, _, _, _ = op.feed_solution_variables(model, self.instance.n_customers, d, c)
        codnodes_achived = [codnodes[i] for i in range(self.instance.n_customers) if y_sol[i] == 1]

        solution = Solution(self.instance.problem)
        solution.set_execution_time(execution_time)
        for codnode in codnodes_achived:
            customer = self.instance.get_customer_by_codnode(codnode)
            solution.add_customer(customer)
        
        solution.compute_metrics()
        return solution

    def get_info_from_problem(self):
        codnodes = []
        c = []
        d = []
        for customer in self.instance.customers_list:
            codnodes.append(customer.codnode)
            c.append(self.instance.distance_matrix[customer.index])
            d.append(customer.demand_scenarios)
        D = self.instance.truck_capacity
        return codnodes, c, d, D
        
