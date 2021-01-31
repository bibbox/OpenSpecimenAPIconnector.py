#! /bin/python3

#### This is for testing reasons online


from ..os_core.users import users
from ..os_core.specimen import specimen
from ..os_core.mandatory import mark_mandatory
from ..os_core.csv_bulk import csv_bulk
from ..os_core.visit import visit
from ..os_core.participant import participant
from ..os_core.collection_protocoll import collection_protocol
from ..os_core.collecttion_protocol_registration import collection_protocol_registration
from ..os_core.collection_protocol_event import collection_protocol_event
from ..os_core.query import query

from .cpevent_util import cpevent_util
from .bulk_operations import bulk_operations
from .query_util import query_util
from .cpr_util import cpr_util
from .visit_util import visit_util
import json
import pandas
import random


