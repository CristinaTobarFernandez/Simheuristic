import pandas as pd
from utils import MachineLearningEnum
from utils.ml_models import models
from utils import handle_exceptions
import numpy as np
import warnings

class Customer:
    def __init__(self, index, codnode, record_data, record_data_train, record_data_val, day_data, node_data):
        self.index = index
        self.codnode = codnode
        self.record_data:pd.DataFrame = record_data
        self.record_data_train:pd.DataFrame = record_data_train
        self.record_data_val:pd.DataFrame = record_data_val
        self.day_data:pd.DataFrame = day_data

        self.real_demand = day_data['Pallets'].values[0]

        self.latitude = node_data['latitude'].values[0]
        self.longitude = node_data['longitude'].values[0]
        self.n_train = len(record_data)

        self.demand_determined = None
        self.demand_scenarios = None

        self.demand_validation_scenarios = self.record_data_val['Pallets'].values

    @handle_exceptions
    def set_demand_scenarios_knn(self, k: int):
        d = [None for _ in range(k)]
        # We generate m scenarios
        X_train = self.record_data_train.drop(['Pallets', 'codnode', 'Date', 'Year', 'Holiday'], axis=1)
        y_train = self.record_data_train['Pallets']
        X_test = self.day_data.drop(['Pallets', 'codnode', 'Date', 'Year', 'Holiday'], axis=1)
        neighbors_demand_values, _, _, _ = models.get_knn_demand(k, X_train, X_test, y_train)
        for s in range(k):
            d[s] = neighbors_demand_values[s]
        self.demand_scenarios = d

    @handle_exceptions
    def set_demand_scenarios_lognormal(self, num_scenarios: int):
        d = [None for _ in range(num_scenarios)]
        demand_node = self.record_data_train['Pallets'].values
        # https://www.probabilidadyestadistica.net/distribucion-lognormal/#grafica-de-la-distribucion-lognormal
        log_demand = np.log(demand_node)
        mu_log = np.mean(log_demand)
        sigma_log = np.std(log_demand)
        sample = np.random.normal(mu_log, sigma_log, num_scenarios)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for s in range(num_scenarios):
                d[s] = np.exp(sample[s])
        self.demand_scenarios = d

    
    @handle_exceptions
    def set_demand_prediction(self, model: MachineLearningEnum):
        # We prepare the data
        X_train = self.record_data_train.drop(['Pallets', 'codnode', 'Date', 'Year', 'Holiday'], axis=1)
        y_train = self.record_data_train['Pallets']
        X_test = self.day_data.drop(['Pallets', 'codnode', 'Date', 'Year', 'Holiday'], axis=1)

        if model.value == 'Linear Regression':
            result = models.linear_regresion(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model.value == 'Random Forest':
            result = models.random_forest(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model.value == 'SVR':
            result = models.svm(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model.value == 'Neural Network':
            result = models.neural_network(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model.value == 'XGBoosting':
            result = models.xgboost_lgbm(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model.value == 'Lasso':
            result = models.lasso_regression(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model.value == 'Ridge':
            result = models.ridge_regression(X_train=X_train, X_test=X_test, y_train=y_train)
        
        self.demand_determined = result['prediction']

    @handle_exceptions
    def set_demand_mean(self):
        demand_node = self.record_data_train['Pallets'].values
        self.demand_determined = np.mean(demand_node)

    @handle_exceptions
    def set_real_demand(self):
        self.demand_determined = self.real_demand


