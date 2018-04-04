# -*-coding:utf-8-*-
class FPNode:


    def __init__(self):
        # to record  how many sequences have this node
        self.counter = 1
        '''
        to save the items
        '''
        self.itemID = -1
        '''
        to point to the father node
        '''
        self.parent = None
        '''
        to save the children node fo this node
        '''
        self.children = []
        '''
        to keep the node which have the same item but not in the same position
        '''
        self.nodeLink = None

    def getChildWithID(self, id):
        for child in self.children:
            if child.itemID == id:
                return child
        return None


