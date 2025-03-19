class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.customer_sequence = []
        self.n_customers = len(problem.customers_list)
        self.capacity_used = 0
        self.total_distance = 0
        self.total_cost = 0
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
