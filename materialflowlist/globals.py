"""Set common variables for use in package."""
import sys
import os
import logging as log

try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'materialflowlist/'

outputpath = modulepath + 'output/'
inputpath = modulepath + 'input/'
flowmappingpath = modulepath + 'flowmapping/'

flow_list_fields = {'Flowable': [{'dtype': 'str'}, {'required': True}],
                    'Unit': [{'dtype': 'str'}, {'required': True}],
                    'Class': [{'dtype': 'str'}, {'required': True}],
                    #'External Reference': [{'dtype': 'str'}, {'required': False}],
                    'Context': [{'dtype': 'str'}, {'required': True}],
                    'Flow UUID': [{'dtype': 'str'}, {'required': True}],
                    #'AltUnit': [{'dtype': 'str'}, {'required': False}],
                    #'AltUnitConversionFactor': [{'dtype': 'float'}, {'required': False}]
                    }

log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

flow_list_specs = {
    "list_version": "0.0.1",
    "flow_classes": ["Aggregate", "Crops", "Glass", "Leather", "Livestock", "Metal", "Minerals",
                     "Other petroleum products", "Other plant matter", "Paper", "Plastic", "Textile", "Wood"],
    "primary_context_classes": ["material","product","waste"],
    "category_context_classes": ["Category"],
    "type_context_classes": ["Type"]
}

def as_path(*args: str) -> str:
    """
    Converts strings to lowercase path-like string
    Take variable order of string inputs
    :param args: variable-length of strings
    :return: string
    """
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).strip().lower())
    return "/".join(strings)