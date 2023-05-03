from sqlalchemy import create_engine, MetaData 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json


username = os.getenv('db_username')#config["database_username"]
password = os.getenv("db_password")#config["database_password"]
hostname = os.getenv("db_host")#config["database_hostname"]
port = os.getenv("db_port")#config["database_port"]
dbname = os.getenv("db_name")#config["database_name"]
# pem_file = os.getenv("db_pem")#config["database_pem"]
pemm_file = os.getenv("dbpem")
ssl_arg = {"ssl_ca":pemm_file}


# Creating engine to connect to the database in Azure
engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{dbname}", connect_args=ssl_arg)

# Instance for the datbase session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# conn = engine.connect()
# meta_data = MetaData()
# print(config)Backend/CONFIG/DigiCertGlobalRootCA.crt.pem