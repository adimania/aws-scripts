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
parser.add_option("-i", "--instance", dest="instance", help="Instance id of the instance to be snapshoted.", metavar="INSTANCE_ID")
parser.add_option("-t", "--tag-value", dest="tag", help="tag value of the instance to be snapshoted.", metavar="INSTANCE_ID")
parser.add_option("-b", "--reboot", dest="reboot", help="Reboot the instance to ensure FS integrity.", metavar="REBOOT", action="store_false", default=True)
parser.add_option("-n", "--name", dest="name", help="AMI name.", metavar="AMI_NAME")
parser.add_option("-d", "--description", dest="desc", help="AMI description.", metavar="AMI_DESC")
parser.add_option("-r", "--region", dest="region", help="Region to be connected", metavar="REGION_NAME")
(options, args) = parser.parse_args()

region_obj = boto.ec2.get_region(options.region,aws_access_key_id=id,aws_secret_access_key=key)

conn = boto.connect_ec2(aws_access_key_id=id,aws_secret_access_key=key,region=region_obj)

if options.tag:
  reservations=conn.get_all_instances(filters={'tag-value':options.tag})
else:
  reservations=conn.get_all_instances(filters={'instance-id':options.instance})

for reservation in reservations:
  instance=str(reservation.instances[0]).split(':')[1]
  if options.desc:
    print reservations
    ami_id=conn.create_image(instance_id=instance, name=options.name, description=options.desc, no_reboot=options.reboot)
  else:
    print reservations
    ami_id=conn.create_image(instance_id=instance, name=options.name, description="Snap on "+str(datetime.datetime.now())[:10], no_reboot=options.reboot)
  print ami_id
