import sqlalchemy
import os

DATABASE = os.getenv('DATABASE')
PASSWORD = os.getenv('PASSWORD')
USER = os.getenv('USER')
HOSTNAME = 'mysql'

def get_connection():
	dbConn = sqlalchemy.create_engine('mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)) # connect to server
	return dbConn

def get_connection_string():
	return 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)

def create_db(db_name=None):
	if db_name!=None:
		dbConn=get_connection()
		dbConn.execute("CREATE DATABASE IF NOT EXISTS %s "%(db_name))
		return True
	else:
		return "DB name should be provided"
