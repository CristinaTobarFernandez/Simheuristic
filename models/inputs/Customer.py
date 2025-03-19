import pandas as pd
from utils import MachineLearningEnum
from utils.ml_models import models
from utils import handle_exceptions

class Customer:
    def __init__(self, index, codnode, record_data, day_data, node_data):
        self.index = index
        self.codnode = codnode
        self.record_data:pd.DataFrame = record_data
        self.day_data:pd.DataFrame = day_data

        self.real_demand = day_data['Pallets'].values[0]

        self.latitude = node_data['latitude'].values[0]
        self.longitude = node_data['longitude'].values[0]
        self.n_train = len(record_data)

    @handle_exceptions
    def predict_day_demand(self, model: MachineLearningEnum):
        X_train = self.record_data.drop(['Pallets', 'codnode'], axis=1)
        y_train = self.record_data['Pallets']
        X_test = self.day_data.drop(['Pallets', 'codnode'], axis=1)

        if model == 'Linear Regression':
            result = models.linear_regresion(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model == 'Random Forest':
            result = models.random_forest(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model == 'SVR':
            result = models.svm(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model == 'Neural Network':
            result = models.neural_network(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model == 'XGBoosting':
            result = models.xgboost_lgbm(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model == 'Lasso':
            result = models.lasso_regression(X_train=X_train, X_test=X_test, y_train=y_train)
        elif model == 'Ridge':
            result = models.ridge_regression(X_train=X_train, X_test=X_test, y_train=y_train)

        prediction = result['prediction']
        model_info = result['model_info']
        coefficients = result['Coefficients']

        return prediction, model_info, coefficients


