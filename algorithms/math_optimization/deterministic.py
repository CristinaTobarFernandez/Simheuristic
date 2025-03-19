import logging
import algorithms.math_optimization.PCTSP as op
from models.outputs.Solution import Solution
import time 

class ExactDeterministic:
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        logging.info("Solving deterministic problem")
        codnodes, c, d, D, latitudes, longitudes= self.get_info_from_problem()
        logging.info('Running optimization...')
        start_time = time.time()
        model, _ = op.prize_collecting_TSP(self.problem.n_customers, c, d, D, self.problem.cost_per_km , self.problem.cost_per_no_del_demand)
        execution_time = time.time() - start_time
        _, y_sol, _, _, _, _ = op.feed_solution_variables(model, self.problem.n_customers, d, c)
        codnodes_achived = [codnodes[i] for i in range(self.problem.n_customers) if y_sol[i] == 1]

        solution = Solution(self.problem)
        solution.set_execution_time(execution_time)
        for codnode in codnodes_achived:
            customer = self.problem.get_customer_by_codnode(codnode)
            solution.add_customer(customer)
        
        solution.compute_metrics()
        return solution

    def get_info_from_problem(self):
        codnodes = []
        c = []
        d = []
        latitudes = []
        longitudes = []
        for customer in self.problem.customers_list:
            codnodes.append(customer.codnode)
            c.append(self.problem.distance_matrix[customer.index])
            d.append(customer.real_demand)
            latitudes.append(customer.latitude)
            longitudes.append(customer.longitude)
        D = self.problem.truck_capacity
        return codnodes, c, d, D, latitudes, longitudes
        
