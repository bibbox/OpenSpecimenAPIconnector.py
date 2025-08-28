#! /bin/python3

from ..os_core.url import url_gen
from ..os_core.jsons import Json_factory
from ..os_core.catalog import catalog


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
