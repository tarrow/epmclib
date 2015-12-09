# epmclib
Python EPMC interface.



#To get the title of a paper referenced by PMCID:

```
from epmclib.epmclib import getPMCID

`pmcid = getPMCID('PMC1234')`
`pmcid.getTitle()`
`print(pmcid.title)`
```

#Similarly to get a chunk of basic metadata:

```
pmcid.getBasicMetadata()
print(pmcid.metadata)

```

#If you just want to test if a PMCID resolves:
```
pmcid.resolves()
```

which returns true or false.

#To query by PMID
Simply use in the same way as PMCIDs:
```
from epmclib.epmclib import getPMID
pmid = getPMID('12324')
```

