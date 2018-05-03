class Node:
    '''
    Node Class
    '''


    """Initialize a Node Instance
    
    Arguments:
        lo {int} -- the low of node's interval
        hi {int} -- the high of node's interval
        sdr {string} -- the sdr owner of node's interval
    """
    def __init__(self, lo, hi, sdr):
        
        # node interval, max of subtree and sdr
        self.lo = lo
        self.hi  = hi
        self.sdr = sdr
        self.max = hi

        # pointers to left and right subtrees
        self.left = None
        self.right = None



class IntervalTree:
    '''
    Interval BST Tree Class
    '''

    
    """Initialize a Interval Tree Instance with root and tree size
    """
    def __init__(self):
        
        self.root = None
        self.size = 0

    
    """Insert new node of given intervals low and high and owner sdr at correct position
    
    Arguments:
        new_lo {int} -- the low of inserting node's interval
        new_hi {int} -- the high of inserting node's interval
        new_sdr {string} -- the sdr owner of inserting node's interval
    """
    def insert(self, new_lo, new_hi, new_sdr):

        if self.root == None:
            self.root = Node(new_lo, new_hi, new_sdr)
        else:
            # recuresively check where to insert
            self.root, self.root.max = self._insert(self.root, new_lo, new_hi, new_sdr)
        
        # increment size of tree
        self.size += 1
    

    """Insert helper function. BST is based on the lo number in node's interval: left subtree's 
        low is less than root's low while right subtree's low is greater than root's low.
    
    Arguments:
        root {Node} -- the low of node's interval
        new_lo {int} -- the low of node's interval
        new_hi {int} -- the high of node's interval
        new_sdr {string} -- the sdr owner of interval
    
    Returns:
        root -- the root of current subtree
        root.max -- max of current subtree
    """
    def _insert(self, root, new_lo, new_hi, new_sdr):
        
        if root == None:
            return Node(new_lo, new_hi, new_sdr), new_hi

        if new_lo <= root.lo:
            root.left, new_max = self._insert(root.left, new_lo, new_hi, new_sdr)
        else:
            root.right, new_max = self._insert(root.right, new_lo, new_hi, new_sdr)
        
        # change the max of the subtrees while moving up recursion
        if new_max > root.max:
            root.max = new_max
        
        return root, root.max
    

    """Add all matching intervals that contain the number 'val' to a list 'res'
    
    Arguments:
        root {Node} -- the low of node's interval
        val {int} -- the number to find the intervals for
        res {list} -- the list of tuples consisting of intervals and owner sdr
    
    Returns:
        root -- the root of current subtree
        root.max -- max of current subtree
    """
    def searchMatchingIntervals(self, root, val, res):

        if root == None:
            return
        
        # if we find a matching interval
        if val >= root.lo and val <= root.hi:
            res.append((root.lo, root.hi, root.sdr))
        
        if root.left and root.left.max >= val:
            self.searchMatchingIntervals(root.left, val, res)
        
        self.searchMatchingIntervals(root.right, val, res)