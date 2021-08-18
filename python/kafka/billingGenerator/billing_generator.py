# Script to generate billing style data and send to both kafka topic (serialized as avro) and to text file. specify the number of messages and number of 
# files to spread the messages across (if you need to re-access the messages again later
#
# Python3
#
# This is a slimmed down version I used for generating test data, it omits the contact map field. Thus it may or may not error because of these changes
#
# Created: 18/08/2021
# peter.carpenter@blaqfire.com
#
#
import sys
import random
import uuid
import json
import datetime
import string
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import os
from confluent_kafka import Consumer, Producer
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# params
value_schema=avro.load('billing.avsc')
key_schema=avro.load('billing_key.avsc')
no_of_lines = int(sys.argv[1])
no_of_files = int(sys.argv[2])
landing_path=/tmp
#
def build_dict():
    rdict = {"BILLING_ID": str(uuid.uuid4()),
             "CATEGORY": random.choice(['MAINTENANCE','INSTALLATION','CONSULTANCY','LOGISTICS']),
             "ORIGIN": {"SITE": random.choice(['MAN','LIV','PET','BIR','LON','GLA','BRI']),"OPERATOR_ID": str(uuid.uuid4())},
             "MOVEMENT_TYPE": random.choice(['SALE','REFUND','CREDIT','DEBIT','CORRECTION']),
             "VALUE":round(random.uniform(0,10000),2),
             "TS": int(datetime.datetime.now().timestamp())
             }
    return rdict

print(str(datetime.datetime.now().strftime("%d-%m-%YT%H:%M:%S"))+" Generating "+str(no_of_lines)+" lines across "+str(no_of_files)+" files...")
lines = [build_dict() for x in range(no_of_lines) ]

#p = Producer({'bootstrap.servers': '127.0.0.1:9092'})
p = AvroProducer({'bootstrap.servers':'127.0.0.1:9092','schema.registry.url': 'http://127.0.0.1:8081'},default_value_schema=value_schema,default_key_schema=key_schema)
#p = AvroProducer({'bootstrap.servers':'127.0.0.1:9092','schema.registry.url': 'http://127.0.0.1:8081'},default_value_schema=value_schema)
for bil in lines:
    value=bil
    key={"Key": bil['BILLING_ID']}
    try:
        p.produce(topic='billing',key=key,value=value)
        print("Posted "+json.dumps(bil))
    except: 
        print("error posting "+json.dumps(bil))

p.poll(0)
p.flush()


files = [ landing_path+str(uuid.uuid4())+'_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S') for x in range(no_of_files) ]
file_handles = [ open(x,'w') for x in files ]
for line in lines:
    file_handles[random.randint(0,len(file_handles)-1)].write(json.dumps(line)+'\n')

for handle in file_handles:
    handle.close()

print(str(datetime.datetime.now().strftime("%d-%m-%YT%H:%M:%S"))+" Completed")

