#
# Basic example for reading file body in S3 (assuming it's textual)
#
import boto3
#
bucket="mybucket"
prefix="path/subpath"
object="file.dat"
access_key_id="AWSACCESSKEYID"
secret_key ="AWSSECRETKEY"
region="eu-west-1"
s3client=boto3.client('s3',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_key)
s3resource=boto3.resource('s3',region_name=region,aws_access_key_id=access_key_id,aws_secret_access_key=secret_key)
obj=s3client.get_object(Bucket=bucket,Key=prefix+'/'+object)
ocontent=obj['Body'].read()
print(ocontent.decode("utf-8"))
