#! /bin/python3

import pandas
import json

from os_core.specimen import specimen

class specimen_util:

    def __init__(self, bas_url, auth):

        self.specimen = specimen(base_url=base_url, auth=auth)

    def search_specimens(self, searchparams):

        pass


#For creation afterwards
#    label, cpId, specimenClass, specimenType, pathology, anatomicSite, laterality, status, initialQty=None, \
#                        availableQty=None,comments=None,  visitId=None, concetration=None, collectionEvent=None, biohazards=None, \
#                        #receivedEvent=None, extensionDetail=None, lineage="New", storageLocation="Not Specified", userId=2):

#       now = datetime.now().isoformat(timespec='milliseconds')+'Z'
#       
#        payload = '{\"label\":\"' + str(label) + '\",\"cpId\":' + str(cpId) + ',\"lineage\":\"' + str(lineage) + '\",\"status\":\"' + str(status) \
#            + '\",\"createdOn\":\"' + now + '\",\"collectionEvent\":{\"user\":{\"id\":\"'+ str(userId) + '\"},\"time\":\"' \
#            + now + '\"},\"receivedEvent\":{\"user\":{\"id\":\"' + str(userId) +'\"},\"receivedQuality\":\"Acceptable\",\"time\":\"' \
#            + now + '\"},\"specimenClass\":\"' + str(specimenClass) +'\",\"type\":\"' + str(specimenType) + '\",\"pathology\":\"' + str(pathology) + '\",' \
#            + '\"anatomicSite\":\"'+ str(anatomicSite) + '\",\"laterality\":\"' + str(laterality) +'\"}'