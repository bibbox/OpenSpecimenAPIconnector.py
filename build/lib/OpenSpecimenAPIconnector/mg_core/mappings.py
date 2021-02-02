#! /bin/python3

import json


class bbmri_mapping:

    def __init__(self):
        pass

    def person_extension(self):

        data = {
            "title_before_name":None,
            "title_after_name":None,
            "zip":"123456",
            "city":"City",
            "country":"GR",
            "collections":None
        }
        return data


    def person_map(self):

        data = {
            "first_name":"firstName",
            "last_name":"lastName",
            "email":"emailAddress",
            "phone":"phoneNumber",
            "address":"address",
            "biobanks":"instituteName"
        }
        return data


    def biobank_extension(self):

        data = {
            "partner_charter_signed":'0',
            "head_title_before_name":None,
            "head_role":"PI",
            "contact_priority":"1"
        }
        return data


    def biobank_map(self):

        data = {
            "name":"name",
            "partner_charter_signed":"partner_chart",
            "collections":"collection_protocols_already_in_biobank",
            "biobank":"biobank_label"
        }
        return data

    def collection_map(self):

        data = {
            "acronym":"shortTitle",
            "name":"title",
            "id":"bbmri_collection_id"
        }
        return data