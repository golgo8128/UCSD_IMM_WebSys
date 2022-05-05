from django.urls import path

from .views import views, views_add_edge1_1, views_add_node1_1, views_del_edge1_1, views_del_node1_1, \
    views_edge_info1_2, views_node_info1_4

app_name = "appNichoAnu"

urlpatterns = [

    path(r'node_info/node_vis_id=(?P<node_vis_id>[^@\s]+)',
         views_node_info1_4.node_vis_id_info, name="node_vis_id_info"),
    path(r'node_info/node_vis_id=(?P<node_vis_id>\S+)@hwidth=(?P<hwidth>\d+)_hheight=(?P<hheight>\d+)_offx=(?P<offx>-?\d+)_offy=(?P<offy>-?\d+)',
         views_node_info1_4.node_vis_id_info, name="node_vis_id_info"),
    path(r'edge_info/(?P<edge_id>\S+)',
         views_edge_info1_2.edge_info, name="edge_info"),
    path(r'del_node/(?P<node_vis_id>\S+)',
         views_del_node1_1.del_node, name="del_node"),
    path(r'del_edge/(?P<edge_id>\S+)',
         views_del_edge1_1.del_edge, name="del_edge"),
    path(r'add_node',
         views_add_node1_1.add_node, name="add_node"),
    path(r'add_edge',
         views_add_edge1_1.add_edge, name="add_edge"),
    path(r'', views.index, name="index"),
    path(r'info_pub', views.pub_db_tools, name="pub_db_tools"),
    path(r'survey', views.survey, name="survey"),
    path(r'member', views.member, name="member"),
    path(r'material_src', views.material_src, name="material_src"),
    path(r'history', views.history, name="history"),
    path(r'work_record', views.work_record, name="work_record"),
    path(r'blog', views.blog, name="blog"),

#     url(r'^node_info/(?P<id>\S+)$',
#         views.node_info, name="node_info"),     
    
]
