#
# Create / overwrite a Hudi table in the datalake store using all rows from the person table in the hr database
#
# This script demonstrates how to connect to a postgres database and retrieve rows from a table called person,
# and then load this into a hudi table in S3. It is intended for research/educational/testing purposes.
# Please not that normally you should not expose S3 credentials in plain text scripts, rather these should be
# part of your spark server config or accessed securely.
#
# This will require the hudi-spark-bundle jars, aws-java-sdk, and spark avro to be in the classpath
#
# Created: 16/02/2021 
# Requirements: Python3 - Spark 2.4.0 - Hudi 0.7.0 - postgresql-42.2.16 - pyspark
# by: Pete Carpenter
#
from pyspark import SparkContext
from pyspark import SparkConf
import boto3
#example script showing how to read from a database and write the results to a parquet file in s3
#spark conf
conf = SparkConf()
conf.setMaster('spark://<SPARK MASTER IP>:7077')
conf.setAppName('DL_Person_Load_To_Hudi')

sc = SparkContext(conf=conf)
sc._conf.set("fs.s3a.access.key", "<AWS IAM USER ACCESS ID>")
sc._conf.set("fs.s3a.secret.key", "<AWS IAM USER SECRET KEY>")
sc._conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "<AWS IAM USER ACCESS ID>")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "<AWS IAM USER SECRET KEY>")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

properties = {
    "driver": "org.postgresql.Driver",
    "user": "<DATABASE USER>",
    "password":"<DATABASE PASSWORD>"
}
url = 'jdbc:postgresql://<POSTGRES SERVER>:5432/<DB>'
df = sqlContext.read.jdbc(url=url, table='hr.person', properties=properties)
df.createOrReplaceTempView("vw_person")
df1 = sqlContext.sql("select * from vw_person")
df1.show()


tableName = "person"
basePath = "s3a://<S3 bucket>/person"
hudi_options = {
  'hoodie.table.name': tableName,
  'hoodie.datasource.write.recordkey.field': 'id',
  'hoodie.datasource.write.partitionpath.field': 'gender',
  'hoodie.datasource.write.table.name': tableName,
  'hoodie.datasource.write.operation': 'insert',
  'hoodie.datasource.write.precombine.field': 'last_update_date',
  'hoodie.upsert.shuffle.parallelism': 2, 
  'hoodie.insert.shuffle.parallelism': 2
}

df1.write.format("hudi"). \
  options(**hudi_options). \
  mode("overwrite"). \
  save(basePath)
