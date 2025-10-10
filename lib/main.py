from symm import *
from graph import *
import random

if __name__=='__main__':

    #nodes = list(filter(lambda y:  y.order.isType(CTYPE.Elementary, 3),Composition.generate(3, 7)))
    nodes = list(filter(lambda y:  y.order.isType(CTYPE.Elementary, 4),
                        Composition.generate(4, 10)))
    graph = symm_graph.connect(nodes, PO_DETAIL.Implicit)
    print(graph.tikz_str)
