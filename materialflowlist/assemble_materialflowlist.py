"""
Generate the material flow master list.
As a pandas dataframe from input files. Write it to the output folder.
"""

import pandas as pd
from materialflowlist.globals import log, inputpath, outputpath, flow_list_specs, flow_list_fields
from materialflowlist.contexts import contexts
from fedelemflowlist.uuid_generators import make_uuid

def read_in_flowclass_file(flowclass):
    flowclassfile = pd.read_csv(inputpath + flowclass + 'FlowableCategory.csv', header=0, dtype=None)
    flowclassfile = flowclassfile.dropna(axis=0, how='all')
    return flowclassfile

#establishing dataframes and full list of flowables
if __name__ == '__main__':
    flowables = pd.DataFrame()
    flows = pd.DataFrame()
    flowables_for_class = pd.read_csv(inputpath + 'FlowableUnits.csv', header=0, dtype=None)
    log.info('Import ' + str(len(flowables_for_class)) + ' flowables from FlowableUnits.csv')

    # Loop through flow class specific files based on those classes specified in flowlistspecs
    for t in flow_list_specs["flow_classes"]:

        # Drop duplicate flowables in list
        flowables_for_class = flowables_for_class.drop_duplicates(subset='Flowable')

        # Add Flow Class to columns
        flowables_for_class['Class'] = t
        flowables = pd.concat([flowables, flowables_for_class], ignore_index=True, sort=False)
        class_category = read_in_flowclass_file(t)
        flowables_for_class = flowables_for_class.drop_duplicates()
        log.info('Import ' + str(len(class_category)) + ' flowable contexts for class ' + t)
        class_category = class_category.dropna(axis=0, how='all')

        # merge in flowables and flowable primary contexts
        class_flowables_w_category = pd.merge(flowables_for_class, class_category, on=['Flowable'], how='left')
        log.info('Create ' + str(len(class_flowables_w_category)) +
                 ' flows with primary context for class ' + t)
        flows = pd.concat([flows, class_flowables_w_category])

    #create waste flows matching all product flows
    product_waste_contexts = contexts[contexts.PrimaryContext != "material"]
    flows = flows.merge(product_waste_contexts, on=['Class', 'Category'], how='inner')

    #adding flowables based on class name for unspecified material flows and matching waste flows
    material_waste_contexts = contexts.copy(deep=True)
    material_waste_contexts = material_waste_contexts[material_waste_contexts.PrimaryContext != "product"]
    classflows_list = flow_list_specs['flow_classes']
    classflows = pd.DataFrame({'Class':classflows_list})
    classflows['Flowable'] = classflows['Class'].str.lower()
    materialflows = pd.merge(classflows,material_waste_contexts,on='Class')
    materialflows['Unit'] = "kg"

    flows = flows.append(materialflows, ignore_index=False)

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

    # Log unique entries
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