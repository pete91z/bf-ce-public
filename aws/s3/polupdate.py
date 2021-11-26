# Script to update a bucket policy. Use at your own risk and test against non-production first!
#
# Ensure you have created the boiler plate policy file nonprod_policy.json
# (use the template file and add your specific details)
#
# This script reads the boiler plate policy file and then replaces various elements based on your variables
#
# Tested against Python3.6.10
import json
import boto3
import datetime
#
# ****** Set variables here ******
#
ext=str(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"))
origpolfile = "pol_orig_"+ext
newpolfile = "pol_new_"+ext
#for the ip list, you can specify an array of different ips if required
arr_iplist = [ "my.accessing.ip.address/32" ]
target_bucket ="myCreatedS3Bucket"
prefix = [ "files/", "files/sub/"]
#
#main
#
s3 = boto3.client('s3')
if target_bucket == "":
   print ("Error, bucket name not set.")
   exit(1)

print("Starting policy update for "+target_bucket+"\n")
print("Backing up existing policy")
try:
    curpol = dict(s3.get_bucket_policy(Bucket=target_bucket))
except:
    print("Couldn't get bucket policy: "+str(getpolerr))
    curpol = {'Policy' : 'NONE'}

try:
    origout = open(origpolfile,'w')
    origout.write(json.dumps(curpol['Policy']))
    origout.close
    print ("Original Policy written to "+origpolfile)
except:
    print("Error writing original policy to file: "+str(origfileerr))
    exit(3)

print("\nSetting up new policy")
try:
    with open('nonprod_policy.json','r') as f:
        newpol = f.read()

    jsnewpol =(json.loads(newpol))
except:
    print("Unable to open policy template: "+str(templerr))
    exit(4)

try:
    print("Applying new policy to bucket")
    jsnewpol['Statement'][0]['Sid'] = "bcklist - "+ext
    jsnewpol['Statement'][0]['Condition']['IpAddress']['aws:SourceIp'] = arr_iplist
    jsnewpol['Statement'][0]['Condition']['StringEquals']['s3:prefix'] = prefix
    jsnewpol['Statement'][1]['Sid'] = "bckcontent - "+ext
    jsnewpol['Statement'][1]['Condition']['IpAddress']['aws:SourceIp'] = arr_iplist
    newout = open(newpolfile,'w')
    newout.write(json.dumps(jsnewpol))
    newout.close
except:
    print("Error setting IPs in policy: "+str(setpolerr))
    exit(6)

try:
    putbckresult = s3.put_bucket_policy(Bucket=target_bucket, Policy=json.dumps(jsnewpol)                           )
except:
    print("Error applying new policy to bucket: "+str(applypolerr))
    exit(7)

print("Complete")
