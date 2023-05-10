import yaml
import itertools
from os.path import dirname, join

current_dir = dirname(__file__)
file_path = join(current_dir, "../../data/produk.yaml")
with open(file_path, 'r') as f:
    laptop = yaml.full_load(f)

def list_produk():
    produk = {}

    for item in laptop['ENTITAS']:
        types_list = []
        for tipe in item['TIPE']:
            types_list.append(tipe.lower())
        produk[item['MERK']] = types_list

    return produk

# list of merk
def list_merk():
    merk = []
    for item in list_produk():
        merk.append(item.lower())
    
    return merk

# original
def original_tipe():
    types = []
    for merk in list_produk():
        for tipe in list_produk()[merk]:
            types.append(tipe)
    
    return types

# permutations of produk's type
def permutation_types():
    types_list_permutation = []

    for merk in list_produk():
        for tipe in list_produk()[merk]:
            permutated_type = set(itertools.permutations(tipe.split()))
            for p in permutated_type:
                types_list_permutation.append(' '.join(p))

    return types_list_permutation