from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

database = create_engine("sqlite:///database.db")
database.connect()
