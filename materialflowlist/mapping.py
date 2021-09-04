# mapping.py (materialflowlist)
# !/usr/bin/env python3
# coding=utf-8
"""
Functions to support creation and modification of mapping files for materialflowlist

"""
import pandas as pd
import materialflowlist

from materialflowlist.globals import log, flowmapping_fields


def add_uuid_to_mapping(flow_mapping):
    """
    Adds UUIDs from FEDEFL to a flow mapping file
    :param flow_mapping: dataframe of flow mapping in standard format
    return: flow_mapping_uuid
    """
    mapping_length = len(flow_mapping)
    all_flows = materialflowlist.get_flows()
    all_flows = all_flows[['Flowable', 'Context', 'Flow UUID', 'Unit']]
    flow_mapping = pd.merge(flow_mapping, all_flows, how='left',
                                      left_on=['TargetFlowName', 'TargetFlowContext', 'TargetUnit'],
                                      right_on=['Flowable', 'Context', 'Unit'])
    columns_to_drop = ['Flowable','Context', 'Unit']
    if 'TargetFlowUUID' in flow_mapping:
        columns_to_drop.append('TargetFlowUUID')
    flow_mapping = flow_mapping.drop(columns=columns_to_drop)
    flow_mapping = flow_mapping.rename(columns={'Flow UUID': 'TargetFlowUUID'})
    flow_mapping_uuid = flow_mapping.dropna(subset=['TargetFlowUUID'])
    mapping_merged_len = len(flow_mapping_uuid)
    if mapping_length > mapping_merged_len:
        log.warning("UUIDs not available for all flows")
        dropped = flow_mapping.loc[~flow_mapping.index.isin(flow_mapping_uuid.index)]
        dropped = dropped[['TargetFlowName','TargetFlowClass',
                           'TargetFlowContext']].drop_duplicates().reset_index(drop=True)
        log.info(dropped)
    flow_mapping_uuid.reset_index(drop=True, inplace=True)
    flowmapping_order = [c for c in list(flowmapping_fields.keys()) if c in flow_mapping_uuid.columns.tolist()]
    flow_mapping_uuid = flow_mapping_uuid[flowmapping_order]
    
    return flow_mapping_uuid

