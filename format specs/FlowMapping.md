# Flow Mapping format

Flow mapping data is in the form of a pandas dataframe with the following fields.

Field | Type | Required? | Note |
----- | ---- | --------  | ----------- |
SourceListName | string | Y | Name and version of the source flowlist, e.g. `openLCA1.7` or `TRACI2.1` |
SourceFlowName | string | Y | Name of the source flow |
SourceFlowUUID | string | N | If no UUID present, UUID generated based on olca algorithm|
SourceFlowContext | string | Y | Compartments separated by `/`, like `product/concrete/ready-mix`|
SourceUnit | string | Y | A unit abbreviation, like `kg`|
MatchCondition | string | N |Single character. `=`, `>`,`<`,`~`. Meaning 'equal to','a superset of', 'a subset of', 'a proxy for'. Assumes `=` if not present |
ConversionFactor | float | N | Value for multiplying with source flow to equal target flow. Assumes `1` if not present |
TargetFlowName | string | Y | Name of the Fed Commons flowable |
TargetFlowClass | string | Y | The flow class, e.g. `Aggregate` or `Metal` |
TargetFlowContext | string | Y | Fed commons context, in form like `product/concrete/ready-mix` |
TargetUnit | string | Y | A unit abbreviation, like `kg`|
TargetFlowUUID | string| Y| UUID for Fed Commons flow |
Mapper | string | N | Person creating the mapping |
Verifier | string | N | Person verifying the mapping |
LastUpdated | datetime | N | Date mapping last updated |

Note that TargetList is not present, because the Fed LCA Commons Material Flow List
 is always assumed target.