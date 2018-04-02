#Decryption
from flask import Flask,render_template, request
from constants import *
import re

##-----------get cipher text from  from txtfile----------------------##
def getCipherText(filename):
    file = open(filename,'r') # r means read and w means write
    cipherText = file.read()
    cipherText = re.sub("[^a-zA-Z]+", "", cipherText)
    return cipherText.lower()


##---------- To get the initial putative key by analyzing the frequency in cipher text----------##
def getFirstKey(cipherText):
    frequencyOfCipherArray = [0 for x in range(rowLen)]
    newKey = [0 for x in range(rowLen)]
    englishFrequencyList = list(englishFrequency)
    for i in range(0,26):
        frequencyOfCipherArray[i]=cipherText.count(numberSpaceList[i])# pushing the count of  each alphabets into an array
    print("The initial frequecy of ciper text letters from a -z is shown below : " )
    print(frequencyOfCipherArray)
    #print("\n\rThe largest frequencies are replaced by -1 and its position is added with the most frequent letters in english language: ")
    for j in range(0, rowLen):
        flag = 0
        for k in range (0, rowLen):
            if frequencyOfCipherArray[flag] <= frequencyOfCipherArray[k]:
                flag = k
        chartemp = englishFrequencyList[j]
        newKey[numberSpace.index(chartemp)] = numberSpace[flag]
        frequencyOfCipherArray[flag]= -1# replace the max frequency value with -1 so that the next biggest value will be taken
        #print(frequencyOfCipherArray)# to see its getting replaced after each step
    return "".join(newKey)


##----------- converts the cipher text into initial plain text with the key generated from above function-------##
def getInitialPlainText(message, key=None):
    newPlainList = []
    for char in message:
        newPlainList.append(key[numberSpace.index(char)]) # Appending the ciphered text into the new list
    return "".join(newPlainList)             #Returning the initial plain text corresponding to the cipher text


#---------This below function returns the diagram frequency matrix numbers for any text string as input----##.
def getDiagramFrequency(plainText):
    diagramMatrix = [[0 for x in range(rowLen)] for y in range(colLen)]  #matrix for storing the diagram of particular language
    diagramFrequencyMatrix = [[0 for x in range(rowLen)] for y in range(colLen)]
    planTextLength = len(plainText)
    value = planTextLength/ float(SenLength)
    for i in range(0,rowLen):
        for j in range(0,colLen):
            a=numberSpaceList[i]
            b=numberSpaceList[j]
            newArray=[a,b] #geting the values aa,ab ac etc
            diagramMatrix[i][j]= "".join(newArray) # initializing the initial diagram frequency matrix
            a = plainText.count(diagramMatrix[i][j])
            diagramFrequencyMatrix[i][j] = a
    for i in range(0,rowLen):
        for j in range(0,colLen):
	        diagramFrequencyMatrix[i][j]=round(diagramFrequencyMatrix[i][j]/ float(value))
    return diagramFrequencyMatrix

##--------The below function returns the score computed with a standard english diagram frequency matrix---------##
def getScore(matrix):
    score = 0
    for  i in range(0,rowLen):
        for  j in range(0,colLen):
            score+= abs(matrix[i][j]-englishDiagramMatrix[i][j])
    return score

##------------The below function is to swap the given rows and column of a given matrix----------------------##
def swapRowColOfMatrix(matrix, pos1, pos2):
    tempRow = 0
    tempCol= 0
    matrixTemp =  [[0 for x in range(rowLen)] for y in range(colLen)]
    matrixTemp= copyMatrixValues(matrix)
    #swapping rows  first
    for j in range(0, colLen):
        tempRow = matrixTemp[pos1][j]
        matrixTemp[pos1][j]=matrixTemp[pos2][j]
        matrixTemp[pos2][j]=tempRow
    #swapping the column
    for i in range(0, rowLen):
        tempCol = matrixTemp[i][pos1]
        matrixTemp[i][pos1]=matrixTemp[i][pos2]
        matrixTemp[i][pos2]=tempCol
    return matrixTemp

##------------------The below function is to swap the characters in key position-------------------##
def swapKeyCharacters(key, pos1, pos2):
    keyList = list(key)
    temp = keyList[pos1]
    keyList[pos1]=keyList[pos2]
    keyList[pos2] = temp
    return "".join(keyList)
#-----------------The below function is to copy the matrix values into a new matrix
def copyMatrixValues(inputMatrix):
    matrixCopy= [[0 for x in range(rowLen)] for y in range(colLen)]
    for i in range(0,rowLen):
        for j in range(0,colLen):
            matrixCopy[i][j] = inputMatrix[i][j]
    return matrixCopy

##----------The below fuction is to compute the iterations and get the final key for the plain text----------------##
def getFinalKey(D, key):
    score = getScore(D)
    for k in range(0, 5):
        for i in range(0, 26):
            for j in range(0, 26-i):
                D2= copyMatrixValues(D)
                D2=swapRowColOfMatrix(D, j, j+i)
                scoreTemp = getScore(D2)
                if(scoreTemp <= score):
                    D=copyMatrixValues(D2)
                    key = swapKeyCharacters(key, j, j+i)
                    score = scoreTemp
    return key

#-------the below function is used to decrypt the  ciper text by giving the  key and cipher as inputs
def decrypt(cipher, key=None):
    if key is not None:
        newDecryptedList = []
        for char in cipher:
            newDecryptedList.append(numberSpace[key.index(char)])
        return "".join(newDecryptedList)

#######---------------------------------MAIN FUNCTION(Can be used if we are getting the input cipher text from a text file)---------------------------######################3
def main():
    cipherText = getCipherText("cipher3.txt")
    #cipherText = getCipherText("cipher2.txt")
    initialKey = getFirstKey(cipherText)


    print("\n\rThe first Key generated from analyzing the cipher text : ")
    print(initialKey)

    print("\n\r The cipher text is")
    print(cipherText)

    print("\n\rThe initial Plan Text : ")
    initialPlainText = decrypt(cipherText, initialKey)
    print(initialPlainText)

    print("\n\rThe Diagram Frequency matrix of initial plain text : ")
    D=getDiagramFrequency(initialPlainText)
    print (D)
    finalKey = getFinalKey(D, initialKey)
    print("The final key after crypto analysis is :" +finalKey)
    print("The final decrypted message is  :   ")
    print(decrypt(cipherText, finalKey))


#----Main Function(To be used if the input is taken from a webpage)--------##

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/decryptText', methods=['POST'])
def decryptText():
    if request.method =="POST":
        cipherText= request.form["cipherText_input"]
        cipherText = re.sub("[^a-zA-Z]+", "", cipherText)
        initialKey = getFirstKey(cipherText)
        print("\n\rThe first Key generated from analyzing the cipher text : ")
        print(initialKey)
        print("\n\r The cipher text is")
        print(cipherText)
        print("\n\rThe initial Plan Text : ")
        initialPlainText = decrypt(cipherText, initialKey)
        print(initialPlainText)
        print("\n\rThe Diagram Frequency matrix of initial plain text : ")
        D=getDiagramFrequency(initialPlainText)
        print (D)
        finalKey = getFinalKey(D, initialKey)
        print("The final key after crypto analysis is :" +finalKey)
        print("The final decrypted message is  :   ")
        finalDecryptedText = decrypt(cipherText, finalKey)
        print(finalDecryptedText)
        return render_template('decryption.html', finalDecryptedText=finalDecryptedText,finalKey=finalKey,cipherText= cipherText )

if (__name__ =="__main__"):
    app.debug=True
    app.run(port=5001)
