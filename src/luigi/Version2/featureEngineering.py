import luigi
import logging
import psycopg2
import sqlalchemy

import pandas.io.sql as psql
import pandas as pd

from sqlalchemy import create_engine
from luigi.contrib.postgres import PostgresQuery, PostgresTarget

import feature_builder as fb
from loadCleaned import loadCleaned

logger = logging.getLogger('luigi-interface')
##############################################################      SEMANTIC       ####################################

############################################################## FEATURE ENGINEERING ####################################

class featureEngineering(PostgresQuery):
    """
    Function to load metadata from the extracting process from mexico city metro data set on the specified date. It
    uploads the data into the specified S3 bucket on AWS. Note: user MUST have the credentials to use the aws s3
    bucket. Requires extractToJson
    """

    #==============================================================================================================
    # Parameters
    #==============================================================================================================
    task_name = 'feature_engineering_04_01'
    date = luigi.Parameter()
    bucket = luigi.Parameter(default='dpaprojs3') # default='dpaprojs3')
    #==============================================================================================================
    # Parameters for database connection
    #==============================================================================================================
    creds = pd.read_csv("../../../credentials_postgres.csv")
    creds_aws = pd.read_csv("../../../credentials.csv")
    print('Credenciales leídas correctamente')
    host = creds.host[0]
    database = creds.db[0]
    user = creds.user[0]
    password = creds.password[0]
    table = 'semantic.metro'
    port = creds.port[0]
    query = """SELECT * FROM semantic.metro;"""
    #=============================================================================================================
    # Indica que para iniciar el proceso de carga de metadatos requiere que el task de extractToJson esté terminado
    def requires(self):
        return loadCleaned(bucket=self.bucket, date=self.date) # , metadataCleaned(bucket = self.bucket, date=  self.date)


    def run(self):
        connection = self.output().connect()
        connection.autocommit = self.autocommit
        cursor = connection.cursor()
        
        df = psql.read_sql('SELECT * FROM semantic.metro;', connection)
        df2 = fb.FeatureBuilder()
        df2 = df2.featurize(df)
        print(df2.shape)
        
        engine = create_engine('postgresql+psycopg2://postgres:12345678@database-1.cqtrfcufxibu.us-west-2.rds.amazonaws.com:5432/dpa')
        #engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'). \
        #    format(self.user,self.password, self.host, self.port,self.database)
        print("ya pasó engine")
        table_name= self.table
        print(table_name)
        scheme='semantic'
        print(scheme)
        df2.to_sql("metro", con=engine, schema='semantic',if_exists='replace')
        print(psql.read_sql('SELECT * FROM semantic.metro LIMIT 10;', connection))
        sql = self.query
        print(sql)
        logger.info('Executing query from task: {name}'.format(name=self.task_name))
        cursor.execute(sql)
        
        
        self.output().touch(connection)

        # commit and close connection
        cursor.close()
        connection.commit()
        connection.close()
        
        
    def output(self):
        """
        Returns a PostgresTarget representing the executed query.

        Normally you don't override this.
        """
        return PostgresTarget(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            table=self.table,
            update_id=self.update_id,
            port=self.port
        )

if __name__ == '__main__':
    luigi.featureEngineering()

