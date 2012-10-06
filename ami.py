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
parser.add_option("-i", "--instance", dest="instance", help="Instance id of the instance to be snapshoted.", metavar="INSTANCE_ID")
parser.add_option("-r", "--reboot", dest="reboot", help="Reboot the instance to ensure FS integrity.", metavar="REBOOT", action="store_false")
parser.add_option("-n", "--name", dest="name", help="AMI name.", metavar="AMI_NAME")
parser.add_option("-d", "--description", dest="desc", help="AMI description.", metavar="AMI_DESC")
(options, args) = parser.parse_args()

conn = boto.connect_ec2(id,key)

if options.desc:
  ami_id=conn.create_image(instance_id=options.instance, name=options.name, description=options.desc, no_reboot=options.reboot)
else:
  ami_id=conn.create_image(instance_id=options.instance, name=options.name, description="Snap by script on "+str(datetime.datetime.now())[:10], no_reboot=options.reboot)

print ami_id
