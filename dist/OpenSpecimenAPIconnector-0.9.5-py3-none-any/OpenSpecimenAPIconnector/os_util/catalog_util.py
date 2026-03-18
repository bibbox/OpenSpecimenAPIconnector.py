#! /bin/python3
import json

from ..os_core.url import url_gen
from ..os_core.jsons import Json_factory
from ..os_core.catalog import catalog
from ..os_core.users import users


class catalog_util:
    """Handles the API calls for the catalog

    Handles the OpenSpecimen API calls for the catalog. This class can
    close a specimen request. The other calls are in the os_core catalog form.

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------
    """

    def __init__(self):
        """Constructor of the Class catalog_util

        Constructor of the class catalog_util, can handle the  API-calls
        to work with the catalog in OpenSpecimen. Connects this class os_core
        classes catalog and Json_factory

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """
        self.catalog = catalog()
        self.jsons = Json_factory()
        self.users = users()

    def place_request(self, catalog_id, user_id, request_form_data, specimen_ids):
        """

        Parameters
        ----------
        catalog_id: int
            ID of the catalog where the order should be placed
        user_id: int
            ID of the user who requests the specimens
        request_form_data: dict
            e.g.: form_data = {
                    "name_of_study": "dfaewf",
                    "short_name_of_study": "fesasfe",
                    "receiving_site_dropdown": "Christoph's office",
                    "comments": "Order placed via the dashboard.",
                    "patient_gender": "No",
                    "patient_age": "No",
                    "material_anatomical_site": "No",
                    "material_specification": "No",
                    "material_collection_method": "No",
                    "block_specification": "No",
                    "slide_specification": "No",
                    "staining": "No",
                    "diagnosis": "No",
                    "macroscopic_description": "No",
                    "histological_description": "No",
                    "molecular_pathological_description": "No",
                    "molecular_pathological_diagnosis": "No",
                    "frozen_section_examination": "No",
                    "additional_information": "No"
                }

        specimen_ids: list
            List of specimen IDs

        Returns
        -------
            response

        """
        requestor = {"requestor": self.users.get_user(user_id)}

        assert isinstance(specimen_ids, list), "Specimen ids have to be given as list!"
        items_list = [{"specimen": {"id": int(specimen_id)}} for specimen_id in specimen_ids]
        items = {"items": items_list}

        attrs_list = [{"name": key, "value": value} for key, value in request_form_data.items()]
        extension_detail = {"extensionDetail": {"attrs": attrs_list}}

        merged_payload = {
            **requestor,
            **items,
            **extension_detail
        }
        payload = json.dumps(merged_payload, indent=2)

        r = self.catalog.place_request(catalog_id, payload)
        return r



    def close_request(self, catalog_id, request_id, reason=None):
        """Close the specimen request in a specific catalog

        Warning: This is not reversible!

        Parameters
        ----------
        catalog_id (int): The ID of the catalog
        request_id (int): The ID of the specifig request
        reason (str): The comment string why the request is closed.

        Returns
        -------
        str
            A JSON-formatted string containing the API response.

        """
        params = self.jsons.close_catalog_request_json(request_id, reason)
        r = self.catalog.close_request(catalog_id, request_id, params)

        return r
