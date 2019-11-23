#Apurva Rai
#EECS 690 Project Fall 2019

import time
import re
import os

inputFileName = ''
outputFileName = ''
cutPoints = None
x = []
y = []
z = []

def fileChecker(passedFileName):
    fileName = passedFileName

    while not os.path.exists(fileName): ##https://stackoverflow.com/questions/2259382/pythonic-way-to-check-if-a-file-exists
        fileName = input("\nInvalid file name.\nEnter a valid file name: ")

    return fileName

def inOutName():
    global inputFileName
    global outputFileName

    inputFileName = fileChecker(input("\nPlease enter the name of the text file: "))
    outputFileName = fileChecker(input("\nPlease enter the name of the output file: "))

def arrayMaker(attributeList):
    inputFileStream = open(inputFileName)
    readFlag = True
    skipFlag = True
    everythingList = []
    temp = []
    i = 0;

    inputFileStream.readline()
    temp = inputFileStream.readline().split()
    attributeList = temp[1:len(temp)-1]
    everythingList.append(attributeList)
    temp = inputFileStream.readline().split()

    for line in inputFileStream:
        split = line.split()
        for element in split:
            if element == '!':
                break
            else:
                if len(attributeList) <= i:
                    everythingList.append(temp)
                    temp = []
                    i = 0
                temp.append(element)
                i += 1

    everythingList.append(temp)
    inputFileStream.close()

    temp = everythingList[1]
    temp2 = temp[len(temp)//2:]
    temp = temp[:len(temp)//2]
    everythingList[1] = temp
    everythingList.insert(2,temp2)

    return everythingList

def attributeTypeSetter(everythingList,attributeList):
    symbolFlag = 0
    numberFlag = 0
    typeList = []
    floatValue = r'\-*' + '[0-9]*' + r'\.*' + '[0-9]*'

    for i in range(0, len(attributeList)-1):
        while True:
            attributeList = everythingList[condition][i]
            matchValue = re.fullmatch(floatingValue + r'\.\.' + floatingValue + r'|[A-Za-z]+', attributeList)

            if matchValue is not None:
                symbolFlag += 1
                typeList.append(1)
                break

            matchValue = re.fullmatch(floatValue, attributeList)

            if matchValue is not None:
                numberFlag += 1
                typeList.append(2)
                break

    return typeList

def attributeValueBlockMaker(everythingList,attributeIndex,attributeType):
    global cutPoints
    attributeValueDictionary = {}

    if attributeType == 2:
        cutPoints = cutPointCalculator(everythingList,attributeIndex)

        for value in cutPoints:
                stringValue = "{}..{}".format(value[0], value[1])
                attributeValueDictionary[stringValue] = set()

    for loop, conditon in enumerate(everythingList):
        val = condition[attributeIndex]

        if attributeType == 2:
            val = float(value)

            for jump in cutPoints:
                if jump[0] <= val <= jump[1]:
                    attributeValueDictionary["{}..{}".format(jump[0], jump[1])].add(loop)

        elif val in attributeValueDictionary:
            attributeValueDictionary[val].add(loop)

        else:
            attributeValueDictionary[val] = {loop}

    return attributeValueDictionary

def cutPointCalculator(everythingList, attributeIndex):
    temp = set()

    for loop, condition in enumerate(everythingList):
        temporary = condition[attributeIndex]
        temp.add(float(temporary))

    temp = sorted(temp, key = float)

    min = temp[0]
    max = temp[-1]
    intervalGap = []

    for loop in range(0, len(temp)-1):
        mid = round(((float(temp[loop]) + float(temp[i+1]))/2), 2)
        intervalGaps.extend([[min, mid],[mid,max]])

    return intervalGaps

def ruleGenerator(everythingList,attributeList,attributeValue,attributeType,conceptList):
    ruleSet = AStarCalculator(everythingList)
    goalSet = goalCalculator(ruleSet, conceptList)

    mlem2Algorithm(attributeValue, attributeType, goalSet, attributeList[-1])

def conceptCalculator(everythingList):

    conceptDictionary = {}

    for currentI, element in enumerate(everythingList):
        value = element[-1]

        if value not in conceptDictionary:
            conceptDictionary[value] = {currentI}
        else:
            conceptDictionary[value].add(currentI)

    return conceptDictionary

def AStarCalculator(everythingList):
    AStar = []

    for loop, comndition in enumerate():
        flag = False

        for AElement in AStar:
            if equalConditions(case, everythingList[aElement[0]]):
                AElement.append(loop)
                flag = True
                break

        if not flag:
            AStar.append([loop])

    for loop, AElement in enumerate(AStar):
        AStar[loop] = set(AElement)

    return AStar

def equal(condtion1, conditon2):
    for loop in range(0, len(condition1)-1):
        if condtion1[loop] != conditon2[loop]:
            return False

    return True

def goalCalculator(ruleSet, conceptList):
    goalDictionary = {}

    for value, concept in conceptList.items():
        goalDictionary[value] = set()

        for bad in ruleSet:
            if bad.issubset(concept):
                goalDictionary[value].update(bad)

    return goalDictionary

def mlem2Algorithm(attributeValue, attributeType, goalSet, decisionValue):
    ruleSetList = []

    for currentDecision, mainGoal in goalSet.items():
        currentGoal = set(mainGoal)
        goalsLeft = currentGoal
        currentBlock = set()
        ruleDictionary = {}

        while len(goalsLeft):
            biggestIntersection = biggestIntersectionCalculator(attributeValue, attribtueType, ruleDictionary, currentGoal)

            if currentBlock:
                currentBlock = currentBlock.intersection(biggestIntersection["matchingBlock"])
            else:
                currentBlock = biggestIntersection["matchingBlock"]

            if biggestIntersection["attributeBlock"] not in ruleDictionary:
                ruleDictionary[biggestIntersection["attributeBlock"]] = [biggestIntersection["valueBlock"]]
            else:
                ruleDictionary[biggestIntersection["attributeBlock"]].append(biggestIntersection["valueBlock"])

            if currentBlock.issubset(goalSet):
                if len(currentBlock) == 0:
                    goalsLeft = goalsLeft - currentGoal
                    currentGoal = goalsLeft
                else:
                    smallerIntervalMaker(ruleDictionary,attributeValue)
                    conditionDropper(ruleDictionary, attributeValue, mainGoal)
                    matchValue = caseCoverageCalculator(ruleDictionary, attributeValue, mainGoal)
                    goalsLeft = goalsLeft - currentGoal
                    currentGoal = goalsLeft
                    ruleSetList.append([ruleDictionary, [decisionValue, currentDecision]])

                ruleDictionary = {}
                currentBlock = set()
            else:
                currentGoal = biggestIntersection["intersectionBlock"]

                if len(currentGoal) == 0
                    currentGoal = goalsLeft
                    ruleDictionary = {}

    droppedRuleSet = ruleMaker(ruleSetList)

    printFromRuleSet(droppedRuleSet)

def biggestIntersectionCalculator(attributeValue, attributeType, ruleDictionary, currentGoal):
    matchDictionary = {"intersectionBlock": set(), "matchingBlock": set(), "attributeBlock": None, "valueBlock": None}

    for loop, (attributeValue, attributeSet) in enumerate(attributeValue.items()):
        for val, value in attributeSet.items():
            if attributeType[loop] == 1 and attributeValue not in ruleDictionary or attributeType[loop] == 2 and (attributeValue not in ruleDictionary or val not in ruleDictionary[attributeValue]):
                if len(value.intersection(currentGoal)) == len(matchDictionary["intersectionBlock"]) and len(value) < len(matchDictionary["matchingBlock"]) or len(value.intersection(currentGoal)) > len(matchDictionary["intersectionBlock"]):
                    matchDictionary["intersectionBlock"] = value.intersection(goal)
                    matchDictionary["matchingBlock"] = value
                    matchDictionary["valueBlock"] = val
                    matchDictionary["attributeBlock"] = attributeValue

    return matchDictionary

def smallerIntervalMaker(ruleDictionary, attributeValue):
    for keyValue, val in ruleDictionary.items():
        if len(val) > 1:
            minimum = None
            maxmimum = None
            intervals = set()

            for gap in ruleDictionary[keyValue]:
                temporary = attributeValue[keyValue][gap]
                edgeOfInterval = floatIntervalGenerator(gap)

                if minimum = None:
                    minimum, maximum = edgeOfInterval
                    intervals = temporary
                else:
                    if edgeOfInterval[0] > minimum:
                        minimum = edgeOfInterval[0]
                    if edgeOfInterval[1] < maximum:
                        maximum = edgeOfInterval[1]
                    intervals = intervals.intersection(temporary)

            newInterval = "{}..{}".format(minimum, maximum)

            if newInterval not in attributeValue[keyValue]:
                attributeValue[keyValue][newInterval] = intervals
            ruleDictionary[keyValue] = [newInterval]

def floatIntervalGenerator(gap):
    edgeofGap = gap.split("..")
    interval = []

    for loop in edgeOfGap:
        interval.append(float(loop))

    return interval

def conditionDropper(ruleDictionary, attributeValue, mainGoal):
    for currentAttribute in list(ruleDictionary):
        temporary = set()

        for tempAttribute, tempValue in ruleDictionary.items()
            currentBlock = attributeValue[tempAttribute][tempValue[0]]

            if tempValue != ruleDictionary[currentAttribute]:
                if temporary:
                    temporary = temporary.intersection(currentBlock)
                else:
                    temporary = currentBlock

        if len(temporary) and temporary.issubset(mainGoal):
            ruleDictionary.pop(currentAttribute, None)

def ruleMaker(ruleSetList):
    global x
    droppedRuleSet = []
    totalConditions = 1

    for currentRule in ruleSetList:
        droppedRule = ""

        for loop, (currentAttribute, val) in enumerate(currentRule[0].items()):
            if loop != 0:
                totalConditions += 1
                droppedRule += " & "

            droppedRule += "({}, {})".format(currentAttribute, val[0])

        droppedRule += " --> ({}, {})".format(currentRule[1][0], currentRule[1][1])
        droppedRuleSet.append(droppedRule)
        x.append(totalConditions)
        totalConditions = 1

    return droppedRuleSet

def printOutput(droppedRuleSet):
    print('\n')
    outputFileStream = open(outputFileName, 'w')
    loop = 0

    for currentRule in droppedRule:
        outputFileStream.write("{}, {}, {} \n".format(x[loop], y[loop], z[loop]))
        outputFileStream.write(currentRule + '\n')
        loop += 1

def main():
    inOutName()

    attributeList = []
    everythingList = arrayMaker(attributeList)
    conceptList = conceptCalculator(everythingList)
    attributeType = attributeTypeSetter(everythingList, attributeList)
    attributeValueDictionary = {}

    for loop, attribute in enumerate(attributeType):
        currentAttribute = attributeList[loop]
        attributeValueDictionary[currentAttribute] = attributeValueBlockMaker(everthing, loop, attributeType)

    ruleGenerator(everythingList,attributeList,attributeValue,attributeType,conceptList)   
        

main()

