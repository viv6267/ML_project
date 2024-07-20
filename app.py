from src.machine_learning_ops.logger import logging
from src.machine_learning_ops.exception import CustomException
import sys

if __name__=='__main__':
    logging.info("The execution has started.")

    try:
        a=1/0 
    except Exception as e:
        logging.INFO("Custom Exception")
        raise CustomException(e,sys)