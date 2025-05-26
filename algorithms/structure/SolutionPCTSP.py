from utils import MultiScenarioMethod
from statistics import mean
import numpy as np

class SolutionPCTSP:
    def __init__(self, instance):
        self.instance = instance
        self.route = []
        self.total_cost = 0

    def add_customer(self, customer):
        self.route.append(customer)

    def compute_total_cost(self, ms: bool = False, ms_method = None, num_scenarios = None, alpha = None):
        cost_per_km = self.instance.cost_per_km
        cost_per_no_del_demand = self.instance.cost_per_no_del_demand
        distance_matrix = self.instance.distance_matrix
        if ms:
            cost_per_scenario = []
            for scenario in range(num_scenarios):
                cost = self.instance.get_initial_cost_by_scenario(scenario)
                for i in range(len(self.route)):
                    prev = self.route[i-1]
                    curr = self.route[i]
                    cost += cost_per_km * distance_matrix[prev.index][curr.index]
                    cost -= cost_per_no_del_demand * curr.demand_scenarios[scenario]
                cost_per_scenario.append(cost)
            if ms_method == MultiScenarioMethod.MAXIMUM_EXPECTATION:
                self.total_cost = mean(cost_per_scenario)
            elif ms_method == MultiScenarioMethod.WORST_CASE_ANALYSIS:
                self.total_cost = max(cost_per_scenario)
            elif ms_method == MultiScenarioMethod.CVAR:
                self.total_cost = self.compute_cvar(cost_per_scenario, alpha)
        else:
            self.total_cost = self.instance.get_initial_determined_cost()
            for i in range(len(self.route)):
                prev_index = self.route[i-1].index
                curr_index = self.route[i].index
                demand_determined = self.route[i].demand_determined

                self.total_cost += cost_per_km * distance_matrix[prev_index][curr_index]
                self.total_cost -= cost_per_no_del_demand * demand_determined

    def is_feasible(self):
        capacity_used = sum([customer.demand_determined for customer in self.route])
        return capacity_used <= self.instance.truck_capacity

    def is_better_than(self, other):
        return self.total_cost < other.total_cost
 
    def is_equal_to(self, other):
        if self.total_cost != other.total_cost:
            return False
        if len(self.route) != len(other.route):
            return False
        doubled_route = self.route + self.route
        return any(doubled_route[i:i+len(other.route)] == other.route for i in range(len(self.route)))
    

    def compute_cvar(self, costs: np.ndarray, alpha: float) -> float:
        """
        Calcula el CVaR para un conjunto de costos y un nivel de confianza alfa.

        :param costos: np.ndarray con los costos asociados a cada escenario.
        :param alpha: Nivel de confianza para el cálculo del CVaR (ej. 0.95 para CVaR al 95%).
        :return: Valor del CVaR.
        """
        # Ordenar los costos de menor a mayor
        costs_ordered = np.sort(costs)
        
        # Índice que corresponde al VaR
        indice_var = int(np.ceil((1 - alpha) * len(costs_ordered)))
        
        # Obtener el CVaR como la media de los costos superiores al VaR
        cvar = np.mean(costs_ordered[indice_var - 1:])
        
        return cvar

        
