#Apurva Rai
#EECS 690 Project
import os

inputFromFile = None
outputToFile = None
inputFileName = ''
outputFileName = ''
everythingDictionary = {}
sortedDictionary = {}

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

def integerOrFloat(passedString): ##https://stackoverflow.com/questions/34425583/how-to-check-if-string-is-int-or-float-in-python-2-7
    try:
        float(passedString)

        if passedString.count('.') == 0:
            return 0
        else:
            return 1

    except ValueError:
        return -1

def arrayMaker():
    global everythingDictionary

    with open(inputFileName,'r') as inputFromFile: ##https://stackoverflow.com/questions/1369526/what-is-the-python-keyword-with-used-for
        inputFromFile.readline()
        tempArray = inputFromFile.readline().split()
        attributeDecisionArray = tempArray[1:(len(tempArray)-1)]

        for element in attributeDecisionArray:
            everythingDictionary[element] = []

        for line in inputFromFile:
            tempArray = line.split()

            if(line[0] == '!'):
                continue

            for attribute in attributeDecisionArray:

                if(integerOrFloat(tempArray[attributeDecisionArray.index(attribute)]) == 0):
                    everythingDictionary[attribute].append(int(tempArray[attributeDecisionArray.index(attribute)]))
                elif(integerOrFloat(tempArray[attributeDecisionArray.index(attribute)]) == 1):
                    everythingDictionary[attribute].append(float(tempArray[attributeDecisionArray.index(attribute)]))
                else:
                    everythingDictionary[attribute].append(tempArray[attributeDecisionArray.index(attribute)])

    print ('\n')
    print (everythingDictionary)
    #print (len(everythingDictionary.keys()))


def cutPointMaker():
    global sortedDictionary

    sortedDictionary = {}
    sortedRanges = []
    i = 0;
    for attribute in everythingDictionary:
        if(i == len(everythingDictionary.keys())-1):
            sortedDictionary[attribute] = everythingDictionary[attribute]
            break

        sortedDictionary[attribute] = sorted(everythingDictionary[attribute])
        i+=1;

        tempArray = []

        for elem in sortedDictionary[attribute]:
            if elem not in tempArray:
                tempArray.append(elem)

        sortedDictionary[attribute] = tempArray

        min = sortedDictionary[attribute][0]
        max = sortedDictionary[attribute][len(sortedDictionary[attribute])-1]
        for num in range(0,len(sortedDictionary[attribute])):
            if num == 0:
                sortedRanges.append([min,(min+sortedDictionary[attribute][1])/2])
            elif num == len(sortedDictionary[attribute])-1:
                sortedRanges.append([(sortedDictionary[attribute][len(sortedDictionary[attribute])-2] + max)/2,max])
            else:
                sortedRanges.append([(sortedDictionary[attribute][num]+sortedDictionary[attribute][num-1])/2,(sortedDictionary[attribute][num+1]+sortedDictionary[attribute][num])/2])


        sortedDictionary[attribute] = sortedRanges

        sortedRanges = []

    print ('\n')
    print (sortedDictionary)

def conceptCalculator():
    conceptDictionary = {}

    for i, element in enumerate(everythingDictionary):
        temp = element[-1]

        if temp not in conceptDictionary:
            conceptDictionary[temp] = {i}
        else:
            conceptDictionary[temp].add(i)

    print ('\n')
    print (conceptDictionary)
    return conceptDictionary

def attributeValueBlockMaker():
    attributeValueDictionary = {}

    if(integerOrFloat != -1):
        pass

def equalCase(case1,case2):
    for i in range(0,len(case1)-1):
        if(case1[i] != case2[i]):
            return False

    return True        

def calculateAStar():
    AStar = []

    for i, element in enumerate(everythingDictionary):
        flag = False

        for aElement in AStar:
            if equalCase(element,everythingDictionary[aElement][0]):
                aElement.append(i)
                flag = True
                break

        if not flag:
            AStar.append([i])

    for i, aElement in enumerate(AStar):
        AStar[i] = set(aElement)

    print('\n')
    print(AStar)




def main():
    inOutName()
    arrayMaker()
    cutPointMaker()
    conceptCalculator()
    calculateAStar()

main()
