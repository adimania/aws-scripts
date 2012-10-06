import boto
import ConfigParser
import os.path
import sys
import datetime
from optparse import OptionParser

check = os.path.isfile(os.path.expanduser('~/.aws.conf'))
if cmp(check,False) == 0:
    print Description
    sys.exit(2)
system_execution = 0
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.aws.conf'))
id = config.get("AWS", "consumer_key", raw=True)
key = config.get("AWS", "consumer_secret", raw=True)

parser = OptionParser()
parser.add_option("-i", "--instance", dest="instance", help="Instance id of the instance.", metavar="INSTANCE_ID")
parser.add_option("-a", "--associate", dest="assoc", help="IP address to associate.", metavar="IP_ADDR")
parser.add_option("-d", "--disassociate", dest="disassoc", help="IP address to disassociate.", metavar="IP_ADDR")
(options, args) = parser.parse_args()

conn = boto.connect_ec2(id,key)

if options.assoc:
  conn.associate_address(instance_id=options.instance, public_ip=options.assoc)
elif options.disassoc:
  conn.disassociate_address(public_ip=options.disassoc)  

