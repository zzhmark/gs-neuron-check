from pathlib import Path
import pandas as pd

if __name__ == '__main__':
    check_result = Path('Z:/SEU-ALLEN/Users/yfliu/transtation/seu_mouse/swc/swc_check/R1741_checker_results.csv')
    tab = pd.read_csv(check_result)
    swc_dir = Path('D:/manual_final/R1741')
    out_dir = Path('D:/manual_final/R1741_multi')
    tab = tab[tab['MultiSoma']]
    for ind, row in tab:
        in_path = swc_dir / row['file']
