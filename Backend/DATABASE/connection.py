from sqlalchemy import create_engine, MetaData 
import os
import json

with open("./config.json") as f:
    config = json.load(f)

username = config["database_username"]
password = config["database_password"]
hostname = config["database_hostname"]
port = config["database_port"]
dbname = config["database_name"]
pem_file = config["database_pem"]
ssl_arg = {"ssl_ca":pem_file}

engine = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{dbname}", connect_args=ssl_arg)

conn = engine.connect()
meta_data = MetaData()
# print(config)
