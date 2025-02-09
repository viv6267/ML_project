# Basic Import
import numpy as np
import pandas as pd
import seaborn as sns
import os
import sys
# Modelling
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
import mlflow
import mlflow.sklearn

from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge,Lasso
#from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from src.machine_learning_ops.utils import save_object,evaluate_models
from dataclasses import dataclass
from src.machine_learning_ops.exception import CustomException
from src.machine_learning_ops.logger import logging
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error,mean_absolute_error
from urllib.parse import urlparse



@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def eval_metrics(self,actual,pred):
        rmse=np.sqrt(mean_squared_error(actual,pred))
        mae=mean_absolute_error(actual,pred)
        r2_score=r2_score(actual,pred)
        return rmse,mae,r2_score

    def initiate_model_trainer(self,train_array,test_array):

        try:
            logging.info("Split the data into train and test array")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
               
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            
            params={
                "Decision Tree": {
                    'criterion': ['mse','friedman_mse','mae'],
                    'max_depth': [5,10,15,20,25,30],
                    'min_samples_split': [2, 5, 10, 15, 20],
                    'min_samples_leaf': [1, 2, 5, 10, 15]
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            

            model_report:dict=evaluate_models(X_train, y_train,X_test,y_test,models,params)

            # To get the most model in the dictionary in the report
            best_model_score = max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[list(model_report.values())\
                                                      .index(best_model_score)]
            
            best_model=models[best_model_name]

            print("This is the best model:")
            print(best_model_name)

            model_names=list(models.keys())

            actual_model=""
            for model_name in model_names:
                if best_model_name==model_name:
                    actual_model+=model_name
            best_params=params[actual_model]

            mlflow.set_registry_uri('https://dagshub.com/viv6267/ML_project.mlflow')
            tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme

            # mlflow 
            with mlflow.start_run():
                predicted_qualities=best_model.predict(X_test)
                (rsme,mae,r2_score) = self.eval_metrics(y_test,predicted_qualities)

                if tracking_url_type_store!="file":
                    # Register the model
                    # There are other ways to use the Model Registry, which depends on the use case,
                    # please refer to the doc for more information:
                    # https://mlflow.org/docs/latest/model-registry.html#api-workflow

                    mlflow.sklearn.log_model(best_model,"model",registered_model_name=actual_model)
                else:
                    mlflow.sklearn.log_model(best_model,"model")




            if best_model_score<0.6:
                raise CustomException("No best model found")
            
            logging.info(f"Best Model: {best_model_name}")

            save_object(self.model_trainer_config.trained_model_file_path,obj=best_model)

            predicted=best_model.predict(X_test)

            r2_square=r2_score(y_test,predicted)

            return r2_square




        except Exception as e:
            raise CustomException(e,sys)
