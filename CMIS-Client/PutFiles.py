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
parser.add_option("--output-id", dest="output_id")
parser.add_option("--local-dir", dest="local_dir")
(options, args) = parser.parse_args()

# Validate options if possible
if options.host == None or options.host_port == None or options.username == None or options.password == None or options.output_id == None:
    raise SystemExit("Params not complete")

if os.path.isdir(options.local_dir) == False:
    raise SystemExit("Local directory not viable")


## Globals ##
ALFRESCO_HOST = options.host
ALFRESCO_PORT = options.host_port
ALFRESCO_USERNAME = options.username
ALFRESCO_PASSWORD = options.password

LOCAL_OUTPUT_DIR = options.local_dir

OUTPUT_CMIS_ID = options.output_id


try:
    # Connect and get repository
    client = CmisClient('http://' + ALFRESCO_HOST + ':' + ALFRESCO_PORT + '/alfresco/api/-default-/public/cmis/versions/1.1/atom', ALFRESCO_USERNAME, ALFRESCO_PASSWORD)
    repo = client.defaultRepository
except:
    raise SystemExit("Could not connect to CMIS repository")


try:
    # Get input and output folders
    output_folder = repo.getObject('workspace://SpacesStore/' + OUTPUT_CMIS_ID)
except:
    raise SystemExit("Could not find input folder in CMIS repository")


# Get output files and upload
for file in os.listdir(LOCAL_OUTPUT_DIR):
    output_file = open(LOCAL_OUTPUT_DIR + "/" + file, "r")

    try:
        output_folder.createDocument(file, contentFile=output_file)
    except:
        print "ERROR - Could not add " + file

    output_file.close()


