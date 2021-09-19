from ItemSet import ItemSet

class FPTree:
    def __init__(self, items, transactions):
        self.linked_lists = []

        # initialize linked list
        for item in items:
            self.linked_lists.append(Node(ItemSet(item.itemset, 0), None, None, []))

        self.root = Node(ItemSet({"Root"}, 0), None, None, []) # make the root        

        # add the tree branches  from the transactions
        for transaction in transactions:
            self.add_transaction(transaction)

    def add_transaction(self, transaction):
        '''
        Add branches out of transaction
        '''

        if transaction:
            # increase support of matching branches and get first unmatched node
            parent, current, index = self.update_matching_branch(transaction)

            if parent is not None and current is not None:                
                for i in range(index, len(transaction)): # add new unmatching nodes remaining in the transaction                    
                    child = Node(transaction[i].duplicate(), None, parent, [])
                    parent.add_children([child])
                    self.add_to_list(child)
                    parent = child

    def update_matching_branch(self, transaction):
        '''
        Increase the count of existing matching branch sections and return
        the starting point of the unmatching branch
        '''

        index = 0
        current = Node(transaction[index], None, None, [])
        parent = self.root
        children = parent.children

        '''
        go down on the tree as long as the transaction has a matching branch
        1- first condition makes sure the transaction is not over
        2- secpmd condition makes sure the current node is among the children (branch keeps matching)
        '''
        while index < len(transaction) and current in children:
            child = parent.find_child(current) # get matching child
            child.items.support += current.items.support # increase its support by the upcoming support   
            
            head = self.linked_lists[self.linked_lists.index(child)]
            head.items.support += current.items.support # head has linked list size 

            index += 1 # continue on the transaction
            if index >= len(transaction): # end if the transaction is over
                break

            current = Node(transaction[index], None, None, []) # make fake node out of next transaction item
            
            parent = child # move down the tree
            children = parent.children # new children

        if index >= len(transaction): # whole transaction was a matching branch
            return None, None, None # signal end of adding transaction
        else: # need to continue down the tree to add unmatching nodes
            # starting point to continue down the tree
            return parent, current, index

    def add_to_list(self, node):
        '''
        Add given Node to its Linked List
        '''
        
        head = self.linked_lists[self.linked_lists.index(node)] # head of the node
        #head.items.increase_support() # head has linked list size
        head.items.support += node.items.support
        
        # make the node the new first child of the list (order does not matter)
        old_first = head.right
        node.right = old_first
        head.right = node            

    def get_paths(self, head):
        '''
        Get all the upward paths of a given head.
        '''
        
        paths = []
        current = head.right

        while current is not None:
            paths.append(self.get_path(current))
            current = current.right

        return paths

    def get_path(self, node):
        '''
        Get the upward path of a given Node.
        '''

        path = []
        self.get_path_rec(node, path)
        path.reverse()
        return path
    
    def get_path_rec(self, node, path):
        '''
        Recursive method to construct the upward path of a Node.
        '''

        if node != self.root:
            parent = node.parent
            path.append(node.items.duplicate())
            self.get_path_rec(parent, path)
                
    def bfs(self):
        levels = []
        self.bfs_rec(self.root, 1, levels) # get denormalized levels
        normalized_levels = {}

        # normalize levels into a map so that there is 1 list for each level
        for level in levels:
            if level[0] in normalized_levels: # expand level if already created
                normalized_levels[level[0]].extend(level[1])
            elif level[1]: # create nonempty level (the pythonic if)
                normalized_levels[level[0]] = level[1]
                
        return normalized_levels

    def bfs_rec(self, current, level, levels):
        '''
        Recursive breadth first search that gives a list of
        (tree level, children) tuples. the list is not
        normalized, meaning there are multiple tuples
        for the same level
        '''
        children = current.children
        levels.append((level, children))
        
        for child in children:
            self.bfs_rec(child, level+1, levels)

    def __str__(self):
        result = ""

        levels = self.bfs()

        for level in levels:
            result += str(level) + ": " + str(levels[level]) + "\n"
        
        result += "\n"
        for linked_list in self.linked_lists:
            current = linked_list
            result += "Head: " + str(current) + "||=> "
            current = current.right

            while current is not None:
                result += str(current) + ", "
                current = current.right
            result += "\n"
        
        return result
    
    def __repr__(self):
        return str(self)

class Node:
    def __init__(self, items, right, parent, children):
        self.items = items
        self.right = right
        self.parent = parent
        self.children = list(children)
          
    def find_child(self, child):
        for ch in self.children:
            if ch == child:
                return ch

    def add_children(self, children):
        for child in children:
            if child not in self.children:
                self.children.append(child)

    def __eq__(self, other):
        return self.items == other.items

    def __str__(self):
        return str(self.items)
    
    def __repr__(self):
        return str(self)