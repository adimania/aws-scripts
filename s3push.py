#!/usr/bin/env python
	
# author: Aditya Patawari <aditya@adityapatawari.com>

import boto
import ConfigParser
import sys
from optparse import OptionParser
import os.path
from boto.s3.key import Key
from boto.s3.lifecycle import Lifecycle
import glob
from types import NoneType

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
parser.add_option("-d", "--directory", dest="dir_name", help="Define a directory structure with a trailing /", metavar="DIRECTORY_NAME")
parser.add_option("-c", "--create-bucket", dest="new_bucket", help="Creates a bucket, if it doesn't exist", metavar="BUCKET_NAME")
parser.add_option("-e", "--expiration", dest="life", help="Expiration in number of days", metavar="LIFE", type="int")
(options, args) = parser.parse_args()

conn = boto.connect_s3(id,key)
if options.new_bucket:
  bucket = conn.lookup(options.new_bucket)
  if type(bucket) is NoneType:
    bucket = conn.create_bucket(options.new_bucket)
    if options.life:
      life=Lifecycle()
      life.add_rule('s3push_expiration_rule','','Enabled',options.life)
      bucket.configure_lifecycle(life)
else:  
  bucket = conn.lookup(def_bucket)

if type(options.dir_name) is NoneType:
  options.dir_name = ''
  
k = Key(bucket)
file_list = glob.glob(options.filename)
for file_name in file_list:
    k.key = options.dir_name + file_name.split('/')[-1]
    k.set_contents_from_filename(file_name)
    print file_name+' uploaded'
