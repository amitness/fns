from functools import lru_cache
import pandas as pd
import numpy as np


@lru_cache(1)
def onegram_count():
    df = pd.read_csv('https://norvig.com/ngrams/count_1w.txt',
                     sep='\t',
                     header=None,
                     names=['word', 'count'])
    df['idf'] = np.log(df['count'].sum() / df['count'])
    df.sort_values(by='idf', ascending=True, inplace=True)
    return df
