from sqlalchemy import create_engine, MetaData 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

with open("Backend/CONFIG/config.json") as f:
    config = json.load(f)

username = config["database_username"]
password = config["database_password"]
hostname = config["database_hostname"]
port = config["database_port"]
dbname = config["database_name"]
pem_file = config["database_pem"]
ssl_arg = {"ssl_ca":pem_file}

# Creating engine to connect to the database in Azure
engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{dbname}", connect_args=ssl_arg)

# Instance for the datbase session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# conn = engine.connect()
# meta_data = MetaData()
# print(config)