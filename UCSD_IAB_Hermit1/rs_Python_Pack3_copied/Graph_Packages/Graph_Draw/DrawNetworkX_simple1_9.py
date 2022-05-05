#!/usr/bin/env python
'''
Created on 2016/04/06

@author: rsaito

Also consider:
https://networkx.github.io/documentation/latest/reference/drawing.html

and igraph ...

'''

from matplotlib import pyplot
from numpy.random import choice
from ..NetworkX.rsNetworkX_DiGraph1 import rsNetworkX_DiGraph
from rs_Python_Pack3_copied.General_Packages.Usefuls.Plane2D_avoid_ovv1 import Plane2D_avoid_ovv

KEY_NODE_COORD_XY        = "coord"
KEY_NODE_LABEL_OFFSET_XY = "label_offset"
KEY_DISP_NODE_LABEL      = "nlabel"
KEY_EDGE_LABEL_LIST      = "elabels"
KEY_EDGE_DIRECTION       = "edir" # "-", "->", "<-" or "<->"
KEY_EDGE_RELAY_POSS      = "erelayposs"

def pos_xy_within_range(ipos_x, ipos_y, irange_x, irange_y):

        irange_x_min, irange_x_max = irange_x       
        irange_y_min, irange_y_max = irange_y
        
        return (irange_x_min <= ipos_x and ipos_x <= irange_x_max and
                irange_y_min <= ipos_y and ipos_y <= irange_y_max)


def get_rate_pos(irange, pos):

    return (pos - irange[0]) / (irange[1] - irange[0])


class DrawNetworkX_simple:
    def __init__(self, igrf):
        self.igrf = igrf

    def nodes_within_range(self, range_x, range_y):

        nodes_wr = {}
        
        for node in self.igrf.nodes():
            if KEY_NODE_COORD_XY in self.igrf.nodes[ node ]:
                pos_x, pos_y = self.igrf.nodes[ node ][ KEY_NODE_COORD_XY ]
                if (pos_xy_within_range(pos_x, pos_y, range_x, range_y)):
                    nodes_wr[ node ] = True

        return list(nodes_wr.keys()) # Use self.igrf.subgraph_given_nodes to get edges.

    def edges_within_range(self, range_x, range_y):
        
        edges_drawn = {}
                
        for iedge in self.igrf.edges(data = True):
            node1, node2, eattr_h = iedge
            if (KEY_NODE_COORD_XY in self.igrf.nodes[ node1 ] and
                KEY_NODE_COORD_XY in self.igrf.nodes[ node2 ]):
                pos_x1, pos_y1 = self.igrf.nodes[ node1 ][ KEY_NODE_COORD_XY ]
                pos_x2, pos_y2 = self.igrf.nodes[ node2 ][ KEY_NODE_COORD_XY ]
                poss_all = [(pos_x1, pos_y1)] + \
                    eattr_h.get(KEY_EDGE_RELAY_POSS, []) + \
                    [(pos_x2, pos_y2)]
                for k in range(len(poss_all) - 1):
                    x1, y1 = poss_all[k]
                    x2, y2 = poss_all[k+1]
                
                    if ((pos_xy_within_range(x1, y1, range_x, range_y)) or
                        (pos_xy_within_range(x2, y2, range_x, range_y))):
                        edges_drawn[ (node1, node2) ] = True # Represents all edges of (node1, node2)
                
        return list(edges_drawn.keys())
    

    def draw_nodes(self, range_x, range_y,
                   nodes_central          = None,
                   nodes_force_label      = None,
                   node_label_font_size_norm   = 12,
                   node_label_font_size_small  = 6,
                   node_label_shrink_num_nodes = 6,
                   node_label_sample_num_nodes = 15,
                   node_label_off_num_nodes    = 20,
                   markersize = 3):
        
        if nodes_central is None:
            nodes_central = []
        if nodes_force_label is None:
            nodes_force_label = []
        
        label_ovv_check = Plane2D_avoid_ovv((0.05, 0.01))
        
        nodes_in_range   = self.nodes_within_range(range_x, range_y)
        nodes_with_label = nodes_in_range
        label_font_size  = node_label_font_size_norm
        
        if len(nodes_in_range) >= node_label_shrink_num_nodes:
            label_font_size = node_label_font_size_small
            
        if len(nodes_in_range) >= node_label_off_num_nodes:
            nodes_with_label = []
        elif len(nodes_in_range) > node_label_sample_num_nodes:
            nodes_with_label = choice(nodes_in_range,
                                      node_label_sample_num_nodes,
                                      replace=False)
                    
        for node in nodes_in_range:       
            pos_x, pos_y = self.igrf.nodes[ node ][ KEY_NODE_COORD_XY ]
            rate_pos_x = get_rate_pos(range_x, pos_x)
            rate_pos_y = get_rate_pos(range_y, pos_y)
            
            if node in nodes_central:
                node_color = "red"
            else:
                node_color = "gray"
            if (pos_xy_within_range(pos_x, pos_y, range_x, range_y)):
                self.ax.plot(pos_x, pos_y, 'o', color = node_color, markersize = markersize)
                
                if KEY_DISP_NODE_LABEL in self.igrf.nodes[ node ]:
                    node_label = self.igrf.nodes[ node ][ KEY_DISP_NODE_LABEL ]
                else:
                    node_label = node
                
                if KEY_NODE_LABEL_OFFSET_XY in self.igrf.nodes[ node ]:
                    offset100_x, offset100_y = self.igrf.nodes[ node ][ KEY_NODE_LABEL_OFFSET_XY ]
                    off_x = (range_x[1] - range_x[0])*offset100_x / 100
                    off_y = (range_y[1] - range_y[0])*offset100_y / 100
                else:
                    off_x = 0
                    off_y = 0
                
                if node in nodes_force_label:
                    self.ax.text(pos_x + off_x, pos_y + off_y,
                                 " " + node_label,
                                 fontsize = node_label_font_size_norm,
                                 horizontalalignment = 'left',
                                 verticalalignment   = 'top')
                    label_ovv_check.put_pos_force((rate_pos_x, rate_pos_y))
                elif node in nodes_with_label:
                    if (len(nodes_in_range) < node_label_shrink_num_nodes or
                        not label_ovv_check.judge_ovv((rate_pos_x, rate_pos_y))):
                        self.ax.text(pos_x + off_x, pos_y + off_y,
                                     " " + node_label,
                                     fontsize = label_font_size,
                                     horizontalalignment = 'left',
                                     verticalalignment   = 'top')
                        label_ovv_check.put_pos((rate_pos_x, rate_pos_y))

        return nodes_in_range
    

    def draw_edge(self,
                  range_x, range_y,
                  ipos_x1, ipos_y1,
                  ipos_x2, ipos_y2,
                  edir, ecolor = "gray",
                  edge_label_list = None,
                  edge_lenrate_label_disp_limit = 0.07,
                  edge_label_draw = True,
                  disp_edge_outrange_node = True,
                  fontsize = 6):
        
        pos_x1, pos_x2 = ipos_x1, ipos_x2
        pos_y1, pos_y2 = ipos_y1, ipos_y2
        range_x_min, range_x_max = range_x        
        range_y_min, range_y_max = range_y
                     
        class E_OutRangeEdge(BaseException):
            pass
        outrange_edge_flag = False

        try:                     
            if pos_x1 < range_x_min:
                if pos_x2 < range_x_min:
                    raise E_OutRangeEdge
                pos_y1 = (range_x_min - pos_x1) / (pos_x2 - pos_x1) * (pos_y2 - pos_y1) + pos_y1
                pos_x1 = range_x_min
    
            if pos_x2 < range_x_min:
                if pos_x1 < range_x_min:
                    raise E_OutRangeEdge
                pos_y2 = (range_x_min - pos_x2) / (pos_x2 - pos_x1) * (pos_y2 - pos_y1) + pos_y2
                pos_x2 = range_x_min
                
            if pos_x1 > range_x_max:
                if pos_x2 > range_x_max:
                    raise E_OutRangeEdge
                pos_y1 = (range_x_max - pos_x2) / (pos_x2 - pos_x1) * (pos_y2 - pos_y1) + pos_y2
                pos_x1 = range_x_max
                                
            if pos_x2 > range_x_max:
                if pos_x1 > range_x_max:
                    raise E_OutRangeEdge
                pos_y2 = (range_x_max - pos_x1) / (pos_x2 - pos_x1) * (pos_y2 - pos_y1) + pos_y1
                pos_x2 = range_x_max
                
            if pos_y1 < range_y_min:
                if pos_y2 < range_y_min:
                    raise E_OutRangeEdge
                pos_x1 = (range_y_min - pos_y2) / (pos_y2 - pos_y1) * (pos_x2 - pos_x1) + pos_x2
                pos_y1 = range_y_min
    
            if pos_y2 < range_y_min:
                if pos_y1 < range_y_min:
                    raise E_OutRangeEdge
                pos_x2 = (range_y_min - pos_y1) / (pos_y2 - pos_y1) * (pos_x2 - pos_x1) + pos_x1
                pos_y2 = range_y_min
    
            if pos_y1 > range_y_max:
                if pos_y2 > range_y_max:
                    raise E_OutRangeEdge
                pos_x1 = (range_y_max - pos_y2) / (pos_y2 - pos_y1) * (pos_x2 - pos_x1) + pos_x2
                pos_y1 = range_y_max
            
            if pos_y2 > range_y_max:
                if pos_y1 > range_y_max:
                    raise E_OutRangeEdge
                pos_x2 = (range_y_max - pos_y1) / (pos_y2 - pos_y1) * (pos_x2 - pos_x1) + pos_x1
                pos_y2 = range_y_max
                
        except E_OutRangeEdge:
            outrange_edge_flag = True # using "else" clause may be another option

        if outrange_edge_flag:
            return False
            
        elif ((pos_xy_within_range(ipos_x1, ipos_y1, range_x, range_y)) or
              (pos_xy_within_range(ipos_x2, ipos_y2, range_x, range_y)) or disp_edge_outrange_node):
            if edir == "-":
                self.ax.annotate(s = "",
                                 xytext = (pos_x1, pos_y1),
                                 xy     = (pos_x2, pos_y2),
                                 arrowprops = \
                        dict(arrowstyle = '%s' % edir,
                             linestyle='dotted',
                             ec = ecolor))
            else:
                self.ax.annotate(s = "",
                                 xytext = (pos_x1, pos_y1),
                                 xy     = (pos_x2, pos_y2),
                                 arrowprops = \
                        dict(arrowstyle = '%s, head_width=0.5, head_length=0.5' % edir,
                             linestyle='dotted',
                             ec = ecolor))
            # print("x:", range_x, "y:", range_y)
            # print("---", (pos_x1, pos_y1), (pos_x2, pos_y2), edir)
            """ The tip (arrow?) may produce:
C:\WinAppl\Anaconda3\lib\site-packages\matplotlib\patches.py:3145: RuntimeWarning: invalid value encountered in double_scalars
  ddx = pad_projected * dx / cp_distance
C:\WinAppl\Anaconda3\lib\site-packages\matplotlib\patches.py:3146: RuntimeWarning: invalid value encountered in double_scalars
  ddy = pad_projected * dy / cp_distance
C:\WinAppl\Anaconda3\lib\site-packages\matplotlib\patches.py:3149: RuntimeWarning: invalid value encountered in double_scalars
  dx = dx / cp_distance * head_dist
C:\WinAppl\Anaconda3\lib\site-packages\matplotlib\patches.py:3150: RuntimeWarning: invalid value encountered in double_scalars
  dy = dy / cp_distance * head_dist
"""            

            edge_len       = ((pos_x2 - pos_x1)**2 + (pos_y2 - pos_y1)**2)**0.5
            range_diag_len = ((range_x_max - range_x_min)**2 + (range_y_max - range_y_min)**2)**0.5
            lenrate = edge_len / range_diag_len
    
            # print(edge_len, range_diag_len, lenrate)
    
            if edge_label_list and edge_label_draw and lenrate >= edge_lenrate_label_disp_limit:
                self.ax.text((pos_x1+pos_x2)/2,
                             (pos_y1+pos_y2)/2,
                             "\n".join(edge_label_list),
                             fontsize = fontsize,
                             horizontalalignment='center',
                             verticalalignment='center')  
            return True
        else:
            return False
  

    def draw_edges(self, range_x, range_y,
                   edges_central = None,
                   edge_label_draw_num_edges_limit = 30,
                   disp_edge_outrange_node = True):
    
        if edges_central is None:
            edges_central = []
        else:
            edges_central = [ (iedge[0], iedge[1]) for iedge in edges_central ]
    
        edges_in_range = self.edges_within_range(range_x, range_y)
        if len(edges_in_range) > edge_label_draw_num_edges_limit:
            edge_label_draw = False
        else:
            edge_label_draw = True
    
        edges_drawn = {}
                                
        for iedge in self.igrf.edges(data = True):
            node1, node2, eattr_h = iedge
            if (KEY_NODE_COORD_XY in self.igrf.nodes[ node1 ] and
                KEY_NODE_COORD_XY in self.igrf.nodes[ node2 ]):
                pos_x1, pos_y1 = self.igrf.nodes[ node1 ][ KEY_NODE_COORD_XY ]
                pos_x2, pos_y2 = self.igrf.nodes[ node2 ][ KEY_NODE_COORD_XY ]
                edir = eattr_h.get(KEY_EDGE_DIRECTION, "->")
                
                poss_all = [(pos_x1, pos_y1)] + \
                    eattr_h.get(KEY_EDGE_RELAY_POSS, []) + \
                    [(pos_x2, pos_y2)]
                for k in range(len(poss_all) - 1):
                    x1, y1 = poss_all[k]
                    x2, y2 = poss_all[k+1]
                    # if k == 0 or k == len(poss_all) - 2:
                    #     edge_label_list = eattr_h.get(KEY_EDGE_LABEL_LIST, None)
                    # else:
                    #     edge_label_list = None
                    edge_label_list = eattr_h.get(KEY_EDGE_LABEL_LIST, None)
                
                    if tuple(iedge[0:2]) in edges_central:
                        ecolor = "red"
                    else:
                        ecolor = "gray"
                    if self.draw_edge(range_x, range_y,
                                      x1, y1,
                                      x2, y2,
                                      edir,
                                      ecolor,
                                      edge_label_list,
                                      edge_label_draw = edge_label_draw,
                                      disp_edge_outrange_node = disp_edge_outrange_node):
                        edges_drawn[ (node1, node2) ] = True # Represents all edges of (node1, node2)

        return list(edges_drawn.keys())


    def search_closest_farthest_nodes(self, node_central):

        cmin = None
        cmax = None
        cmin_node = None
        cmax_node = None
        
        max_abs_dist_x = 0
        max_abs_dist_y = 0
        
        if KEY_NODE_COORD_XY in self.igrf.nodes[ node_central ]:
            central_pos_x, central_pos_y = \
                self.igrf.nodes[ node_central ][ KEY_NODE_COORD_XY ]
            for inode in self.igrf.nodes():
                if inode != node_central and KEY_NODE_COORD_XY in self.igrf.nodes[ inode ]:
                    node_pos_x, node_pos_y = self.igrf.nodes[ inode ][ KEY_NODE_COORD_XY ]
                    if (cmin is None or
                        cmin > (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2):
                        cmin = (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2
                        cmin_node = inode
                    if (cmax is None or
                        cmax < (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2):
                        cmax = (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2
                        cmax_node = inode
                        
                    if max_abs_dist_x < abs(node_pos_x - central_pos_x):
                        max_abs_dist_x = abs(node_pos_x - central_pos_x)
                    if max_abs_dist_y < abs(node_pos_y - central_pos_y):
                        max_abs_dist_y = abs(node_pos_y - central_pos_y)                    
                    
        return cmin_node, cmax_node, max_abs_dist_x, max_abs_dist_y

    def search_closest_farthest_nodes2(self, node_central1, node_central2):

        cmin = None
        cmax = None
        cmin_node = None
        cmax_node = None
        
        max_abs_dist_x = 0
        max_abs_dist_y = 0
                
        if (KEY_NODE_COORD_XY in self.igrf.nodes[ node_central1 ] and
            KEY_NODE_COORD_XY in self.igrf.nodes[ node_central2 ]):
            
            central_pos_x = \
                (self.igrf.nodes[ node_central1 ][ KEY_NODE_COORD_XY ][0] +
                 self.igrf.nodes[ node_central2 ][ KEY_NODE_COORD_XY ][0]) / 2
            central_pos_y = \
                (self.igrf.nodes[ node_central1 ][ KEY_NODE_COORD_XY ][1] +
                 self.igrf.nodes[ node_central2 ][ KEY_NODE_COORD_XY ][1]) / 2
                                  
            for inode in self.igrf.nodes():
                if inode not in (node_central1, node_central2) and KEY_NODE_COORD_XY in self.igrf.nodes[ inode ]:
                    node_pos_x, node_pos_y = self.igrf.nodes[ inode ][ KEY_NODE_COORD_XY ]
                    if (cmin is None or
                        cmin > (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2):
                        cmin = (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2
                        cmin_node = inode
                    if (cmax is None or
                        cmax < (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2):
                        cmax = (node_pos_x - central_pos_x)**2 + (node_pos_y - central_pos_y)**2
                        cmax_node = inode                    

                    if max_abs_dist_x < abs(node_pos_x - central_pos_x):
                        max_abs_dist_x = abs(node_pos_x - central_pos_x)
                    if max_abs_dist_y < abs(node_pos_y - central_pos_y):
                        max_abs_dist_y = abs(node_pos_y - central_pos_y)           
                    
        return cmin_node, cmax_node, max_abs_dist_x, max_abs_dist_y

    def output_fig_around_node(self, node_central,
                               outer = 1.2, rate = 0.0,
                               outfile = None,
                               axis_bg_color = (0.9, 0.9, 0.8),
                               fig_face_color = (0.8, 0.8, 0.7),
                               xlabel = "X-axis", ylabel = "Y-axis",
                               figsize = (8, 7), dpi = None):
        # node_central has to have coordinate.
        
        if node_central not in self.igrf.nodes:
            return "Node %s not found" % node_central
        if KEY_NODE_COORD_XY not in self.igrf.nodes[ node_central ]:
            return "Coordinate for node %s not found" % node_central
        node_central_pos_x, node_central_pos_y = self.igrf.nodes[ node_central ][ KEY_NODE_COORD_XY ]
        
        
        (cmin_node, cmax_node,
         max_abs_dist_x, max_abs_dist_y) = self.search_closest_farthest_nodes(node_central)
        # If cmin_node is None, cmax_node is None as well. This will cause error.
        
        # print("Closest farthest for", node_central,
        #       self.search_closest_farthest_nodes(node_central))
        
        if cmin_node is None or cmax_node is None:
            return "Single node %s in the map" %  node_central
        
        cmin_node_pos_x, cmin_node_pos_y = self.igrf.nodes[ cmin_node ][ KEY_NODE_COORD_XY ]
        cmax_node_pos_x, cmax_node_pos_y = self.igrf.nodes[ cmax_node ][ KEY_NODE_COORD_XY ]
        
        half_width_small  = abs(cmin_node_pos_x - node_central_pos_x)
        half_height_small = abs(cmin_node_pos_y - node_central_pos_y)
        
        half_width_large  = max_abs_dist_x # abs(cmax_node_pos_x - node_central_pos_x)
        half_height_large = max_abs_dist_y # abs(cmax_node_pos_y - node_central_pos_y)
        
        half_width_range  = half_width_large - half_width_small
        half_height_range = half_height_large - half_height_small
        
        half_width  = (half_width_small + half_width_range * rate) * outer
        half_height = (half_height_small + half_height_range * rate) * outer

        # Create a Figure object.
        self.fig = pyplot.figure(figsize = figsize, dpi = dpi, facecolor = fig_face_color)

        # Create an Axes object.
        self.ax = self.fig.add_subplot(1,1,1) # one row, one column, first plot
        self.ax.set_axis_bgcolor(axis_bg_color)
        # self.ax.patch.set_facecolor(axis_bg_color)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        range_x_min = node_central_pos_x - half_width
        range_x_max = node_central_pos_x + half_width
        range_y_min = node_central_pos_y - half_height
        range_y_max = node_central_pos_y + half_height
        
        pyplot.xlim([range_x_min, range_x_max])
        pyplot.ylim([range_y_min, range_y_max])
        
        # print("Display range for", node_central, [range_x_min, range_x_max], [range_y_min, range_y_max])
        
        self.draw_nodes([range_x_min, range_x_max],
                        [range_y_min, range_y_max], node_central)
        self.draw_edges([range_x_min, range_x_max],
                        [range_y_min, range_y_max])
        
        # print("node_central_pos x y:", node_central_pos_x, node_central_pos_y)
        
        pyplot.title("Network around %s" % node_central)
        
        if outfile:
            pyplot.savefig(outfile,
                           facecolor = self.fig.get_facecolor())
        else:
            pyplot.show()

        return "OK"

    def output_fig_around_node_simple(self,
                                      node_central,
                                      half_width, half_height,
                                      offset_x = 0, offset_y = 0,
                                      outfile = None,
                                      axis_bg_color = (0.9, 0.9, 0.8),
                                      fig_face_color = (0.8, 0.8, 0.7),
                                      xlabel = "X-axis", ylabel = "Y-axis",
                                      figsize = (8, 7), dpi = None):
        # node_central has to have coordinate.
        
        if node_central not in self.igrf.nodes:
            return "Node %s not found" % node_central
        if KEY_NODE_COORD_XY not in self.igrf.nodes[ node_central ]:
            return "Coordinate for node %s not found" % node_central
        node_central_pos_x, node_central_pos_y = self.igrf.nodes[ node_central ][ KEY_NODE_COORD_XY ]
        
        
        # Create a Figure object.
        self.fig = pyplot.figure(figsize = figsize,
                                 dpi = dpi,
                                 facecolor = fig_face_color)

        # Create an Axes object.
        self.ax = self.fig.add_subplot(1,1,1) # one row, one column, first plot
        self.ax.set_facecolor(axis_bg_color) # set_axis_bgcolor(axis_bg_color)
        # self.ax.patch.set_facecolor(axis_bg_color)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        range_x_min = node_central_pos_x - half_width + offset_x
        range_x_max = node_central_pos_x + half_width + offset_x
        range_y_min = node_central_pos_y - half_height + offset_y
        range_y_max = node_central_pos_y + half_height + offset_y
        
        pyplot.xlim([range_x_min, range_x_max])
        pyplot.ylim([range_y_min, range_y_max])
        
        # print("Display range for", node_central, [range_x_min, range_x_max], [range_y_min, range_y_max])
        
        nodes_drawn = self.draw_nodes([range_x_min, range_x_max],
                                      [range_y_min, range_y_max],
                                      nodes_central = [ node_central ])
        edges_drawn = self.draw_edges([range_x_min, range_x_max],
                                      [range_y_min, range_y_max])
        
        # print("Nodes drawn:", nodes_drawn)
        # print("Nodes expected to be drawn:", self.nodes_within_range([range_x_min, range_x_max],
        #                                                              [range_y_min, range_y_max]))
        # print("Edges drawn:", edges_drawn)
        # print("Edges expected to be drawn:", self.edges_within_range([range_x_min, range_x_max],
        #                                                              [range_y_min, range_y_max]))                    
        # print("node_central_pos x y:", node_central_pos_x, node_central_pos_y)
        
        pyplot.title("Network around %s" % node_central)
        
        if outfile:
            pyplot.savefig(outfile,
                           facecolor = self.fig.get_facecolor())
        else:
            pyplot.show()

        return nodes_drawn, edges_drawn


    def output_fig_around_region_simple(self,
                                        range_x, range_y,
                                        nodes_central = None,
                                        edges_central = None,
                                        outfile = None,
                                        axis_bg_color = (0.9, 0.9, 0.8),
                                        fig_face_color = (0.8, 0.8, 0.7),
                                        node_label_font_size_norm   = 12,
                                        node_label_font_size_small  = 6,
                                        node_label_shrink_num_nodes = 6,
                                        node_label_sample_num_nodes = 15,
                                        node_label_off_num_nodes    = 20,
                                        edge_label_draw_num_edges_limit = 30,
                                        disp_edge_outrange_node = True,
                                        xlabel = "X-axis", ylabel = "Y-axis",
                                        title = "Network",
                                        figsize = (8, 7), dpi = None):      
        
        # Create a Figure object.
        self.fig = pyplot.figure(figsize = figsize,
                                 dpi = dpi,
                                 facecolor = fig_face_color)

        # Create an Axes object.
        self.ax = self.fig.add_subplot(1,1,1) # one row, one column, first plot
        self.ax.set_facecolor(axis_bg_color) # set_axis_bgcolor(axis_bg_color)
        # self.ax.patch.set_facecolor(axis_bg_color)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        range_x_min, range_x_max = range_x
        range_y_min, range_y_max = range_y
        
        pyplot.xlim([range_x_min, range_x_max])
        pyplot.ylim([range_y_min, range_y_max])
        
        # print("Display range for", node_central, [range_x_min, range_x_max], [range_y_min, range_y_max])

        edges_drawn = self.draw_edges([range_x_min, range_x_max],
                                      [range_y_min, range_y_max],
                                      edges_central = edges_central,
                                      edge_label_draw_num_edges_limit = edge_label_draw_num_edges_limit,
                                      disp_edge_outrange_node = disp_edge_outrange_node)
        
        nodes_drawn = self.draw_nodes([range_x_min, range_x_max],
                                      [range_y_min, range_y_max],
                                      nodes_central = nodes_central,
                                      nodes_force_label = nodes_central,
                                      node_label_font_size_norm   = node_label_font_size_norm,
                                      node_label_font_size_small  = node_label_font_size_small,
                                      node_label_shrink_num_nodes = node_label_shrink_num_nodes,
                                      node_label_sample_num_nodes = node_label_sample_num_nodes,
                                      node_label_off_num_nodes    = node_label_off_num_nodes)

        
        # print("Nodes drawn:", nodes_drawn)
        # print("Nodes expected to be drawn:", self.nodes_within_range([range_x_min, range_x_max],
        #                                                              [range_y_min, range_y_max]))
        # print("Edges drawn:", edges_drawn)
        # print("Edges expected to be drawn:", self.edges_within_range([range_x_min, range_x_max],
        #                                                              [range_y_min, range_y_max]))                    
        # print("node_central_pos x y:", node_central_pos_x, node_central_pos_y)
        
        pyplot.title(title)
        
        if outfile:
            pyplot.savefig(outfile,
                           facecolor = self.fig.get_facecolor())
        else:
            pyplot.show()

        return nodes_drawn, edges_drawn


    def output_fig_around_edge(self,
                               edge_central,
                               outer = 1.2, rate = 0.0,
                               outfile = None,
                               axis_bg_color = (0.9, 0.9, 0.8),
                               fig_face_color = (0.8, 0.8, 0.7),
                               xlabel = "X-axis", ylabel = "Y-axis",
                               figsize = (8, 7), dpi = None):
        # node_central has to have coordinate.
        
        worked_msg = "OK"
        
        if not self.igrf.has_edge(*edge_central):
            rev_edge_central = list(edge_central)
            rev_edge_central[0], rev_edge_central[1] = rev_edge_central[1], rev_edge_central[0] 
            if not self.igrf.has_edge(*rev_edge_central):
                return "Edge %s not found" % str(edge_central)
            else:
                edge_central = rev_edge_central
                worked_msg = "Reversed"
                
        node_central1, node_central2 = edge_central[0:2]
        
        if KEY_NODE_COORD_XY not in self.igrf.nodes[ node_central1 ]:
            return "Coordinate for node %s not found" % node_central1
        if KEY_NODE_COORD_XY not in self.igrf.nodes[ node_central2 ]:
            return "Coordinate for node %s not found" % node_central2
        
        node_central_pos_x1, node_central_pos_y1 = self.igrf.nodes[ node_central1 ][ KEY_NODE_COORD_XY ]
        node_central_pos_x2, node_central_pos_y2 = self.igrf.nodes[ node_central2 ][ KEY_NODE_COORD_XY ]
        
        rect_central_x      = (node_central_pos_x1 + node_central_pos_x2) / 2
        rect_central_y      = (node_central_pos_y1 + node_central_pos_y2) / 2
        rect_central_x_min  = min(node_central_pos_x1, node_central_pos_x2)
        rect_central_x_max  = max(node_central_pos_x1, node_central_pos_x2)
        rect_central_y_min  = min(node_central_pos_y1, node_central_pos_y2)
        rect_central_y_max  = max(node_central_pos_y1, node_central_pos_y2)
        rect_central_width  = rect_central_x_max - rect_central_x_min
        rect_central_height = rect_central_y_max - rect_central_y_min
        
        (cmin_node, cmax_node,
         max_abs_dist_x, max_abs_dist_y) = self.search_closest_farthest_nodes2(node_central1, node_central2)
        # If cmin_node is None, cmax_node is None as well. This will cause error.
        
        if cmin_node is None or cmax_node is None:
            cmin_node_pos_x, cmin_node_pos_y = rect_central_x_min, rect_central_y_min
            cmax_node_pos_x, cmax_node_pos_y = rect_central_x_max, rect_central_y_max
        else:
            cmin_node_pos_x, cmin_node_pos_y = self.igrf.nodes[ cmin_node ][ KEY_NODE_COORD_XY ]
            cmax_node_pos_x, cmax_node_pos_y = self.igrf.nodes[ cmax_node ][ KEY_NODE_COORD_XY ]
        
        half_width_small  = abs(cmin_node_pos_x - rect_central_x)
        if half_width_small < rect_central_width / 2:
            half_width_small = rect_central_width / 2

        half_height_small = abs(cmin_node_pos_y - rect_central_y)
        if half_height_small < rect_central_height / 2:
            half_height_small = rect_central_height / 2
                    
        half_width_large  = max_abs_dist_x # abs(cmax_node_pos_x - rect_central_x)
        if half_width_large < rect_central_width / 2:
            half_width_large = rect_central_width / 2
        
        half_height_large = max_abs_dist_y # abs(cmax_node_pos_y - rect_central_y)
        if half_height_large < rect_central_height / 2:
            half_height_large = rect_central_height / 2        
        
        half_width_range  = half_width_large - half_width_small
        half_height_range = half_height_large - half_height_small
        
        half_width  = (half_width_small + half_width_range * rate) * outer
        half_height = (half_height_small + half_height_range * rate) * outer

        # Create a Figure object.
        self.fig = pyplot.figure(figsize = figsize, dpi = dpi, facecolor = fig_face_color)

        # Create an Axes object.
        self.ax = self.fig.add_subplot(1,1,1) # one row, one column, first plot
        self.ax.set_axis_bgcolor(axis_bg_color)
        # self.ax.patch.set_facecolor(axis_bg_color)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        range_x_min = rect_central_x - half_width
        range_x_max = rect_central_x + half_width
        range_y_min = rect_central_y - half_height
        range_y_max = rect_central_y + half_height
        
        pyplot.xlim([range_x_min, range_x_max])
        pyplot.ylim([range_y_min, range_y_max])
        
        self.draw_nodes([range_x_min, range_x_max],
                        [range_y_min, range_y_max])
        self.draw_edges([range_x_min, range_x_max],
                        [range_y_min, range_y_max], edge_central)
        
        # print("node_central_pos x y:", node_central_pos_x, node_central_pos_y)
        
        pyplot.title("Network around %s and %s"
                     % (node_central1, node_central2))
        
        if outfile:
            pyplot.savefig(outfile,
                           facecolor = self.fig.get_facecolor())
        else:
            pyplot.show()


        return worked_msg


if __name__ == '__main__':

    from FileDirPath.rsFilePath1 import RSFPath
    dg = rsNetworkX_DiGraph()

    dg.add_edge("Node A", "Node B",
                **{ KEY_EDGE_DIRECTION : "<->" })
    dg.add_edge("Node A", "Node C",
                **{ KEY_EDGE_LABEL_LIST : ["1.2.15.6", "3.1.1.4"],
                    KEY_EDGE_RELAY_POSS : [(-3, 10), (-5, 6), (-9, 5)] })
    dg.add_edge("Node A", "Node E",
                **{ KEY_EDGE_DIRECTION : "-" })
    dg.add_edge("Node F", "Node E")
    dg.add_edge("Node C", "Node D")
    dg.add_edge("Node E", "Node D")
    dg.add_edge("Node F", "Node D")
    dg.add_edge("Node G", "Node H")
    dg.add_edge("Node I", "Node J")
    dg.add_edge("Node I", "Node K")
    dg.add_edge("Node L", "Node K")
    dg.add_edge("Node N", "Node M")
    dg.add_edge("Node O", "Node P")
    dg.add_edge("Node Q", "Node R")
    dg.add_edge("Node S", "Node T")
    dg.node["Node A"][ KEY_NODE_COORD_XY ] = (5, 15)
    dg.node["Node A"][ KEY_NODE_LABEL_OFFSET_XY ] = (-3, 5)
    dg.node["Node B"][ KEY_NODE_COORD_XY ] = (2,  6)
    dg.node["Node C"][ KEY_NODE_COORD_XY ] = (-10, 0)
    dg.node["Node D"][ KEY_NODE_COORD_XY ] = (20, 25)
    dg.node["Node E"][ KEY_NODE_COORD_XY ] = (-10,25)
    dg.node["Node F"][ KEY_NODE_COORD_XY ] = (-11,20)
    dg.node["Node G"][ KEY_NODE_COORD_XY ] = (-7, 9)
    dg.node["Node H"][ KEY_NODE_COORD_XY ] = (-6, 8)
    dg.node["Node I"][ KEY_NODE_COORD_XY ] = (-5, 8)
    dg.node["Node J"][ KEY_NODE_COORD_XY ] = (-4, 8)    
    dg.node["Node K"][ KEY_NODE_COORD_XY ] = (-3, 8)
    dg.node["Node L"][ KEY_NODE_COORD_XY ] = (-2, 8)
    dg.node["Node M"][ KEY_NODE_COORD_XY ] = (-1, 7)
    dg.node["Node N"][ KEY_NODE_COORD_XY ] = (-4, 6)
    dg.node["Node O"][ KEY_NODE_COORD_XY ] = ( 5, 5)
    dg.node["Node P"][ KEY_NODE_COORD_XY ] = (-1, 4)
    dg.node["Node Q"][ KEY_NODE_COORD_XY ] = ( 3, 3)
    dg.node["Node R"][ KEY_NODE_COORD_XY ] = (-1, 2)
    dg.node["Node S"][ KEY_NODE_COORD_XY ] = ( 6, 1)
    dg.node["Node T"][ KEY_NODE_COORD_XY ] = (-1, 0)
    dg.node["Node B"][ KEY_DISP_NODE_LABEL  ] = "Hello!"
    dg.output(keyw = True, noval_str = "---")
    
    drawgrf = DrawNetworkX_simple(dg)
        
#     drawgrf.output_fig_around_node("Node E", rate = 0.3)
#     print("Around edge:",
#           drawgrf.output_fig_around_edge(("Node C", "Node D"), rate = 0.3))
#     print("Around edge:",
#           drawgrf.output_fig_around_edge(("Node D", "Node C"), rate = 0.3))
#     
#     savepdf1 = RSFPath("DESKTOP", "tmpintrxgraph1_2.pdf")
#     drawgrf.output_fig_around_node("Node A", rate = 0.3,
#                                    outfile = savepdf1,
#                                    # axis_bg_color = (0.9, 0.5, 0.5),
#                                    figsize = (7,8),
#                                    dpi = 1200)
    savepdf2 = RSFPath("DESKTOP", "tmpintrxgraph1_3.pdf")
    nodes_drawn, edges_drawn \
        = drawgrf.output_fig_around_node_simple("Node A",
                                                half_width = 17, half_height = 15,
                                                offset_x = +0, offset_y = -10, # offset_x = 2 okay, 3 --> warning.
                                                outfile = savepdf2,
                                                # axis_bg_color = (0.9, 0.5, 0.5),
                                                figsize = (7,8),
                                                dpi = 1200)
    print("Nodes drawn:", nodes_drawn)
    print("Edges drawn:", edges_drawn)
    
    
    savepdf3 = RSFPath("DESKTOP", "tmpintrxgraph1_4.pdf")
    nodes_drawn, edges_drawn \
        = drawgrf.output_fig_around_region_simple(
            range_x = [-30, 30], range_y = [-30, 30],
            nodes_central = ["Node A", "Node C"],
            edges_central = [("Node A", "Node E"), ("Node A", "Node B")],
            outfile = savepdf3,
            node_label_font_size_norm   = 12,
            node_label_font_size_small  = 6,
            node_label_shrink_num_nodes = 6,
            node_label_sample_num_nodes = 10,
            node_label_off_num_nodes    = 25,
            disp_edge_outrange_node = True,
            title = "Regional output",
            # axis_bg_color = (0.9, 0.5, 0.5),
            figsize = (7,8),
            dpi = 1200)
    print("Nodes drawn:", nodes_drawn)
    print("Edges drawn:", edges_drawn)
