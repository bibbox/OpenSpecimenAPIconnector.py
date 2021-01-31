#! /bin/python3

import pandas
import json
from datetime import date

from ..os_core.specimen import specimen
from ..os_core.url import url_gen
from ..os_core.jsons import Json_factory
from ..os_core.req_util import OS_request_gen
from ..os_core.users import users



class specimen_util:

    def __init__(self, bas_url, auth):

        self.req_gen =OS_request_gen(auth = auth)
        self.specimen = specimen(base_url = base_url, auth = auth)
        self.url = url_gen()
        self.jsons = Json_factory()


    def search_specimens(self, label = None, cprid = None, eventid = None, visitid = None, maxres = "100", exact = "false", extension = "true"):

        search_string = self.url.search_specimen(self, label = label, cprid = cprid, eventid = eventid, visitid = visitid,
                                             maxres = maxres, exact = exact, extension = extension)
        
        r = self.specimen.search_specimens(search_string = search_string)

        return r

    def create_specimen(self, label, specimenclass, specimentype , pathology , anatomic, laterality, initqty, avaqty, visitid, recqlt,
                        colltime = None, rectime = None, lineage = 'New', status = 'Collected', stor_name = None, storlocx = None,
                        storlocy = None, concetration = None, biohazard = None, userid = None, comments = None,  collproc=None, 
                        conttype=None, extensionudn="false", extensionmap=None, extensiondict =None):
        
        if userid != None:
            users = users.get_all_users()
            logname= self.req_gen.user_name()
            for user in users:
                if user['loginName'] == logname:
                    userid = user['id']
        
        if rectime == None:
            rectime = date.today()
        
        if colltime == None:
            colltime = date.today()

        storloc = self.jsons.storage_location_json(name = stor_name, xpos = storlocx, ypos = storlocy)

        extension = self.jsons.create_extension(attrsmap = extensionmap, extensiondict = extensiondict, useudn = extensionudn)

        params = self.jsons.create_specimen_json(label = label, specimenclass = specimenclass, specimentype = specimentype, pathology =pathology,
                anatomic= anatomic, laterality = laterality, initqty = initqty, avaqty = avaqty, visitid = visitid, colltime = colltime,
                userid = userid, comments = comments, collproc = collproc, conttype = conttype, recqlt = recqlt, rectime = rectime,
                lineage = lineage, status = status, storloc = storloc, concentration = concetration, biohazard = biohazard,
                comments = comments, collproc = collproc, conttype = conttype, extension = extension)
        
        r = self.specimen.create_specimen(params = params)

        return r


        def update_specimen(self, specimenid, label = None, specimenclass = None, specimentype = None, pathology = None, anatomic = None, laterality = None,
                            initqty = None, avaqty = None, visitid = None, recqlt = None, colltime = None, rectime = None, lineage = 'New',
                            status = 'Collected', stor_name = None, storlocx = None, storlocy = None, concetration = None, biohazard = None,
                            userid = None, comments = None,  collproc=None, conttype=None, extensionudn="false", extensionmap=None, extensiondict =None):

        if userid != None:
            users = users.get_all_users()
            logname= self.req_gen.user_name()
            for user in users:
                if user['loginName'] == logname:
                    userid = user['id']

        storloc = self.jsons.storage_location_json(name = stor_name, xpos = storlocx, ypos = storlocy)

        extension = self.jsons.create_extension(attrsmap = extensionmap, extensiondict = extensiondict, useudn = extensionudn)

        params = self.jsons.create_specimen_json(label = label, specimenclass = specimenclass, specimentype = specimentype, pathology =pathology,
                anatomic= anatomic, laterality = laterality, initqty = initqty, avaqty = avaqty, visitid = visitid, colltime = colltime,
                userid = userid, comments = comments, collproc = collproc, conttype = conttype, recqlt = recqlt, rectime = rectime,
                lineage = lineage, status = status, storloc = storloc, concentration = concetration, biohazard = biohazard,
                comments = comments, collproc = collproc, conttype = conttype, extension = extension)
        
        r = self.specimen.update_specimen(specimenid = specimenid,params = params)

        return r

        def delete_specimens(self, specimenids):

