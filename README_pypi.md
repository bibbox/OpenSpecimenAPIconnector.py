# OpenSpecimenAPIconnector.py
Version 0.9.2
python framework for importing, exporting and combining various data entries from OpenSpecimen and Molgenis


Info about OpenSpecimen: https://openspecimen.atlassian.net/wiki/spaces/CAT/overview

Code can be found at https://github.com/bibbox/OpenSpecimenAPIconnector.py<br>
Find the Documentation at https://openspecimenapiconnectorpy.readthedocs.io/en/latest/index.html

General Framework strucutre (Early Alpha Stage. More Updates Soon):

In general the Framework is comprised of 2 individual Levels:<br>
  - core_OS/MG: contains the core classes that handle 1 call operations like get/set/post/put for Molgenis   and OpenSpecimen, the requests are generated here such that OpenSpecimen's needs are fullfilled and it generates json-formatted strings, which OpenSpecimen can read according to the different entities.<br>
  - utility_OS/MG/merge contains classes that handle combinations of the mehtods given in the core level to accomplish more complex operations (combining 2 or more API calls) like creating of collections and participants.<br>
  - All further operations are then handled via python scripts that use the methods from above to implement the desired functionality.

