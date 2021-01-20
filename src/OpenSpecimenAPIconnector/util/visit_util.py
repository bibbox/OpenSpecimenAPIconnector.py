#! /bin/python3

from os_core.visit import visit
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory
import json
import io
import pandas
import time

class visit_util:

    #   Constructor
    def __init__(self, base_url, auth):

        self.visit = visit(base_url=base_url, auth=auth)
        self.jsons = Json_factory()

    #Add visit and specimen
    def add_visit_speci(self, cprid, name, lineage, visit_id, av_qty, user, init_qty, spec_class, spec_type, anat_site,
                        site, speclabel, eventid=None,eventlabel=None,ppid=None, cptitle=None, cpshorttitle=None,
                        diagnosis=None, clinicalstatus=None, acitivity=None, visitstatus=None, missedreason=None,
                        missedby=None, comments=None,pathologynumber=None,cohort=None, visitdate=None, cpid=None,                         
                        stor_loc=None, status="Collected", cont=None, proced=None, qual="Acceptable", concent=None,  
                        path=None, laterality=None, visitDate=None):

        vis = self.jsons.add_visit_json(cprid=cprid, name=name, site=site, eventid=eventid, eventlabel=eventlabel, ppid=ppid, cptitle=cptitle, 
                                        cpshorttitle=cpshorttitle, diagnosis=diagnosis,clinicalstatus=clinicalstatus, activity=acitivity,
                                        visitstatus=visitstatus, missedreason=missedreason, missedby=missedby, comments=comments,
                                        pathologynumber=pathologynumber, cohort=cohort, visitdate=visitdate, cpid=cpid)
        
        speci = self.jsons.create_spec_json(lineage=lineage,  av_qty=av_qty, user=user, visitDate=visitdate, init_qty=init_qty, visit_id=None,
                                        spec_class=spec_class, spec_type=spec_type, anat_site=anat_site, stor_loc=stor_loc, label=speclabel,
                                        status=status, cont=cont, proced=proced, qual=qual, concent=concent, path=path, laterality=laterality)
        
        vis = json.loads(vis)
        speci= json.loads(speci)
        
        params={}
        params={"visit":vis,
            "specimens":[speci]}
        
        params=json.dumps(params)

        r = self.visit.add_visit_specimen(params)

        return r