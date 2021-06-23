"""
Gizem Kurnaz
Web Mining Homework 1

"""

import csv
from collections import defaultdict
from optparse import OptionParser





class Apriori(object):

    def fit(self, filePath):
        transListSet = self.getTransListSet(filePath)
        itemSet = self.getOneItemSet(transListSet)
        itemCountDict = defaultdict(int)
        freqSet = dict()
        self.transLength = len(transListSet)
        self.itemSet = itemSet

        freqOneTermSet = self.getItemsWithMinSupp(transListSet, itemSet, itemCountDict, self.minSupp)

        k = 1
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet
            k += 1
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k)
            currFreqTermSet = self.getItemsWithMinSupp(transListSet, currCandiItemSet, itemCountDict, self.minSupp)

        self.itemCountDict = itemCountDict
        self.freqSet = freqSet
        return itemCountDict, freqSet



    def __init__(self, minSupp, minConf):
        self.minSupp = minSupp
        self.minConf = minConf


    def getTransListSet(self, filePath):
        transListSet = []
        with open(filePath, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                transListSet.append(set(line))
        return transListSet



    def getOneItemSet(self, transListSet):
        itemSet = set()
        for line in transListSet:
            for item in line:
                itemSet.add(frozenset([item]))
        return itemSet


    def getSupport(self, item):
        return self.itemCountDict[item] / self.transLength

    def getJoinedItemSet(self, termSet, k):
        return set([term1.union(term2) for term1 in termSet for term2 in termSet
                    if len(term1.union(term2)) == k])



    def getItemsWithMinSupp(self, transListSet, itemSet, freqSet, minSupp):
        itemSet_ = set()
        localSet_ = defaultdict(int)
        for item in itemSet:
            freqSet[item] += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])

        n = len(transListSet)
        for item, cnt in localSet_.items():
            itemSet_.add(item) if float(cnt) / n >= minSupp else None
        return itemSet_


if __name__ == '__main__':
    optParser = OptionParser()
    optParser.add_option('-f', '--file',
                         dest='filePath',
                         default="Transactions.txt")

    optParser.add_option('-s', '--minSupp',
                         dest='minSupp',
                         type='float',
                         default=0.30)

    optParser.add_option('-c', '--minConf', dest='minConf',
                         type='float',
                         default=0.80)


    (options, args) = optParser.parse_args()

    filePath = options.filePath
    minSupp = options.minSupp
    minConf = options.minConf



    print(""" \n data: {} \n\n mininum support: {} \n mininum confidence: {} \n""".format(filePath, minSupp, minConf))


    objApriori = Apriori(minSupp, minConf)
    itemCountDict, freqSet = objApriori.fit(filePath)
    for key, value in freqSet.items():
        print('\n F{}:'.format(key))
        print("                ")
        for itemset in value:
            print(list(itemset))



