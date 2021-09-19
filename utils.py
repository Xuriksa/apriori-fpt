from itertools import chain, combinations

def parse_file(file):
    '''
    Get relation (Table) in the file.
    Returns minimum support, minimum confidence and transactions as a tid: itemset dictionary
    '''

    min_sup = 0
    min_conf = 0
    min_lift = 0
    transactions = {}
    
    line1 = file.readline()
    min_sup = float(line1.strip('\n').split()[0])
    min_conf = float(line1.strip('\n').split()[1])
    min_lift = float((line1.strip('\n').split()[2]))

    for line in file:                        
        tid = line.strip('\n').split()[0]
        item = line.strip('\n').split()[1]
            
        if tid in transactions:
            transactions[tid].add(item)
        else:
            itemset = set()
            itemset.add(item)
            transactions[tid] = itemset
    
    return min_sup, min_conf, min_lift, transactions

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

