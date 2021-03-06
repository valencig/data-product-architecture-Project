# existe un bug con bot3 y luigi para pasar las credenciales
# necesitas enviar el parametro AWS_PROFILE e indicar el profile
# con el que quieres que se corra
# PYTHONPATH='.' AWS_PROFILE=mge luigi --module ex3_luigi S3Task --local-scheduler ...
import luigi
import luigi.contrib.s3
import boto3
import pandas as pd
import os


class S3Task(luigi.Task):
    task_name = "EL"

    bucket = luigi.Parameter()


    def run(self):
        ses = boto3.session.Session(profile_name='gabster', region_name='us-west-2')
        s3_resource = ses.resource('s3')

        obj = s3_resource.Bucket(self.bucket)
        print(ses)
        
        #Extraccion de base de datos
        url = 'https://datos.cdmx.gob.mx/explore/dataset/afluencia-diaria-del-metro-cdmx/download/?format=csv&refine.ano=2019&refine.linea=Linea+3&refine.estacion=Potrero&timezone=America/Mexico_City&lang=es&use_labels_for_header=true&csv_separator=%2C'
        file = pd.read_csv(url)

        with self.output().open('w') as output_file:
            file.to_csv(output_file)


    def output(self):
        output_path = "s3://{}/{}/bd.csv".\
        format(self.bucket,
        self.task_name)

        #return luigi.local_target.LocalTarget('/home/silil/Documents/itam/metodos_gran_escala/data-product-architecture/luigi/test.csv')
        return luigi.contrib.s3.S3Target(path=output_path) 
