"""
Provides a pandas dataframe.

Of contexts as paths and as a pattern of context classes. Used by
assemble_materialflowlist.py.
"""

import pandas as pd
from materialflowlist.globals import inputpath, flow_list_specs

contexts = pd.read_csv(inputpath + 'Contexts.csv', na_values='N/A')

# Get levels for max number of compartment classes
max_compartment_classes = len(contexts.columns)

# Define compartment_classes
compartment_classes = flow_list_specs['flow_classes'] + \
                      flow_list_specs['secondary_context_classes'] + \
                      flow_list_specs['detail_context_classes']

# Create dictionary of context levels
context_levels = {}
counter = 0
for c in compartment_classes:
    context_levels['c_' + str(counter)] = c
    counter = counter + 1

# Drop duplicates just as a check
contexts = contexts.drop_duplicates()

#Merge contexts into single database
primarycontexts = pd.DataFrame(data=flow_list_specs['primary_context_classes'],columns=['PrimaryContext'])
primarycontexts['target'] = 1
contexts['target'] = 1
contexts = pd.merge(primarycontexts, contexts, on='target').drop('target', axis=1)