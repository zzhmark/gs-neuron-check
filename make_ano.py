import pandas as pd
from pathlib import Path
from multiprocessing import Pool
from utils import *


def make(outpath, swc, nodes, path):
    hash_dict = get_hash_dict(swc)
    apo = str(outpath) + '.apo'
    with open(apo, 'w') as f:
        f.write('##n,orderinfo,name,comment,z,x,y, pixmax,intensity,sdev,volsize,mass,,,, color_r,color_g,color_b\n')
        for i in nodes.lstrip('[').rstrip(']').split(','):
            j = hash_dict[int(i)]
            x, y, z = swc['x'][j], swc['y'][j], swc['z'][j]
            f.write(f'0,,,,{z},{x},{y},0.000,0.000,0.000,314.159,0.000,,,,0,0,255\n')
    with open(str(outpath) + '.ano', 'w') as f:
        f.write(f'SWCFILE={Path(path).name}\n')
        f.write(f'APOFILE={Path(apo).name}\n')


if __name__ == '__main__':
    proc = 10
    tab = pd.read_csv('multifurcation_4.csv')
    ano_dir = Path(r'D:\manual_final')
    tab = tab[tab['#multi'] > 0]
    with Pool(proc) as p:
        files = p.map(load_swc, tab['path'], chunksize=20)
        outpath = [ano_dir / row['type'] / Path(row['path']).name for ind, row in tab.iterrows()]
        p.starmap(make, zip(outpath, files, tab['nodes'], tab['path']), chunksize=20)
