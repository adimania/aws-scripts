import boto
import boto.ec2
import ConfigParser
import os.path
import sys
import datetime
from optparse import OptionParser

check = os.path.isfile(os.path.expanduser('~/.aws.conf'))
if cmp(check,False) == 0:
    print Description
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.aws.conf'))
id = config.get("AWS", "consumer_key", raw=True)
key = config.get("AWS", "consumer_secret", raw=True)

parser = OptionParser()
parser.add_option("-i", "--instance", dest="instance", help="Instance id of the instance.", metavar="INSTANCE_ID")
parser.add_option("-a", "--associate", dest="assoc", help="IP address to associate.", metavar="IP_ADDR")
parser.add_option("-d", "--disassociate", dest="disassoc", help="IP address to disassociate.", metavar="IP_ADDR")
parser.add_option("-r", "--region", dest="region", help="Region to be connected", metavar="REGION_NAME")
(options, args) = parser.parse_args()

region_obj = boto.ec2.get_region(options.region,aws_access_key_id=id,aws_secret_access_key=key)

conn = boto.connect_ec2(aws_access_key_id=id,aws_secret_access_key=key,region=region_obj)

if options.assoc:
  conn.associate_address(instance_id=options.instance, public_ip=options.assoc)
elif options.disassoc:
  conn.disassociate_address(public_ip=options.disassoc)

