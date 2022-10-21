from itertools import compress, product

def combinations(items):
    combinations_list = ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )
    return set(list([frozenset(it) for it in combinations_list if len(it) == 2]))