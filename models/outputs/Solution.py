from statistics import mean, variance

class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.customer_sequence = []
        self.n_customers = len(problem.customers_list)
        self.capacity_used = 0
        self.total_distance = 0
        self.total_cost = 0
        self.mean_scenario_cost = 0
        self.variance_scenario_cost = 0
        self.reliability_scenario_cost = 0
        self.execution_time = 0
        self.is_feasible = True

    def add_customer(self, customer):
        self.customer_sequence.append(customer)

    def set_execution_time(self, execution_time):
        self.execution_time = execution_time

    def compute_metrics(self):
        for i in range(len(self.customer_sequence)):
            self.capacity_used += self.customer_sequence[i].real_demand
            self.total_distance += self.problem.distance_matrix[self.customer_sequence[i-1].index][self.customer_sequence[i].index]
        
        if self.capacity_used > self.problem.truck_capacity:
            self.is_feasible = False

        self.total_cost = self.total_distance * self.problem.cost_per_km + (self.problem.get_all_real_demands() - self.capacity_used) * self.problem.cost_per_no_del_demand

        self.compute_scenarios_validation_metrics()


    def compute_scenarios_validation_metrics(self):
        num_scenarios = len(self.customer_sequence[0].demand_validation_scenarios)
        cost_per_scenario = []
        feasible_per_scenario = []
        for scenario in range(num_scenarios):
            cost = self.problem.get_initial_validation_cost(scenario)
            capacity_used = 0
            for i in range(len(self.customer_sequence)):
                cost += self.problem.cost_per_km * self.problem.distance_matrix[self.customer_sequence[i-1].index][self.customer_sequence[i].index]
                cost -= self.problem.cost_per_no_del_demand * self.customer_sequence[i].demand_validation_scenarios[scenario]

                capacity_used += self.customer_sequence[i].demand_validation_scenarios[scenario]
            cost_per_scenario.append(cost)
            if capacity_used <= self.problem.truck_capacity:
                feasible_per_scenario.append(1)
            else:
                feasible_per_scenario.append(0)

        self.mean_scenario_cost = mean(cost_per_scenario)
        self.variance_scenario_cost = variance(cost_per_scenario)
        self.reliability_scenario_cost = mean(feasible_per_scenario)
