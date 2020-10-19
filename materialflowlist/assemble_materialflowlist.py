"""
Generate the elementary flow master list.

As a pandas dataframe from input files. Write it to the output folder.
"""

import pandas as pd
from materialflowlist.globals import log, inputpath, outputpath, flow_list_specs, flow_list_fields, as_path
from materialflowlist.contexts import all_contexts, contexts
from fedelemflowlist.uuid_generators import make_uuid

#altunits_data_types = {'Conversion Factor': flow_list_fields['AltUnitConversionFactor'][0]['dtype']} #AltUnitConversionFactor

def read_in_flowclass_file(flowclass, flowclasstype):
    """
    Declare data types for select variables in flow class input files.

    :param flowclass: One of the flow class names
    :param flowclasstype: either 'Flowables',or 'FlowablePrimaryContexts'
    :return: pd dataframe for that flow class file
    """
    data_types = None
    #if flowclasstype == 'FlowableAltUnits':
        #data_types = altunits_data_types
    flowclassfile = pd.read_csv(inputpath + flowclass + flowclasstype + '.csv', header=0, dtype=data_types)
    flowclassfile = flowclassfile.dropna(axis=0, how='all')
    return flowclassfile

if __name__ == '__main__':

    flowables = pd.DataFrame()
    flows = pd.DataFrame()
    #flowables_w_primary_contexts = pd.DataFrame()
    #primary_contexts = pd.DataFrame()

    # Loop through flow class specific files based on those classes specified in flowlistspecs
    for t in flow_list_specs["flow_classes"]:
        # Handle flowables first
        flowables_for_class = read_in_flowclass_file(t, 'Flowables')
        log.info('Import ' + str(len(flowables_for_class)) + ' flowables for class ' + t)
        # Drop duplicate flowables in list
        flowables_for_class = flowables_for_class.drop_duplicates(subset='Flowable')
        # Add Flow Class to columns
        flowables_for_class['Class'] = t
        flowables = pd.concat([flowables, flowables_for_class], ignore_index=True, sort=False)
        class_primary_contexts = read_in_flowclass_file(t, 'FlowablePrimaryContexts')
        flowables_for_class = flowables_for_class.drop_duplicates()
        log.info('Import ' + str(len(class_primary_contexts)) + ' flowable contexts for class ' + t)
        class_primary_contexts = class_primary_contexts.dropna(axis=0, how='all')

        # merge in flowables and flowable primary contexts
        class_flowables_w_primary_contexts = pd.merge(flowables_for_class, class_primary_contexts, on=['Flowable'], how='left')
        # Add in Alt units
        try:
            altunits_for_class = read_in_flowclass_file(t, 'FlowableAltUnits')
            altunits_for_class = altunits_for_class.drop_duplicates()
            # Drop external reference for now
            altunits_for_class = altunits_for_class.drop(columns=['External Reference'])
            # Left join in alt units
            # rename cols to match final flow list specs
            altunits_for_class = altunits_for_class.rename(columns={'Conversion Factor': 'AltUnitConversionFactor',
                                                                    'Alternate Unit': 'AltUnit'})
            class_flowables_w_primary_contexts = pd.merge(class_flowables_w_primary_contexts, altunits_for_class,
                                                          left_on=['Flowable', 'Unit'],
                                                          right_on=['Flowable', 'Reference Unit'], how='left')
            # Drop old reference unit
            class_flowables_w_primary_contexts = class_flowables_w_primary_contexts.drop(columns=['Reference Unit'])
        except FileNotFoundError:
            altunits_for_class = None  # Do nothing
        log.info('Create ' + str(len(class_flowables_w_primary_contexts)) +
                 ' flows with primary context for class ' + t)
        flows = pd.concat([flows, class_flowables_w_primary_contexts])
    flows = flows.merge(contexts, on=['Class', 'PrimaryContext'], how='inner')
    log.info('Total of ' + str(len(flows)) + ' flows with contexts created.')

    #Write to csv
    flows.to_csv(outputpath+'MaterialFlowList'+flow_list_specs['list_version']+'_draft.csv', index=False)
    log.info('CSV version in ' + 'output/MaterialFlowListMaster_draft.csv')



    """
    # Read in flowable context membership
    SecondaryContextMembership = import_secondary_context_membership()

    secondary_context_classes = flow_list_specs["secondary_context_classes"]
    context_patterns_used = pd.DataFrame(
        columns=['Class', 'PrimaryContext', 'Primary_Context_Path', 'Pattern'])
    for index, row in SecondaryContextMembership.iterrows():
        pattern = [x for x in secondary_context_classes if row[x] != 0]
        pattern_w_primary = flow_list_specs["primary_context_classes"].copy() + pattern
        # convert to string
        pattern_w_primary = ','.join(pattern_w_primary)
        primary_context_path = as_path(row['PrimaryContext'])
        context_patterns_used = context_patterns_used.append({'Class': row['Class'],
                                                              'PrimaryContext': row['PrimaryContext'],
                                                              'Primary_Context_Path': primary_context_path,
                                                              'Pattern': pattern_w_primary},
                                                             ignore_index=True)
    """

"""
    # Cycle through these class context patterns and get context_paths
    log.info('Getting relevant contexts for each class ...')
    field_to_keep = ['Class', 'PrimaryContext', 'SecondaryContext']
    class_contexts_list = []
    for index, row in contexts.iterrows():
        class_context_patterns_row = row[field_to_keep]
        # Get the contexts specific to this class by matching the Pattern and Primary_Context_Path
        contexts_df = all_contexts[(all_contexts['Pattern'] == row['Pattern']) & (
            all_contexts['Context'].str.contains(row['Primary_Context_Path']))]
        c_group = []
        for i in contexts_df['Context']:
            c = {}
            c['Context'] = i
            for f in field_to_keep:
                c[f] = row[f]
            c_group.append(c)
        class_contexts_list.extend(c_group)
    class_contexts = pd.DataFrame(class_contexts_list)

    # Merge this table now with the flowables and primary contexts with the full contexts per class, creating flows for each compartment relevant for that flow type, using major
    flows = pd.merge(flowables_w_primary_contexts, class_contexts,
                     on=['Class', 'PrimaryContext'])

    # Drop duplicate flows if they exist
    if len(flows[flows.duplicated(keep=False)]) > 0:
        log.debug("Duplicate flows exist. They will be removed.")
        flows = flows.drop_duplicates()

    # Drop unneeded columns
    cols_to_drop = ['PrimaryContext']
    flows = flows.drop(columns=cols_to_drop)

    # Loop through flows generating UUID for each
    flowids = []
    log.info('Generating unique UUIDs for each flow...')
    for index, row in flows.iterrows():
        flowid = make_uuid(row['Flowable'], row['Context'], row['Unit'])
        flowids.append(flowid)
    flows['Flow UUID'] = flowids

    # Drop duplicate entries due to multiple alt units
    flows['Duplicates'] = flows.duplicated(subset=['Flow UUID'], keep='first')
    if flows['Duplicates'].sum() > 0:
        log.info(str(flows['Duplicates'].sum()) + " flows with multiple alt unit; these duplicates have been removed:")
        duplicates_df = flows.loc[flows['Duplicates'] == True, 'Flowable']
        print(duplicates_df.drop_duplicates().to_string(index=False))
        flows = flows.drop_duplicates(subset=['Flow UUID'], keep='first')
    flows.drop(columns='Duplicates')

    contexts_in_flows = pd.unique(flows['Context'])
    log.info('Created ' + str(len(flows)) + ' flows with ' + str(len(contexts_in_flows)) + ' unique contexts')

    # Conform flows to final list structure
    flows = flows[list(flow_list_fields.keys())]

    # Write it to parquet
    flows.to_parquet(outputpath + 'MaterialFlowListMaster.parquet',
                     index=False, compression=None)
    log.info('Stored flows in ' + 'output/MaterialFlowListMaster.parquet')

    #Write to excel
    #flows.to_excel(outputpath+'MaterialFlowList'+flow_list_specs['list_version']+'_all.xlsx', index=False)
    #log.info('Excel version in ' + 'output/MaterialFlowListMaster_all.xlsx')

    #Write to csv
    flows.to_csv(outputpath+'MaterialFlowList'+flow_list_specs['list_version']+'_all.csv', index=False)
    log.info('CSV version in ' + 'output/MaterialFlowListMaster_all.csv')
    
"""