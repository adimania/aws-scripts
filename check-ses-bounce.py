#!/usr/bin/env python

import boto.ses
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
parser.add_option("-w", "--warning", dest="warning", help="The warning threshold", metavar="WARNING")
parser.add_option("-c", "--critical", dest="critical", help="The critical threshold", metavar="CRITICAL")
(options, args) = parser.parse_args()

conn=boto.ses.connect_to_region(options.region,aws_access_key_id=id,aws_secret_access_key=key)
stats=conn.get_send_statistics()
stats_sorted=sorted(stats['GetSendStatisticsResponse']['GetSendStatisticsResult']['SendDataPoints'],key=lambda timestamp: timestamp['Timestamp'])
latest=stats_sorted[-1]

print latest
bounce_percent=100*float(latest['Bounces'])/float(latest['DeliveryAttempts'])

if bounce_percent < int(options.warning):
  sys.exit(0)
elif bounce_percent > int(options.critical):
  sys.exit(2)
elif bounce_percent > int(options.warning):
  sys.exit(1)
else:
  sys.exit(3)

