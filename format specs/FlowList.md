# Flow List format

A Flow List is in the form of a pandas data frame with the following fields.

 Field | Type | Required |  Note |
----------- |  ---- | ---------| -----  |
 Flowable | string | Y | The flow name |
 Unit | string | Y  | The reference unit. uses [olca-ipc.py](https://github.com/GreenDelta/olca-ipc.py) units |
 Class | string | Y | The flow class, e.g. `Aggregate` or `Metal` |
 Context | string | Y | A set of context compartments that define the primary context (eg. material, product, waste) and properties of the flowables... e.g. `product/concrete/ready-mix`| 
 Flow UUID | string | Y | Unique hexadecimal ID for the flow |