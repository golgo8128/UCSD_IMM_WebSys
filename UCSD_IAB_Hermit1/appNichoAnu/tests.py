from django.test import TestCase

# The testing system will automatically find tests in any file whose
# name begins with test.

# ./manage.py test appNichoAnu

# Create your tests here.

from django.contrib.auth.models import User
from django.utils import timezone
from .models import *
from .modules.to_networkx1_4 import del_networkx_rec, to_networkx_from_rec

class MetabNetTests(TestCase):

    def test_simple_message(self):
    
        self.dummy1 = "Hello!"
        print("Test of testing ...", self)
        print(self.dummy1)
        
    def test_nodeadd(self):
        
        # print(User.objects.all()) # empty
        # print(self.dummy1) # no attribute error

        testuser = User(username = "testuser")
        testuser.save()        
       
        testnode1 = NichoNode(
            user         = testuser,
            timestamp    = timezone.now(),
            node_id      = "Nodo 1", 
            node_vis_id  = "Nodo 1",
            pos_x_on_map = 100,
            pos_y_on_map = 200,
            )
        testnode1.save()
        
        testnode2 = NichoNode(
            user         = testuser,
            timestamp    = timezone.now(),
            node_id      = "Nodo 2", 
            node_vis_id  = "Nodo 2",
            pos_x_on_map = 300,
            pos_y_on_map = 500,
        )
        testnode2.save()

        testedge1to2_1 = NichoEdge(
            user        = testuser,
            timestamp   = timezone.now(),
            node_src    = testnode1,
            node_tgt    = testnode2,
            is_directed = True,

            relay_pos_x1_on_map = 120,
            relay_pos_y1_on_map = 210,
        )
        testedge1to2_1.save()  
        
        testedge1to2_2 = NichoEdge(
            user        = testuser,
            timestamp   = timezone.now(),
            node_src    = testnode1,
            node_tgt    = testnode2,
            is_directed = True,

            relay_pos_x1_on_map = 125,
            relay_pos_y1_on_map = 215,
            relay_pos_x2_on_map = 155,
            relay_pos_y2_on_map = 295,
        )              
        testedge1to2_2.save()
        
        testedge2to1_1 = NichoEdge(
            user        = testuser,
            timestamp   = timezone.now(),
            node_src    = testnode2,
            node_tgt    = testnode1,
            is_directed = True,

            relay_pos_x1_on_map = 400,
            relay_pos_y1_on_map = 300,
            relay_pos_x2_on_map = 410,
            relay_pos_y2_on_map = 320,            
        )              
        testedge2to1_1.save()        
        
        testedge2to1_2 = NichoEdge(
            user        = testuser,
            timestamp   = timezone.now(),
            node_src    = testnode2,
            node_tgt    = testnode1,
            is_directed = True,

            relay_pos_x1_on_map = 125,
            relay_pos_y1_on_map = 215,
            relay_pos_x2_on_map = 155,
            relay_pos_y2_on_map = 295,
        )              
        testedge2to1_2.save()        
        
        testgrf = to_networkx_from_rec(update = True)
        testgrf.output(keyw = True)

        testgrf = to_networkx_from_rec(focus_edge = testedge2to1_2)
        testgrf.output(keyw = True)
               
        print(testedge1to2_1.pick_one_relay_set(inc_reverse = True))
        
        del_networkx_rec()
        
        
        