# FlowableUnit Input File Format

The FlowableUnit file is a list of all product flowables present in the Material Flow List and designates the reference 
unit used within the list. These flowables define the function of the product flow, whereas the context specifies the 
physical medium of the flow. Each product flow is automatically assigned both 'product' and 'waste' as primary contexts.
The flowables are only used if specified in one or more of the [ClassInputFiles](ClassInputFiles.md).

The FlowableUnit input file is the form of CSV data with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | The flowable name |
 Unit | string | Y  | The reference unit. Uses [olca-ipc.py](https://github.com/GreenDelta/olca-ipc.py) units |