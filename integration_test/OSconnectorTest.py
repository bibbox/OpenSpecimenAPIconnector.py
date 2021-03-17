#! /bin/python3

#Import
import OpenSpecimenAPIconnector as OSconn
import OpenSpecimenAPIconnector.os_core as os_core
import OpenSpecimenAPIconnector.os_util as os_util

import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import time
import shutil
import json

class integrationTest:

    """Integration Test for OpenSpecimenAPIconnector.py

    Integration test for the PIP Package OpenSpecimenAPIconnector.py. This class test if the OpenSpecimen
    distribution which the user uses is compatibel with this package. Through to changes of tables the minimum version 
    is 6.1.RC1. It tests if the package has a connection to a defined OpenSpecimen instance, and if the different calls
    have a response. Errors like double entries, won't be checked. Other errors are filtered through the response and created from 
    OpenSpecimen itself.
    """

    def __init__(self, base_url, auth, filename = None, logpath = "log/"):

        """Constructor

        Constructor of the class integrationTest. If one initialize this class, a filename is created  with the name
        OSapiConnIntTest_*now*.txt, where *now* equals the time now with the format YYYY-MM-DD hh:mm:ss.microsecond.
        This filename is a member of the class.
        """

        self.base_url = base_url
        self.auth = auth
        
        # create paths for log, csv-template file checkups
        p = Path(__file__)
        self.base_path = p.resolve().parent
        self.log_path = self.base_path.joinpath(logpath)

        self.csv_template_path = self.base_path.joinpath("csv/template")
        self.csv_temp_export_path = self.base_path.joinpath("csv/exports")
        if not self.csv_template_path.is_dir():
            self.csv_template_path.mkdir(parents=True, exist_ok=True)
        if not self.log_path.is_dir():
            self.log_path.mkdir(parents=True, exist_ok=True)
        if not self.csv_temp_export_path.is_dir():
            self.csv_temp_export_path.mkdir(parents=True, exist_ok=True)
        if filename is None:
            filename = "OSapiConnIntTest_"+str(datetime.now())+".txt"
        self.logFile = self.log_path.joinpath(filename).open("a")

        self.ID = {}
        self.names = {}
        
        # Set Login 
        OSconn.config_manager.set_login(url = base_url, auth = auth)
        
        # Json/pandas template class 
        self.json_template = os_core.Json_factory()

        # Institute API
        self.inst = os_core.institutes()
        self.inst_util = os_util.institutes_util()

        # Site API
        self.site = os_core.sites()
        self.site_util = os_util.site_util()

        # User API
        self.user = os_core.users()
        self.user_util = os_util.user_util()
        
        # Collection protocol API
        self.cp = os_core.collection_protocol()
        self.cp_util = os_util.collection_protocol_util()

        # Collection protocol registration API
        self.cpr = os_core.collection_protocol_registration()
        self.cpr_util = os_util.cpr_util()
        self.part = os_core.participant()

        # Collection protocol event API
        self.cpe = os_core.collection_protocol_event()
        self.cpe_util = os_util.cpevent_util()

        # Visit API
        self.vis = os_core.visit()
        self.vis_util = os_util.visit_util()

        # Specimen API
        self.spec = os_core.specimen()
        self.spec_util = os_util.specimen_util()
        
        # Query API
        self.qry = os_core.query()
        self.qry_util = os_util.query_util()
        
        # Json API
        self.jsons = os_core.Json_factory()
        self.url = os_core.url_gen()

        # CSV import API
        self.csv_core_import = os_core.csv_bulk()
        self.csv_util_import = os_util.bulk_operations()

        # CSV export API
        self.csv_core_export = os_core.CSV_exporter()
        self.csv_util_export = os_util.csv_exporter()

        
    def runIntegrationTest(self):
                
        try:
            self.IntegrationTest()
        except AssertionError as error:
            print(error)
        finally:
            self.cleanUp()

    def csv_get_templates(self):
        
        schemes = ["cp", "specimen", "cpr", "user", "userRoles", "site", "shipment",
            "institute", "dpRequirement", "distributionProtocol", "distributionOrder", "storageContainer", "storageContainerType",
            "containerShipment", "cpe", "masterSpecimen", "participant", "sr", "visit", "specimenAliquot", "specimenDerivative",
            "specimenDisposal", "consent"]
        
        for scheme in schemes:
            pandas, csv_raw = self.csv_core_import.get_template(scheme)
            with open(self.csv_template_path.joinpath("{}_template.csv".format(scheme)), "w") as f:
                csv_raw.seek(0)
                shutil.copyfileobj(csv_raw, f)

    
    def IntegrationTest(self):

        #####################################################################################
        ################################## C S V  ###########################################
        #####################################################################################

        self.logFile.write("-Fetching templates- \n")
        try:
            self.csv_get_templates()
        except AssertionError as error:
            self.logFile.write("-Error fetching templates- \n" + str(error) + "\n")
            raise AssertionError("-Error fetching templates- \n" + str(error) + "\n") 
        self.logFile.write("-Fetching templates complete- \n")

        ## Hierarchially ordered
        #######################################################################################################
        ########################### C R E A T I N G / U P D A T I N G #########################################
        #######################################################################################################
        # Institutes
        
        # First Create an Institute
        self.logFile.write("-Creating an Institute- \n")
        response = self.inst_util.create_institute(institutename = "IntegrationTestInstitute")
        assert str(response).lower().find('error')==-1, "Error creating institute: "+str(response)
        assert bool(response), "Error creating institute"
        self.logFile.write(str(response)+ " \n")

        # Searching for an institute by name
        self.logFile.write("-Search for an Institute via Substring- \n")
        response = self.inst.search_institutes(substring = "IntegrationTestInstitute")
        assert str(response).lower().find('error')==-1, "Error searchin for an institute: "+str(response)
        assert bool(response), "Error searchin for an institute"
        self.logFile.write(str(response) + " \n")
        self.ID['institute'] = response[0]["id"]

        # Updating an institute
        self.logFile.write("-Updating an Institute- \n")
        self.names['institute']= "IntegrationTestInstitute1"
        params = self.jsons.create_institute(institutename = self.names['institute'])
        response = self.inst.update_institute(inid = self.ID['institute'], params = params)
        assert str(response).lower().find('error')==-1, "Error updating an institute: "+str(response)
        assert bool(response), "error updating an institute"
        self.logFile.write(str(response) + " \n")

        # Export Institute via csv
        self.logFile.write("-Export Institute Data as CSV- \n")
        try:
            export_csv = self.csv_util_export.csv_export(objecttype="institute", recordids=[self.ID["institute"]], csv=True)
            self.csv_temp_export_path.joinpath("test_institute.csv").open("w").write(export_csv)
        except AssertionError as error:
            self.logFile.write("-Error exporting Institute CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error exporting Institute CSV- \n" + str(error) + "\n")
        self.logFile.write(str(export_csv) + " \n")

        # Delete Institute
        self.logFile.write("- Delete Institute- \n")
        response = self.inst.delete_institute(inid = self.ID['institute'])
        assert str(response).lower().find('error') == -1, "Error deleting Institute: "+str(response)
        assert response, "Error deleting Institute"
        self.logFile.write(str(response)+ ' \n')
        
        # Create an Institute by CSV
        self.logFile.write("-Creating an Institute via CSV- \n")
        try:
            # csv = self.json_template.create_institute(institutename = "IntegrationTestInstitute", get_csv=True)
            csv = self.csv_temp_export_path.joinpath("test_institute.csv").open("r")
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="institute", operation="CREATE")
        except AssertionError as error:
            self.logFile.write("-Error creating Institute via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error creating Institute via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")
        
        # Searching for an institute by name
        self.logFile.write("-Search for an Institute via Substring- \n")
        response = self.inst.search_institutes(substring = "IntegrationTestInstitute")
        assert str(response).lower().find('error')==-1, "Error searchin for an institute: "+str(response)
        assert bool(response), "Error searchin for an institute"
        self.logFile.write(str(response) + " \n")
        self.ID['institute'] = response[0]["id"]

        # Updating an institute via CSV
        self.logFile.write("-Updating an Institute via CSV- \n")
        try:
            csv = self.json_template.create_institute(institutename = self.names['institute'], inst_id=self.ID['institute'], get_csv=True)
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="institute", operation="UPDATE")
        except AssertionError as error:
            self.logFile.write("-Error upadting Institute via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error updating Institute via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")
        
        ## Sites
        # Create a Site
        self.logFile.write("-Creating a Site- \n")
        response = self.site_util.create_sites(name = "IntegrationTestSite", institutename = self.names["institute"],type_="not specified")
        assert str(response).lower().find('error')==-1, "Error creating a site: "+str(response)
        assert bool(response), " error creating a site"
        self.logFile.write(str(response) + ' \n')

        #Search a site by attributes
        self.logFile.write("-Searching for a site- \n")
        response = self.site_util.search_sites(sitename ="IntegrationTestSite")
        assert str(response).lower().find('error')==-1, "Error searching for sites by attributes: "+str(response)
        assert  bool(response), "error searching for sites by attributes"
        self.ID['site'] = response[0]['id']
        self.logFile.write(str(response)+ ' \n')

        #Updating a site
        self.logFile.write("-Updating a site- \n")
        self.names["site"] = "IntegrationTestSite1"
        response = self.site_util.update_sites(siteid = self.ID["site"], name = self.names['site'], institutename=self.names['institute'], type_='not specified')
        assert str(response).lower().find('error')==-1, "Error updating site: "+str(response)
        assert bool(response), "error updating site"
        self.logFile.write(str(response) + ' \n')

        #Export Site via CSV
        self.logFile.write("-Export Site Data as CSV- \n")
        try:
            export_csv = self.csv_util_export.csv_export(objecttype="site", recordids=[self.ID["site"]], csv=True)
            self.csv_temp_export_path.joinpath("test_site.csv").open("w").write(export_csv)
        except AssertionError as error:
            self.logFile.write("-Error exporting Site CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error exporting Site CSV- \n" + str(error) + "\n")
        self.logFile.write(str(export_csv) + " \n")


        #Get all sites
        self.logFile.write('-Get all sites- \n')
        response = self.inst.get_all_institutes()
        assert str(response).lower().find('error')==-1, "Error getting all sites: "+str(response)
        assert bool(response), "error getting all sites"
        self.logFile.write(str(response) + " \n")

        #delete site
        self.logFile.write("-Delete Site- \n")
        response = self.site.delete_sites(siid = self.ID['site'])
        assert str(response).lower().find('error')==-1, "Error deleting Site: "+str(response)
        assert bool(response), "Error deleting Site"
        self.logFile.write(str(response) + " \n")

        # Create Site by csv
        self.logFile.write("-Creating a Site via CSV- \n")
        try:
            # data = {"Name": "IntegrationTestSite", "Institute Name": self.names["institute"], "Type": "not specified"}
            # csv = pd.DataFrame(data, index=[0]).to_csv(index=False)
            csv = self.csv_temp_export_path.joinpath("test_site.csv").open("r")
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="site", operation="CREATE")
        except AssertionError as error:
            self.logFile.write("-Error creating Site via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error creating Site via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")
        
        #Search a site by attributes
        self.logFile.write("-Searching for a site- \n")
        response = self.site_util.search_sites(sitename ="IntegrationTestSite")
        assert str(response).lower().find('error')==-1, "Error searching for sites by attributes: "+str(response)
        assert  bool(response), "error searching for sites by attributes"
        self.ID['site'] = response[0]['id']
        self.logFile.write(str(response)+ ' \n')

        # Update Site by csv
        self.logFile.write("-Update a Site via CSV- \n")
        try:
            # data = {"Identifier": self.ID['site'], "Name": self.names["site"], "Institute Name": self.names["institute"], "Type": "Collection Site"}
            csv = pd.read_csv(self.csv_temp_export_path.joinpath("test_site.csv").open("r"))
            # ignore warning 
            csv.Type[0] = "Collection Site"
            csv = pd.DataFrame(csv, index=[0]).to_csv(index=False)
            # csv = pd.DataFrame(data, index=[0]).to_csv(index=False) 
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="site", operation="UPDATE")
        except AssertionError as error:
            self.logFile.write("-Error updating Site via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error updating Site via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")

        ## Users
        #Creating a user
        self.logFile.write("-create an User- \n")
        response = self.user_util.create_user(first = "Integration", last = "TestUser", email = "email@address.com", login = "TestUser",
                   institute = self.names["institute"], type_ = "SUPER")
        assert str(response).lower().find('error')==-1, "Error creating User: "+str(response)
        assert bool(response), "error creating User"
        self.logFile.write(str(response)+ ' \n')
        self.ID['user'] = response['id']
        self.names['user'] = "TestUser"

        #Export User via CSV
        self.logFile.write("-Export User Data as CSV- \n")
        try:
            export_csv = self.csv_util_export.csv_export(objecttype="User", recordids=[self.ID["user"]], csv=True)
            self.csv_temp_export_path.joinpath("test_user.csv").open("w").write(export_csv)
        except AssertionError as error:
            self.logFile.write("-Error exporting User CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error exporting User CSV- \n" + str(error) + "\n")
        self.logFile.write(str(export_csv) + " \n")

        #Update a User
        self.logFile.write("-update an User- \n")
        response = self.user_util.update_user(userid = self.ID['user'],first ="Integration", last = "TestUser1", email = "email@address.com", login = "TestUser",
                   institute = self.names["institute"])
        assert str(response).lower().find('error')==-1, "Error updating an User: "+str(response)
        assert bool(response), "Error updating an User"
        self.logFile.write(str(response)+ ' \n')

        #Change Password 
        self.logFile.write("-change Password- \n")
        response = self.user_util.change_password(userid = self.ID['user'], newpw = "P4ssW0rd!")
        assert str(response).lower().find('error')==-1, "Error changing password: "+str(response)
        assert bool(response), "Error changing password"
        self.logFile.write(str(response) + ' \n')

        #Get all users
        self.logFile.write('-get all users- \n')
        response = self.user.get_all_users()
        assert str(response).lower().find('error')==-1, "Error getting all users: "+str(response)
        assert bool(response), "Error getting all users"
        self.logFile.write(str(response) + ' \n')

        #Get Roles
        self.logFile.write('-get roles- \n')
        response = self.user.get_roles(userid=self.ID['user'])
        assert str(response).lower().find('error')==-1, "Error getting roles: "+str(response)
        self.logFile.write(str(response) + ' \n')

        #delete user
        self.logFile.write("-Delete User- \n")
        response = self.user.delete_user(userid = self.ID['user'])
        assert str(response).lower().find('error')==-1, "Error deleting User: "+str(response)
        assert bool(response), "Error deleting User"
        self.logFile.write(str(response) + ' \n')

        # Create User via CSV
        self.logFile.write("-create a User via CSV- \n")
        try:
            # data = {"Last Name":"TestUser", "First Name":"Integration", "Email Address":"email@address.com", "Login Name":"TestUser",
                   #"Institute": self.names["institute"]}
            # csv = pd.DataFrame(data, index=[0]).to_csv(index=False)
            csv = self.csv_temp_export_path.joinpath("test_user.csv").open("r")
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="user", operation="CREATE")
        except AssertionError as error:
            self.logFile.write("-Error creating User via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error creating User via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")
        
        #Export User via CSV
        self.logFile.write("-Export User Data as CSV- \n")
        try:
            export_csv = self.csv_util_export.csv_export(objecttype="User", recordids=[self.ID["user"]], csv=True)
            self.csv_temp_export_path.joinpath("test_user.csv").open("w").write(export_csv)
        except AssertionError as error:
            self.logFile.write("-Error exporting User CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error exporting User CSV- \n" + str(error) + "\n")
        self.logFile.write(str(export_csv) + " \n")
        
        # Update User via CSV
        self.logFile.write("-create a User via CSV- \n")
        try:
            # data = {"identifier": self.ID['user'], "Last Name":"TestUser1", "First Name":"Integration", "Email Address":"email@address.com", "Login Name":"TestUser",
                   # "Institute": self.names["institute"]}
            # csv = pd.DataFrame(data, index=[0]).to_csv(index=False)
            csv = pd.read_csv(self.csv_temp_export_path.joinpath("test_user.csv").open("r"))
            self.ID['user'] = str(int(csv["Identifier"][0]))
            csv["Last Name"][0] = "TestUser1"
            csv = pd.DataFrame(csv, index=[0]).to_csv(index=False)
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="user", operation="UPDATE")
        except AssertionError as error:
            self.logFile.write("-Error updating User via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error updating User via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")

        ##Collection protocol
        # create collection protocol
        self.logFile.write("-Create Collection protocol- \n")
        self.names['CP']="IntegrationTestCP"
        response = self.cp_util.create_cp(short_title = "IntTestCP", title = self.names['CP'], pi_mail = "admin", sites = [self.names["site"]])
        assert str(response).lower().find('error')==-1, "Error creating Colelction protocol: "+str(response)
        assert bool(response), "Error creating Colelction protocol"
        self.logFile.write(str(response) + ' \n')

        # create collection protocol
        self.logFile.write("-Create Collection protocol- \n")
        self.names['CP2']="IntegrationTestCP2"
        response = self.cp_util.create_cp(short_title = "IntTestCP2", title = self.names['CP2'], pi_mail = "admin", sites = [self.names["site"]])
        assert str(response).lower().find('error')==-1, "Error creating Colelction protocol: "+str(response)
        assert bool(response), "Error creating Colelction protocol"
        self.logFile.write(str(response) + ' \n')
        self.ID['CP2'] = response['id']

        #merge Collection protocols
        self.logFile.write('-Merge Colletion Protocol- \n')
        response = self.cp_util.merge_cps(src_cp = "IntTestCP2", trg_cp ="IntTestCP")
        assert str(response).lower().find('error')==-1, "Error merging Colelction protocols: "+str(response)
        assert bool(response), "Error merging Colelction protocols"
        self.logFile.write(str(response) + ' \n')

        #getting all Collection Protocols
        self.logFile.write('-Getting all Collection protocols- \n')
        response = self.cp.get_all_collection_protocols()
        assert str(response).lower().find('error')==-1, "Error getting all Collection protocols: "+str(response)
        assert bool(response), "Error getting all Colelction protocols"
        self.logFile.write(str(response) + ' \n')
        
        #search cp
        self.logFile.write("-Search CP- \n")
        response = self.cp_util.search_cps(title=self.names['CP'])
        assert str(response).lower().find('error')==-1, "Error searching for a Collection protocol: "+str(response)
        assert bool(response), "Error searching for a Collection protocol"
        self.ID['CP']=response[0]['id']
        self.logFile.write(str(response) + ' \n')

        #update CP
        self.logFile.write("-update CP- \n")
        response = self.cp_util.update_cp(cpid = self.ID['CP'], short_title = "IntTestCP", title = self.names['CP'], pi_mail = "admin",
                        time_start="2021-02-24", sites = [self.names["site"]])
        assert str(response).lower().find('error')==-1, "Error updating CP: "+str(response)
        assert bool(response), "Error updating CP"
        self.logFile.write(str(response)+ ' \n')

        #assign roles
        self.logFile.write('-assign role- \n')
        response = self.user_util.assign_role(userid = self.ID['user'], siteid = self.ID['site'], cpid = self.ID['CP'], role = 'Technician')
        assert str(response).lower().find('error')==-1, "Error assigning role: "+str(response)
        assert bool(response), "Error assigning role"
        self.logFile.write(str(response)+ ' \n')

        #delete CP
        self.logFile.write("-Delete CP- \n")
        response = self.cp.delete_collection_protocol(cpid = self.ID['CP'])
        assert str(response).lower().find('error')==-1, "Error deleting CP: "+str(response)
        assert bool(response), "Error deleting CP"
        self .logFile.write(str(response) + ' \n')

        # create CP via CSV
        self.logFile.write("-create a CP via CSV- \n")
        try:
            data = {"Title":self.names['CP'], "Short Title":"IntTestCP", "PI#PI Email":"admin@localhost", "Sites#1#Name":self.names["site"]}
            csv = pd.DataFrame(data, index=[0]).to_csv(index=False)
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="cp", operation="CREATE")
        except AssertionError as error:
            self.logFile.write("-Error updating CP via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error updating CP via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")

        #search cp
        self.logFile.write("-Search CP- \n")
        response = self.cp_util.search_cps(title=self.names['CP'])
        assert str(response).lower().find('error')==-1, "Error searching for a Collection protocol: "+str(response)
        assert bool(response), "Error searching for a Collection protocol"
        self.ID['CP']=response[0]['id']
        self.logFile.write(str(response) + ' \n')

        #Upddate a CP via CSV
        self.logFile.write("-Update a CP via CSV- \n")
        try:
            data = {"Identifier": self.ID["CP"], "Title":self.names['CP'], "Short Title":"IntTestCP1", "PI#PI Email":"admin@localhost", "Sites#1#Name": self.names["site"]}
            csv = pd.DataFrame(data, index=[0]).to_csv(index=False)
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="cp", operation="UPDATE")
        except AssertionError as error:
            self.logFile.write("-Error updating CP via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error updating CP via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")
        
        ## Collection Protocol Registration
        # Create a Registration
        self.logFile.write('-Create Registration- \n')
        response = self.cpr_util.create_registration(regdate = "2021-02-24", cpid = self.ID['CP'], ppid = "IntegrationTestPPID",lastname = "Sepp")
        assert str(response).lower().find('error')==-1, "Error creating Participant: "+str(response)
        assert bool(response), "Error creating Participant"
        self.ID['cpr']=response['id']
        self.ID['part']=response['participant']['id']
        self.logFile.write(str(response)+ ' \n')
        
        # Update a Registration
        self.logFile.write('-Update Registration- \n')
        self.ID['ppid']="IntegrationTestPPID1"
        response = self.cpr_util.update_registration(cprid= self.ID['cpr'], id_=self.ID['part'],regdate = "2021-02-24", cpid = self.ID['CP'],
                         ppid = self.ID['ppid'],lastname = "Sepp")
        assert str(response).lower().find('error')==-1, "Error updating Participant: "+str(response)
        assert bool(response), "Error updating Participant"
        self.logFile.write(str(response)+ ' \n')

        # Get Participant
        self.logFile.write('-Get Participant via CPRID- \n')
        response = self.part.get_participant(ppid = self.ID['part'])
        assert str(response).lower().find('error')==-1, "Error getting Participant: "+str(response)
        assert bool(response), "Error getting Participant"
        self.logFile.write(str(response)+ ' \n')

        # Register to CP
        self.logFile.write('-Register Participant to protocol- \n')
        response = self.cpr_util.register_to_cp(cprid =self.ID['part'], regdate = "2021-03-02", cpid = self.ID['CP2'], ppid = self.ID['ppid'])
        assert str(response).lower().find('error')==-1, "Error register Participant to another CP: "+str(response)
        assert bool(response), "Error register Participant to another CP"
        self.logFile.write(str(response)+ ' \n')
        self.ID['cpr2']=response['id']

        # Export CPR via CSV
        self.logFile.write("-Export CPR Data as CSV- \n")
        try:
            export_csv = self.csv_util_export.csv_export(objecttype="cpr", cpid = self.ID['CP'], csv=True)
            self.csv_temp_export_path.joinpath("test_cpr.csv").open("w").write(export_csv)
        except AssertionError as error:
            self.logFile.write("-Error exporting Site CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error exporting Site CSV- \n" + str(error) + "\n")
        self.logFile.write(str(export_csv) + " \n")

        # Get Participants
        self.logFile.write('-Getting Participants- \n')
        response = self.cpr_util.get_participants(lastname="Sepp")
        assert str(response).lower().find('error')==-1, "Error getting participants: "+str(response)
        self.logFile.write(str(response)+ ' \n')

        # merge Pariticipants
        self.logFile.write('-Merge participants')
        response = self.cpr.merge_participants(id_from = self.ID['cpr2'], id_to = self.ID['cpr'])
        assert str(response).lower().find('error')==-1, "Error merging Participants: "+str(response)
        assert bool(response), "Error merging Participants"
        self.logFile.write(str(response)+ ' \n')

        # get regisrtations
        self.logFile.write('-get registrations')
        response = self.cpr_util.get_registrations(cpid = self.ID['CP'])
        assert str(response).lower().find('error')==-1, "Error getting registrations: "+str(response)
        assert bool(response), "Error getting registrations"
        self.logFile.write(str(response)+ ' \n')

        # delete Registration
        self.logFile.write('-Delete Registration- \n')
        response = self.cpr.delete_participant(cprid = self.ID["cpr"])
        assert str(response).lower().find('error')==-1, "Error deleting Participant: "+str(response)
        assert bool(response), " Error deleting Participant"
        self.logFile.write(str(response) + ' \n')
        
        # Create a Registration via CSV
        self.logFile.write("-create a CP via CSV- \n")
        try:
            csv = self.csv_temp_export_path.joinpath("test_cpr.csv").open("r")
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="cpr", operation="CREATE")
        except AssertionError as error:
            self.logFile.write("-Error creating CPR via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error creating CPR via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")

        # Export CPR via CSV
        self.logFile.write("-Export CPR Data as CSV- \n")
        try:
            export_csv = self.csv_util_export.csv_export(objecttype="cpr", cpid = self.ID['CP'], csv=True)
            self.csv_temp_export_path.joinpath("test_cpr.csv").open("w").write(export_csv)
        except AssertionError as error:
            self.logFile.write("-Error exporting Site CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error exporting Site CSV- \n" + str(error) + "\n")
        self.logFile.write(str(export_csv) + " \n")

        # Update a Registration via CSV
        self.logFile.write("-update a CP via CSV- \n")
        try:
            csv = pd.read_csv(self.csv_temp_export_path.joinpath("test_cpr.csv").open("r"))
            csv["Vital Status"][0] = "Dead"
            self.ID['cpr'] = str(int(csv["Identifier"][0]))
            csv = pd.DataFrame(csv, index=[0]).to_csv(index=False)
            response = self.csv_util_import.bulk_import(csv, filename="integration_test.csv", schemaname="cpr", operation="UPDATE")
        except AssertionError as error:
            self.logFile.write("-Error updating CPR via CSV- \n" + str(error) + "\n")
            raise AssertionError("-Error updating CPR via CSV- \n" + str(error) + "\n")
        self.logFile.write(str(response)+ " \n")

        ## Events
        #Create an Event
        self.logFile.write('-Create CP Event- \n')
        self.names['eventLabel']="IntegrationTestLabel"
        response = self.cpe_util.create_event(label = self.names['eventLabel'], point = 0, cp = self.names['CP'], site = self.names['site'],
                        diagnosis ="Not Specified", status = "Not Specified", activity = "Active", unit = "DAYS")
        assert str(response).lower().find('error')==-1, "Error creating an Event: "+str(response)
        assert bool(response), "Error creating an Event"
        self.ID['event']=response['id']
        self.logFile.write(str(response)+ ' \n')

        #Update an Event
        self.logFile.write('-Update CP Event- \n')
        self.names['eventLabel']="IntegrationTestLabel1"
        response = self.cpe_util.update_event(eventid=self.ID['event'],label = self.names['eventLabel'], point = 0, cp = self.names['CP'],
                        site = self.names['site'], diagnosis ="Not Specified", status = "Not Specified", activity = "Active", unit = "DAYS")
        assert str(response).lower().find('error')==-1, "Error creating an Event: "+str(response)
        assert bool(response), "Error creating an Event"
        self.ID['event']=response['id']
        self.logFile.write(str(response)+ ' \n')

        input()

        ##Visits
        #Create a Visit
        self.logFile.write('-Create a Visit- \n')
        self.names['visit']="IntegrationTestVisit"
        response = self.vis_util.add_visit(cprid = self.ID['cpr'], name = self.names['visit'], site = self.names['site'])
        assert str(response).lower().find('error')==-1, "Error creating a Visit: "+str(response)
        assert bool(response), "Error creating a Visit"
        self.ID['visit']=response['id']
        self.logFile.write(str(response)+ ' \n')

        #searchvisits
        self.logFile.write('-search for visits- \n')
        response = self.vis_util.search_visit_namespr(visitname = self.names['visit'])
        assert str(response).lower().find('error')==-1, "Error searching for a Visit: "+str(response)
        self.logFile.write(str(response)+ ' \n')

        #Get visit with cprID
        self.logFile.write('- Get visit by CPRID- \n')
        response = self.vis_util.search_visit_cprid(cprid = self.ID['cpr'])
        assert str(response).lower().find('error')==-1, "Error getting visit: "+str(response)
        assert bool(response), "Error getting visit"
        self.logFile.write(str(response)+ ' \n')
        
        #Get all events
        self.logFile.write('-Get all Events- \n')
        response = self.cpe.get_all_events(cpid=self.ID['CP'])
        assert str(response).lower().find('error')==-1, "Error getting all Events: "+str(response)
        assert bool(response), "Error getting all events"
        self.logFile.write(str(response)+ ' \n')

        #Update a Visit
        self.logFile.write('-Update a Visit- \n')
        self.names['visit']="IntegrationTestVisit1"
        response = self.vis_util.update_visit(visitid = self.ID['visit'], cprid = self.ID['cpr'], name = self.names['visit'], site = self.names['site'])
        assert str(response).lower().find('error')==-1, "Error updating a Visit: "+str(response)
        assert bool(response), "Error updating a Visit"
        self.logFile.write(str(response)+ ' \n')

        #Add a Visit and Specimen in one turn
        self.logFile.write('-Add Visit and Specimen- \n')
        self.names['visit2']="IntegrationTestVisit2"
        self.names['speci2']="IntegrationTestSpeci2"
        response = self.vis_util.add_visit_speci(name = self.names["visit2"], lineage = "New", av_qty = 10, user = 2, init_qty = 10, spec_class ='Fluid', 
                    spec_type = "Bile", anat_site ="Anal Canal", path='Malignant', site = self.names['site'], speclabel=self.names['speci2'],cpid=self.ID['CP'],
                     ppid="IntegrationPPID", cprid=self.ID['cpr'],colltime="2021-03-01",rectime='2021-03-01')
        assert str(response).lower().find('error')==-1, "Error adding a Visit and a Specimen in one turn: "+str(response)
        assert bool(response), "Error adding a Visit and a Specimen in one turn"
        self.ID['visit2']=response['visit']['id']
        self.ID['speci2']=response['specimens'][0]['id']
        self.logFile.write(str(response)+ ' \n')

        ##Specimens
        #Add a Specimen
        self.logFile.write('-Add a Specimen- \n')
        self.names['speci']="IntegrationTestSpeci"
        response = self.spec_util.create_specimen(specimenclass = 'Fluid', specimentype = 'Bile', pathology = 'Malignant', anatomic = 'Anal Canal',  
                 laterality = 'Left', initqty = 10, avaqty =10, visitid = self.ID['visit'], recqlt = 'Acceptable', userid = 2, label = self.names['speci'],
                 colltime = '2021-03-01', rectime = '2021-03-01')
        assert str(response).lower().find('error')==-1, "Error creating Specimen: "+str(response)
        assert bool(response), "Error creating Specimen"
        self.ID['speci']=response['id']
        self.logFile.write(str(response)+ ' \n')

        #check label
        self.logFile.write('-Check if label exist- \n')
        response = self.spec.check_specimen(specimenLabel = self.names['speci'])
        assert str(response).lower().find('error')==-1, "Error checking Specimen: "+str(response)
        assert bool(response), "Error checking Specimen"
        self.logFile.write(str(response)+ ' \n')

        #update Specimen
        self.logFile.write('-Update Specimen- \n')
        self.names['speci']="IntegrationTestSpeci1"
        response = self.spec_util.update_specimen(specimenid = self.ID['speci'], specimenclass = 'Fluid', specimentype = 'Bile', pathology = 'Malignant', anatomic = 'Anal Canal',  
                 laterality = 'Left', initqty = 10, avaqty =10, visitid = self.ID['visit'], recqlt = 'Acceptable', userid = 2, label = self.names['speci'],
                 colltime = '2021-03-01', rectime = '2021-03-01')
        assert str(response).lower().find('error')==-1, "Error updating Specimen: "+str(response)
        assert bool(response), "Error updating Specimen"
        self.logFile.write(str(response) + ' \n')

        #search Specimens
        self.logFile.write('Search Specimens- \n')
        response = self.spec_util.search_specimens(label=self.names['speci'])
        assert str(response).lower().find('error')==-1, "Error searching for a Specimen: "+str(response)
        assert bool(response), "Error searching for a Specimen"
        self.logFile.write(str(response) + ' \n')

        #Queries
        #Create AQL
        self.logFile.write('-Executing AQL- \n')
        response = self.qry_util.create_aql(cpid = self.ID['CP'], aql = "select Participant.ppid, SpecimenCollectionGroup.collectionDate, count(distinct Specimen.id) where Specimen.lineage = \"New\"")
        assert str(response).lower().find('error')==-1, "Error executing AQL: "+str(response)
        assert bool(response), "Error executing AQL"
        self.logFile.write(str(response) + ' \n')

        #Search Queries
        self.logFile.write('-Searching for queries- \n')
        response = self.qry_util.search_query()
        assert str(response).lower().find('error')==-1, "Error searching for queries: "+str(response)
        assert bool(response), "Error searching for queries"
        self.logFile.write(str(response) + ' \n')

        #Executing saved queries
        self.logFile.write('-Executing a saved query- \n')
        response = self.qry_util.execute_query(qryid = '1')
        assert str(response).lower().find('error')==-1, "Error executing saved query: "+str(response)
        assert bool(response), "Error executing saved query"
        self.logFile.write(str(response) + ' \n')


        ######################################################################################
        ############################## C L E A N   U P #######################################
        ######################################################################################

        #delete Specimen
        self.logFile.write('-Delete a Specimen- \n')
        response = self.spec_util.delete_specimens(specimenids = self.ID['speci'])
        assert str(response).lower().find('error')==-1, "Error deleting a Specimen: "+str(response)
        assert bool(response), "Error deleting a Specimen"
        self.logFile.write(str(response) + ' \n')

        #get a Specimen
        self.logFile.write('-Get Specimen by ID(already deleted)- \n')
        response = self.spec.get_specimen(specimenid = self.ID['speci'])
        assert str(response).lower().find('error')==-1, "Error getting a Specimen: "+str(response)
        assert bool(response), "Error getting a Specimen"
        self.logFile.write(str(response) + ' \n')

        #delete Specimen
        self.logFile.write('-Delete a Specimen- \n')
        response = self.spec_util.delete_specimens(specimenids = self.ID['speci2'])
        assert str(response).lower().find('error')==-1, "Error deleting a Specimen: "+str(response)
        assert bool(response), "Error deleting a Specimen"
        self.logFile.write(str(response) + ' \n')

        #delete Visit
        self.logFile.write('-Delete a Visit- \n')
        response = self.vis.delete_visit(visitid = self.ID['visit2'])
        assert str(response).lower().find('error')==-1, "Error deleting a Visit: "+str(response)
        assert bool(response), "Error deleting a Visit"
        self.logFile.write(str(response) + ' \n')

        #delete Visit
        self.logFile.write('-Delete a Visit- \n')
        response = self.vis.delete_visit(visitid = self.ID['visit'])
        assert str(response).lower().find('error')==-1, "Error deleting a Visit: "+str(response)
        assert bool(response), "Error deleting a Visit"
        self.logFile.write(str(response) + ' \n')

        #get Visit
        self.logFile.write('Get Visit by ID(already deleted)- \n')
        response = self.vis.get_visit(visitid = self.ID['visit'])
        assert str(response).lower().find('error')==-1, "Error getting a visit: "+str(response)
        assert bool(response), "Error getting a visit"
        self.logFile.write(str(response) + ' \n')

        #delete Event
        self.logFile.write('-Delete and Event- \n')
        response = self.cpe.delete_event(eventid = self.ID['event'])
        assert str(response).lower().find('error')==-1, "Error deleting an event: "+str(response)
        assert bool(response), "Error deleting an event"
        self.logFile.write(str(response) + ' \n')

        #get Event
        self.logFile.write('Get event(already deleted)- \n')
        response = self.cpe.get_event(eventid = self.ID['event'])
        assert str(response).lower().find('error')==-1, "Error getting an Event: "+str(response)
        assert bool(response), "Error getting an Event"
        self.logFile.write(str(response) + ' \n')

        #delete Registration
        self.logFile.write('-Delete Registration- \n')
        response = self.cpr.delete_participant(cprid = self.ID["cpr"])
        assert str(response).lower().find('error')==-1, "Error deleting Participant: "+str(response)
        assert bool(response), " Error deleting Participant"
        self.logFile.write(str(response) + ' \n')

        #get deleted Registration
        self.logFile.write('-Get Registration-')
        response = self.cpr.get_registration(cprid = self.ID['cpr'])
        assert str(response).lower().find('error')==-1, "Error getting Participan: "+str(response)
        assert bool(response), "Error getting Participant"
        self.logFile.write(str(response)+ ' \n')
        
        #delete CP
        self.logFile.write("-Delete CP- \n")
        response = self.cp.delete_collection_protocol(cpid = self.ID['CP'])
        assert str(response).lower().find('error')==-1, "Error deleting CP: "+str(response)
        assert bool(response), "Error deleting CP"
        self .logFile.write(str(response) + ' \n')

        #get deleted CP
        self.logFile.write("-Get CP via Id(is already deleted)- \n")
        response = self.cp.get_collection_protocol(cpid = self.ID['CP'])
        assert str(response).lower().find('error')==-1, "Error getting a CP: "+str(response)
        assert bool(response), "Error getting a CP"
        self.logFile.write(str(response) + ' \n') 

        #delete user
        self.logFile.write("-Delete User- \n")
        response = self.user.delete_user(userid = self.ID['user'])
        assert str(response).lower().find('error')==-1, "Error deleting User: "+str(response)
        assert bool(response), "Error deleting User"
        self.logFile.write(str(response) + ' \n')

        #get deleted user
        self.logFile.write("-Get User  via ID(is already deleted- \n")
        response = self.user.get_user(userId = self.ID['user'])
        assert str(response).lower().find('error')==-1, "Error getting User: "+str(response)
        assert bool(response), "Error getting User"
        self.logFile.write(str(response) + ' \n')

        #delete site
        self.logFile.write("-Delete Site- \n")
        response = self.site.delete_sites(siid = self.ID['site'])
        assert str(response).lower().find('error')==-1, "Error deleting Site: "+str(response)
        assert bool(response), "Error deleting Site"
        self.logFile.write(str(response) + " \n")

        #get deleted site
        self.logFile.write("-Get Site via ID(is already deleted- \n")
        response = self.site.get_site(siteid = self.ID['site'])
        assert str(response).lower().find('error')==-1, "Error getting Site: "+str(response)
        assert bool(response), "Error getting Site"
        self.logFile.write(str(response) + ' \n')

        #delete Institute
        self.logFile.write("- Delete Institute- \n")
        response = self.inst.delete_institute(inid = self.ID['institute'])
        assert str(response).lower().find('error')==-1, "Error deleting Site: "+str(response)
        assert bool(response), "Error deleting Site"
        self.logFile.write(str(response)+ ' \n')

        #get Institute
        self.logFile.write("-Get Institute- \n")
        response = self.inst.get_institute(inid = self.ID['institute'])
        assert str(response).lower().find('error')==-1, "Error getting institute: "+str(response)
        assert bool(response), "Error getting institute"
        self.logFile.write(str(response)+ ' \n')

        return "end_of Test"

    def cleanUp(self):
        if 'speci' in self.ID.keys():
            self.spec_util.delete_specimens(specimenids =self.ID['speci'])
        if 'speci2' in self.ID.keys():
            self.spec_util.delete_specimens(specimenids = self.ID['speci2'])
        if 'visit2' in self.ID.keys():
            self.vis.delete_visit(visitid = self.ID['visit2'])
        if 'visit' in self.ID.keys():
            self.vis.delete_visit(visitid = self.ID['visit'])
        if 'event' in self.ID.keys():
            self.cpe.delete_event(eventid = self.ID['event'])
        if 'cpr2' in self.ID.keys():
            self.cpr.delete_participant(cprid = self.ID['cpr2'])
        if 'cpr' in self.ID.keys():
            self.cpr.delete_participant(cprid = self.ID["cpr"])
        if 'CP' in self.ID.keys():
            self.cp.delete_collection_protocol(cpid = self.ID['CP'])
        if 'CP2' in self.ID.keys():
            self.cp.delete_collection_protocol(cpid = self.ID['CP2'])
        if 'user' in self.ID.keys():
            self.user.delete_user(userid = self.ID['user'])
        if 'site' in self.ID.keys():
            self.site.delete_sites(siid = self.ID['site'])
        if 'institute' in self.ID.keys():
            self.inst.delete_institute(inid = self.ID['institute'])