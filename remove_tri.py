import pandas as pd

from dsm.swc_qc import SWCQualityControl
from dsm.swc import *
from pathlib import Path
from itertools import chain
from multiprocessing import Pool


def save_swc(path, df: pd.DataFrame):
    df.to_csv(path)


def convert(path):
    df = read_swc(str(path))
    qc = SWCQualityControl(df)
    qc.degrade_to_bifurcation()
    df.index = df.index.astype(int)
    df['parent'] = df['parent'].astype(int)
    df['type'] = df['type'].astype(int)
    df.index.name = '##n'
    df.to_csv(path, sep=' ')


if __name__ == '__main__':
    dir1 = Path(r"C:\Users\zzh\Documents\WXWork\1688850447617822\Cache\File\2023-01\150k_0602_registered")
    dir2 = Path(r"C:\Users\zzh\Documents\WXWork\1688850447617822\Cache\File\2023-01\50k_0602_registered")
    with Pool(10) as p:
        p.map(convert, chain(dir1.rglob('*swc'), dir2.rglob('*swc')))
