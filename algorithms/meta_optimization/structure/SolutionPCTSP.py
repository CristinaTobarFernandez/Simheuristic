
class SolutionPCTSP:
    def __init__(self, instance):
        self.instance = instance
        self.route = []
        self.total_cost = 0

    def add_customer(self, customer):
        self.route.append(customer)

    def compute_total_cost(self):
        self.total_cost = sum([customer.real_demand for customer in self.instance.customers_list])*self.instance.cost_per_no_del_demand
        for i in range(len(self.route)):
            self.total_cost += self.instance.cost_per_km * self.instance.distance_matrix[self.route[i-1].index][self.route[i].index]
            self.total_cost -= self.instance.cost_per_no_del_demand * self.route[i].real_demand

    def is_feasible(self):
        capacity_used = sum([customer.real_demand for customer in self.route])
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

        
