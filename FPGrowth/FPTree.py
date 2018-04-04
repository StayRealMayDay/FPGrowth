# -*-coding:utf-8-*-
import queue
from FPGrowth.FPNode import FPNode


class FPTree:


    def __init__(self):
        # init toot node
        self.root = FPNode()
        # sotre 1 frequent item by down sequence
        self.headerList = []
        # map the item int headerList to the tree node
        self.mapItemNodes = {}
        # map the item to the last same item nodes in the FPTree
        self.mapItemLastNode = {}
        # create root node

    '''
    one transaction is a sequence
    and this method will add these item in the transaction into the tree sequentially
    '''
    def addTransaction(self, transactions, mapSupport, minSupport):

        for transaction in transactions:
            currentNode = self.root
            for item in transaction:
                if mapSupport[item] > minSupport:
                    child = currentNode.getChildWithID(item)
                    if child is None:
                        newNode = FPNode()
                        newNode.itemID = item
                        newNode.parent = currentNode
                        currentNode.children.append(newNode)
                        currentNode = newNode
                        self.fixNodeLinks(item, newNode)
                    else:
                        child.counter = child.counter + 1
                        currentNode = child

    '''
    this method is to find the last node which has the same itemID in the node link
    and add this node to the last position of the link
    '''
    def fixNodeLinks(self, item, node):
        if item in self.mapItemLastNode:
            self.mapItemLastNode[item].nodeLink = node
        self.mapItemLastNode[item] = node
        if item not in self.mapItemNodes:
            self.mapItemNodes[item] = node



    '''
    this method will create the header list in which the item ordered from more to less according to the support degree'''
    def createHeaderList(self,mapSupport):
        x = sorted(mapSupport.items(), key=lambda item: item[1], reverse=True)
        self.headerList = list(dict(x).keys())

    def display(self, gap, Node):
        if len(Node.children) > 0:
            for node in Node.children:
                print(gap + "(" + str(node.itemID) + ";" + str(node.counter) + ")")
                self.display(gap+"     ", node)


