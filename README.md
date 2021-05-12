# Dfam API tool

The purpose of these scripts and data is to make it easier to access data from Dfam
using the Dfam API.

Help page for API is here: [https://www.dfam.org/help/api](https://www.dfam.org/help/api)

API Docs are here: [https://www.dfam.org/releases/Dfam_3.3/apidocs/](https://www.dfam.org/releases/Dfam_3.3/apidocs/)




### Human coding sequences

This is to get all consensus coding amino acid sequences for human TEs. The workflow here grabs 
all TE families in humans, and using the family level data in Dfam, 
extracts the (curated?) coding sequences. 


NOTE: This is not all possible coding sequences encoded by the genome. Instead, these are coding sequences annotated in Dfam TE consensus models.


```python
from dfam_query import *
sums = search_families("Homo sapiens")
famd = load_families(sums)
coding_seqs(famd, 'Homo.sapiens/coding_seqs.faa', 'Homo.sapiens/coding_seqs.tsv')
```

