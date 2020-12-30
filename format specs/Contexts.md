# Contexts Input File Format

The context input file lists the possible combinations specifying the physical medium of flows belonging to each Class.
PrimaryContext is absent here because it is automatically designated 'product' for each Flowable, 'material' for 
each Class, and every flow in the list is represented in the 'waste' PrimaryContext. The script 'assemble_materialflowlist.py'
automatically generates flow contexts that are cutoff after the SecondaryContext without applying the ContextDetail 
(eg. product/stone). These flows are useful for mapping from source data that is not specific enough to determine an 
appropriate ContextDetail designation.

The context input file is in the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Class | string |  Y |  The flow class, e.g. `Aggregate` or `Metal` |
 SecondaryContext | string | Y | The second tier context designation that describes the primary medium and determines which ContextDetails are included. |  
 ContextDetail | string | Y | The third tier context designation that provides more specific physical properties for the flows. |