#!/usr/bin/env python

import itertools
from rs_Python_Pack3_copied.General_Packages.Usefuls.DictProc1 import dict_subset_key

import networkx as nx
import random

class rsNetworkX_Graph(nx.Graph):

    def rsnetworkx(self):
        return self

    def connected_nodes(self, node):
        return self.neighbors(node)

    def ret_distance(self, node):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.ret_distance(self, node)

    def dist_common(self, node1, node2):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.dist_common(self, node1, node2)

    def dist_score(self, node1, node2):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.dist_score(self, node1, node2)

    def shortest_paths(self, node1, node2):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.shortest_paths(self, node1, node2)

    def shortest_path_merged_DiGraph(self, node1, node2):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.shortest_path_merged_DiGraph(self, node1, node2)

    def shortest_path_merged_DiGraph_multi(self, nodeset1, nodeset2):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.shortest_path_merged_DiGraph_multi(self, nodeset1, nodeset2)

    def source_as_bait(self, baits):
        import Graph_Packages.NetworkX.Subgraph1 as Subgraph1
        return Subgraph1.source_as_bait(self, baits)

    def subgraph_given_nodes(self, nodes):
        import Graph_Packages.NetworkX.Subgraph1 as Subgraph1
        return Subgraph1.subgraph_given_nodes(self, nodes)

    def subgraph_given_nodes2(self, inodes, nonexistmessage = None):
        import Graph_Packages.NetworkX.Subgraph1 as Subgraph1
        return  Subgraph1.subgraph_given_nodes2(self, inodes, nonexistmessage)

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

    def extract_related_nodes_dist_common(self, node1, node2):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.extract_related_nodes_dist_common(self, node1, node2)

    def extract_subgraph_dist_common(self, node1, node2):
        import Graph_Packages.NetworkX.Distance1 as Distance1
        return Distance1.extract_subgraph_dist_common(self, node1, node2)

    def ret_copied_graph_simple(self):

        ogrf = rsNetworkX_Graph()
        for node1, node2 in self.nonred_edges():
            ogrf.add_edge(node1, node2)

        return ogrf


    def ret_copied_graph(self, copy_edge_attribs = "all"):
        # Node attributes not copied.

        ogrf = rsNetworkX_Graph()
        for node1, node2 in self.nonred_edges():
            if copy_edge_attribs == "all":
                ogrf.add_edge(node1, node2, **(self[node1][node2]))
            else:
                valid_copy_edge_attribs_h = dict_subset_key(self[node1][node2], copy_edge_attribs)
                ogrf.add_edge(node1, node2, **valid_copy_edge_attribs_h)

        return ogrf

    # Note: Be careful - merge_graph method series will change graph content
    # If it is referenced by dictionary, for example, the dictionary
    # content may be changed unintendedly.
    # ret_merged_graph method series may be safer.
    def merge_graph_simple(self, grf, **kwargs):
        for node1 in grf:
            for node2 in grf[node1]:
                self.add_edge(node1, node2, **kwargs)

    def merge_graph_simple2(self, grf, **kwargs):

        for edge in grf.edges(data = True):
            node1, node2, attr = edge
            integ_attr = dict(list(kwargs.items()) + list(attr.items()))
            self.add_edge(node1, node2, **integ_attr)


    def ret_merged_graph_simple(self, igrf):

        ogrf = self.ret_copied_graph_simple()
        ogrf.merge_graph_simple(igrf)
        return ogrf

    def merge_graph(self, grf):
        import Graph_Packages.NetworkX.merge_graph1 as merge_graph1
        merge_graph1.merge_graph(self, grf)


    def ret_merged_graph(self, grf):
        import Graph_Packages.NetworkX.merge_graph1 as merge_graph1
        merge_graph1.get_merged_graph(self, grf)


    def nonred_edges(self):
        log = {}
        ret = []
        for node1 in self:
            for node2 in self[node1]:
                pair_str1 = "\t".join((node1, node2))
                pair_str2 = "\t".join((node2, node1))
                if (not pair_str1 in log) and (not pair_str2 in log):
                    ret.append([node1, node2])
                    log[ pair_str1 ] = True
                    log[ pair_str2 ] = True

        return ret

    def get_edge_attribs(self):

        return list(set(itertools.chain(*[ list(einfo[2].keys()) for einfo in self.edges(data = True) ])))

    def apply_func_edge_attribs(self, attrib_name, afunc):

        for eedge in self.edges_iter():
            if attrib_name in self.edge[eedge[0]][eedge[1]]:
                self.edge[eedge[0]][eedge[1]][ attrib_name ] \
                    = afunc(self.edge[eedge[0]][eedge[1]][ attrib_name ])


    def cluster_to_unlinked_graph_set(self):
        import Graph_Packages.NetworkX.UnlinkedGraphs as UnlinkedGraphs
        return UnlinkedGraphs.cluster_to_unlinked_graph_set(self)

    def edge_rewire(self, iter_rewire = 3, iter_swap = 3):

        import Graph_Packages.NetworkX.Graph_randomize1 as Graph_randomize1
        graph_rewired, rate_rewired = Graph_randomize1.node_label_swap(self, iter_swap)
        # sys.stderr.write("Label shuffling rate: %f\n" % rate_rewired)
        graph_rewired, rate_rewired = Graph_randomize1.edge_rewire1(graph_rewired, iter_rewire)
        # sys.stderr.write("Edge shuffling rate: %f\n" % rate_rewired)

        # sys.stderr.write("Resulting shuffling rate: %f\n" % Graph_randomize1.change_rate(self, graph_rewired))

        return graph_rewired

    def import_as_matrix(self, nodeset, attr = None, value = None):

        for i in range(len(nodeset) - 1):
            for j in range(i+1, len(nodeset)):
                self.add_edge(nodeset[i], nodeset[j])
                if attr:
                    self[nodeset[i]][nodeset[j]][ attr ] = value

    def number_of_e_edges(self):
        """ Number of estimated edges. In this class, this is exact number. """

        return self.number_of_edges()

    def to_undirected_simple(self):

        return self.ret_copied_graph_simple()

    def sample_edges_simple(self, num_of_edges):

        sampled_edges = random.sample(self.edges(), num_of_edges)
        ogrf = rsNetworkX_Graph()
        for edge in sampled_edges:
            ogrf.add_edge(*edge)
        return ogrf

    def sort_nodes_by_degree(self, neighb_method = None):

        import Graph_Packages.NetworkX.Hub1 as Hub1
        return Hub1.sort_nodes_by_degree(self, neighb_method)


    def common_partner_new_net(self, min_obs = 2, oe = 2.0):

        import Graph_Packages.NetworkX.common_partner1 as common_partner1
        return common_partner1.common_partner_new_net(self, min_obs, oe)


    def bridge_partner_new_net(self, min_obs = 2, oe = 2.0):

        import Graph_Packages.NetworkX.common_partner1 as common_partner1
        return common_partner1.bridge_partner_new_net(self, min_obs, oe)


    def extract_hub_net(self, prop = 0.1, igraph_neighb_method = None):

        import Graph_Packages.NetworkX.Hub1 as Hub1
        return Hub1.extract_hub_net(self, prop, igraph_neighb_method)


    def hub_connection(self, hub_thres = 10):

        from Graph_Packages.Graph_Useful.Node_Group_Matrix3 import Node_Group_Matrix

        hubs = []
        for node in self.nodes():
            if len(self.neighbors(node)) >= hub_thres:
                hubs.append(node)

        # print "Hubs:", hubs

        ngm = Node_Group_Matrix()
        inp = {}
        for hub in hubs:
            inp[ hub ] = "Hub"
        for hub in hubs:
            ngm.set_node_group(inp)

        """
        hubgraph = self.__class__()
        for i in range(len(hubs)-1):
            for j in range(i+1, len(hubs)):
                hubgraph.add_edge(hubs[i], hubs[j])
        """

        return ngm

    def neighbor_selected_nodes(self, nodes, dist = 1, neighbor_func = None):

        import Graph_Packages.NetworkX.neighbor_selected_nodes1 as neighbor_selected_nodes1
        return neighbor_selected_nodes1.neighbor_selected_nodes(self, nodes, dist, neighbor_func)

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

    dg = rsNetworkX_Graph()

    dg.add_edge("A", "B")
    dg.add_edge("A", "C")
    dg.add_edge("C", "D")
    dg.add_edge("D", "E")
    dg.add_edge("E", "C")
    dg.add_edge("E", "F")
    dg.add_edge("Alpha1", "Alpha2")

    print(dg.neighbors("C"))
    print(dg.ret_distance("A"))
    print(dg.ret_distance("F"))
    print(dg.ret_distance("C"))
    print(dg.dist_common("B", "E"), dg.dist_score("B", "E"))
    print(dg.dist_common("B", "X"), dg.dist_score("B", "X"))
    print(dg.dist_common("A", "Alpha1"), dg.dist_score("A", "Alpha1"))
    dg.output()

    print("[[[]]]")
    print(dg.sort_nodes_by_degree())
    print("[[[!!!]]]")
    print(dg.shortest_paths("A", "F"))

    print("---")
    dg2 = dg.source_as_bait(["C", "E"])
    dg2.output()
    print("--- subgraph ---")
    dg3 = dg.subgraph_given_nodes(set(("A", "B", "C", "D")))
    dg3.output()
    dg3_2 = dg.subgraph_given_nodes2(set(("A", "B", "C", "D")), "These nodes not found:")
    dg3_2.output()
    print("---")
    print(dg.extract_related_nodes_dist_common("B", "D"))
    dg4 = dg.extract_subgraph_dist_common("B", "D")
    dg4.output()

    print("---!!!---")
    dg.shortest_path_merged_DiGraph("B", "D").output()

    dg3 = rsNetworkX_Graph()
    dg3.add_edge("Alpha2", "C")

    print("===")
    dg.merge_graph_simple(dg3)
    dg.output()
    print(dg.nonred_edges())
    print("======")
    dg_copied = dg.ret_copied_graph_simple()
    dg_copied.output()

    dg4 = rsNetworkX_Graph()
    dg4.add_edge("XX_XX", "XX__Y")

    print("[][][]")

    dg5 = dg.ret_merged_graph_simple(dg4)
    dg5.output()

    print("XXXXX")

    dg2 = rsNetworkX_Graph()
    dg2.add_edge("A", "B")
    dg2.add_edge("B", "C")
    dg2.add_edge("C", "H")
    dg2.add_edge("H", "L")
    dg2.add_edge("A", "D")
    dg2.add_edge("D", "F")
    dg2.add_edge("B", "E")
    dg2.add_edge("E", "G")
    dg2.add_edge("H", "I")
    dg2.add_edge("I", "J")
    dg2.add_edge("L", "M")
    dg2.add_edge("E", "F")

    print("DG2:")
    dg2.output()
    print("Hub net")
    hubgrp = dg2.hub_connection(3)
    print(hubgrp.get_group_to_nodes())
    hubgrp.rsnetworkx().output()

    print("???")
    dg2.shortest_path_merged_DiGraph_multi(["A","B","C","H","L"], ["F","G"]).output()

    print("---")
    dg3 = rsNetworkX_Graph()
    dg3.add_edge("A", "B")
    dg3.add_edge("A", "C")
    dg3.add_edge("C", "D")
    dg3.add_edge("D", "E")
    dg3.add_edge("E", "C")
    dg3.add_edge("E", "F")

    dg4 = dg3.edge_rewire()

    dg3.output()
    print("---")
    dg4.output()

    dg10 = rsNetworkX_Graph()
    dg10.add_edge("A", "B")
    dg10.add_edge("A", "C")
    dg10.add_edge("E", "D")
    dg10.add_edge("E", "E")
    dg10.add_edge("F", "G")
    dg10.add_edge("E", "F")
    dg10.add_edge("Alpha1", "Alpha2")
    print("Unlinked Subgraphs")
    subgrfs = dg10.cluster_to_unlinked_graph_set()
    for subgrf in subgrfs:
        print("***")
        subgrf.output()


    print("Matrix approach:")
    dg11 = rsNetworkX_Graph()
    dg11.import_as_matrix(("A", "B", "C", "D", "E"), "Matrix", "Test")
    dg11.output("Matrix")

    print("Network incorporation")
    dg12 = rsNetworkX_Graph()
    dg12.add_edge("1", "2", itype = "Orig")
    dg12.merge_graph_simple(dg11, itype = "Incorp")
    dg12.output("itype")

    print(dg10.connected_nodes("E"))

    print("Before:")
    dg10.output()
    dg12 = dg10.sample_edges_simple(3)
    print("After:")
    dg12.output()

    print("Common partners:")
    dg10.common_partner_new_net(1, 1).output()
    print("Bridge partners:")
    dg10.bridge_partner_new_net(1, 1).output()

    print("Hub network:")
    dg10.extract_hub_net(0.5).output()

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
    dg.subset_given_grf(ngm.rsnetworkx()).output()
    dg.subset_given_grf(dg3).output()



    print("!!---!!")
    dg21 = rsNetworkX_Graph()
    dg21.add_edge("A", "B", label1 = "C21")
    dg21.add_edge("A", "C", label1 = "X1")
    dg21.add_edge("C", "D", label1 = "X2")
    dg21.add_edge("D", "E", label1 = "X3")
    dg21.add_edge("E", "C", label1 = "X4")
    dg21.add_edge("E", "F", label1 = "X5")
    dg21.add_edge("P", "Q", label1 = "XX")
    dg21.output(True)
    print("---")

    dg22 = rsNetworkX_Graph()
    dg22.add_edge("A", "B", label1 = "C22", label2 = "J2")
    dg22.add_edge("A", "C")
    dg22.add_edge("E", "D", label2 = "JJ")
    dg22.add_edge("E", "E", label2 = "XY")
    dg22.add_edge("F", "G", label1 = "PY")
    dg22.add_edge("E", "F")
    dg22.add_edge("Alpha1", "Alpha2")
    dg22.output(True)

    dg22.merge_graph_simple2(dg21, nettype = "Merged")
    dg22.output(True)

    print(dg22.neighbor_selected_nodes("A"))

    print("Copied:")
    dg23 = dg22.ret_copied_graph(copy_edge_attribs = ["label1", "nettype", "non-exist"])
    dg23.output(True)

    print("Attribute change")
    dg24 = dg22.ret_copied_graph(copy_edge_attribs = ["label1", "nettype"])
    dg24.apply_func_edge_attribs("label1", lambda ix: ix + "!!!")
    dg24.output(True)

