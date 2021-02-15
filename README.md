# OpenSpecimenAPIconnector.py
Version 0.9.0
python framework for importing, exporting and combining various data entries from Open Specimen and Molgenis

SORCE code can be found in src/OpenSpecimenAPIconnector/

Framework strucutre:

In general the Framework is comprised of 2 individual Levels:<br>
  - core_OS/MG: contains the core classes that handle 1 call operations like get/set/post/put for Molgenis   and OpenSpecimen, the requests are generated here such that OpenSpecimen's needs are fullfilled and it generates json-formatted strings, which OpenSpecimen can read according to the different entities.<br>
  - utility_OS/MG/merge contains classes that handle combinations of the mehtods given in the core level to accomplish more complex operations (combining 2 or more API calls) like creating of collections and participants.<br>
  - It does not generate any data_files and accepts json input/csv finished data inputs. More clearly it only does operations that setup predifined structures. Use inheritance as needed (see code file template in util folders for more information)<br>
  - All further operations are then handled via python scripts that use the methods from above to implement the desired functionality.
  
Currently the new structure is applied to the initial code. Further the concept of limitied objects which are passed by call by reference is reworked to a better

run python API_query from within the initial code folder,py from root dir to see the first few methods in action <br>
Make Sure to provide a valid OS URL

To install the pip package after cloning run:<br>
pip install dist/OpenSpecimenAPIconnector-0.9.1-py3-none-any.whl