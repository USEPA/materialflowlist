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
                    'Context': [{'dtype': 'str'}, {'required': True}],
                    'Flow UUID': [{'dtype': 'str'}, {'required': True}],
                    }

log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

flow_list_specs = {
    "list_version": "0.0.1",
    "flow_classes": ["Aggregate", "Glass", "Leather", "Metal", "Mineral",
                     "Other petroleum products", "Paper", "Biomass", "Plastic", "Textile", "Wood", "Energy"],
    "primary_context_classes": ["material","product","waste"],
    "secondary_context_classes": ["SecondaryContext"],
    "detail_context_classes": ["ContextDetail"]
}

