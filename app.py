from src.machine_learning_ops.logger import logging
from src.machine_learning_ops.exception import CustomException
import sys
from src.machine_learning_ops.components.data_ingestion import DataIngestion
from src.machine_learning_ops.components.data_transformation import DataTransformation

if __name__=='__main__':
    logging.info("The execution has started.")

    try:
        data_injestion = DataIngestion()
        train_data_path,test_data_path=data_injestion.initiate_data_ingestion()
        # logging.info("Data Ingestion Process Completed Successfully.")

        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(train_data_path,test_data_path)
        logging.info("Data Transformation Process Completed Successfully.")
        
    except Exception as e:
        logging.INFO("Custom Exception")
        raise CustomException(e,sys)