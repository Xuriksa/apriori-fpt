from operator import attrgetter, methodcaller

from FPTree import FPTree
from ItemSet import ItemSet

def fpt_itemsets(min_sup, transactions):
    '''
    Starting point of frequent pattern tree algorithm
    '''
        
    results = [] # final results are a list of level sets (the ith level is a set of i frequent itemsets)
    denormalized_results = [] #results as a list of frequent itemsets

    next_transactions = []

    for transaction in transactions.values(): # transform transactions into a list of list of itemsets
        next_transactions.append(list(map(lambda items: ItemSet(set({items}), 1), transaction)))
            
    fpt = create_fpt(min_sup, next_transactions) # create initial tree
    
    # recursively mine the tree to find all frequent patterns
    fpt_itemsets_rec(min_sup, fpt, ItemSet(set(), float("inf")), denormalized_results)
 
    results = get_normalized_results(denormalized_results) # normalize results    

    return results

def create_fpt(min_sup, transactions):
    '''
    Creates a frequent pattern based on the given transactions and minimum support
    '''

    #l1 = get_l1(min_sup, transactions) # get level 1 itemsets

    # sort in descending support, ascending lexicographic
    frequent_items = list(get_frequent_items(min_sup, transactions))
    frequent_items.sort(key=methodcaller("itemset_string")) # sort secondary on item name
    frequent_items.sort(key=attrgetter("support"), reverse=True) # sort primary on descending support

    # order the transactions based in the sort order of the frequent items
    orderered_transactions = get_orderered_transactions(frequent_items, transactions)

    # create frequent patten tree based on the ordered frequent items/transactions
    tree = FPTree(frequent_items, orderered_transactions) 

    return tree

def fpt_itemsets_rec(min_sup, fptree, prefix, results):
    '''
    Recursively mine the tree to find frequent itemsets.
    prefix is the frequent itemset mined on the previous iteration
    '''

    # have to iterate over items in reverse frequency
    linked_lists = list(fptree.linked_lists)
    linked_lists.reverse()

    for linked_list in linked_lists: # for each item
        new_set = prefix.duplicate() # duplicate prefix to not affect it

        # add item to item_set
        new_set.add(linked_list.items)
        results.append(new_set) # add frequent itemset to results
        
        next_transactions = get_next_transactions(linked_list, fptree) # get frequent pattern bases

        if next_transactions:
            # create conditional frequent pattern tree based the new transactions (frequent pattern bases)
            Condfpt = create_fpt(min_sup, next_transactions)

            if Condfpt.linked_lists: # conditional tree not empty
                fpt_itemsets_rec(min_sup, Condfpt, new_set, results) # recursive call            

def get_next_transactions(head, fpt):
    '''
    Get the transactions (conditional pattern bases) of the given node.
    '''

    paths = fpt.get_paths(head) # get updward paths of all the nodes in the linked list

    '''
    the itemsets in the paths obtained have their original supports and
    the path contains the leaf. need to prune the leaf and make
    the other itemsets have the leaf's support
    '''
    processed_paths = []
    for path in paths:
        p = list(path)
        p.reverse()

        leaf_support = p[0].support # use the leaft's support for all itemsets

        processed_path = []
        for step in p[1:]: # don't include the leaf in the final path
            step.support = leaf_support
            processed_path.append(step)

        if processed_path: # don't add empty paths (i.e. leaf was a child of the root)
            processed_paths.append(processed_path)

    return processed_paths        

def get_orderered_transactions(frequent_items, transactions):
    '''
    Order the elements in the given transactions according to
    the order of the given frequent items
    '''

    orderered_transactions = []

    for transaction in transactions: # for each transaction
        # add transaction items in that exist in the frequent items
        new_transaction = [transaction[transaction.index(item)] for item in frequent_items if item in transaction]
        
        orderered_transactions.append(new_transaction) # store new transaction

    return orderered_transactions

def get_frequent_items(min_sup, transactions):
    l1 = {}
    frequent_items = set()

    for transaction in transactions:
        for item in transaction:            
            iname = get_single_item_name(item)
            if iname in l1:
                l1[iname] += item.support
            else:
                l1[iname] = item.support

    l1 = {k: v for k,v in l1.items() if v >= min_sup} # prune itemsets below the minimum support

    for item in l1:
        frequent_items.add(ItemSet(set({item}), l1[item]))

    return frequent_items


def get_single_item_name(items):
    '''
    Gets the name of the item in a 1-item itemset
    '''

    return list(items.itemset)[0]

def get_normalized_results(denormalized_results):
    '''
    Normalizes the list of frequent itemsets into a list of levels of frequent itemsets.
    Denormailized results is a list of itemsets [ItemSet, ItemSet...]
    Normalized results is a list of level sets of itemsets [{1-ItemSet, 1-ItemSet...}, {2-ItemSet, 2-ItemSet...}, {3-ItemSet, 3-ItemSet...}...]
    '''

    results = []
    denormalized_results.sort(key=lambda items: len(items.itemset)) # sort by ascending itemset size
    
    i = 0
    while i < len(denormalized_results): # for each ordered itemset
        current_length = len(denormalized_results[i].itemset)
        level = set()
        level.add(denormalized_results[i])
        
        '''
        Since itemsets are sorted in ascending itemset size, itemsets with the same size as the current one
        are the next elements in the list. They all belong to the same level.
        '''
        j = i+1
        while j < len(denormalized_results) and len(denormalized_results[j].itemset) == current_length:
            level.add(denormalized_results[j])
            j += 1
        
        # here when j reached a new level
        results.append(level)
        i = j # continue at the start of the new level
    
    results.sort(key=lambda level: len(list(level)[0].itemset)) # sort by ascending level
    return results