polupdate.py script updates a bucket policy, and allows
you to specify a whitelist of external IPs and prefix restriction.
It has been designed for work a single user, so for multi user policies
you will need to amend the script.

It has been developed against python 3.6.10

Configuration
=============

1. copy nonprod_policy.json_template to nonprod_policy.json
2. update nonprod_policy.json to specify the AWS account ID, IAM user you are granting access for
   and the S3 bucket.
   
To execute, simply run python3 polupdate.py