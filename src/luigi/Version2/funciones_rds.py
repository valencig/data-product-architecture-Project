import os
import psycopg2
import sqlalchemy
import pandas as pd
import pandas.io.sql as psql
from sqlalchemy import create_engine

#creds = pd.read_csv("../../../credentials_postgres.csv")
#host = creds['host'][0]
#database = creds['database'][0]
#user = creds['user'][0]
#password = creds['password'][0]
#table = 'raw.metro' 
#port = creds['port'][0]

def dbaspandas():
    creds = pd.read_csv("../../../credentials_postgres.csv")
    connection = psycopg2.connect(user=creds.user[0],
                          password=creds.password[0],
                          host=creds.host[0],
                          port=creds.port[0],
                          database=creds.db[0])
    cursor = connection.cursor()
    
    df = psql.read_sql('SELECT * FROM raw.metro;', connection)
    print(df.head())
    # close connection
    cursor.close()
    connection.close()
    print(len(df))
    return len(df)

def tiposDBcleaned():
    creds = pd.read_csv("../../../credentials_postgres.csv")
    connection = psycopg2.connect(user=creds.user[0],
                          password=creds.password[0],
                          host=creds.host[0],
                          port=creds.port[0],
                          database=creds.db[0])
    cursor = connection.cursor()
    
    df = psql.read_sql("""SELECT column_name, data_type FROM information_schema.columns 
                       WHERE table_schema = 'cleaned' AND table_name = 'metro';""", connection)
    print(df.head())
    # close connection
    cursor.close()
    connection.close()
    print("debuggeando tiposDBcleaned regresa el dataframe")
    print(df)
    return df

def columnasFeatureEngineering():
    creds = pd.read_csv("../../../credentials_postgres.csv")
    connection = psycopg2.connect(user=creds.user[0],
                          password=creds.password[0],
                          host=creds.host[0],
                          port=creds.port[0],
                          database=creds.db[0])
    cursor = connection.cursor()
    
    df = psql.read_sql("""SELECT * FROM semantic.metro;""", connection)
    print(df.head())
    numero_de_columnas = len(df.columns)
    print("numero de columnas funciones_rds:", numero_de_columnas )
    
    
    # close connection
    cursor.close()
    connection.close()
    return numero_de_columnas

def obtienePrediccionesdeldia(fecha):
    creds = pd.read_csv("../../../credentials_postgres.csv")
    connection = psycopg2.connect(user=creds.user[0],
                          password=creds.password[0],
                          host=creds.host[0],
                          port=creds.port[0],
                          database=creds.db[0])
    cursor = connection.cursor()
    
    query = """SELECT * FROM predict.metro WHERE fecha = '{fecha}' ;""".format(fecha=fecha)
    
    df = psql.read_sql(query, connection)
    print(df.head())
    numero_de_columnas = len(df.columns)
    print("numero de columnas funciones_rds:", numero_de_columnas )
    
    
    # close connection
    cursor.close()
    connection.close()
    return numero_de_columnas


#class conectaAtablaRawMetro(object):
#    
#    def __init__(self): #host,database,user,password,table,port):
#        creds = pd.read_csv("../../../credentials_postgres.csv")
#        #self.host = host
#        #self.database = database
#        #self.user = user
#        #self.password = password
#        #self.table = table
#        #self.port = port
#        
#        
#    def dbaspandas(self):
#        creds = pd.read_csv("../../../credentials_postgres.csv")
#        connection = psycopg2.connect(user=creds.user[0],
#                              password=creds.password[0],
#                              host=creds.host[0],
#                              port=creds.port[0],
#                              database=creds.database[0])
#        cursor = connection.cursor()
#        
#        df = psql.read_sql('SELECT * FROM raw.metro;', connection)
#        print(df.head())
#        # close connection
#        cursor.close()
#        connection.close()
#        print(len(df))
#        return len(df)
#        
#    
#class conectaAtablaCleanedMetro(object):
#    
#    def __init__(self,host,database,user,password,table,port):
#        creds = pd.read_csv("../../../credentials_postgres.csv")
#        self.host = creds.host[0]
#        self.database = creds.database[0]
#        self.user = creds.user[0]
#        self.password = creds.password[0]
#        self.table = 'cleaned.metro' 
#        self.port = creds.port[0]
#        
#        
#    def dbaspandas(self):
#        creds = pd.read_csv("../../../credentials_postgres.csv")
#        connection = psycopg2.connect(user=creds.user[0],
#                              password=creds.password[0],
#                              host=creds.host[0],
#                              port=creds.port[0],
#                              database=creds.database[0])        
#        
#        
#        
#        #connection = psycopg2.connect(user=self.user,
#        #                      password=self.password,
#        #                      host=self.host,
#        #                      port=self.port,
#        #                      database=self.database)
#        cursor = connection.cursor()
#        
#        df = psql.read_sql('SELECT * FROM cleaned.metro;', connection)
#        # close connection
#        cursor.close()
#        connection.close()
#        return df
#    
#    
#    