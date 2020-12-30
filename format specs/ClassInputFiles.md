# Class Input File Format

The class input files (eg. Aggregate.csv) include a list of flowables that belong to the class and 
SecondaryContext designates which context paths are available for each flowable (see [Contexts](Contexts.md)).
Flowables may belong to one or many classes and each flowable may be assigned one or many SecondaryContext designations.
The list of flowables available for representation in the class input files can be found in [FlowableUnits](FlowableUnits.md).
The class names also define material flows of the same name. Each material flow is automatically assigned both 'material'
and 'waste' as primary contexts. Each class must be specified in the 'flow_list_specs' of globals.py to read in the input file.

The class input files are in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | The flow name. Same as 'Class' in [FlowList](FlowList.md). |
 SecondaryContext | string | Y | The second tier context designation that describes the primary medium and determines which ContextDetails are included.. Same as in [Contexts](Contexts.md). |