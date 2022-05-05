#!/usr/bin/env python

'''
Created on 2011/04/18

@author: rsaito
'''

import random
import itertools
import networkx as nx
from .rsNetworkX_Graph1 import rsNetworkX_Graph
from rs_Python_Pack3_copied.General_Packages.Usefuls.DictProc1 import dict_subset_key

class rsNetworkX_DiGraph(nx.DiGraph):

    def rsnetworkx(self):
        return self

    def add_edge(self, node1, node2, *args, **kwargs):
        nx.DiGraph.add_edge(self, node1, node2, *args, **kwargs)
        self[node1][node2]['isDirected'] = True

    def connected_nodes(self, node):
        return list(set(self.predecessors(node) + self.successors(node)))

    def ret_distance(self, node, direction = "p"):
        import Graph_Packages.NetworkX.Distance_DiGraph1 as Distance_DiGraph1
        return Distance_DiGraph1.ret_distance(self, node, direction)

    def dist_common(self, node1, node2, direction = "p"):
        import Graph_Packages.NetworkX.Distance_DiGraph1 as Distance_DiGraph1
        return Distance_DiGraph1.dist_common(self, node1, node2, direction)

    def dist_score(self, node1, node2, direction = "p"):
        import Graph_Packages.NetworkX.Distance_DiGraph1 as Distance_DiGraph1
        return Distance_DiGraph1.dist_score(self, node1, node2, direction)

    def shortest_paths(self, node1, node2, direction = "p"):
        import Graph_Packages.NetworkX.Distance_DiGraph1 as Distance_DiGraph1
        return Distance_DiGraph1.shortest_paths(self, node1, node2, direction)

    def source_as_bait(self, baits):
        import Graph_Packages.NetworkX.Subgraph1 as Subgraph1
        return Subgraph1.source_as_bait(self, baits)

    def subgraph_given_nodes(self, nodes):
        import Graph_Packages.NetworkX.Subgraph1 as Subgraph1
        return Subgraph1.subgraph_given_nodes(self, nodes)

    def subgraph_given_groups(self, groups):
        import Graph_Packages.NetworkX.Subgraph1 as Subgraph1
        return Subgraph1.subgraph_given_groups(self, groups)

    def subset_given_nodes(self, nodes):
        return self.subgraph_given_nodes(nodes)

    def subgraph_given_grf(self, grf):
        import Graph_Packages.NetworkX.Subgraph1 as Subgraph1
        return Subgraph1.subgraph_given_grf(self, grf)

    def subset_given_grf(self, grf):
        return self.subgraph_given_grf(grf)

    def extract_related_nodes_dist_common(self, node1, node2, direction = "p"):
        import Graph_Packages.NetworkX.Distance_DiGraph1 as Distance_DiGraph1
        return Distance_DiGraph1.extract_related_nodes_dist_common(self, node1, node2, direction)

    def extract_subgraph_dist_common(self, node1, node2, direction = "p"):
        import Graph_Packages.NetworkX.Distance_DiGraph1 as Distance_DiGraph1
        return Distance_DiGraph1.extract_subgraph_dist_common(self, node1, node2, direction)

    def cluster_to_unlinked_graph_set(self):
        import Graph_Packages.NetworkX.UnlinkedGraphs as UnlinkedGraphs
        return UnlinkedGraphs.cluster_to_unlinked_graph_set(self)

    def nonred_edges(self):

        return self.edges()

        """ Just self.edges() may be sufficient
        ret = []
        for node1 in self:
            for node2 in self[node1]:
                ret.append([node1, node2])

        return ret
        """

    def get_edge_attribs(self):

        return list(set(itertools.chain(*[ list(einfo[2].keys()) for einfo in self.edges(data = True) ])))


    def apply_func_edge_attribs(self, attrib_name, afunc):

        for eedge in self.edges_iter():
            if attrib_name in self.edge[eedge[0]][eedge[1]]:
                self.edge[eedge[0]][eedge[1]][ attrib_name ] \
                    = afunc(self.edge[eedge[0]][eedge[1]][ attrib_name ])


    def edge_rewire(self, iter_rewire = 3, iter_swap = 3):

        import Graph_Packages.NetworkX.Graph_randomize1 as Graph_randomize1
        graph_rewired, rate_rewired = Graph_randomize1.node_label_swap(self, iter_swap)
        # sys.stderr.write("Label shuffling rate: %f\n" % rate_rewired)
        graph_rewired, rate_rewired = Graph_randomize1.edge_rewire1(graph_rewired, iter_rewire)
        # sys.stderr.write("Edge shuffling rate: %f\n" % rate_rewired)

        # sys.stderr.write("Resulting shuffling rate: %f\n" % Graph_randomize1.change_rate(self, graph_rewired))

        return graph_rewired


    def merge_graph_simple(self, grf, directed = True):
        for node1 in grf:
            for node2 in grf[node1]:
                self.add_edge(node1, node2)
                self[node1][node2]['isDirected'] = directed
                if not directed:
                    self.add_edge(node2, node1)
                    self[node2][node1]['isDirected'] = directed


    def ret_copied_graph_simple(self):

        ogrf = rsNetworkX_DiGraph()
        for node1, node2 in self.edges():
            ogrf.add_edge(node1, node2)

        return ogrf

    def number_of_e_edges(self):
        """ Number of estimated edges. In this class, this is exact number. """

        return self.number_of_edges()

    def sample_edges_simple(self, num_of_edges):

        sampled_edges = random.sample(self.edges(), num_of_edges)
        ogrf = rsNetworkX_DiGraph()
        for edge in sampled_edges:
            ogrf.add_edge(*edge)
        return ogrf

    def sort_nodes_by_degree(self, neighb_method = None):

        import Graph_Packages.NetworkX.Hub1 as Hub1
        return Hub1.sort_nodes_by_degree(self, neighb_method)


    def to_undirected_simple(self):

        from .rsNetworkX_Graph1 import rsNetworkX_Graph

        ogrf = rsNetworkX_Graph()
        for node1, node2 in self.edges():
            ogrf.add_edge(node1, node2)

        return ogrf

    def to_undirected(self, copy_edge_attribs = "all"):
        # Node attributes not copied.
        # For A->B and B->A, only one of attributes for A-B will be selected?

        ogrf = rsNetworkX_Graph()
        for node1, node2 in self.edges():
            edge_h = self[node1][node2].copy()
            edge_h.pop("isDirected", None)

            if copy_edge_attribs == "all":
                ogrf.add_edge(node1, node2, **(edge_h))
            else:
                valid_copy_edge_attribs_h = dict_subset_key(edge_h, copy_edge_attribs)
                ogrf.add_edge(node1, node2, **valid_copy_edge_attribs_h)

        return ogrf
        

    def input(self, inttable_filename,
              node1_colname = "Node 1",
              node2_colname = "Node 2"):

        import Graph_Packages.NetworkX.IntTable2_2 as IntTable2_2
        IntTable2_2.readIntTable(inttable_filename, self,
                               node1_colname, node2_colname)

    def output(self, keyw = None, filename = None, noval_str = "''"):

        import Graph_Packages.NetworkX.IntTable2_2 as IntTable2_2
        IntTable2_2.output_table(self, keyw, filename, noval_str)

    def input_simple(self, inttable_wo_header_filename):

        import Graph_Packages.NetworkX.IntTable2_2 as IntTable2_2
        IntTable2_2.readIntTable_simple(inttable_wo_header_filename, self)

    def output_simple(self, filename = None):

        import Graph_Packages.NetworkX.IntTable2_2 as IntTable2_2
        IntTable2_2.output_table_simple(self, filename)


if __name__ == "__main__":

    dg = rsNetworkX_DiGraph()

    dg.add_edge("A", "B")
    dg.add_edge("A", "C")
    dg.add_edge("C", "D")
    dg.add_edge("D", "E")
    dg.add_edge("E", "C")
    dg.add_edge("E", "F")
    dg.add_edge("Alpha1", "Alpha2")

    print(dg.neighbors("C"))
    print(dg.predecessors("C"))
    print(dg.successors("C"))
    print(dg.connected_nodes("C"))
    print(dg.ret_distance("A"))
    print(dg.ret_distance("F", "p"))
    print(dg.ret_distance("C", "b"))
    print(dg.dist_common("B", "E"), dg.dist_score("B", "E"))
    print(dg.dist_common("B", "X"), dg.dist_score("B", "X"))
    print(dg.dist_common("A", "Alpha1"), dg.dist_score("A", "Alpha1"))
    dg.output()
    print("[[[]]]")
    print(dg.sort_nodes_by_degree())
    print("[[[!!!]]]")
    print(dg.shortest_paths("A", "F", direction = "s"))

    print("---")
    dg2 = dg.source_as_bait(["C", "E"])
    dg2.output()
    print("--- Subgraph ---")
    dg3 = dg.subgraph_given_nodes(set(("A", "B", "C", "D")))
    dg3.output()
    print("---")
    print(dg.extract_related_nodes_dist_common("B", "D", direction = "p"))
    dg4 = dg.extract_subgraph_dist_common("B", "D", direction = "p")
    dg4.output()

    print("---")
    dg5 = dg4.edge_rewire()
    dg6 = dg5.ret_copied_graph_simple()

    dg5.output()
    print("---")
    dg6.output()

    dg10 = rsNetworkX_DiGraph()
    dg10.add_edge("A", "B", attrib1 = "Hello")
    dg10.add_edge("A", "C", attrib1 = "Hi")
    dg10.add_edge("E", "D", attrib2 = "Bye")
    dg10.add_edge("E", "E", attrib2 = "Good bye")
    dg10.add_edge("F", "G")
    dg10.add_edge("E", "F", attrib1 = "Forward", attrib2 = "Clock")
    dg10.add_edge("F", "E", attrib1 = "Back",    attrib2 = "AntiClock")
    dg10.add_edge("Alpha1", "Alpha2")
    print("Unlinked Subgraphs")
    subgrfs = dg10.cluster_to_unlinked_graph_set()
    for subgrf in subgrfs:
        print("***")
        subgrf.output()

    g10 = dg10.to_undirected()
    g10.output(keyw = True)


    dg11 = rsNetworkX_DiGraph()
    dg11.add_edge("G", "H")
    dg11.add_edge("G", "I")
    dg11.add_edge("E", "I")
    dg11.add_edge("D", "E")
    dg11.add_edge("E", "C")
    dg10.merge_graph_simple(dg11, directed = False)
    print("-x-x-x-x-")
    dg10.output('isDirected')

    print("Before:")
    dg10.output()
    dg12 = dg10.sample_edges_simple(5)
    print("After:")
    dg12.output()

    import Graph_Packages.Graph_Useful.Node_Group_Matrix3
    import FileDirPath.TmpFile
    tmp_obj = FileDirPath.TmpFile.TmpFile_III("""
Node Group
A    Group@1
B    Group@1
B    Group@2
C    Group@2
D    Group@3
E    Group@3
F    Group@3
G    Group@3
H    Group@3
I    Group@2
""", tospace = "@")

    ngm = Graph_Packages.Graph_Useful.Node_Group_Matrix3.Node_Group_Matrix()
    ngm.input(tmp_obj.filename())
    dg.subgraph_given_groups(ngm).output()
    print(":::")
    dg.subgraph_given_grf(dg11).output()

