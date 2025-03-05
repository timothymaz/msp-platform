import os
import boto3

ssm = boto3.client('ssm')
response = ssm.get_parameter(Name="DATABASE_URL", WithDecryption=True)
DATABASE_URL = response['Parameter']['Value']

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
