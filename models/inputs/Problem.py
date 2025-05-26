from geopy.distance import geodesic
from .Customer import Customer
import pandas as pd
import datetime
import random
import os
from utils import ConfigLog, handle_exceptions
from utils.io.io_utils import create_path
from utils.ml_models import models

class Problem:
    def __init__(self, date, problem_name, max_customers:int = 50):
        self.date_str = date
        year, month, day = date.split('-')
        self.date = datetime.datetime(int(year), int(month), int(day))
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)

        self.max_customers = max_customers

        self.problem_name = problem_name

        self.cost_per_km = 1
        self.cost_per_no_del_demand = 0.1
        self.truck_capacity_per_customer = 100

        self.customers_map = {}
        self.customers_list = []

        self.distance_matrix = {}

        self.truck_capacity = 0
        self.n_customers = 0

        self.node_data = None
        self.demand_data = None

        self.initial_validation_cost = {}
        self.all_real_demands = None

    @handle_exceptions
    def feed(self):
        self.read_data()
        path = create_path(self.date, self.max_customers)
        node_data_model, demand_data_model, real_demand = self.select_execution_data(path=path)
        for _, row in real_demand.iterrows():
            record_data = demand_data_model[demand_data_model['codnode'] == row['codnode']]
            day_data = real_demand[real_demand['codnode'] == row['codnode']]
            node_data = node_data_model[node_data_model['codnode'] == row['codnode']]
            val_size = 0.2
            k = 100 # int(len(record_data) * val_size) TODO
            # Prepare data for KNN
            X_train = record_data.drop(columns=['Pallets', 'codnode', 'Date', 'Year', 'Holiday'])  # Drop non-feature columns
            y_train = record_data['Pallets']  
            X_test = day_data.drop(columns=['Pallets', 'codnode', 'Date', 'Year', 'Holiday'])
            _, _, _, indices = models.get_knn_demand(k, X_train, X_test, y_train)

            # Select the top 20% as validation set
            record_data_val = record_data.iloc[indices[0]]
            record_data_train = record_data.drop(record_data_val.index)
            self.add_customer(row['codnode'], record_data, record_data_train, record_data_val, day_data, node_data)

        self.truck_capacity = self.truck_capacity_per_customer * len(self.customers_list)
        self.n_customers = len(self.customers_list)

        self.compute_distance_matrix()

    @handle_exceptions
    def select_execution_data(self, path):
        random.seed(10051347)
        codnode_list = list(self.demand_data[self.demand_data['Date'] == self.date]['codnode'].values)
        number_nodes = len(codnode_list)
        if number_nodes > self.max_customers:
            codnode_list = random.sample(codnode_list, self.max_customers)
        node_data_model = self.node_data[self.node_data['codnode'].isin(codnode_list)]

        demand_data_model = self.demand_data[(self.demand_data['Date'] < self.date) & 
                                    (self.demand_data['codnode'].isin(codnode_list))]
        real_demand= self.demand_data[(self.demand_data['Date'] == self.date) & (self.demand_data['codnode']
                                                            .isin(codnode_list))]                       
        # Sort based on codnode_list
        node_data_model = node_data_model.sort_values(by='codnode')
        demand_data_model = demand_data_model.sort_values(by='codnode')
        real_demand = real_demand.sort_values(by='codnode')

        node_data_model.to_csv(os.path.join(path, "nodeDataSelected.csv"), index=False)
        demand_data_model.to_csv(os.path.join(path, "demandDataSelected.csv"), index=False)
        real_demand.to_csv(os.path.join(path, "realDemand.csv"), index=False)
        return node_data_model, demand_data_model, real_demand

    @handle_exceptions
    def read_data(self):
        node_data_github_link = "https://raw.githubusercontent.com/critobfer/StocasticOpt/main/data/nodeData.csv"
        demand_data_github_link = "https://raw.githubusercontent.com/critobfer/StocasticOpt/main/data/demandDataComplete.csv"

        node_data = pd.read_csv(node_data_github_link, sep=';', encoding='latin-1') 

        demand_data = pd.read_csv(demand_data_github_link, sep=';', encoding='latin-1') 
        demand_data['Date'] = pd.to_datetime(demand_data['Date'], format="%d/%m/%Y")     

        demand_data = self.extend_demand_data(demand_data)

        self.node_data = node_data
        self.demand_data = demand_data

    @handle_exceptions
    def extend_demand_data(self, demand_data):
        print(demand_data.columns)
        print(demand_data.head())
        # Define the number of new records to create per existing record
        n = 5  # Por ejemplo, crear 5 registros adicionales por cada registro existente
        
        # Create new records with noise stratified by codnode
        selected_columns = ['Pallets', 'WIND SPEED (m/s)', 'WIND DIRECTION (Â°)', 
                    'TEMPERATURE (ÂºC)', 'RELATIVE HUMIDITY (%)', 
                    'BARIOMETRIC PRESSURE (mb)', 'SOLAR RADIATION (W/m2)', 
                    'PRECIPITATION (l/m2)']
        new_records = []
        for _, group in demand_data.groupby('codnode'):
            # Calculate the standard deviation for each column within the group
            noise_std = group[selected_columns].std()
            
            for _, row in group.iterrows():
                for _ in range(n):
                    new_record = row.copy()
                    for column in noise_std.index:
                        if column in ['Pallets', 'WIND SPEED (m/s)', 'WIND DIRECTION (Â°)', 
                                      'TEMPERATURE (ÂºC)', 'RELATIVE HUMIDITY (%)', 
                                      'BARIOMETRIC PRESSURE (mb)', 'SOLAR RADIATION (W/m2)', 
                                      'PRECIPITATION (l/m2)']:
                            # Add noise and ensure the value is positive
                            new_value = row[column] + random.gauss(0, noise_std[column])
                            if new_value < 0:
                                new_value = row[column]
                    new_records.append(new_record)
        
        # Append new records to the original data
        extended_demand_data = pd.concat([demand_data, pd.DataFrame(new_records)], ignore_index=True)
        
        return extended_demand_data

    @handle_exceptions
    def add_customer(self, codnode, record_data, record_data_train, record_data_val, day_data, node_data):
        index = len(self.customers_list)
        customer = Customer(index, codnode, record_data, record_data_train, record_data_val, day_data, node_data)
        self.customers_map[customer.codnode] = customer
        self.customers_list.append(customer)
    
    def get_customer_by_codnode(self, codnode):
        return self.customers_map[codnode]

    @handle_exceptions
    def compute_distance_matrix(self):
        self.distance_matrix = [[None for _ in range(len(self.customers_list))] for _ in range(len(self.customers_list))]
        
        for customer in self.customers_list:
            for other_customer in self.customers_list:
                if self.distance_matrix[customer.index][other_customer.index] is not None:
                    continue
                if customer != other_customer:
                    distance = self.compute_distance(customer, other_customer)
                    self.distance_matrix[customer.index][other_customer.index] = distance
                    self.distance_matrix[other_customer.index][customer.index] = distance
                else:
                    self.distance_matrix[customer.index][other_customer.index] = 0

    @handle_exceptions
    def compute_distance(self, customer1, customer2):
        return geodesic((customer1.latitude, customer1.longitude), (customer2.latitude, customer2.longitude)).kilometers
    
    def get_all_real_demands(self):
        if self.all_real_demands is None:
            self.all_real_demands = sum([customer.real_demand for customer in self.customers_list])
        return self.all_real_demands

    def get_initial_validation_cost(self, scenario):
        if scenario not in self.initial_validation_cost:
            self.initial_validation_cost[scenario] = sum([customer.demand_validation_scenarios[scenario] for customer in self.customers_list]) * self.cost_per_no_del_demand
        return self.initial_validation_cost[scenario]
