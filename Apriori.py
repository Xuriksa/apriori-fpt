from ItemSet import ItemSet

def Apriori(min_sup, transactions):
    all_levels = [] # stores all the levels   
    
    i = 1
    li = get_li(min_sup, transactions, i, {}) # get level 1
    
    while not len(li) == 0: # while more Levels can be generated
        all_levels.append(li) # store current Level                
        i += 1 # go to next Level
        li = get_li(min_sup, transactions, i, li) # attempt to compute next Level

    return all_levels

def get_li(min_sup, transactions, level, lprev):
    '''
    Generalized function to get the ith Level itemsets
    '''

    if level == 1:
        return get_l1(min_sup, transactions) # call function specialized for Level 1 itemests
    else:
        li = itemset_join(lprev, level) # get the next level candidates

        for item in li: # get absolute support for itemsets
            for transaction in transactions.values():
                if item.itemset.issubset(transaction):
                    item.increase_support()
                
        li = set(filter(lambda s: s.support >= min_sup, li)) # prune itemsets below the minimum support
        return li

def get_l1(min_sup, transactions):
    '''
    Get the Level 1 itemsets given some transaction and minimum support.
    '''

    l1 = {}
    result = set()

    # de-normalize transactions to have multi-valued item field (the itemsets)
    # store key transaction id, value absolute support count
    for transaction in transactions.values():        
        for item in transaction:
            if item in l1:
                l1[item] += 1
            else:
                l1[item] = 1
    
    l1 = {k: v for k,v in l1.items() if v >= min_sup} # prune itemsets below the minimum support
    
    for item, support in l1.items():
        result.add(ItemSet({item}, support))
    
    return result

def itemset_join(itemsets, level):
    '''
    Perform the join operation on an itemset level to obtain the next level candidates.
    The way the function is coded also takes care of level 2 cross product.
    '''
    
    results = set()

    # cross product
    for i in itemsets:
        for j in itemsets:
            if not i == j:
                A = list(i.itemset)
                A.sort()
                B = list(j.itemset)
                B.sort()
                
                match = True
                for k in range(level-2): # join on first level-2 attributes
                    if not A[k] == B[k]:
                        match = False
                
                if match: # join condition successful?
                    results.add(  ItemSet(i.itemset.union(j.itemset ) , 0)  )
    return results
