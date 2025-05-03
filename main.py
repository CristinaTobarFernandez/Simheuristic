from models import Problem
from algorithms import Algorithm
from utils import ConfigLog
from utils import MultiScenarioMethod, MethodsEnum
import logging
import pandas as pd
import time
if __name__ == "__main__":
    ConfigLog.config()
    problem = Problem(date="2024-03-05", problem_name="Día 5 marzo 2024", max_customers=1000)
    problem.feed()
    logging.info(f"Truck capacity: {problem.truck_capacity}")
    logging.info(f"Number of customers: {problem.n_customers}")
    
    alpha = 0.95
    num_scenarios = 80
    results = []
    for i in MethodsEnum:
        if 'EXACT' in i.name:
            continue
        logging.info(f"==> Running {i.name}")
        start_time = time.time()
        if 'MULTI' in i.name:
            for ms_method in MultiScenarioMethod:
                algorithm = Algorithm(problem, method=i, num_scenarios=num_scenarios, ms_method=ms_method, alpha=alpha)
                solution = algorithm.solve()
                results.append({
                    'method': i.name,
                    'num_scenarios': num_scenarios,
                    'ms_method': ms_method.name,
                    'total_cost': solution.total_cost,
                    'total_distance': solution.total_distance,
                    'capacity_used': solution.capacity_used,
                    'execution_time': solution.execution_time,
                    'mean_scenarios_validation_cost': solution.mean_scenario_cost,
                    'variance_scenarios_validation_cost': solution.variance_scenario_cost,
                    'reliability_scenarios_validation_cost': solution.reliability_scenario_cost
                })
        else:
            algorithm = Algorithm(problem, method=i)
            solution = algorithm.solve()
            results.append({
                'method': i.name,
                'num_scenarios': 1,
                'ms_method': 'None',
                'total_cost': solution.total_cost,
                'total_distance': solution.total_distance,
                'capacity_used': solution.capacity_used,
                'execution_time': solution.execution_time,
                'mean_scenarios_validation_cost': solution.mean_scenario_cost,
                'variance_scenarios_validation_cost': solution.variance_scenario_cost,
                'reliability_scenarios_validation_cost': solution.reliability_scenario_cost
            })
        end_time = time.time()
        logging.info(f"Execution time: {end_time - start_time} seconds")
    results_df = pd.DataFrame(results)
    results_df.to_csv(f'results_{problem.n_customers}_{problem.date.day}_{problem.date.month}_{problem.date.year}.csv', 
                      index=False, sep=';', decimal=',')

