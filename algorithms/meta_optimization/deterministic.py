import logging
import random
from algorithms.meta_optimization.structure.InstancePCTSP import InstancePCTSP
from algorithms.meta_optimization.structure.SolutionPCTSP import SolutionPCTSP
from models.outputs.Solution import Solution
import copy
import time

class Deterministic:
    def __init__(self, instance: InstancePCTSP):
        self.instance = instance

    def solve(self):
        start_time = time.time()
        best_solution = None
        max_iterations = 100
        alpha = 0.2
        for _ in range(max_iterations):
            if _ % 100 == 0:
                logging.info(f"Iteration {_}")
            # Construct a new solution
            solution = self.constructive_heuristic(alpha)
            # Improve the constructed solution
            self.improve(solution)
            # Update the best solutuon if the new solution is better
            if best_solution is None:
                best_solution = solution
            elif solution.is_better_than(best_solution):
                logging.info(f"New best solution found with cost {solution.total_cost}")
                best_solution = copy.deepcopy(solution)
        logging.info(f"Best solution: {best_solution.total_cost}")
        execution_time = time.time() - start_time

        solution = Solution(self.instance)
        solution.set_execution_time(execution_time)
        for customer in best_solution.route:
            solution.add_customer(customer)
        solution.compute_metrics()
        return solution


    def constructive_heuristic(self, alpha):
        # Podría ser que no haya clientes que puedan ser el primer cliente ya que su demanda es mayor que la capacidad de la camioneta
        posibles_first_customers = [customer for customer in self.instance.customers_list if customer.real_demand <= self.instance.truck_capacity]
        if len(posibles_first_customers) == 0:
            logging.info("No hay clientes que puedan ser el primer cliente")
            return None
        first_customer = random.choice(posibles_first_customers)
        # Inicializar variables
        current_customer = first_customer  # Comenzar en un cliente cualquiera
        unvisited_customers = set(self.instance.customers_list)
        unvisited_customers.remove(current_customer)
        route = [current_customer]
        total_cost = 0
        total_demand_not_delivered = 0
        capacity_used = first_customer.real_demand
        for customer in unvisited_customers:
            total_demand_not_delivered += customer.real_demand

        while unvisited_customers:
            # Calcular y almacenar los valores para cada cliente
            candidate_customers = []
            for customer in unvisited_customers:
                value = (
                    self.instance.cost_per_km * self.instance.distance_matrix[current_customer.index][customer.index] -
                    self.instance.cost_per_no_del_demand * customer.real_demand
                )
                if capacity_used + customer.real_demand <= self.instance.truck_capacity:
                    logging.info(f'Capacidad usada en caso de añadir el cliente {customer.codnode}: {capacity_used + customer.real_demand}')
                    candidate_customers.append((customer, value))
                else:
                    continue
            
            if len(candidate_customers) == 0:
                break
            # Ordenar los clientes no visitados usando los valores calculados
            sorted_customers = sorted(
                candidate_customers,
                key=lambda customer: customer[1]
            )
            
            # Select one of the top alpha% customers
            top_count = max(1, int(len(sorted_customers) * alpha))
            best_candidate = random.choice(sorted_customers[:top_count])
            if best_candidate[1] > 0: # Si empeoramos la solución, no seguimos buscando
                break
            next_customer = best_candidate[0]

            # Actualizar el costo total
            total_cost += self.instance.cost_per_km * self.instance.distance_matrix[current_customer.index][next_customer.index]
            total_demand_not_delivered -= next_customer.real_demand
            capacity_used += next_customer.real_demand

            # Mover al siguiente cliente
            current_location = next_customer
            route.append(current_location)
            unvisited_customers.remove(current_location)

        # Regresar al depósito
        total_cost += self.instance.cost_per_km * self.instance.distance_matrix[current_customer.index][0]
        # Considerar la penalización por demanda no entregada
        total_cost += self.instance.cost_per_no_del_demand * total_demand_not_delivered
        solution = SolutionPCTSP(self.instance)
        for customer in route:
            solution.add_customer(customer)
        solution.compute_total_cost()
        return solution

    def improve(self, solution):
        improved = True
        while improved:
            improved = False
            # Intercambio de clientes
            for i in range(1, len(solution.route) - 2):
                for j in range(i + 1, len(solution.route)):
                    if j - i == 1:  # Consecutive nodes, no need to swap
                        continue
                    new_route = solution.route[:]
                    new_route[i:j] = reversed(solution.route[i:j])
                    new_solution = SolutionPCTSP(self.instance)
                    for customer in new_route:
                        new_solution.add_customer(customer)
                    new_solution.compute_total_cost()
                    if new_solution.is_better_than(solution) and new_solution.is_feasible():
                        solution.route = new_route
                        solution.total_cost = new_solution.total_cost
                        improved = True

            # Selección de otro cliente
            for i in range(1, len(solution.route) - 1):
                for potential_customer in self.instance.customers_list:
                    if potential_customer not in solution.route:
                        new_route = solution.route[:]
                        new_route[i] = potential_customer
                        new_solution = SolutionPCTSP(self.instance)
                        for customer in new_route:
                            new_solution.add_customer(customer)
                        new_solution.compute_total_cost()
                        if new_solution.is_better_than(solution) and new_solution.is_feasible():
                            logging.info(f'Capacidad usada en caso de añadir cambiar el cliente {sum([customer.real_demand for customer in new_route])}')
                            solution.route = new_route
                            solution.total_cost = new_solution.total_cost
                            improved = True
        

        

