import luigi
import boto3
import json
import psycopg2
import pandas as pd
from luigi.contrib.postgres import CopyToTable
from extract import extractToJson



class metadataExtract(CopyToTable):
    """
    Function to load metadata from the extracting process from mexico city metro data set on the specified date. It
    uploads the data into the specified S3 bucket on AWS. Note: user MUST have the credentials to use the aws s3
    bucket. Requires extractToJson
    """
    #==============================================================================================================
    # Parameters
    #==============================================================================================================
    task_name = 'metadataExtract_task_02_02'
    date = luigi.Parameter()
    bucket = luigi.Parameter(default='dpaprojs3')
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
    table = 'raw.metadataextract'
    columns = ["fecha_ejecucion", "fecha_json", "usuario", "ip_ec2", "nombre_bucket", "columns_read"] # "status","recordid","fecha_de_registro"]
    port = creds.port[0]
    #=============================================================================================================
    
    
    def requires(self):
        return extractToJson(bucket=self.bucket,date=self.date)
    
    
    def rows(self):
        clientEC2 = boto3.client('ec2')
        information_metadata_ours = clientEC2.describe_instances()
        fecha_ejecucion = pd.Timestamp.now()
        fecha_json = self.date
        usuario = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('KeyName')
        ip_ec2 = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('PrivateIpAddress')
        nombre_bucket = self.bucket
        
        with self.input().open('r') as json_file:
            data = json.load(json_file)
            columns_read = data['nhits']
            status = 'Loaded'
            #datasetid = data['records'][0].get('datasetid')
            for line in data['records']:
                datasetid = line.get('datasetid')
                recordid = line.get('recordid')
                fecha_de_registro = line.get('record_timestamp')
                yield (fecha_ejecucion,fecha_json,usuario,ip_ec2,nombre_bucket, columns_read) # status,recordid,fecha_de_registro)


#
#        # Esta línea lee el archivo especificado en content_object
#        #file_content = content_object.get()['Body'].read().decode('utf-8')
#        #columns_read = content_object.get()['Body'].read().decode('utf-8')['facet_groups']['facets']['count']
#        print("contenido leído exitosamente")
#        # Carga el Json content desde el archivo leído de la S3 Bucket
#        #json_content = json.loads(file_content)
#        print("contenido cargado exitosamente")
#
#        # Inicializa el data frame que se va a meter la información de los metadatos
##        df = pd.DataFrame(columns=["fecha_ejecucion", "fecha_json", "usuario", "ip_ec2", "ruta_bucket", "status", "columns_read"])
#        
#        #función de EC2 para describir la instancia en la que se está trabajando
#        information_metadata_ours = clientEC2.describe_instances()
#        print("ec2 descrita correctamente")
#        
#        
#        
#        # Columns read indica la cantidad de columnas leidas
#        columns_read = 196 # len(json_content['records'])
#        fecha_ejecucion = pd.Timestamp.now()
#        user = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('KeyName')
#        fecha_json = self.date
#        ip_ec2 = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('PrivateIpAddress')
#        nombre_bucket = self.bucket
#        status = 'Loaded'
#        print("variables a cargar listas")



if __name__ == '__main__':
    luigi.metadataExtract()    
    
    
    
#    def rows(self):
#        """
#        Return/yield tuples or lists corresponding to each row to be inserted.
#        """        
#        with self.input().open('w') as json_file:
#            json.dump(data_raw.json(), json_file)
#        
##        with self.input().open('r') as json_file:
##            for line in json_file:
##                yield line.strip('\n').split('\t')
##                
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Carga de metadatos de Extract completada! :)")
#        
#        
#        #Se conecta a la postgres en el RDS con las credenciales correspondientes
##        connection = psycopg2.connect(user=creds.user[0],
##                                      password=creds.password[0],
##                                      host=creds.host[0],
##                                      port=creds.port[0],
##                                      database=creds.db[0])
##
##
##        # Allows Python code to execute PostgreSQL command in a database session.
##        cursor = connection.cursor()
##        
##
##        # Inserta los metadatos en la tabla metadata_extract
##        text = "INSERT INTO raw.metadataextract  VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
##        user,fecha_ejecucion, fecha_json,ip_ec2, nombre_bucket, columns_read)
##        print(text)
##        
##        cursor.execute(text) #Execute a database operation (query or command).
##
##        
##        connection.commit() # This method sends a COMMIT statement to the MySQL server, committing the current transaction. 
##        cursor.close()# Close the cursor now (rather than whenever del is executed). The cursor will be unusable from this point forward
##        connection.close() # For a connection obtained from a connection pool, close() does not actually close it but returns it to the pool and makes it available for subsequent connection requests.
##        print("#...")
##        print("##...")
##        print("###...")
##        print("####...")
##        print("#####...")
##        print("######...")
##        print("Carga de metadatos de Extract completada! :)")
#        
#        # para los outputs que no vamos a usar
##        vacio = ' '
##        data_vacia = {'vacio':[vacio]}
##        pandas_a_csv = pd.DataFrame(data=data_vacia)
##        pandas_a_csv.to_csv(self.output().path, index=False)
##        #with self.output().open('w') as json_file:
##        #    json.dump(data_raw.json(), json_file)
##
##    
##    # Envía el output al S3 bucket especificado con el nombre de output_path
##    def output(self):
##        output_path = "s3://{}/{}/metro_{}.csv". \
##            format(self.bucket, self.task_name, self.date) #Formato del nombre para el json que entra al bucket S3
##        return luigi.contrib.s3.S3Target(path=output_path)
#
#    
#   
#   

#class CopyToTable(rdbms.CopyToTable):
#    """
#    Template task for inserting a data set into Postgres
#
#    Usage:
#    Subclass and override the required `host`, `database`, `user`,
#    `password`, `table` and `columns` attributes.
#
#    To customize how to access data from an input task, override the `rows` method
#    with a generator that yields each row as a tuple with fields ordered according to `columns`.
#    """
#
#    def rows(self):
#        """
#        Return/yield tuples or lists corresponding to each row to be inserted.
#        """
#        with self.input().open('r') as fobj:
#            for line in fobj:
#                yield line.strip('\n').split('\t')
#
#
#    def map_column(self, value):
#        """
#        Applied to each column of every row returned by `rows`.
#
#        Default behaviour is to escape special characters and identify any self.null_values.
#        """
#        if value in self.null_values:
#            return r'\\N'
#        else:
#            return default_escape(six.text_type(value))
#
#
## everything below will rarely have to be overridden
#
#    def output(self):
#        """
#        Returns a PostgresTarget representing the inserted dataset.
#
#        Normally you don't override this.
#        """
#        return PostgresTarget(
#            host=self.host,
#            database=self.database,
#            user=self.user,
#            password=self.password,
#            table=self.table,
#            update_id=self.update_id,
#            port=self.port
#        )
#
#
#    def copy(self, cursor, file):
#        if isinstance(self.columns[0], six.string_types):
#            column_names = self.columns
#        elif len(self.columns[0]) == 2:
#            column_names = [c[0] for c in self.columns]
#        else:
#            raise Exception('columns must consist of column strings or (column string, type string) tuples (was %r ...)' % (self.columns[0],))
#        cursor.copy_from(file, self.table, null=r'\\N', sep=self.column_separator, columns=column_names)
#
#
#    def run(self):
#        """
#        Inserts data generated by rows() into target table.
#
#        If the target table doesn't exist, self.create_table will be called to attempt to create the table.
#
#        Normally you don't want to override this.
#        """
#        if not (self.table and self.columns):
#            raise Exception("table and columns need to be specified")
#
#        connection = self.output().connect()
#        # transform all data generated by rows() using map_column and write data
#        # to a temporary file for import using postgres COPY
#        tmp_dir = luigi.configuration.get_config().get('postgres', 'local-tmp-dir', None)
#        tmp_file = tempfile.TemporaryFile(dir=tmp_dir)
#        n = 0
#        for row in self.rows():
#            n += 1
#            if n % 100000 == 0:
#                logger.info("Wrote %d lines", n)
#            rowstr = self.column_separator.join(self.map_column(val) for val in row)
#            rowstr += "\n"
#            tmp_file.write(rowstr.encode('utf-8'))
#
#        logger.info("Done writing, importing at %s", datetime.datetime.now())
#        tmp_file.seek(0)
#
#        # attempt to copy the data into postgres
#        # if it fails because the target table doesn't exist
#        # try to create it by running self.create_table
#        for attempt in range(2):
#            try:
#                cursor = connection.cursor()
#                self.init_copy(connection)
#                self.copy(cursor, tmp_file)
#                self.post_copy(connection)
#                if self.enable_metadata_columns:
#                    self.post_copy_metacolumns(cursor)
#            except psycopg2.ProgrammingError as e:
#                if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE and attempt == 0:
#                    # if first attempt fails with "relation not found", try creating table
#                    logger.info("Creating table %s", self.table)
#                    connection.reset()
#                    self.create_table(connection)
#                else:
#                    raise
#            else:
#                break
#
#        # mark as complete in same transaction
#        self.output().touch(connection)
#
#        # commit and clean up
#        connection.commit()
#        connection.close()
#        tmp_file.close()
#
#
#












############################################################# METADATA  EXTRACT TASK ##################################
#class metadataExtract(luigi.Task):
#    """
#    Function to load metadata from the extracting process from mexico city metro data set on the specified date. It
#    uploads the data into the specified S3 bucket on AWS. Note: user MUST have the credentials to use the aws s3
#    bucket. Requires extractToJson
#    """
#    #==============================================================================================================
#    # Parameters
#    #==============================================================================================================
#    task_name = 'metadataExtract_task_02_02'
#    date = luigi.Parameter()
#    bucket = luigi.Parameter(default='dpaprojs3') # default='dpaprojs3')
#    #==============================================================================================================
#
#    # Indica que para iniciar el proceso de carga de metadatos requiere que el task de extractToJson esté terminado
#    def requires(self):
#        return extractToJson(self.bucket,self.date)
#
#    # Esta sección indica lo que se va a correr:
#    def run(self):
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Inicia la carga de los metadatos del extract...")
#
#        # Lee nuevamente el archivo JSON que se subió al S3 bucket, para después obtener metadatos sobre la carga
#        file_to_read = 'extractToJson_task_01/metro_'+ self.date +'.json'
#        print("El archivo a buscar es: ",file_to_read)
#
#        #Lee las credenciales de los archivos correspondientes
#        creds = pd.read_csv("../../credentials_postgres.csv")
#        creds_aws = pd.read_csv("../../credentials.csv")
#        print('Credenciales leídas correctamente')
#
#        # Conexión a la S3
#        ses = boto3.session.Session(profile_name='rafael-dpa-proj') #, region_name='us-west-2') # Pasamos los parámetros apra la creación del recurso S3 (bucket) al que se va a conectar
#        s3_resource = ses.resource('s3') # Inicialzamos e recursoS3
#        obj = s3_resource.Bucket(self.bucket) # Metemos el bucket S3 en una variable obj
#        dev_s3_client = ses.client('s3')
#
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Conectando al S3 Bucket...")
#        # Obtiene el acceso al S3 Bucket con las credenciales correspondientes. Utiliza la paquetería boto3
#        
#        # Metemos el ec2 y el s3 actuales en un objeto, para poder obtener sus metadatos
#        clientEC2 = boto3.client('ec2')
#        clientS3 = boto3.client('s3')
#        print("Inicializados el EC2 y el S3")
#
#        # El content object está especificando el objeto que se va a extraer del bucket S3
#        # (la carga que se acaba de hacer desde la API)
#        content_object = s3_resource.Object(self.bucket, file_to_read)
#        print("s3 encontrada exitosamente")
#
#        # Esta línea lee el archivo especificado en content_object
#        #file_content = content_object.get()['Body'].read().decode('utf-8')
#        #columns_read = content_object.get()['Body'].read().decode('utf-8')['facet_groups']['facets']['count']
#        print("contenido leído exitosamente")
#        # Carga el Json content desde el archivo leído de la S3 Bucket
#        #json_content = json.loads(file_content)
#        print("contenido cargado exitosamente")
#
#        # Inicializa el data frame que se va a meter la información de los metadatos
##        df = pd.DataFrame(columns=["fecha_ejecucion", "fecha_json", "usuario", "ip_ec2", "ruta_bucket", "status", "columns_read"])
#        
#        #función de EC2 para describir la instancia en la que se está trabajando
#        information_metadata_ours = clientEC2.describe_instances()
#        print("ec2 descrita correctamente")
#        
#        
#        
#        # Columns read indica la cantidad de columnas leidas
#        columns_read = 196 # len(json_content['records'])
#        fecha_ejecucion = pd.Timestamp.now()
#        user = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('KeyName')
#        fecha_json = self.date
#        ip_ec2 = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('PrivateIpAddress')
#        nombre_bucket = self.bucket
#        status = 'Loaded'
#        print("variables a cargar listas")
#        
##        client.get('Reservations')[0].get('Instances')[0].get('KeyName')
#
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Conectandose a la instancia RDS con los datos RAW...")
#        #Se conecta a la postgres en el RDS con las credenciales correspondientes
#        connection = psycopg2.connect(user=creds.user[0],
#                                      password=creds.password[0],
#                                      host=creds.host[0],
#                                      port=creds.port[0],
#                                      database=creds.db[0])
#
#
#        # Allows Python code to execute PostgreSQL command in a database session.
#        cursor = connection.cursor()
#        
#
#        # Inserta los metadatos en la tabla metadata_extract
#        text = "INSERT INTO raw.metadataextract  VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
#        user,fecha_ejecucion, fecha_json,ip_ec2, nombre_bucket, columns_read)
#        print(text)
#        
#        cursor.execute(text) #Execute a database operation (query or command).
#
#        
#        connection.commit() # This method sends a COMMIT statement to the MySQL server, committing the current transaction. 
#        cursor.close()# Close the cursor now (rather than whenever del is executed). The cursor will be unusable from this point forward
#        connection.close() # For a connection obtained from a connection pool, close() does not actually close it but returns it to the pool and makes it available for subsequent connection requests.
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Carga de metadatos de Extract completada! :)")
#        
#        # para los outputs que no vamos a usar
#        vacio = ' '
#        data_vacia = {'vacio':[vacio]}
#        pandas_a_csv = pd.DataFrame(data=data_vacia)
#        pandas_a_csv.to_csv(self.output().path, index=False)
#        #with self.output().open('w') as json_file:
#        #    json.dump(data_raw.json(), json_file)
#
#    
#    # Envía el output al S3 bucket especificado con el nombre de output_path
#    def output(self):
#        output_path = "s3://{}/{}/metro_{}.csv". \
#            format(self.bucket, self.task_name, self.date) #Formato del nombre para el json que entra al bucket S3
#        return luigi.contrib.s3.S3Target(path=output_path)
#
#
#











































############################################################################################################################################################

#class metadataExtract(luigi.Task):
#    """
#    Function to load metadata from the extracting process from mexico city metro data set on the specified date. It
#    uploads the data into the specified S3 bucket on AWS. Note: user MUST have the credentials to use the aws s3
#    bucket. Requires extractToJson
#    """
#    #==============================================================================================================
#    # Parameters
#    #==============================================================================================================
#    task_name = 'metadataExtract_task_02_02'
#    date = luigi.Parameter()
#    bucket = luigi.Parameter(default='dpaprojs3') # default='dpaprojs3')
#    #==============================================================================================================
#
#    # Indica que para iniciar el proceso de carga de metadatos requiere que el task de extractToJson esté terminado
#    def requires(self):
#        return extractToJson(self.bucket,self.date)
#
#    # Esta sección indica lo que se va a correr:
#    def run(self):
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Inicia la carga de los metadatos del extract...")
#
#        # Lee nuevamente el archivo JSON que se subió al S3 bucket, para después obtener metadatos sobre la carga
#        file_to_read = 'extractToJson_task_01/metro_'+ self.date +'.json'
#        print("El archivo a buscar es: ",file_to_read)
#
#        #Lee las credenciales de los archivos correspondientes
#        creds = pd.read_csv("../../credentials_postgres.csv")
#        creds_aws = pd.read_csv("../../credentials.csv")
#        print('Credenciales leídas correctamente')
#
#        # Conexión a la S3
#        ses = boto3.session.Session(profile_name='rafael-dpa-proj') #, region_name='us-west-2') # Pasamos los parámetros apra la creación del recurso S3 (bucket) al que se va a conectar
#        s3_resource = ses.resource('s3') # Inicialzamos e recursoS3
#        obj = s3_resource.Bucket(self.bucket) # Metemos el bucket S3 en una variable obj
#        dev_s3_client = ses.client('s3')
#
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Conectando al S3 Bucket...")
#        # Obtiene el acceso al S3 Bucket con las credenciales correspondientes. Utiliza la paquetería boto3
#        
#        # Metemos el ec2 y el s3 actuales en un objeto, para poder obtener sus metadatos
#        clientEC2 = boto3.client('ec2')
#        clientS3 = boto3.client('s3')
#        print("Inicializados el EC2 y el S3")
#
#        # El content object está especificando el objeto que se va a extraer del bucket S3
#        # (la carga que se acaba de hacer desde la API)
#        content_object = s3_resource.Object(self.bucket, file_to_read)
#        print("s3 encontrada exitosamente")
#
#        # Esta línea lee el archivo especificado en content_object
#        #file_content = content_object.get()['Body'].read().decode('utf-8')
#        #columns_read = content_object.get()['Body'].read().decode('utf-8')['facet_groups']['facets']['count']
#        print("contenido leído exitosamente")
#        # Carga el Json content desde el archivo leído de la S3 Bucket
#        #json_content = json.loads(file_content)
#        print("contenido cargado exitosamente")
#
#        # Inicializa el data frame que se va a meter la información de los metadatos
##        df = pd.DataFrame(columns=["fecha_ejecucion", "fecha_json", "usuario", "ip_ec2", "ruta_bucket", "status", "columns_read"])
#        
#        #función de EC2 para describir la instancia en la que se está trabajando
#        information_metadata_ours = clientEC2.describe_instances()
#        print("ec2 descrita correctamente")
#        
#        
#        
#        # Columns read indica la cantidad de columnas leidas
#        columns_read = 196 # len(json_content['records'])
#        fecha_ejecucion = pd.Timestamp.now()
#        user = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('KeyName')
#        fecha_json = self.date
#        ip_ec2 = information_metadata_ours.get('Reservations')[0].get('Instances')[0].get('PrivateIpAddress')
#        nombre_bucket = self.bucket
#        status = 'Loaded'
#        print("variables a cargar listas")
#        
##        client.get('Reservations')[0].get('Instances')[0].get('KeyName')
#
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Conectandose a la instancia RDS con los datos RAW...")
#        #Se conecta a la postgres en el RDS con las credenciales correspondientes
#        connection = psycopg2.connect(user=creds.user[0],
#                                      password=creds.password[0],
#                                      host=creds.host[0],
#                                      port=creds.port[0],
#                                      database=creds.db[0])
#
#
#        # Allows Python code to execute PostgreSQL command in a database session.
#        cursor = connection.cursor()
#        
#
#        # Inserta los metadatos en la tabla metadata_extract
#        text = "INSERT INTO raw.metadataextract  VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
#        user,fecha_ejecucion, fecha_json,ip_ec2, nombre_bucket, columns_read)
#        print(text)
#        
#        cursor.execute(text) #Execute a database operation (query or command).
#
#        
#        connection.commit() # This method sends a COMMIT statement to the MySQL server, committing the current transaction. 
#        cursor.close()# Close the cursor now (rather than whenever del is executed). The cursor will be unusable from this point forward
#        connection.close() # For a connection obtained from a connection pool, close() does not actually close it but returns it to the pool and makes it available for subsequent connection requests.
#        print("#...")
#        print("##...")
#        print("###...")
#        print("####...")
#        print("#####...")
#        print("######...")
#        print("Carga de metadatos de Extract completada! :)")
#        
#        # para los outputs que no vamos a usar
#        vacio = ' '
#        data_vacia = {'vacio':[vacio]}
#        pandas_a_csv = pd.DataFrame(data=data_vacia)
#        pandas_a_csv.to_csv(self.output().path, index=False)
#        #with self.output().open('w') as json_file:
#        #    json.dump(data_raw.json(), json_file)
#
#    
#    # Envía el output al S3 bucket especificado con el nombre de output_path
#    def output(self):
#        output_path = "s3://{}/{}/metro_{}.csv". \
#            format(self.bucket, self.task_name, self.date) #Formato del nombre para el json que entra al bucket S3
#        return luigi.contrib.s3.S3Target(path=output_path)

if __name__ == '__main__':
    luigi.runAll()
    
    

