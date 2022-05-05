'''
Created on 2016/08/10

@author: rsaito
'''

class Plane2D_avoid_ovv:
    def __init__(self, space_info):
        
        self.space_info = space_info
        self.poss = {}
    
    def judge_ovv_single_pos(self, pos1, pos2):    
        
        pos_x1, pos_y1 = pos1
        pos_x2, pos_y2 = pos2
        
        return (abs(pos_x1 - pos_x2) < self.space_info[0] and
                abs(pos_y1 - pos_y2) < self.space_info[1])
    
    def judge_ovv(self, pos_new):

        for pos_rec in self.poss:
            if self.judge_ovv_single_pos(pos_new, pos_rec):
                return True
        
        return False
    
    def put_pos(self, pos_new): # pos_new must be hashable
        
        if self.judge_ovv(pos_new):
            return False
        else:     
            self.poss[ pos_new ] = True
            return True
        
    def put_pos_force(self, pos_new):

        self.poss[ pos_new ] = True


if __name__ == '__main__':
    
    av_ovv = Plane2D_avoid_ovv((2, 1))
    print(av_ovv.put_pos((5, 10)))
    print(av_ovv.put_pos((6, 10.9)))
    print(av_ovv.put_pos((7, 14)))
    print(av_ovv.put_pos((10, 20)))
    print(av_ovv.put_pos((11, 23)))
    print(av_ovv.poss)
    