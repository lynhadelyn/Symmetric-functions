from symm import *

# -------------- Global Variables ----------------

'''The detail level for the partial ordering graph'''
PO_DETAIL = enum.Enum('Detail', {"Abstract": '', 'Implicit': 'I', "Complete": 'C'})

#Todo: Use Tikz
class CompositionGraph ():
    '''
    A compositionGraph is composed of a graph with edges and back edges,
    >along with a index dictionary which associates the keys to specific compositions.

    **Attributes**:\n
    >graph: A dictionary mapping each node key to a set of children keys.\n
    >nodes: A list of compositions, where the index is the key in the graph.\n
    >detail: The detail level of the graph, see PO_DETAIL for options.\n
    >tikz_str: A string representation of the graph in Tikz format.\n

    **Methods**:\n
    >below: Return the set of all nodes below a given key.
    '''

    _tizk_settings: str = "random seed = 1, spring layout, node distance=20mm"
    _spacing: int = 0 #0 for tight, 1 for spaced

    _detail = PO_DETAIL.Abstract
    graph: dict[int, set[int]] = dict()
    nodes: dict[int, Composition] = dict()

    def __init__(self, _graph: dict[int, set[int]], _nodes: list[Composition], detail = PO_DETAIL.Implicit):
        self.graph = _graph
        self.nodes = dict([(i, _nodes[i]) for i in _graph.keys()])
        self._detail = detail

    @property
    def detail(self):
        return self._detail

    def below(self, key)->set[int]:
        if(self.detail == PO_DETAIL.Complete):
            return self.graph[key]
        else:
            if(self.graph[key] == set()):
                return set()
            else:
                root = set()
                root.add(*[self.below(i) for i in self.graph[key]])
                return root

    @property
    def tikz_str(self):
        spaceStr = [['', ''], [' ', '\n']][self._spacing]
        label = lambda key: str(self.nodes[key])
        children = lambda key: ",{}".format(spaceStr[0]).join(map(label, self.graph[key]))
        connections = spaceStr[1].join(map(lambda key: "{}->{space}{{{}}};"
                                  .format(label(key), children(key), space = spaceStr[0]) if(self.graph[key]) 
                               else (label(key) + ';'),
                               self.graph))
        return '\\begin{{tikzpicture}}\\graph[{}]{line}{{{line}{}{line}}};\\end{{tikzpicture}}'.format(self._tizk_settings, connections, line = spaceStr[1])
    
    def plot(self):
        import matplotlib.pyplot as plt
        raise NotImplementedError("Plotting not yet implemented")


class symm_graph:
    '''
    A class interface providing method to generate compositionGraph objects, as well as operating on them.

    **Methods**:
    >connect: Return a composition graph with vertices from a given list, and directed edges for alpha > beta.

    '''

    @staticmethod
    def normalize(nodes: list[Composition])->list[Composition]:
        '''
        Normalize a list of compositions by their gcd.
        '''
        for node in nodes:
            node.norm()

        # Remove duplicates
        keys = list(range(len(nodes)))
        for i in range(len(nodes)):
            for j in range(i):
                if(nodes[i]==nodes[j] and i in keys and j in keys):
                    keys.remove(i)
        return nodes

    @staticmethod
    def connect(nodes: list[Composition], detail = PO_DETAIL.Implicit)->CompositionGraph:
        '''
        Run a component bases tree insertion like algortihm.
        
        **Implicit Algorithm**\n
        0. Set the heads to all nodes\n
        1. Consider a new node x in nodes\n
        2. Travel iteratively down from each head passing through node.\n
        3. At each step if x lies inbetween the current node and it's children, insert it.\n
        4. Repeat\n

        **Complete Algorithm**
        1. Go through every pair of nodes
        2. Connect a new node based on the comparison criteria
        '''

        keys = list(range(len(nodes)))

        # Setup the graph
        graph: dict[int, set[int]] = dict([(i, set()) for i in keys])

        if(detail == PO_DETAIL.Implicit):
            heads: list[int] = list(keys)
            queue: list[int] = list()
            for index in keys:
                # Pick a new node to try and insert
                heads_copy = heads.copy()
                for _head in heads_copy:
                    queue = [_head]
                    while(queue):
                        search_index = queue.pop(0) # Breadth first search
                        if(nodes[search_index] > nodes[index]): # Index node is below node search node, and is not head
                            if index in heads: heads.remove(index)
                            children = set(list(graph[search_index])) # Copy the set of children
                            graph[search_index].add(index) # Connect it below the search node
                            while(children):
                                child_index = children.pop()
                                if (nodes[index] > nodes[child_index]): # Index node is between search node and child node, so insert
                                    #graph[index].add(child_index)
                                    graph[search_index].remove(child_index)
                                else:
                                    if(nodes[child_index] > nodes[index]):
                                        if index in graph[search_index]: graph[search_index].remove(index) # Detach index node from search node
                                    queue.append(child_index) # Continue the search
        elif(detail == PO_DETAIL.Complete):
            for i in keys:
                for j in keys:
                    if(i!=j and nodes[i] > nodes[j]):
                        graph[i].add(j)
        return CompositionGraph(graph, nodes)