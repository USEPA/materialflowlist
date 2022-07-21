"""Set common variables for use in package."""
import sys
import os
import logging as log


try:
    modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError:
    modulepath = 'materialflowlist/'

PKG_VERSION_NUMBER = '0.0.2'

outputpath = modulepath + 'output/'
inputpath = modulepath + 'input/'
flowmappingpath = modulepath + 'flowmapping/'

flow_list_fields = {'Flowable': [{'dtype': 'str'}, {'required': True}],
                    'Unit': [{'dtype': 'str'}, {'required': True}],
                    'Class': [{'dtype': 'str'}, {'required': True}],
                    'Context': [{'dtype': 'str'}, {'required': True}],
                    'Flow UUID': [{'dtype': 'str'}, {'required': True}],
                    }

flowmapping_fields = {'SourceListName': [{'dtype': 'str'}, {'required': True}],
                      'SourceFlowName': [{'dtype': 'str'}, {'required': True}],
                      'SourceFlowUUID': [{'dtype': 'str'}, {'required': False}],
                      'SourceFlowContext': [{'dtype': 'str'}, {'required': True}],
                      'SourceUnit': [{'dtype': 'str'}, {'required': True}],
                      'MatchCondition': [{'dtype': 'str'}, {'required': False}],
                      'ConversionFactor': [{'dtype': 'float'}, {'required': False}],
                      'TargetFlowName': [{'dtype': 'str'}, {'required': True}],
                      'TargetFlowClass': [{'dtype': 'str'}, {'required': True}],
                      'TargetFlowContext': [{'dtype': 'str'}, {'required': True}],
                      'TargetUnit': [{'dtype': 'str'}, {'required': True}],
                      'TargetFlowUUID': [{'dtype': 'str'}, {'required': True}],
                      'Mapper': [{'dtype': 'str'}, {'required': False}],
                      'Verifier': [{'dtype': 'str'}, {'required': False}],
                      'LastUpdated': [{'dtype': 'str'}, {'required': False}]}

log.basicConfig(level=log.DEBUG, format='%(levelname)s %(message)s',
                stream=sys.stdout)

flow_list_specs = {
    "list_version": PKG_VERSION_NUMBER,
    "flow_classes": ["Aggregate", "Glass", "Leather", "Metal", "Mineral",
                     "Other petroleum products", "Paper", "Biomass",
                     "Plastic", "Textile", "Wood", "Energy"],
    "primary_context_classes": ["material","product","waste"],
    "secondary_context_classes": ["SecondaryContext"],
    "detail_context_classes": ["ContextDetail"]
}


