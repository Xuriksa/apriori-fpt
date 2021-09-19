class ItemSet:
    def __init__(self, iset, support):
        self.itemset = iset
        self.support = support        

    def add(self, other):
        self.itemset.update(other.itemset)
        self.support = min(self.support, other.support)        

    def duplicate(self):
        new_set = set(self.itemset)
        return ItemSet(new_set, self.support)
    
    def increase_support(self):
        self.support += 1

    def itemset_string(self):
        result = ""
        ilist = list(self.itemset)
        ilist.sort()
        for item in ilist:
            result += item + ", "
        return result[0:len(result)-2] # get sorted itemset as string

    def __gt__(self, other):
        return self.itemset_string() > other.itemset_string()

    def __eq__(self, other):
        return self.itemset == other.itemset
    
    def __hash__(self):
        return hash(self.itemset_string())

    def __str__(self):        
        return self.itemset_string() + ": " + str(self.support)
    
    def __repr__(self):
        return str(self)