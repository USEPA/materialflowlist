# materialflowlist

`materialflowlist` is a Python package that generates and provides a standardized material flow list for use in life cycle assessment (LCA) data
 as well as mappings to convert data from other sources. This list supports the [Federal LCA Commons](http://www.lcacommons.gov),
 where preferred flows from the active version of the flow list produced by this package can be found in formats for use in LCA software.

 Standard formats for a [Flow List](./format%20specs/FlowList.md)
 and a [Flow Mapping](./format%20specs/FlowMapping.md) are defined and provided by `materialflowlist`.
  They are implemented as [pandas](https://pandas.pydata.org/) dataframes.
   Standard formats are also described for the input files used in building the flow list, and implemented as .csv files
   in the [input](https://github.com/USEPA/materialflowlist/tree/master/materialflowlist/input) directory.  

 The version of the package (see [Releases](https://github.com/USEPA/materialflowlist/releases/))
 corresponds to the version of the flow list that it provides. The complete or 'master' list contains all valid flows for use in LCA data.
  
`materialflowlist` can export complete or subsets of the flow list and mapping files as a .zip archive of [JSON-LD](https://json-ld.org/)
 files conforming to the [openLCA schema](http://greendelta.github.io/olca-schema/).

See the [Wiki](https://github.com/USEPA/materialflowlist/wiki/) for installation, more info on repository
contents, use examples, and for instructions on how to contribute to the flow list through additions or edits to flows or flow mappings.

## Disclaimer

The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis
 and the user assumes responsibility for its use.  EPA has relinquished control of the information and no longer
  has responsibility to protect the integrity , confidentiality, or availability of the information.  Any
   reference to specific commercial products, processes, or services by service mark, trademark, manufacturer,
    or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA.  The EPA seal
     and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or
      the United States Government.
