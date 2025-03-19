
class InstancePCTSP:
    def __init__(self, problem):
        self.customers_list = problem.customers_list
        self.distance_matrix = problem.distance_matrix
        self.cost_per_km = problem.cost_per_km
        self.cost_per_no_del_demand = problem.cost_per_no_del_demand
