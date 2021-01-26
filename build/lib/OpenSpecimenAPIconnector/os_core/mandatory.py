#! /bin/python3

import json
import pandas
import numpy


class mark_mandatory:

    def __init__(self):

        pass

#   This class at the 'identifier' to the name of the mandatory fields,
    def mark_as_mandatory(self, names_list, mandatory_list, mand_ident, identifier):

        print('#-1')
        print(numpy.nonzero(mandatory_list))
        print('#0')
        print(mand_ident)
        ind = numpy.where(mandatory_list == mand_ident)
        print('#1')
        print(ind)
        new_list = names_list
        print('#2')
        print(new_list)
        new_list[ind]=[str(identifier)+ item for item in new_list[ind]]
        print('#3')
        print(new_list)
        return(new_list)
