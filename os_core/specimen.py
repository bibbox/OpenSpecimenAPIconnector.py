#! /bin/python3

# Import
import json
from datetime import datetime

from os_core.req_util import OS_request_gen


class specimen:

    # Constructor
    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)

        self.base_url = base_url
        

# Check URL, Password, header
    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)

# Get Specimen/s

    def get_specimen(self, specimenId):

        endpoint = '/specimens/' + str(specimenId)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


# Check if Specimen with Label 'xxx' exists

    def check_specimen(self, specimenLabel):

        endpoint = '/specimens?label=' + str(specimenLabel)
        url = self.base_url + endpoint
        r = self.OS_request_gen.head_request(url)

        if r.status_code == 200:
            r = 'Specimen with Label ' + str(specimenLabel) + ' exists.'
        else:
            r = 'Specimen with Label ' + \
                str(specimenLabel) + ' does not exist.'

        return r

# Create Specimen via API with the OS standard form

    def create_specimen_api(self, label, cpId, specimenClass, specimenType, pathology, anatomicSite, laterality, status, initialQty=None, \
                        availableQty=None,comments=None,  visitId=None, concetration=None, collectionEvent=None, biohazards=None, \
                        receivedEvent=None, extensionDetail=None, lineage="New", storageLocation="Not Specified", userId=2):

        endpoint = '/specimens'
        url = self.base_url + endpoint

        now = datetime.now().isoformat(timespec='milliseconds')+'Z'
        
        payload = '{\"label\":\"' + str(label) + '\",\"cpId\":' + str(cpId) + ',\"lineage\":\"' + str(lineage) + '\",\"status\":\"' + str(status) \
            + '\",\"createdOn\":\"' + now + '\",\"collectionEvent\":{\"user\":{\"id\":\"'+ str(userId) + '\"},\"time\":\"' \
            + now + '\"},\"receivedEvent\":{\"user\":{\"id\":\"' + str(userId) +'\"},\"receivedQuality\":\"Acceptable\",\"time\":\"' \
            + now + '\"},\"specimenClass\":\"' + str(specimenClass) +'\",\"type\":\"' + str(specimenType) + '\",\"pathology\":\"' + str(pathology) + '\",' \
            + '\"anatomicSite\":\"'+ str(anatomicSite) + '\",\"laterality\":\"' + str(laterality) +'\"}'
        
        r = self.OS_request_gen.post_request(url, data = payload)
            
        return json.loads(r.text)
    
#Create Specimen via CSV import
    #def
# Create Aliquot via API

#    def create_aliquot_api(self, ):

#"container":"Not Specified","procedure":"Not Specified",
 #"receivedEvent":{"user":{"loginName":"admin"},"receivedQuality":"Acceptable","time":"2020-11-18T07:49:35.366Z"},
 # "specimenClass":"Fluid","type":"Bile","pathology":"Malignant","anatomicSite":"Abdomen, NOS","laterality":"Bilateral","children":[],"specimensPool":[]}]
