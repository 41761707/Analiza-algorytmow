import networkx as nx
import itertools
import random
import matplotlib.pyplot as plt
from networkx import Graph
import sys


class PrintGraph(Graph):
    """
    Example subclass of the Graph class.

    Prints activity log to file or standard output.
    """

    def __init__(self, data=None, name="", file=None, **attr):
        super().__init__(data=data, name=name, **attr)
        if file is None:
            import sys

            self.fh = sys.stdout
        else:
            self.fh = open(file, "w")

    def add_node(self, n, attr_dict=None, **attr):
        super().add_node(n, attr_dict=attr_dict, **attr)
        self.fh.write(f"Add node: {n}\n")

    def add_nodes_from(self, nodes, **attr):
        for n in nodes:
            self.add_node(n, **attr)

    def remove_node(self, n):
        super().remove_node(n)
        self.fh.write(f"Remove node: {n}\n")

    def remove_nodes_from(self, nodes):
        for n in nodes:
            self.remove_node(n)

    def add_edge(self, u, v, attr_dict=None, **attr):
        super().add_edge(u, v, attr_dict=attr_dict, **attr)
        self.fh.write(f"Add edge: {u}-{v}\n")

    def add_edges_from(self, ebunch, attr_dict=None, **attr):
        for e in ebunch:
            u, v = e[0:2]
            self.add_edge(u, v, attr_dict=attr_dict, **attr)

    def remove_edge(self, u, v):
        super().remove_edge(u, v)
        self.fh.write(f"Remove edge: {u}-{v}\n")

    def remove_edges_from(self, ebunch):
        for e in ebunch:
            u, v = e[0:2]
            self.remove_edge(u, v)

    def clear(self):
        super().clear()
        self.fh.write("Clear graph\n")

def mis_errors(graph,mis):
    for node in list(graph.nodes()):
        neighbors = list(graph.neighbors(node))
        node_in_mis = False
        neighbor_in_mis = False
        if(mis[node]==1):
            node_in_mis = True
        if(sum(mis[node] for node in neighbors)  > 0 ):
            neighbor_in_mis = True
        if node_in_mis and neighbor_in_mis:
            return True #blad, incydentne wierzcholki w zbiorze mis
        if not node_in_mis and not neighbor_in_mis:
            return True #blad, mis nie jest maksymalny
    return False

def recompute(graph,node,mis):
    neighbors = list(graph.neighbors(node))
    node_in_mis = False
    neighbor_in_mis = False
    if(mis[node]==1):
        node_in_mis = True
    if(sum(mis[node] for node in neighbors)  > 0 ):
        neighbor_in_mis = True
    if neighbor_in_mis:
        mis[node] = 0 #istnieje sasiad w zbiorze mis
    else:
        mis[node] = 1 #nie istnieje sasiad w zbiorze mis


def mis_run(g):
    nodes = list(g.nodes())
    mis = []
    for _ in range(len(nodes)):
        mis.append(random.randint(0,1))
    print(mis)
    while(mis_errors(g,mis)):
        index = random.randint(0,len(nodes)-1)
        #print(index, " ", mis)
        recompute(g,index,mis)
    return mis





            
def main():
    n = int(sys.argv[1])
    p = float(sys.argv[2])
    fails = 0
    while fails < 10:
        g = nx.erdos_renyi_graph(n, p)
        if not nx.is_connected(g):
            fails = fails + 1
        else:
            print("Wygenerowany graf")
            break
    if fails == 10:
        print("10 nieudanych prób generacji grafu- spróbuj zmodyfikować parametry n, p i uruchom program ponownie")
        sys.exit()
    mis = []
    mis = mis_run(g)
    print("Maksymalny zbiór niezależny:", mis)

    pos = nx.spring_layout(g, seed=225)  # Seed for reproducible layout
    color_map = []
    for element in mis:
        if element == 1:
            color_map.append('red')
        else:
            color_map.append('yellow')    
    nx.draw(g, pos, node_color=color_map, with_labels=True)
    plt.savefig('graph.png')
    plt.clf()

if __name__ == '__main__':
    main()