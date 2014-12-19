#!/usr/bin/python -B

import pycurl
import time

import xml.etree.ElementTree as ET

from StringIO import StringIO
from optparse import OptionParser


parser = OptionParser()
parser.add_option("--url", dest="url", help="Optional, if set the preset vCloud API address will be ignored")
parser.add_option("-u", "--username", dest="username", help="vCloud API username", metavar="username@organisation")
parser.add_option("-p", "--password", dest="password", help="vCloud API password", metavar="password")
parser.add_option("-a", "--action", dest="action", help="Backup or restore [backup, restore]", choices=["backup", "restore"])
parser.add_option("-f", "--file-path", dest="path", help="File path, destination or source", metavar="/file/path.xml")
parser.add_option("--vdc-name", dest="vdc_name", help="Optional, if set only this vDC will be interogated for Edge Gateways")
parser.add_option("--gw-name", dest="gw_name", help="Optional, if set action will only affect this gateway")

(options, args) = parser.parse_args()


#### GLOBALs ####
ACCESS_URL = "https://vcloud.ceda.ac.uk/api"
API_VERSION_TAG = "Accept: application/*+xml;version=5.5"

AUTH_TOKEN_KEY = "x-vcloud-authorization"
AUTH_TOKEN = None


def __GetAuthToken(header_line):
# Filter response headers during session authentication
    global AUTH_TOKEN
    
    # Decode line to iso-8859-1 and remove non-relevant lines
    header_line = header_line.decode('iso-8859-1')
    if ':' not in header_line:
        return
    
    # Break the header line into tuple
    name, value = header_line.split(':', 1)
    
    # Sanitise data
    name = name.strip()
    name = name.lower()
    value = value.strip()
    
    # Set the auth token if key is found
    if name == AUTH_TOKEN_KEY: AUTH_TOKEN = AUTH_TOKEN_KEY + ":" + value

 
def _SessionAuth(url, username, password):
# Create authenticated session
    buffer = StringIO()
    
    try: 
        # Make cURL request
        c = pycurl.Curl()
        c.setopt(c.URL, url + "/sessions")
        c.setopt(c.HTTPHEADER, [API_VERSION_TAG])
        c.setopt(c.USERPWD, username + ":" + password)
        c.setopt(c.CUSTOMREQUEST, "POST")
        c.setopt(c.HEADERFUNCTION, __GetAuthToken)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()

    except:
        raise SystemExit("Could not connect to vCloud API")
    
    
    # Check for 'good' response code
    if c.getinfo(c.RESPONSE_CODE) == 200:
        # Parse response, convert to XML tree
        xml_response = ET.XML(buffer.getvalue())
        return(xml_response, c.getinfo(c.RESPONSE_CODE))
    else:
        raise SystemExit("The vCloud API did not respond correctly (non-200 response)")


def _DeleteAuth(url, token):
# Log out/close authenticated session
    try:        
        c = pycurl.Curl()
        c.setopt(c.URL, url + "/sessions")
        c.setopt(c.HTTPHEADER, [API_VERSION_TAG, token])
        c.setopt(c.CUSTOMREQUEST, "DELETE")
        c.perform()
        return("Session Deleted")
    except:
        raise SystemExit("Could not connect to vCloud API")



def _GetvDCName(url, token, vdc_name):
# List vDC this session has access to
    buffer = StringIO()
	
    try:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, [API_VERSION_TAG, token])
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
    except:
        raise SystemExit("Could not connect to vCloud API")    
	
    # Parse response, convert to XML tree
    xml_response = ET.XML(buffer.getvalue())


    for item in xml_response.iter():
        if vdc_name == None and item.get("type") == "application/vnd.vmware.vcloud.vdc+xml": 
            return(item.get("name"), item.get("href"))
        elif vdc_name == item.get("name") and item.get("type") == "application/vnd.vmware.vcloud.vdc+xml":
            return(item.get("name"), item.get("href"))

    raise SystemExit("No viable vDCs found")



def _GetEdgeGateway(url, token, gw_name):
# Return any 'ready' edgegateways name & url
    buffer = StringIO()

    # Convert 'user' URL to 'admin' URL
    admin_url = ACCESS_URL + "/admin" + url.split(ACCESS_URL)[1]
    
    try:
        c = pycurl.Curl()
        c.setopt(c.URL, admin_url + "/edgeGateways")
        c.setopt(c.HTTPHEADER, ["Accept: application/*+xml;version=5.5", token])
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
    except:
        raise SystemExit("Could not connect to vCloud API")
		
    # Parse response, convert to XML tree
    xml_response = ET.XML(buffer.getvalue())

    for gateway in xml_response.iter():
        if gw_name == None and gateway.get("gatewayStatus") == "READY": 
            return(gateway.get("name"), gateway.get("href"))
        elif gw_name == gateway.get("name") and gateway.get("gatewayStatus") == "READY":
            return(gateway.get("name"), gateway.get("href"))

    raise SystemExit("No viable Edge Gateway found")



def _RestoreEdgeGateway(url, token, backup_file):
# Add XML config to edge gateway config
    raw_xml = ET.parse(backup_file)
    xml_root = raw_xml.getroot()
    xmldata = ET.tostring(xml_root)

    buffer = StringIO()

    try:
        c = pycurl.Curl()
        c.setopt(c.URL, url + "/action/configureServices")
        c.setopt(c.HTTPHEADER, [API_VERSION_TAG, token, 'Content-Type:application/vnd.vmware.admin.edgeGatewayServiceConfiguration+xml; charset=ISO-8859-1'])
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.POSTFIELDS, xmldata)
        c.perform()
    except:
        raise SystemExit("Could not connect to vCloud API")
		
    # Parse response, convert to XML tree
    xml_response = ET.XML(buffer.getvalue())

    for item in xml_response.iter():
        if item.get("operationName") != None:
            return item.get("href")


def _DumpEdgeGatewayConfig(url, token):
# merge new firewall rule suppled as xmlroot with rules in edge gateway
    buffer = StringIO()
	
    try:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, ["Accept: application/*+xml;version=5.5", token])
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
    except:
        raise SystemExit("Could not connect to vCloud API")
		
    # Parse response, convert to XML tree
    xml_response = ET.XML(buffer.getvalue())
	
    for i in xml_response.iter("{http://www.vmware.com/vcloud/v1.5}EdgeGatewayServiceConfiguration"):
        return(i)

 

def _ValidateOptions():
    global ACCESS_URL

    ## In order of parser options ##
    # Override default URL if one is specified
    if options.url != None: ACCESS_URL = options_url

    # Check username format and password
    if "@" not in options.username: 
        raise SystemExit("Username must be in the format USERNAME@ORG_ID")
    elif options.password == None: 
        raise SystemExit("Password not supplied - check syntax")

    if options.action == "restore" and options.path == None:
        raise SystemExit("Restore action requires a file path")

    if options.gw_name == None:
        print("No gateway name specified - action will be performed on first viable Edge Gateway")

    if options.vdc_name == None:
        print("No vDC name specified - viable gateway in first vDC found will be used")

            
def main():

    _ValidateOptions()    
    
    # Create authenticated session
    print("Authenticating session.....")
    session_xml, session_rcode = _SessionAuth(ACCESS_URL, options.username, options.password)
   
    # If authentication token is present, continue
    if AUTH_TOKEN != None:
        print("Authentication token obtained.....")

        for session_detail in session_xml.iter():
            if session_detail.get("name") != None:
                vdc_name, vdc_href = _GetvDCName(session_detail.get("href"), AUTH_TOKEN, options.vdc_name) 
                print("Working in vDC: " + vdc_name)

		gateway_name, gateway_href = _GetEdgeGateway(vdc_href, AUTH_TOKEN, options.gw_name)
		print("Working with gateway: " + gateway_name)

      
                # Backup 
                if options.action == "backup":
                    gateway_config = _DumpEdgeGatewayConfig(gateway_href, AUTH_TOKEN)
                
                    if options.path == None:
                        print(ET.tostring(gateway_config))
                    else:
                        file = open(options.path, "w")
                        file.write(ET.tostring(gateway_config))
                        file.close()

                elif options.action == "restore":
                    _RestoreEdgeGateway(gateway_href, AUTH_TOKEN, options.path)

    else:
        raise SystemExit("Authentication token not present")

    print("Closing session.....")
    _DeleteAuth(ACCESS_URL, AUTH_TOKEN)

	
if __name__ == "__main__":
    main()







