#!/usr/bin/env python

import boto.ec2.elb
import ConfigParser
import os.path
import sys
from optparse import OptionParser

check = os.path.isfile(os.path.expanduser('~/.aws.conf'))
if cmp(check,False) == 0:
  print "~/.aws.conf is missing"
  sys.exit(2)
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.aws.conf'))
id = config.get("AWS", "consumer_key", raw=True)
key = config.get("AWS", "consumer_secret", raw=True)

parser = OptionParser()
parser.add_option("-r", "--region", dest="region", help="Region to be connected", metavar="REGION_NAME")
parser.add_option("-l", "--elb", dest="elb", help="elb name", metavar="ELB_NAME")
parser.add_option("-c", "--critical", dest="critical", help="The critical threshold in percentage, without '%' symbol.", metavar="CRITICAL")
parser.add_option("-w", "--warning", dest="warning", help="The warning threshold in percentage, without '%' symbol.", metavar="WARNING")
(options, args) = parser.parse_args()

conn = boto.ec2.elb.connect_to_region(options.region,aws_access_key_id=id,aws_secret_access_key=key)

status=conn.describe_instance_health(options.elb)
instance_list=str(status)[1:-1].split(', ')
print instance_list
bad=0
for instance in instance_list:
  if instance[-10:-1] != 'InService':
    bad=bad+1
if bad*100.0/len(instance_list) < options.warning:
  sys.exit(0)
elif bad*100.0/len(instance_list) < options.critical:
  sys.exit(1)
elif bad*100.0/len(instance_list) > options.critical:
  sys.exit(2)
else:
  sys.exit(3)
