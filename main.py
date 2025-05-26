from models import Problem
from algorithms import Algorithm
from utils import ConfigLog
from utils import MultiScenarioMethod, MethodsEnum, MachineLearningEnum
import logging
import pandas as pd
import time
if __name__ == "__main__":
    ConfigLog.config()
    # problem = Problem(date="2024-03-05", problem_name="Día 5 marzo 2024", max_customers=1000)
    problem = Problem(date="2024-03-11", problem_name="Día 5 marzo 2024", max_customers=1000)

    # problem = Problem(date="2024-03-07", problem_name="Día 3 marzo 2024", max_customers=500)
    
    problem.feed()
    logging.info(f"Truck capacity: {problem.truck_capacity}")
    logging.info(f"Number of customers: {problem.n_customers}")
    
    alpha = 0.95
    num_scenarios = 100 
    results = []
    try:
        for i in MethodsEnum:
            if 'EXACT' in i.name or 'MACHINE_LEARNING' in i.name:
                continue
            logging.info(f"==> Running {i.name}")
            if 'MULTI' in i.name:
                if 'KNN' in i.name:
                    for ms_method in MultiScenarioMethod:
                        for ml_model in MachineLearningEnum:
                            start_time = time.time()
                            algorithm = Algorithm(problem, method=i, num_scenarios=num_scenarios, ms_method=ms_method, ml_model=ml_model, alpha=alpha)
                            solutions = algorithm.solve()
                            end_time = time.time()
                            for solution in solutions:
                                results.append({
                                    'method': i.name,
                                    'num_scenarios': num_scenarios,
                                    'ms_method': ms_method.name,
                                    'ml_model': ml_model.name,
                                    'total_cost': solution.total_cost,
                                    'total_distance': solution.total_distance,
                                    'capacity_used': solution.capacity_used,
                                    'execution_time': end_time - start_time,
                                    'mean_scenarios_validation_cost': solution.mean_scenario_cost,
                                    'variance_scenarios_validation_cost': solution.variance_scenario_cost,
                                    'reliability_scenarios_validation_cost': solution.reliability_scenario_cost
                                })
                                
                                logging.info(f"Execution time: {end_time - start_time} seconds")
                                print(results[-1])
                else:
                    for ms_method in MultiScenarioMethod:
                        start_time = time.time()
                        algorithm = Algorithm(problem, method=i, num_scenarios=num_scenarios, ms_method=ms_method, alpha=alpha)
                        solutions = algorithm.solve()
                        end_time = time.time()
                        for solution in solutions:
                            results.append({
                                'method': i.name,
                                'num_scenarios': num_scenarios,
                                'ms_method': ms_method.name,
                                'ml_model': 'None',
                                'total_cost': solution.total_cost,
                                'total_distance': solution.total_distance,
                                'capacity_used': solution.capacity_used,
                                'execution_time': end_time - start_time,
                                'mean_scenarios_validation_cost': solution.mean_scenario_cost,
                                'variance_scenarios_validation_cost': solution.variance_scenario_cost,
                                'reliability_scenarios_validation_cost': solution.reliability_scenario_cost
                            })
                            logging.info(f"Execution time: {end_time - start_time} seconds")
                            print(results[-1])
            else:
                start_time = time.time()
                algorithm = Algorithm(problem, method=i)
                solutions = algorithm.solve()
                end_time = time.time()
                for solution in solutions:
                    results.append({
                        'method': i.name,
                        'num_scenarios': 1,
                        'ms_method': 'None',
                        'ml_model': 'None',
                        'total_cost': solution.total_cost,
                        'total_distance': solution.total_distance,
                        'capacity_used': solution.capacity_used,
                        'execution_time': end_time - start_time,
                        'mean_scenarios_validation_cost': solution.mean_scenario_cost,
                        'variance_scenarios_validation_cost': solution.variance_scenario_cost,
                        'reliability_scenarios_validation_cost': solution.reliability_scenario_cost
                    })
                    logging.info(f"Execution time: {end_time - start_time} seconds")
                    print(results[-1])
        raise Exception("Stop here")
    except Exception as e:
        logging.error(f"Error: {e}")
            
    results_df = pd.DataFrame(results)
    results_df.to_csv(f'results_{problem.n_customers}_{problem.date.day}_{problem.date.month}_{problem.date.year}.csv', 
                      index=False, sep=';', decimal=',')

