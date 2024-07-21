import os
import sys
import pandas as pd
from src.machine_learning_ops.exception import CustomException
from src.machine_learning_ops.logger import logging
from src.machine_learning_ops.utils import read_sql_data
from sklearn.model_selection import train_test_split

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join('artifacts', 'train_data.csv')
    test_data_path=os.path.join('artifacts', 'test_data.csv')
    raw_data_path=os.path.join('artifacts', 'raw_data.csv')

class DataIngestion:
    def __init__(self):
        self.injection_config =DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            #reading code
            df=read_sql_data()
            logging.info("Reading from SQL database.")
            os.makedirs(os.path.dirname(self.injection_config.train_data_path),exist_ok=True)
            df.to_csv(self.injection_config.raw_data_path,index=False,header=True)
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.injection_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.injection_config.test_data_path,index=False,header=True)

            logging.info("Data injection is comleted.")

            return (self.injection_config.train_data_path,
                    self.injection_config.test_data_path)
            
        except Exception as e:
            raise CustomException(e,sys)
            