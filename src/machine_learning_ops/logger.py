import logging
import os
from datetime import datetime

timestamp=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(os.getcwd(),"logs",timestamp)
os.makedirs(log_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(log_path,timestamp)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)