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

##Checks if the file exists
def fileChecker(passedFileName):
    fileName = passedFileName

    while not os.path.exists(fileName): ##https://stackoverflow.com/questions/2259382/pythonic-way-to-check-if-a-file-exists
        fileName = input("\nInvalid file name.\nEnter a valid file name: ")

    return fileName

##Takes two input strings from the user and then stores them into global variables respectively
def inOutName():
    global inputFileName
    global outputFileName

    inputFileName = fileChecker(input("\nPlease enter the name of the text file: "))
    outputFileName = fileChecker(input("\nPlease enter the name of the output file: "))

##inputFileStream takes values from the input text and stores them into a list of lists for later access
def arrayMaker(attributeList):
    inputFileStream = open(inputFileName)
    readFlag = True
    skipFlag = True
    everythingList = []
    temp = []
    i = 0;

    for currentLine in inputFileStream:
        currentSymbolList = currentLine.split()
        for currentSymbol in currentSymbolList:
            if currentSymbol == '!':
                break
            elif currentSymbol == '<':
                skipFlag = True
                readFlag = False
            elif currentSymbol == '>':
                skipFlag = False
                readFlag = True
            elif readFlag and not skipFlag:
                if currentSymbol == '[':
                    readFlag = True
                elif currentSymbol != '[' and currentSymbol != ']':
                    if currentSymbol not in attributeList:
                        attributeList.append(currentSymbol)
                elif currentSymbol == ']':
                    readFlag = False
            elif not readFlag and not skipFlag:
                if i >= len(attributeList):
                    everythingList.append(temp)
                    temp = []
                    i = 0
                temp.append(currentSymbol)
                i += 1
    everythingList.append(temp)
    inputFileStream.close()
    return everythingList

##Sets the type of attribute for any given attribute list and returns an int depending on whether it is a symbol or float/int
def attributeTypeSetter(everythingList,attributeList):
    symbolFlag = 0
    numberFlag = 0
    typeList = []
    floatValue = r'\-*' + '[0-9]*' + r'\.*' + '[0-9]*'

    for i in range(0, len(attributeList)-1):
        condition = 0
        while True:
            att = everythingList[condition][i]
            matchValue = re.fullmatch(floatValue + r'\.\.' + floatValue + r'|[A-Za-z]+', att)

            if matchValue is not None:
                symbolFlag += 1
                typeList.append(1)
                break

            matchValue = re.fullmatch(floatValue, att)

            if matchValue is not None:
                numberFlag += 1
                typeList.append(2)
                break

    return typeList

##Makes a dictionary of attribute value blocks for comparison
def attributeValueBlockMaker(everythingList,attributeIndex,attributeType):
    global cutPoints
    attributeValueDiction = {}

    if attributeType == 2:
        cutPoints = cutPointCalculator(everythingList,attributeIndex)

        for value in cutPoints:
                stringValue = "{}..{}".format(value[0], value[1])
                attributeValueDiction[stringValue] = set()

    for loop, condition in enumerate(everythingList):
        val = condition[attributeIndex]

        if attributeType == 2:
            val = float(val)

            for jump in cutPoints:
                if jump[0] <= val <= jump[1]:
                    attributeValueDiction["{}..{}".format(jump[0], jump[1])].add(loop)

        elif val in attributeValueDiction:
            attributeValueDiction[val].add(loop)

        else:
            attributeValueDiction[val] = {loop}

    return attributeValueDiction

##calculates the cut points i.e. the average of two consecutive ordered values
def cutPointCalculator(everythingList, attributeIndex):
    temp = set()

    for loop, condition in enumerate(everythingList):
        temporary = condition[attributeIndex]
        temp.add(float(temporary))


    temp = sorted(temp, key = float)

    min = temp[0]
    max = temp[-1]
    intervalGaps = []

    for loop in range(0, len(temp)-1):
        mid = round(((float(temp[loop]) + float(temp[loop+1]))/2), 2)
        intervalGaps.extend([[min, mid],[mid,max]])

    return intervalGaps

##Calls MLEM2 and runs the algorithm
def ruleGenerator(everythingList,attributeList,attributeValue,attributeType,conceptList):
    ruleSet = AStarCalculator(everythingList)
    goalSet = goalCalculator(ruleSet, conceptList)

    mlem2Algorithm(attributeValue, attributeType, goalSet, attributeList[-1])

##calculates a dictionary of concepts
def conceptCalculator(everythingList):

    conceptDictionary = {}

    for currentI, element in enumerate(everythingList):
        value = element[-1]

        if value not in conceptDictionary:
            conceptDictionary[value] = {currentI}
        else:
            conceptDictionary[value].add(currentI)

    return conceptDictionary

##calculates a list of AStar i.e. all possible A combinations
def AStarCalculator(everythingList):
    AStar = []

    for loop, condition in enumerate(everythingList):
        flag = False

        for AElement in AStar:
            if equalConditions(condition, everythingList[AElement[0]]):
                AElement.append(loop)
                flag = True
                break

        if not flag:
            AStar.append([loop])

    for loop, AElement in enumerate(AStar):
        AStar[loop] = set(AElement)

    return AStar

##checks whether the passed conditions are equaivalent or not
def equalConditions(condition1, condition2):
    for loop in range(0, len(condition1)-1):
        if condition1[loop] != condition2[loop]:
            return False

    return True

## calculates a dictionary of goals
def goalCalculator(ruleSet, conceptList):
    goalDictionary = {}

    for value, concept in conceptList.items():
        goalDictionary[value] = set()

        for bad in ruleSet:
            if bad.issubset(concept):
                goalDictionary[value].update(bad)

    return goalDictionary

## Implementation of the MLEM2 algorithm
def mlem2Algorithm(attributeValue, attributeType, goalSet, decisionValue):
    ruleSetList = []

    for currentDecision, mainGoal in goalSet.items():
        currentGoal = set(mainGoal)
        goalsLeft = currentGoal
        currentBlock = set()
        ruleDictionary = {}

        while len(goalsLeft):
            biggestIntersection = biggestIntersectionCalculator(attributeValue, attributeType, ruleDictionary, currentGoal)
            if currentBlock:
                currentBlock = currentBlock.intersection(biggestIntersection["matchingBlock"])
            else:
                currentBlock = biggestIntersection["matchingBlock"]

            if biggestIntersection["attributeBlock"] not in ruleDictionary:
                ruleDictionary[biggestIntersection["attributeBlock"]] = [biggestIntersection["valueBlock"]]
            else:
                ruleDictionary[biggestIntersection["attributeBlock"]].append(biggestIntersection["valueBlock"])

            if currentBlock.issubset(mainGoal):
                if len(currentBlock) == 0:
                    goalsLeft = goalsLeft - currentGoal
                    currentGoal = goalsLeft
                else:
                    smallerIntervalMaker(ruleDictionary,attributeValue)
                    conditionDropper(ruleDictionary, attributeValue, mainGoal)
                    matchValue = caseCoverageCalculator(ruleDictionary, attributeValue, mainGoal)
                    goalsLeft = goalsLeft - matchValue
                    currentGoal = goalsLeft
                    ruleSetList.append([ruleDictionary, [decisionValue, currentDecision]])

                ruleDictionary = {}
                currentBlock = set()
            else:
                currentGoal = biggestIntersection["intersectionBlock"]
                print(currentGoal)
                if len(currentGoal) == 0:
                    currentGoal = goalsLeft
                    ruleDictionary = {}

    droppedRuleSet = ruleMaker(ruleSetList)
    printOutput(droppedRuleSet)

##Calculates the value of y and z
def caseCoverageCalculator(ruleDictionary,attributeValue,mainGoal):
    global y
    global z
    matchCase = mainGoal

    for a, v in ruleDictionary.items():
        currentBlock = set(attributeValue[a][v[0]])
        matchCase = matchCase.intersection(currentBlock)
    if len(matchCase):
        c = len(matchCase)
        y.append(c)
    z = y

    return matchCase

##Calculates the intersection agaist all possible subsets
def biggestIntersectionCalculator(attributeValue, attributeType, ruleDictionary, currentGoal):
    matchDictionary = {"intersectionBlock": set(), "matchingBlock": set(), "valueBlock": None, "attributeBlock": None}

    for loop, (attribute, attributeValueSet) in enumerate(attributeValue.items()):
        for value, valueBlock in attributeValueSet.items():
            if (attributeType[loop] == 1 and attribute not in ruleDictionary) or (attributeType[loop] == 2 and (attribute not in ruleDictionary or value not in ruleDictionary[attribute])):
                if len(valueBlock.intersection(currentGoal)) == len(matchDictionary["intersectionBlock"]) and len(valueBlock) < len(matchDictionary["matchingBlock"]) or len(valueBlock.intersection(currentGoal)) > len(matchDictionary["intersectionBlock"]):
                    matchDictionary["intersectionBlock"] = valueBlock.intersection(currentGoal)
                    matchDictionary["matchingBlock"] = valueBlock
                    matchDictionary["valueBlock"] = value
                    matchDictionary["attributeBlock"] = attribute
    return matchDictionary

##Makes a smaller interval
def smallerIntervalMaker(ruleDictionary, attributeValue):
    for keyValue, val in ruleDictionary.items():
        if len(val) > 1:
            minimum = None
            maxmimum = None
            intervals = set()

            for gap in ruleDictionary[keyValue]:
                temporary = attributeValue[keyValue][gap]
                edgeOfInterval = floatIntervalGenerator(gap)

                if minimum == None:
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

##Generates a float for the interval value when its not a symbol
def floatIntervalGenerator(gap):
    edgeOfGap = gap.split("..")
    interval = []

    for loop in edgeOfGap:
        interval.append(float(loop))

    return interval

##Checks for redundant or weaker conditions and drops them
def conditionDropper(ruleDictionary, attributeValue, mainGoal):
    for currentAttribute in list(ruleDictionary):
        temporary = set()

        for tempAttribute, tempValue in ruleDictionary.items():
            currentBlock = attributeValue[tempAttribute][tempValue[0]]

            if tempValue != ruleDictionary[currentAttribute]:
                if temporary:
                    temporary = temporary.intersection(currentBlock)
                else:
                    temporary = currentBlock

        if len(temporary) and temporary.issubset(mainGoal):
            ruleDictionary.pop(currentAttribute, None)

##Makes the string for outputting rules
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

##prints to the output file passed as a name
def printOutput(droppedRuleSet):
    print('\n')
    outputFileStream = open(outputFileName, 'w')
    loop = 0

    for currentRule in droppedRuleSet:
        outputFileStream.write("{}, {}, {} \n".format(x[loop], y[loop], z[loop]))
        outputFileStream.write(currentRule + '\n')
        loop += 1

##Calls all the names
def main():
    inOutName()

    attributeList = []
    everythingList = arrayMaker(attributeList)
    conceptList = conceptCalculator(everythingList)
    attributeType = attributeTypeSetter(everythingList, attributeList)
    attributeValueDictionary = {}

    for loop, attribute in enumerate(attributeType):
        currentAttribute = attributeList[loop]
        attributeValueDictionary[currentAttribute] = attributeValueBlockMaker(everythingList, loop, attribute)

    ruleGenerator(everythingList,attributeList,attributeValueDictionary,attributeType,conceptList)

    print ("The rules have been calculated and stored in the appropriate output file")

main()
