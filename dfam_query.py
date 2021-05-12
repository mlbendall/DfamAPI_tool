#! /usr/bin/env python

import os
import sys
import requests
import json
from collections import defaultdict

CACHE_DIR = 'dfam.cache'

def wrap(s, n=60):
    """ Wrap string every n characters """
    return '\n'.join(s[i:(i+n)] for i in range(0,len(s), n))


def search_families(clade, clade_relatives='both'):
    url = "https://dfam.org/api/families"
    params = {
        "format": "summary", # The summary format is metadata-only
        "limit": "10000",
        "clade": clade,
        "clade_relatives": clade_relatives, # Include 'ancestors', 'descendants', or 'both'
    }
    response = requests.get(url, params=params)
    results = response.json()
    
    # There were 1313 families in human as of May 12, 2021
    print('Found %d families' % results['total_count'], file=sys.stderr)
    return results['results']


def load_families(summaries, cache_dir=CACHE_DIR):
    """ Load data records for families
        
    Args:
        summaries (:obj:`list` of :obj:`dict`): List of family summaries, as returned by 
            an API call to the "families" endpoint. Each family summary should contain the
            Dfam accession number with the key "accession".
        cache_dir (str): Path to cache directory. This directory is checked for a json 
            file corresponding to the family, and the results of API calls are written
            to this directory.

    Returns:
        :obj:`dict` with accession numbers as keys and full family data as value
    """
    famd = {}
    for fam_sum in summaries:
        f = '%s/%s.json' % (cache_dir, fam_sum['accession'])
        if os.path.exists(f):
            print('found %s' % f, file=sys.stderr)
            results2 = json.load(open(f, 'r'))
        else:
            url2 = "https://dfam.org/api/families/%s" %  fam_sum['accession']
            print('query Dfam API: %s' % url2,  file=sys.stderr)        
            response2 = requests.get(url2)
            results2 = response2.json()
            with open(f, 'w') as outh:
                json.dump(results2, outh)
        famd[fam_sum['accession']] = results2
    return famd

# table = []
# for acc, famdata in famd.items():
#     row = [
#         famdata['accession'],
#         famdata['name'],
#         famdata['length'],
#         famdata['title'],
#         famdata['repeat_type_name'],
#         famdata['repeat_subtype_name'] if 'repeat_subtype_name' in famdata else '.',
#     ]
#     table.append(row)

def coding_seqs(famd, fa_file='coding_seqs.faa', tsv_file='coding_seqs.tsv'):
    """ Extract coding sequences from family data """
    table_cols = ['name', 'acc',]
    table_cols += ['protein_type',  'start', 'end', 'exon_count', 'exon_starts', 'exon_ends',
                   'external_reference', 'reverse', 'stop_codons', 'frameshifts', 'gaps', 'percent_identity',
                   'left_unaligned', 'right_unaligned',
                   'align_data',  'classification_id', 'description', ]
    with open(fa_file, 'w') as out_fa, open(tsv_file, 'w') as out_tsv:
        print('\t'.join(table_cols), file=out_tsv)
        for acc, famdata in famd.items():
            if 'coding_seqs' in famdata and famdata['coding_seqs']:
                for cs in famdata['coding_seqs']:
                    name = cs['product']
                    seq = cs['translation']
                    print('>%s\n%s' % (name, wrap(seq)), file=out_fa)
                    row = [name, acc, ] + [cs[k] for k in table_cols[2:]]
                    print('\t'.join(map(str, row)), file=out_tsv)





