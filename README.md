# OpenSpecimenAPIconnector.py
Version 0.9.1
python framework for importing, exporting and combining various data entries from Open Specimen and Molgenis

SORCE code can be found in src/OpenSpecimenAPIconnector/

Framework strucutre:

In general the Framework is comprised of 2 individual Levels:<br>
  - core_OS/MG: contains the core classes that handle 1 call operations like get/set/post/put for Molgenis   and OpenSpecimen, the requests are generated here such that OpenSpecimen's needs are fullfilled and it generates json-formatted strings, which OpenSpecimen can read according to the different entities.<br>
  - utility_OS/MG/merge contains classes that handle combinations of the mehtods given in the core level to accomplish more complex operations (combining 2 or more API calls) like creating of collections and participants.<br>
  - It does not generate any data_files and accepts json input/csv finished data inputs. More clearly it only does operations that setup predifined structures. Use inheritance as needed (see code file template in util folders for more information)<br>
  - All further operations are then handled via python scripts that use the methods from above to implement the desired functionality.

To install the pip package after cloning run:<br>
pip install dist/OpenSpecimenAPIconnector-0.9.1-py3-none-any.whl