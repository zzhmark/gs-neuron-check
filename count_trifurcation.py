import matplotlib.pyplot as plt
import pandas as pd
from utils import *
from pathlib import Path
from multiprocessing import Pool
import itertools
import numpy as np

fur = 4
def find_multifurcation(swc: dict):
    child_dict = get_child_dict(swc)
    hash_dict = get_hash_dict(swc)
    out = []
    for k, v in child_dict.items():
        if len(v) >= fur and swc['type'][hash_dict[k]] != 1:
            out.append(k)
    return out


def plot():
    fig, (ax0, ax1) = plt.subplots(ncols=2)
    labels = tab['type'].unique()
    tab['pass'] = tab['#multi'] == 0
    tab['not_pass'] = tab['#multi'] > 0
    agg = tab.pivot_table(index='type', values=['pass', 'not_pass'], aggfunc=np.sum)

    ax0.bar(labels, agg['pass'], label='only bifurcation')
    ax0.bar(labels, agg['not_pass'], bottom=agg['pass'], label='failed')
    ax0.set_ylabel('#swc')
    ax0.set_title(f'Count of >={fur} SWC')
    ax0.legend()

    no_pass = tab.loc[tab['not_pass']]
    ax1.hist([no_pass.loc[no_pass['type'] == i, '#multi'] for i in labels], 20, stacked=False, color=plt.get_cmap('Accent')(range(len(labels))))
    ax1.legend(labels)
    ax1.set_xlabel('#multifurcation')
    ax1.set_title('Histogram of #multi-furcation')

    plt.savefig('plot_4.png')


if __name__ == '__main__':
    swc_dir = Path(r"C:\Users\zzh\Documents\WXWork\1688850447617822\Cache\File\2023-01\150k_0602_registered")
    # sub = [swc_dir / 'R165', swc_dir / 'R1741']
    # path = [*itertools.chain(*[i.glob('*swc') for i in sub])]
    path = [*swc_dir.rglob('*swc')]
    # print(path)
    # path = [*itertools.chain(
    #     *[[Path(j) / 'ResampleData' / f'resample_{j.name}' for j in os.scandir(i)] for i in swc_dir.glob('*L0')])]
    proc = 10

    with Pool(proc) as p:
        files = p.map(load_swc, path, chunksize=10)
        multi = p.map(find_multifurcation, files, chunksize=10)
    tab = pd.DataFrame({'path': [str(i) for i in path],
                        '#multi': [*map(len, multi)],
                        'nodes': multi,
                        'type': [i.relative_to(swc_dir).parts[0] for i in path]})
    tab.to_csv('multifurcation_test.csv', index=False)
    # plot()
