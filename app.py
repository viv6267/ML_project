from src.machine_learning_ops.logger import logging
from src.machine_learning_ops.exception import CustomException
import sys
from src.machine_learning_ops.components.data_ingestion import DataIngestion

if __name__=='__main__':
    logging.info("The execution has started.")

    try:
        data_injestion = DataIngestion()
        data_injestion.initiate_data_ingestion()
        logging.info("Data Ingestion Process Completed Successfully.")
        
    except Exception as e:
        logging.INFO("Custom Exception")
        raise CustomException(e,sys)