# -*-coding:utf-8-*-
from FPGrowth.FPTree import *
class AlgoFPGrowth:


    def __init__(self):
        self.transactionCount = 0
        self.maxPatternLength = 1000
        self.patterns = {}
        self.minSupport = 0



    def runAlgorrithm(self, path, minSupport):
        self.minSupport = minSupport
        mapSupport = self.scanDatabaseToDetermineFrequencyOfSingleItems(path)
        transcations = self.scanDatabaseToGetTheOrderedTransactions(path, minSupport, mapSupport)
        tree = FPTree()
        tree.addTransaction(transcations, mapSupport, minSupport)
        tree.display(" ", tree.root)
        tree.createHeaderList(mapSupport)
        if len(tree.headerList) > 0:
            postfix = []
            self.fpgrowth(tree, mapSupport, postfix, 0, self.transactionCount)

        print(tree)

    '''
    if the tree only has one path ,it call the saveAllCombinationOfPrefixPath() method to save all the possible pattern
    if not , it will pick up all the item in the tree`s header list one by one reversely 
    whenever it pick up a item, it save the pattern all item in the postfix + this item
    and build a new tree that contain all the paths which contain this item and recursion '''

    def fpgrowth(self, tree, mapSupport, postfix, postfixLength, postfixSupport):
        currentNode = tree.root
        isSinglePath = True;
        tempFPNodeList = []
        tempFPNodeListLength = 0
        if len(currentNode.children) < 2:
            currentNode = currentNode.children[0]
            while True:
                if len(currentNode.children) > 1:
                    isSinglePath = False
                    break
                tempFPNodeList.append(currentNode)
                tempFPNodeListLength += 1
                if len(currentNode.children) == 0:
                    break
                currentNode = currentNode.children[0]
        if isSinglePath:
            self.saveAllCombinationOfPrefixPath(tempFPNodeList, tempFPNodeListLength, postfix, postfixLength)
        else:
            for item in tree.headerList[::-1]:
                support = mapSupport[item]
                postfix.append(item)
                betaSupport = postfixSupport
                betaMapSupport = {}
                if betaSupport > support:
                    betaSupport = support
                    temp = [str(i) for i in postfix]
                self.patterns["".join(temp)] = betaSupport
                if postfixLength + 1 < self.maxPatternLength:
                    prefixPaths = []
                    path = tree.mapItemNodes[item]
                    while path is not None:
                        pathCounter = path.counter
                        pathParent = path.parent
                        prefixPath = []
                        while pathParent.itemID != -1:
                            prefixPath.append(path)
                            pathParent = pathParent.parent
                            if pathParent.itemID in betaMapSupport:
                                betaMapSupport[pathParent.itemID] += pathCounter
                            else:
                                betaMapSupport[pathParent.itemID] = pathCounter
                        while pathCounter > 0:
                            prefixPaths.append(prefixPath)
                        path = path.nodeLink
                    betaTree = FPTree()
                    betaTree.addTransaction(prefixPaths, betaMapSupport, self.minSupport)
                    if len(betaTree.root.children) > 0:
                        betaTree.createHeaderList(betaMapSupport)
                        self.fpgrowth(betaTree, betaMapSupport, postfix, postfixLength, betaSupport)

    '''
    if the tree only has one path then this recursion is to the end 
    it will call this method to save all the possible combination of nodes in the tempFPNodeList (it contain 
    all the nodes in the single path) with the nodes in the postfix'''
    def saveAllCombinationOfPrefixPath(self, tempFPNodeList, tempFPNodeListLength, postfix, postfixLength):
        support = 0
        i = 1
        max = 1 << tempFPNodeListLength
        while i < max:
            j = 0
            newPostfixLength = postfixLength
            newpostfix = postfix.copy()
            while j < tempFPNodeListLength:
                set = i & (1 << j)
                if newPostfixLength > self.maxPatternLength:
                    continue
                if set > 0:
                    newpostfix.append(tempFPNodeList[j].itemID)
                    newPostfixLength += 1
                if support == 0:
                    support = tempFPNodeList[j].counter
                else:
                    support = min(support, tempFPNodeList[j].counter)
                j += 1
            i += 1
            temp = [str(i) for i in newpostfix]
            self.patterns["".join(temp)] = support

    '''
    this method scan the database again and reorder the items in each sequence by the support degree of the item
    :return a list of transaction (sequence)
    '''

    def scanDatabaseToGetTheOrderedTransactions(self, path, minSupport, mapSupport):
        transactions = []
        f = open(path)
        lines = f.readlines()
        for line in lines:
            if line.isspace():
                continue
            line = line.strip()
            lineSplited = line.split(" ")
            transaction = {}
            for itemString in lineSplited:
                item = int(itemString)
                if mapSupport[item] > minSupport:
                    transaction[item] = mapSupport[item]
            x = sorted(transaction.items(), key=lambda item: item[1], reverse=True)
            transaction = dict(x)
            transactions.append(list(transaction.keys()))
        return transactions

    '''
    this method will read the file and input the data 
    return a dictionary which key is item value is the frequency of this item
    '''

    def scanDatabaseToDetermineFrequencyOfSingleItems(self, path):
        mapSupport = {}
        f = open(path)
        lines = f.readlines()
        for line in lines:
            if line.isspace():
                continue
            line = line.strip()
            lineSplited = line.split(" ")
            for itemString in lineSplited:
                item = int(itemString)
                if item in mapSupport:
                    mapSupport[item] += 1
                else:
                    mapSupport[item] = 1
            self.transactionCount += 1
        return mapSupport

path = "/Users/renhaoran/PycharmProjects/FPGrowth/FPGrowth/testdata.txt"

a = AlgoFPGrowth()
a.runAlgorrithm(path, 1)


