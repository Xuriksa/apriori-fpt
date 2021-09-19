from utils import powerset

def file_write(out, input=''):
    out.write(str(input) + "\n")

def print_inputs(out, min_sup, min_conf, min_lift, transactions):
    file_write(out, "Minimum Support: " + str(min_sup))
    file_write(out, "Minimum Confidence: " + str(min_conf))
    file_write(out, "Minimum Lift: " + str(min_lift))
    file_write(out)

    file_write(out,"Transactions:")
    print_transactions(out, transactions)

def print_transactions(out, transactions):
    '''
    Print transactions. The format of the transactions is a dictionary {tid: {item, item...}, ...}
    '''

    for tid in transactions:
        transaction = list(transactions[tid])
        transaction.sort()
        file_write(out, tid + " " + str(transaction))

def print_results(out, pr, levels, min_sup, min_conf, min_lift, transactions):

    levels.sort(key=lambda level: len(list(level)[0].itemset)) # sort by ascending level

    i = 1
    for level in levels:
        print_level(out, level, i)

        if pr:
            print_association_rules(out, level, min_conf, min_lift, levels, len(transactions))
        i += 1

def print_levels(out, levels):
    '''
    Print all the levels of frequent itemsets.
    '''

    levels.sort(key=lambda level: len(list(level)[0].itemset)) # sort by ascending level

    i = 1
    for level in levels:
        print_level(out, level, i)
        i += 1

def print_level(out, level, level_number):
    '''
    Print a level of frequent itemsets
    '''

    level_list = list(level)
    level_list.sort()

    file_write(out, "Level #" + str(level_number))
    for itemset in level_list:
        file_write(out,itemset)
    file_write(out)

def print_association_rules(out, level, min_conf, min_lift, all_results, number_of_transactions):
    '''
    Prints a level's association rules A ==> B [support, confidence]
    '''

    l = list(level)
    l.sort()
    level = len(l[0].itemset)

    if level != 1: # no rules for Level 1
        for items in l:
            il = list(items.itemset)
            il.sort()
            subsets = list(powerset(il)) # get all subsets of itemset

            for subset in subsets:
                sl = set(subset) # determinantsubset
                dif = items.itemset.difference(sl) # determinee (superset - subset)
                dif = list(dif)
                dif.sort()
                diflevel = len(dif)

                if  diflevel != 0: # superset - subset not empty
                    determinant = "{ "
                    determinee = "{ "

                    # determinant (subset) as a string
                    for i in subset:
                        determinant = determinant + str(i) + ", "
                    determinant = determinant[0:len(determinant)-2] # remove last ", "
                    determinant = determinant + " }"

                    # determinee (superset - subset) as a string
                    for i in dif:
                        determinee = determinee + str(i) + ", "
                    determinee = determinee[0:len(determinee)-2] # remove last ", "
                    determinee = determinee + " }"

                    set_support = items.support/number_of_transactions # itemset relative support
                    sub_support = find_support(subset, all_results)/number_of_transactions # determinant relative support
                    dif_support = find_support(dif, all_results)/number_of_transactions # determinee relative support

                    confidence = set_support/sub_support # confidence of A ==> B is P(B|A) = P(A union B)/P(A)
                    
                    '''
                    lift of A ==> B is P(A union B)/(P(A) * P(B)).
                    lift < 1 -> A and B negatively correlated
                    lift == 1 -> A and B independent
                    lift > 1 -> A and B positively correlated
                    '''
                    lift = set_support/(sub_support * dif_support) 

                    # rule must exceed minimum confidence and lift thresholds
                    if confidence >= min_conf and lift >= min_lift: 
                        file_write(out, determinant + " ==> " + determinee + " [ Support= " + str(set_support) + ", Confidence= " + str(confidence) + ", Lift= " + str(lift) + " ]")
        file_write(out)

def find_support(subset, levels):
    '''
    Finds an itemsets' support in the list of levels.
    '''

    subset = set(subset)
    level = len(subset)

    for item in levels[level-1]: # don't check latest level because it may not yet exist like in Apriori
        if item.itemset == subset:
            return item.support