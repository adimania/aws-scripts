#!/usr/bin/env python

import boto.ec2.cloudwatch
import ConfigParser
import os.path
import datetime
import sys
from optparse import OptionParser

check = os.path.isfile(os.path.expanduser('~/.aws.conf'))
if cmp(check,False) == 0:
    print "~/.aws.conf is missing"
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.aws.conf'))
id = config.get("AWS", "consumer_key", raw=True)
key = config.get("AWS", "consumer_secret", raw=True)

parser = OptionParser()
parser.add_option("-r", "--region", dest="region", help="Region to be connected", metavar="REGION_NAME")
parser.add_option("-m", "--metric-name", dest="metric", help="Metric to be monitored", metavar="METRIC_NAME")
parser.add_option("-w", "--warning", dest="warning", help="The warning threshold", metavar="WARNING")
parser.add_option("-c", "--critical", dest="critical", help="The critical threshold", metavar="CRITICAL")
(options, args) = parser.parse_args()

conn=boto.ec2.cloudwatch.connect_to_region(options.region,aws_access_key_id=id, aws_secret_access_key=key)

datapoint=conn.get_metric_statistics(60,datetime.datetime.utcnow() - datetime.timedelta(seconds=300), datetime.datetime.utcnow(), options.metric, 'AWS/RDS', 'Minimum')
sorted(datapoint,key=lambda data: data['Timestamp'].minute)
data=datapoint[-1]
print data
if data['Minimum'] > int(options.warning):
  sys.exit(0)
elif data['Minimum'] > int(options.critical):
  sys.exit(1)
elif data['Minimum'] < int(options.critical):
  sys.exit(2)
else:
  sys.exit(3)

