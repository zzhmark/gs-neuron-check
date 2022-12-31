def load_swc(path):
    swc = {
        'n': [],
        'x': [],
        'y': [],
        'z': [],
        'parent': []
    }
    with open(path, 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line = line.rstrip().split(' ')
            swc['n'].append(int(line[0]))
            swc['x'].append(float(line[2]))
            swc['y'].append(float(line[3]))
            swc['z'].append(float(line[4]))
            swc['parent'].append(int(line[6]))
    return swc


def get_hash_dict(swc: dict):
    out = {}
    for i, k in enumerate(swc['n']):
        out[k] = i
    return out


def get_child_dict(swc: dict):
    out = {}
    for i, p in enumerate(swc['parent']):
        if p == -1:
            continue
        if p not in out:
            out[p] = []
        out[p].append(swc['n'][i])
    return out
