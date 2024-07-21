import os
import sys
import pandas as pd
from src.machine_learning_ops.exception import CustomException
from src.machine_learning_ops.logger import logging
from dotenv import load_dotenv
import pymysql

load_dotenv()
host=os.getenv("host")
user=os.getenv("user")
passwd=os.getenv("password")
db=os.getenv("db")

def read_sql_data():
    logging.info("Reading SQL database started")
    try:
        mydb=pymysql.connect(
            host=host, 
            user=user, 
            passwd=passwd,
            db=db
        )
        logging.info("Connection Established",mydb)
        df=pd.read_sql_query('select * from student_table',mydb)
        print(df.head())

        return df

    except Exception as e:
        raise CustomException(e,sys)

