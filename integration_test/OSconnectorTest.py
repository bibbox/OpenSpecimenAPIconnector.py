#! /bin/python3

#Import
import OpenSpecimenAPIconnector as OSconn
import OpenSpecimenAPIconnector.os_core as os_core
import OpenSpecimenAPIconnector.os_util as os_util

from datetime import datetime
import time

class integrationTest:

    """Integration Test for OpenSpecimenAPIconnector.py

    Integration test for the PIP Package OpenSpecimenAPIconnector.py. This class test if the OpenSpecimen
    distribution which the user uses is compatibel with this package. Throught to changes of tables the minimum version 
    is 6.1.RC1. It testes if the package has a connection to through the API to openSpecimen, and if the different calls
    have a response. Errors like double entries, won't be checked. The error is then in the response and created from 
    OpenSpecimen itself.
    """

    def __init__(self, base_url, auth, filename = None, path = "log/"):

        """Constructor

        Constructor of the class integrationTest. If one initialize this class, a filename is created  with the name
        OSapiConnIntTest_*now*.txt, where *now* equals the time now with the format YYYY-MM-DD hh:mm:ss.microsecond.
        This filename is a member of the class.
        """

        self.base_url = base_url
        self.auth = auth
        if filename == None:
            filename = "OSapiConnIntTest2_"+str(datetime.now())+".txt"
        self.logFile = open(path +filename, "a")

        self.ID = {}
        self.names = {}

        OSconn.config_manager.set_login(url = base_url, auth = auth)

        self.inst = os_core.institutes()
        self.inst_util = os_util.institutes_util()

        self.site = os_core.sites()
        self.site_util = os_util.site_util()

        self.user = os_core.users()
        self.user_util = os_util.user_util()
        
        self.cp = os_core.collection_protocol()
        self.cp_util = os_util.collection_protocol_util()

        self.cpr = os_core.collection_protocol_registration()
        self.cpr_util = os_util.cpr_util()
        self.part = os_core.participant()

        self.cpe = os_core.collection_protocol_event()
        self.cpe_util = os_util.cpevent_util()

        self.vis = os_core.visit()
        self.vis_util = os_util.visit_util()

        self.spec = os_core.specimen()
        self.spec_util = os_util.specimen_util()

        self.qry = os_core.query()
        self.qry_util = os_util.query_util()
        
        self.jsons = os_core.Json_factory()
        self.url = os_core.url_gen()


    def runIntegrationTest(self):
                
        try:
            self.IntegrationTest()
        except AssertionError as error:
            print(error)
        finally:
            self.cleanUp()


    def IntegrationTest(self):
        ### Hierarchially ordered
        ########################################################################################################
        ############################ C R E A T I N G / U P D A T I N G #########################################
        ########################################################################################################
        ## Institutes
        #  First Create an Institute
        self.logFile.write("-Creating an Institute- \n")
        response = self.inst_util.create_institute(institutename = "IntegrationTestInstitute")
        assert str(response).lower().find('error')==-1, "Error creating institute: "+str(response)
        assert bool(response), "error creating institute"
        self.logFile.write(str(response)+ " \n")

        # Searching for an institute by name
        self.logFile.write("-Search for an Institute via Substring- \n")
        response = self.inst.search_institutes(substring = "IntegrationTestInstitute")
        assert str(response).lower().find('error')==-1, "Error searchin for an institute: "+str(response)
        assert bool(response), "error searchin for an institute"
        self.logFile.write(str(response) + " \n")
        self.ID['institute'] = response[0]["id"]

        #Updating and institute
        self.logFile.write("-Updating an Institute- \n")
        self.names['institute']= "IntegrationTestInstitute1"
        params = self.jsons.create_institute(institutename = self.names['institute'])
        response = self.inst.update_institute(inid = self.ID['institute'], params = params)
        assert str(response).lower().find('error')==-1, "Error updating an institute: "+str(response)
        assert bool(response), "error updating an institute"
        self.logFile.write(str(response) + " \n")
        

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

        
        ##Collection protocol
        # create collection protocol
        self.logFile.write("-Create Collection protocol- \n")
        self.names['CP']="IntegrationTestCP"
        response = self.cp_util.create_cp(short_title = "IntTestCP", title = self.names['CP'], pi_mail = "admin", sites = [self.names["site"]])
        assert str(response).lower().find('error')==-1, "Error creating Colelction protocol: "+str(response)
        assert bool(response), "Error creating Colelction protocol"
        self.logFile.write(str(response) + ' \n')
        
        #search cp
        self.logFile.write("-Search CPS- \n")
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


        ##Collection Protocol Registration
        #Create a Registration
        self.logFile.write('-Create Registration- \n')
        response = self.cpr_util.create_registration(regdate = "2021-02-24", cpid = self.ID['CP'], ppid = "IntegrationTestPPID")
        assert str(response).lower().find('error')==-1, "Error creating Participant: "+str(response)
        assert bool(response), "Error creating Participant"
        self.ID['cpr']=response['id']
        self.logFile.write(str(response)+ ' \n')

        #Update a Registration
        self.logFile.write('-Update Registration- \n')
        self.ID['ppid']="IntegrationTestPPID1"
        response = self.cpr_util.update_registration(cprid= self.ID['cpr'], regdate = "2021-02-24", cpid = self.ID['CP'], ppid = self.ID['ppid'])
        assert str(response).lower().find('error')==-1, "Error updating Participant: "+str(response)
        assert bool(response), "Error updating Participant"
        self.logFile.write(str(response)+ ' \n')

        #Get Participant
        self.logFile.write('-Get Participant via PPID- \n')
        response = self.part.get_participant(ppid = self.ID['ppid'])
        assert str(response).lower().find('error')==-1, "Error getting Participant: "+str(response)
        assert bool(response), "Error getting Participant"
        self.logFile.write(str(response)+ ' \n')

        
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

        
        ##Visits
        #Create a Visit
        self.logFile.write('-Create a Visit- \n')
        self.names['visit']="IntegrationTestVisit"
        response = self.vis_util.add_visit(cprid = self.ID['cpr'], name = self.names['visit'], site = self.names['site'])
        assert str(response).lower().find('error')==-1, "Error creating a Visit: "+str(response)
        assert bool(response), "Error creating a Visit"
        self.ID['visit']=response['id']
        self.logFile.write(str(response)+ ' \n')

        #Get visit with cprID
        self.logFile.write('- Get visit by CPRID- \n')
        response = self.vis_util.search_visit_cprid(cprid = self.ID['cpr'])
        assert str(response).lower().find('error')==-1, "Error getting visit: "+str(response)
        assert bool(response), "Error getting visit"
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

        #####################################################################################
        ################################## C S V  ###########################################
        #####################################################################################


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
        self.logFile.write("-Get Site  via ID(is already deleted- \n")
        response = self.site.get_site(siteid = self.ID['site'])
        assert str(response).lower().find('error')==-1, "Error getting Site: "+str(response)
        assert bool(response), "Error getting Site"
        self.logFile.write(str(response) + ' \n')

        #delete Isntitute
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
        if 'cpr' in self.ID.keys():
            self.cpr.delete_participant(cprid = self.ID["cpr"])
        if 'CP' in self.ID.keys():
            self.cp.delete_collection_protocol(cpid = self.ID['CP'])
        if 'user' in self.ID.keys():
            self.user.delete_user(userid = self.ID['user'])
        if 'site' in self.ID.keys():
            self.site.delete_sites(siid = self.ID['site'])
        if 'institute' in self.ID.keys():
            self.inst.delete_institute(inid = self.ID['institute'])