from models import Problem
from algorithms import Algorithm
from utils import ConfigLog
from algorithms.algorithm import MethodsEnum
import logging

if __name__ == "__main__":
    ConfigLog.config()
    problem = Problem(date="2024-01-30", problem_name="Día 30 enero 2024", max_customers=20)
    problem.feed()
    logging.info(f"Truck capacity: {problem.truck_capacity}")
    algorithm = Algorithm(problem, method=MethodsEnum.EXACT_DETERMINISTIC)
    solution_exact = algorithm.solve()

    algorithm = Algorithm(problem, method=MethodsEnum.DETERMINISTIC)
    solution_deterministic = algorithm.solve()
    print(f"Exact solution: {solution_exact.total_cost} with {len(solution_exact.customer_sequence)} customers, {solution_exact.total_distance} km, capacity used {solution_exact.capacity_used}, execution time {solution_exact.execution_time}")
    print(f"Deterministic solution: {solution_deterministic.total_cost} with {len(solution_deterministic.customer_sequence)} customers, {solution_deterministic.total_distance} km, capacity used {solution_deterministic.capacity_used}, execution time {solution_deterministic.execution_time}")
