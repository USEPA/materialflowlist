"""
Generate the material flow master list.
As a pandas dataframe from input files. Write it to the output folder.
"""

import pandas as pd
from materialflowlist.globals import log, inputpath, outputpath, flow_list_specs, flow_list_fields
from materialflowlist.contexts import contexts
from fedelemflowlist.uuid_generators import make_uuid

def read_in_flowclass_file(flowclass):
    flowclassfile = pd.read_csv(inputpath + flowclass + '.csv', header=0, dtype=None)
    flowclassfile = flowclassfile.dropna(axis=0, how='all')
    return flowclassfile

def firstpluslast(s):
    return s[0]+s[-1]

def get_mat_acr(df):
    cols = ["Flowable","SecondaryContext","ContextDetail"]
    acr = df[cols[0]].apply(firstpluslast) + df[cols[1]].apply(firstpluslast) + df[cols[2]].apply(firstpluslast)
    return acr


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
        class_secondarycontext = read_in_flowclass_file(t)
        flowables_for_class = flowables_for_class.drop_duplicates()
        log.info('Import ' + str(len(class_secondarycontext)) + ' flowable contexts for class ' + t)
        class_secondarycontext = class_secondarycontext.dropna(axis=0, how='all')

        # merge in flowables and flowable primary contexts
        class_flowables_w_secondarycontext = pd.merge(flowables_for_class, class_secondarycontext, on=['Flowable'], how='left')
        log.info('Create ' + str(len(class_flowables_w_secondarycontext)) +
                 ' flows with primary context for class ' + t)
        flows = pd.concat([flows, class_flowables_w_secondarycontext])

    #create all product flows and matching waste flows
    product_waste_contexts = contexts[contexts.PrimaryContext != "material"]
    flows = flows.merge(product_waste_contexts, on=['Class', 'SecondaryContext'], how='inner')

    #adding flowables based on class name for unspecified material flows and matching waste flows
    material_waste_contexts = contexts.copy(deep=True)
    material_waste_contexts = material_waste_contexts[material_waste_contexts.PrimaryContext != "product"]
    class_list = flow_list_specs['flow_classes']
    classflows = pd.DataFrame({'Class':class_list})
    classflows['Flowable'] = classflows['Class'].str.lower()
    materialflows = pd.merge(classflows,material_waste_contexts,on='Class')
    materialflows['Unit'] = "kg"

    flows = flows.append(materialflows, ignore_index=False)

    #Add material abbreviation
    flows['mat_abbr'] = get_mat_acr(flows)

