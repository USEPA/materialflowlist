# Class Input File Format

The Class Input Files (eg. Aggregate.csv) include a list of flowables that belong to the class and 
SecondaryContext designates which context paths are available for each flowable (see [Contexts](Contexts.md).
Flowables may belong to one or many Classes and each flowable may be assigned one or many SecondaryContext designations.
The list of flowables available for representation in the Class Input Files can be found in [FlowableUnits](FlowableUnits.md).

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | The flow name. Same as 'Class' in [FlowList](FlowList.md). |
 SecondaryContext | string | Y | The second tier context designation that determines which ContextDetails are included. Same as in [Contexts](Contexts.md).  |