
class InstancePCTSP:
    def __init__(self, problem, n_scenarios: int = None, p_scenarios: list[float] = None):
        self.problem = problem
        self.customers_list = problem.customers_list
        self.customers_map = problem.customers_map
        self.truck_capacity = problem.truck_capacity
        self.n_customers = problem.n_customers
        self.distance_matrix = problem.distance_matrix
        self.cost_per_km = problem.cost_per_km
        self.cost_per_no_del_demand = problem.cost_per_no_del_demand

        self.n_scenarios = n_scenarios
        self.p_scenarios:list[float] = p_scenarios

    def get_customer_by_codnode(self, codnode: int):
        return self.customers_map[codnode]
    
    def get_all_real_demands(self):
        return [customer.real_demand for customer in self.customers_list]
    
    def set_num_scenarios(self, n_scenarios: int):
        self.n_scenarios = n_scenarios

    def set_demand_prediction_to_customers(self, codnode: int, demand_prediction: float):
        customer = self.customers_map[codnode]
        customer.set_demand_prediction(demand_prediction)

    def set_demand_scenarios(self, codnode: int, demand_scenarios: list[float]):
        if len(demand_scenarios) != self.n_scenarios:
            raise ValueError(f"The number of demand scenarios must be equal to the number of scenarios: {self.n_scenarios}")
        customer = self.customers_map[codnode]
        customer.set_demand_scenarios(demand_scenarios)

    def set_demand_scenario_probabilities(self, p_scenarios: list[float]):
        if len(p_scenarios) != self.n_scenarios:
            raise ValueError(f"The number of demand scenario probabilities must be equal to the number of scenarios: {self.n_scenarios}")
        self.p_scenarios = p_scenarios
    
    def set_equiprobable_demand_scenario_probabilities(self):
        self.p_scenarios = [1/self.n_scenarios for _ in range(self.n_scenarios)]
    
    def set_progressive_demand_scenario_probabilities(self):
        self.p_scenarios = [1/i for i in range(1, self.n_scenarios+1)]
        self.p_scenarios = [p/sum(self.p_scenarios) for p in self.p_scenarios]


