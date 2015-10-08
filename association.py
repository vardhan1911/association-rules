#! /usr/bin/python

import sys
from collections import deque

def readData():
  data = dict()
  idx = 0
  with open('data.2') as f:
    content = f.readlines()
    for line in content:
      idx+=1
      line = line.strip()
      items = line.split(" ")
      docId = idx
      data[docId] = items
  return data


def buildInvertedIndex(data):
  # Building Whitelist of items
  itemsWhitelist = set()
  
  for docId, items in data.iteritems():
    for item in items:
      itemsWhitelist.add(item)

  # Build Inverted Index {val} -> (List of doc ids)
  invertedIndex = dict()
  for item in itemsWhitelist:
    itemDocIds = set()
    for docId, items in data.iteritems():
      if item in items:
        itemDocIds.add(docId)
    invertedIndex[item] = itemDocIds

  return invertedIndex


def isValidNewKey(originalChain, newKey):
  origChainList = originalChain.split("-")
  if newKey in originalChain:
    return False
  return True


def buildKey(originalChain, newKey):
  origChainList = originalChain.split("-")
  origChainList.append(newKey)
  origChainList = sorted(origChainList)
  return "-".join(origChainList)


def getJointDocIds(originalChain, newKey, invertedIndex):
  originalChainDocs = invertedIndex[originalChain]
  newKeyDocs = invertedIndex[newKey]
  return originalChainDocs.intersection(newKeyDocs)


def getConfidence(originalChain, newKey, invertedIndex):
  commonNumDocs = len(getJointDocIds(originalChain, newKey, invertedIndex))
  origChainNumDocs = len(invertedIndex[originalChain])
  confidence = float(commonNumDocs)/float(origChainNumDocs)
  return confidence


def getAssociationInterest(originalChain, newKey, invertedIndex, confidence, totalNumDocs):
  c = getConfidence(originalChain, newKey, invertedIndex)
  if c < confidence:
    return None

  # Freq(2)/TotalDocs
  newKeyNumDocs = len(invertedIndex[newKey])
  freqConfidence = float(newKeyNumDocs)/float(totalNumDocs)

  # Interest = Freq(1,2)/Freq(1) - Freq(2)/TotalDocs
  return c - freqConfidence


def buildAssociationRules(invertedIndex, totalNumDocs):
  # Build initial Queue
  print totalNumDocs
  docIds = invertedIndex.keys()
  queue = deque([])
  support = 0.05
  confidence = 0.5
  for docId in docIds:
    # Check for 'support' of docIds
    if len(invertedIndex[docId]) > support * totalNumDocs:
      queue.append(docId)

  while len(queue) != 0:
    originalChain = queue.popleft()
    for docId in docIds:

      # Check if new Doc Id is valid
      if isValidNewKey(originalChain, docId) == False:
        continue

      interest = getAssociationInterest(originalChain, docId, invertedIndex, confidence, totalNumDocs)
      if interest is not None and interest > 0.5:
        print originalChain, docId, interest
        commonDocs = getJointDocIds(originalChain, docId, invertedIndex)
        newChain = buildKey(originalChain, docId)
        invertedIndex[newChain] = commonDocs
        queue.append(newChain)


def main(argv=None):
  if argv is None:
    argv = sys.argv

  data = readData()
  totalNumDocs = len(data)
  print "Done reading data..."
  
  invertedIndex = buildInvertedIndex(data)
  print "Done building inverted index..."

  buildAssociationRules(invertedIndex, totalNumDocs)  


if __name__ == '__main__':
  main()