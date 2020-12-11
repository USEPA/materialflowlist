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

    #generating context cutoff at category and full contexts
    flowscategorycutoff = flows.copy(deep=True)
    flowscategorycutoff['Context'] = flowscategorycutoff['PrimaryContext'] + "/" + flowscategorycutoff['Category']
    flowscategorycutoff = flowscategorycutoff.drop(columns=['PrimaryContext', 'Category', 'Type'])
    flows['Context'] = flows['PrimaryContext'] + "/" + flows['Category'] + "/" + flows['Type']
    flows = flows.drop(columns=['PrimaryContext', 'Category', 'Type'])

    flows = flows.append(flowscategorycutoff, ignore_index=False)

    log.info('Total of ' + str(len(flows)) + ' flows with contexts created.')

    # Loop through flows generating UUID for each
    flowids = []
    log.info('Generating unique UUIDs for each flow...')
    for index, row in flows.iterrows():
        flowid = make_uuid(row['Flowable'], row['Context'], row['Unit'])
        flowids.append(flowid)
    flows['Flow UUID'] = flowids

    # Drop entries due to duplicate UUIDs
    flows['Duplicates'] = flows.duplicated(subset=['Flow UUID'], keep='first')
    if flows['Duplicates'].sum() > 0:
        log.info(str(flows['Duplicates'].sum()) + " flows with same UUID; these duplicates have been removed.")
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
    log.info('CSV version in MaterialFlowList'+flow_list_specs['list_version']+'_all.csv')