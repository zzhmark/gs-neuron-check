import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils import *
from pathlib import Path
from multiprocessing import Pool


def find_multifurcation(swc: dict):
    child_dict = get_child_dict(swc)
    out = []
    for k, v in child_dict.items():
        if len(v) > 2:
            out.append(k)
    return out


def plot():
    fig, (ax0, ax1) = plt.subplots(ncols=2)
    labels = tab['type'].unique()
    tab['pass'] = tab['#multi'] == 0
    tab['not_pass'] = tab['#multi'] > 0
    agg = tab.pivot_table(index='type', values=['pass', 'not_pass'])

    ax0.bar(labels, agg['pass'], label='only bifurcation')
    ax0.bar(labels, agg['not_pass'], bottom=agg['pass'], label='failed')

    ax0.set_title('Count of SWC with multi-furcation')
    ax0.legend()

    no_pass = tab.loc[tab['not_pass']]
    ax1.hist([no_pass.loc[no_pass['type']==i, '#multi'] for i in labels],
             20, stacked=True)
    ax1.set_title('Histogram of # of multi-furcation in SWC')

    plt.savefig('plot.png')


if __name__ == '__main__':
    swc_dir = Path('data')
    proc = 10
    with Pool(proc) as p:
        path = [*swc_dir.rglob('*swc')]
        files = p.map(load_swc, path)
        multi = p.map(find_multifurcation, files)
    tab = pd.DataFrame({'path': [str(i) for i in path],
                        '#multi': [*map(len, multi)],
                        'nodes': multi,
                        'type': [i.parent.name for i in path]})
    tab.to_csv('multifurcation.csv', index=False)
    plot()
