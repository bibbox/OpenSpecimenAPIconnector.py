#! /bin/python3

# Import
import json

from .req_util import OS_request_gen
from .. import config_manager

class collection_protocol_registration:

    """Handles the API calls to registrate participants to a Collection Protocol

    Handles the OpenSpecimen API calls to registrate participants to an existing Collection Protocol.
    This class can create participants, delete participants, register existing participants to another protocol,
    merge participants, get the details of an existing participant or more existing participants, update a participant,
    get the consent forms of a participant, download a consent form and delete consents form of participants.

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where also Participants are registrated is in the Jupyter-Notebook

        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the core class collection_protocol_registration

        Constructor of the class collection_protocol_event. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py).

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """
        self.base_url = config_manager.get_url() + '/collection-protocol-registrations'
        self.auth = config_manager.get_auth() 
        self.OS_request_gen = OS_request_gen(self.auth)

    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are any unexpected errors, one can easily test if the URL and login data is spelled correctly.
        The function prints the URL and login data to the output terminal, which was handed over to the class.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def create_participant(self, params):

        """Create or update a participant to a Collection Protocol.

        This function can create a new participant or update an existing participant to an already existing
        Collection Protocol. To use this function one has to know either the Collection Protocoll id <cpId>,
        the title of the Collection Protocol <cpTitle> or the short title of the Collection Protocol <cpshorttitle> .
        Those values can be seen via GUI, extracted from the responses with the class collection_protocol in os_core or
        collection_protocol_util in os_util. To update a participant, one has to specify the unique ID of the participant.
        This Id can be searched via the function get_participant_matches in the os_core class participants.

        Parameters
        ----------
        params : string
            JSON formatted string with the parameters of the participant. The paramter participant is a JSON-formatted string itself,
            for creating a participant it can be left empty; for updating the ID of the participant is needed. The keys of the participant
            dict are id[mandatory for updating], firstName, middleName, lastName, uid, birthdate, vitalStatus, deathDate, gender,
            race, ethnicities, sexGenotype, pmis, mrn, siteName, empi.

        One of the following keys is mandatory to identify the protocol where the participant is created or updated cpId, cpTitle or cpShortTitle.

            The key ppid has to be left blank, if it is set to be autogenerated by the system and is mandatory, if it is created manually.

        registrationDate is a mandatory key, the date format is YYYY-MM-DD .

        Returns
        -------
        JSON-dict
            Details of the created or updated Participant or the OpenSpecimen error message as Dictionary.
        """

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


    def delete_consent(self, cprid):

        """Delete a consent form of a participant.

        Deletes a consent form of an existing participant with the uniquely participant ID <cprid>
        which is generated from the system. The ID has to be known and can be seen for Examples via 
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.

        Parameters
        ---------
        cprid : int
            System generated unique ID of the participant. Will get converted to a string.

        Returns
        -------
        JSON-dict
            dict with value true or error message 
        """

        endpoint = '/' + str(cprid) + '/consent-form'
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def delete_participant(self, cprid):

        """Delete a participant from a Collection Protocol

        Deletes an existing participant with the uniquely participant ID <cprid>
        which is generated from the system. The ID has to be known and can be seen for Examples via 
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.

        Parameters
        ---------
        cprid : int
            System generated unique ID of the participant. Will get converted to a string.

        Returns
        -------
        JSON-dict
            Details of the deleted participant or OpenSpecimen's error message.
        """

        endpoint = '/' + str(cprid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def download_consent_form(self, cprid):

        """Download the consent form of a participant.

        Downloads the consent form of an existing participant with the uniquely participant ID <cprid>
        which is generated from the system. The ID has to be known and can be seen for Examples via 
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.

        Parameters
        ---------
        cprid : int
            System generated unique ID of the participant. Will get converted to a string.

        Returns
        -------
        binary
            Binary file content of the consent form or a status code.
        """

        endpoint = '/' + str(cprid) + '/consent-form'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return r


    def get_consents(self, cprid):

        """Get the consent form of a participant.

        Gets the consent form of an existing participant with the uniquely participant ID <cprid>
        which is generated from the system. The ID has to be known and can be seen for Examples via 
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.

        Parameters
        ---------
        cprid : int
            System generated unique ID of the participant. Will get converted to a string.

        Returns
        -------
        JSON-dict
            Details of the consent form or the openSpecimen's error message.
        """

        endpoint = '/' + str(cprid) + '/consents'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return r


    def get_extension_records(self, cprid):

        """Get the extension forms of a participant.

        Gets the extension forms of an existing participant with the uniquely participant ID <cprid>
        which is generated from the system. The ID has to be known and can be seen for Examples via
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.

        Parameters
        ---------
        cprid : int
            System generated unique ID of the participant. Will get converted to a string.

        Returns
        -------
        JSON-dict
            Details of the extension form or the openSpecimen's error message.
        """

        endpoint = '/' + str(cprid) + '/extension-records'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)



    def get_registration(self, cprid):

        """Get the details form of a participant.

        Gets the details as JSON-dict form of an existing participant with the uniquely participant ID <cprid>
        which is generated from the system. The ID has to be known and can be seen for Examples via 
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.

        Parameters
        ---------
        cprid : int
            System generated unique ID of the participant. Will get converted to a string.

        Returns
        -------
        JSON-dict
            Details of the participant or the openSpecimen's error message.
        """
 
        endpoint = '/' + str(cprid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_registrations(self, params):

        """Search for one or more participants

        Gets the details of one or more participants, which are specified in the parameters.
        The Parameters are passed via a JSON-formatted string. This function is used in the 
        os_util class cpr_util, where the specific parameters can be passed.

        Parameters
        ---------
        params : string
            Json formatted string with keys: cpId, registrationDate[optional], name(substring of first, last or middlename)[optional],
            ppid[optional], participantId[optional], dob[optional], specimen[optional], startAt(default=0)[optional],
            maxResults(default=100)[optional], includeStats(default=false)[optional], exactMatch(default=false)[optional]

        Returns
        -------
        JSON-dict
            Details of the Participant, who are matching the search criteria.
        """

        endpoint = '/list'
        url = self.base_url + endpoint
        payload= params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)

  
    def register_to_cp(self, params):

        """Register a participant to another Collection Protocol

        Registers an already existing Participant to another Collection Protocol.
        The Participants unique ID has to be known and can be seen for Examples via 
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.
        Also, the collection protocol ID of the Protocol in which the participant is registered at has to be known.

        Parameters
        ---------
        params : string
            JSON-formatted string with the Parameters: the keys are participant( value is a dict with key id and value
            Pariticipant ID[mandatory])[mandatory], registrationDate [mandatory], cpId [mandatory],
            ppid[mandatory if manually generated, leave empty if system-generated]

        Returns
        -------
        JSON-dict
            JSON-dict of the participant which is registred to another protocol.
        """

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)



    def merge_participants(self, id_from, id_to):

        """Merge Participant x to Participant y

        Merges Participant with the unique Participant ID <id_from> to the Participant with
        unique Participant ID <id_to>. This will move data from all visits and specimens from the source participant to the target participant
        and then deletes the source participant.
        The Participants unique ID has to be known and can be seen for Examples via 
        the GUI in the URL: http(s)://<host>:<port>/openspecimen/cp-view/{cpId}/participants/{cprid}/...
        or with the function get_participant_matches in the os_core class participants.

        Parameters
        ----------
        id_from : int
            System generated unique ID of the source participant. Will get converted to a string.
        
        id_to : int
            System generated unique ID of the target participant. Will get converted to a string.

        Returns
        -------
        JSON-dict
           Returns details of the merged participants as JSON-dict or OpenSpecimen's error message.
        """

        endpoint = '/'+ str(id_from)
        url = self.base_url + endpoint
        payload = '{\"participant\":{\"id\":\"' + str(id_to) + '\"}}'
        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)

    
    def update_participant(self, cprid, params):

        """Update a participant already in a Collection Protocol.

        This function can update an existing participant with a unique Participant ID <cprid> to an already existing
        Collection Protocol. To use this function one has to know either the Collection Protocoll id <cpId>,
        the title of the Collection Protocol <cpTitle> or the short title of the Collection Protocol <cpshorttitle> .
        Those values can be seen via GUI, extracted from the responses with the class collection_protocol in os_core or
        collection_protocol_util in os_util. To update a participant, one has to specify the unique ID of the participant.
        This Id can be searched via the function get_participant_matches in the os_core class participants.

        Parameters
        ----------
        cprid : int
            System generated unique ID of the participant. Will get converted to a string.

        params : string
            JSON formatted string with the parameters of the participant. The paramter participant is a JSON-formatted string itself,
            the parameters which are passed will get updated. The keys of the participant
            dict are id[mandatory], firstName, middleName, lastName, uid, birthdate, vitalStatus, deathDate, gender,
            race, ethnicities, sexGenotype, pmis, mrn, siteName, empi.

        One of the following keys is mandatory to identify the protocol, where the participant is created or updated cpId, cpTitle or cpShortTitle.

            The key ppid has to be left blank, if it is set to be autogenerated by the system and is mandatory, if it is created manually.

        registrationDate is a mandatory key, the date format is YYYY-MM-DD .

        Returns
        -------
        JSON-dict
            Details of the created or updated Participant or the OpenSpecimen error message as Dictionary.
        """

        endpoint = '/' + str(cprid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)
        return json.loads(r.text)
