"""
materialflowlist
"""

import os
import pandas as pd
from materialflowlist.globals import outputpath, flowmappingpath

def get_flows(preferred_only=None):
    """Gets a flow list in a standard format

    Returns the full master flow list unless preferred flows is lists
    :param preferred_only:
    :return: standard Flow List dataframe
    """
    list_file = outputpath + 'MaterialFlowListMaster.parquet'
    flows = pd.read_parquet(list_file)
    if preferred_only:
        flows = flows[flows['Preferred'] == 1]
    return flows

def get_flowmapping(source=None):
    """Gets a flow mapping in standard format

    Looks for a dataframe of the mapping file specific to the source
    If a source list is provided, it returns only the desired mappings
    Returns an error if specified source does not equal the source name
    :param source: Name of source list in
    :return: standard Flow Mapping dataframe
    """
    flowmappings = pd.DataFrame()
    if source is not None:
        if type(source).__name__ == 'str':
            source = [source]
        for f in source:
            mapping_file = flowmappingpath+f+'.csv'
            try:
                flowmapping = pd.read_csv(mapping_file, header=0)
                flowmappings = pd.concat([flowmappings, flowmapping])
            except FileNotFoundError:
                print("No mapping file found for " + str(f))
    else:
        # load all mappings in directory
        files = os.listdir(flowmappingpath)
        for name in files:
            if name.endswith(".csv"):
                flowmapping = pd.read_csv(flowmappingpath+name, header=0)
                flowmappings = pd.concat([flowmappings, flowmapping])
    return flowmappings

