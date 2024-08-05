from pathlib import Path
from multiprocessing import Pool
import os


def main(in_path: Path, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    os.system(f'Vaa3D-x /x pruning_swc_simple /f pruning_iterative /i {in_path} /o {out_path} /p {10}')


if __name__ == '__main__':
    swc_dir = Path('D:/manual_final')
    out_dir = Path('D:/manual_final_pruned')
    proc = 10

    in_file = [*swc_dir.rglob('*swc')]
    out_file = [out_dir / i.relative_to(swc_dir) for i in in_file]
    with Pool(proc) as p:
        p.starmap(main, zip(in_file, out_file), chunksize=20)