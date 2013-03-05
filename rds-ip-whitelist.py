from boto import rds
from boto.rds.dbsecuritygroup import DBSecurityGroup
import ConfigParser
import os.path
import sys
import datetime
from optparse import OptionParser

check = os.path.isfile(os.path.expanduser('~/.aws.conf'))
if cmp(check,False) == 0:
    print "~/.aws.conf is missing"
    sys.exit(2)
system_execution = 0
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.aws.conf'))
id = config.get("AWS", "consumer_key", raw=True)
key = config.get("AWS", "consumer_secret", raw=True)

parser = OptionParser()
parser.add_option("-s", "--sg", dest="sg", help="Security Group", metavar="SEC_GRP")
parser.add_option("-c", "--cidr", dest="cidr", help="CIDR", metavar="CIDR")
(options, args) = parser.parse_args()

rds_conn = rds.RDSConnection(id,key)
sg=DBSecurityGroup(connection=rds_conn,name=options.sg)
sg.authorize(cidr_ip=options.cidr)
