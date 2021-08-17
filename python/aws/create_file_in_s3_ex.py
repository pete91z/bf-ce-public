#
# Basic example for creating a new file in S3 (not putting an existing local one)
#
import boto3
#
bucket="mybucket"
prefix="path/subpath"
object="file.txt"
access_key_id="ACCESSKEYID"
secret_key ="SECRETKEY"
region="eu-west-1"
s3client=boto3.client('s3',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_key)
s3resource=boto3.resource('s3',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_key)
contents = """
1|'Pete'|'Flannagan'|'1973-02-23'|0|'TN130578M'\n
2|'Tom'|'Davids'|'1982-07-31'|0|'TN456322T'\n
3|'Sally'|'Robinson'|'1985-09-31'|0|'TN130422X'\n
4|'Alison'|'Smith'|'1975-09-31'|0|'TN130823U'
"""
obj = s3resource.Object(bucket, prefix+'/'+object)
obj.put(Body=bytes(contents,'utf-8'))
