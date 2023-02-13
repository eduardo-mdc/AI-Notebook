from collections import deque

#Bucket state class
class BucketState:
    c1 = 4   # capacity for bucket 1
    c2 = 3   # capacity for bucket 2
    
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2

    '''needed for the visited list'''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.b1, self.b2)) 
    ''' - '''

    def __str__(self):
        return "(" + str(self.b1) + ", " + str(self.b2) + ")"


# <-- STATES START -->

# emptying the first bucket
def empty1(state):
    if state.b1 > 0:
        return BucketState(0, state.b2)
    return None

# emptying the second bucket
def empty2(state):
    if state.b2 > 0:
        return BucketState(state.b1,0)

def fill1(state):
    if state.b1 < state.c1:
        return BucketState(state.c1,state.b2)

def fill2(state):
    if state.b2 < state.c1:
        return BucketState(state.b1,state.c2)

def pour12_empty1(state):
    if (state.b1 > 0 and state.b2 < state.c2 and (state.b1 + state.b2 <= state.c2)):
        return BucketState(0,state.b2 + state.b1)

def pour21_empty2(state):
    if (state.b2 > 0 and state.b1 < state.c1 and (state.b1 + state.b2 <= state.c1)):
        return BucketState(state.b2 + state.b1,0)

def pour12_fill2(state):
    if (state.b1 > 0 and state.b2 < state.c2 and state.b1 - (state.c2 - state.b2) > 0):
        return BucketState(state.b1 - (state.c2 - state.b2),state.c2)

def pour21_fill1(state):
    if (state.b2 > 0 and state.b1 < state.c1 and state.b2 - (state.c1 - state.b1) > 0):
        return BucketState(state.b2 - (state.c1 - state.b1),state.c2)

def child_bucket_states(state):
    new_states = []
    if(empty1(state)):
        new_states.append(empty1(state))
    if(empty2(state)):
        new_states.append(empty2(state))
    if(fill1(state)):
        new_states.append(fill1(state))
    if(fill2(state)):
        new_states.append(fill2(state))
    if(pour12_fill2(state)):
        new_states.append(pour12_fill2(state))
    if(pour12_empty1(state)):
        new_states.append(pour12_empty1(state))
    if(pour21_fill1(state)):
        new_states.append(pour21_fill1(state))
    if(pour21_empty2(state)):
        new_states.append(pour21_empty2(state))
    return new_states

# <-- STATES END -->

def goal_bucket_state(state):
    if state.b1 == 2 and state.b2 == 0:
        return True
    

# A generic definition of a tree node holding a state of the problem
class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self



def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)   # create the root node in the search tree
    queue = deque([root])   # initialize the queue to store the nodes
    
    while queue:
        node = queue.popleft()   # get first element in the queue
        if goal_state_func(node.state):   # check goal state
            return node
        
        for state in operators_func(node.state):   # go through next states
            # create tree node with the new state
            leaf = TreeNode(state)
            
            # link child node to its parent in the tree
            node.add_child(leaf)
            
            # enqueue the child node
            queue.append(leaf)
            

    return None


def main():

    goal = breadth_first_search(BucketState(0,0), 
                            goal_bucket_state, 
                            child_bucket_states)
    while (goal.parent != None):
        print(goal.state)
        goal = goal.parent
    print(goal.state)
    

main()