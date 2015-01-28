#!/usr/bin/python -B

import io
import os

from cmislib.model import CmisClient
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--host", dest="host")
parser.add_option("--port", dest="host_port")
parser.add_option("-u", "--username", dest="username")
parser.add_option("-p", "--password", dest="password")
parser.add_option("--input-id", dest="input_id")
parser.add_option("--local-dir", dest="local_dir")
(options, args) = parser.parse_args()

# Validate options if possible
if options.host == None or options.host_port == None or options.username == None or options.password == None or options.input_id == None:
    raise SystemExit("Params not complete")

if os.path.isdir(options.local_dir) == False: 
    raise SystemExit("Local directory not viable")


## Globals ##
ALFRESCO_HOST = options.host
ALFRESCO_PORT = options.host_port
ALFRESCO_USERNAME = options.username
ALFRESCO_PASSWORD = options.password

LOCAL_INPUT_DIR = options.local_dir

INPUT_CMIS_ID = options.input_id


try:
    # Connect and get repository
    client = CmisClient('http://' + ALFRESCO_HOST + ':' + ALFRESCO_PORT + '/alfresco/api/-default-/public/cmis/versions/1.1/atom', ALFRESCO_USERNAME, ALFRESCO_PASSWORD)
    repo = client.defaultRepository
except:
    raise SystemExit("Could not connect to CMIS repository")


try:
    # Get input and output folders
    input_folder = repo.getObject('workspace://SpacesStore/' + INPUT_CMIS_ID)
except:
    raise SystemExit("Could not find input folder in CMIS repository")


try:
    # Get and write out input files
    input_files = input_folder.getChildren()
    for input_file in input_files:
        content = input_file.getContentStream()
        file = open(LOCAL_INPUT_DIR + "/" + input_file.name, "wb")
        file.write(content.read())
        file.close()
except:
    raise SystemExit("Could not write out input files")
