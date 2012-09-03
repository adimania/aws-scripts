
#!/usr/bin/env python
	
# author: Aditya Patawari <aditya@adityapatawari.com>

import boto
import ConfigParser
from optparse import OptionParser
import os.path
from boto.s3.key import Key
import glob

__author__ = "Aditya Patawari <aditya@adityapatawari.com>"

Description = '''
The format for the file is : 
[AWS]
consumer_key: <Consumer Key>
consumer_secret: <Consumer Secret>
[DEFAULTS]
s3_bucket: <bucket>
'''

check = os.path.isfile(os.path.expanduser('~/.aws.conf'))
if cmp(check,False) == 0:
    print Description
    sys.exit(2)
system_execution = 0
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/.aws.conf'))
id = config.get("AWS", "consumer_key", raw=True)
key = config.get("AWS", "consumer_secret", raw=True)
def_bucket = config.get("DEFAULTS", "s3_bucket", raw=True)

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="Upload the FILE to AWS S3", metavar="FILE")
(options, args) = parser.parse_args()

conn = boto.connect_s3(id,key)
bucket = conn.lookup(def_bucket)
k = Key(bucket)
file_list = glob.glob(options.filename)
for file_name in file_list:
    k.key = file_name.split('/')[-1]
    k.set_contents_from_filename(file_name)
    print file_name+' uploaded'
