
from flask import Flask,render_template, request
import random
import re
numberSpace = "abcdefghijklmnopqrstuvwxyz"

def removeMessageCharacters(message):
    message = re.sub("[^a-zA-Z]+", "", message)
    return message.lower()

def convertMessageFromTextFile(filename):
    file = open(filename,encoding="utf8") # r means read and w means write
    message = file.read()
    message = re.sub("[^a-zA-Z]+", "", message)
    return message.lower()

def encrypt(message, key=None):
    if key is None:
        numberSpaceList = list(numberSpace)
        random.shuffle(numberSpaceList)
        key = "".join(numberSpaceList)
    newCipherList = []
    try:
        for char in message:
            newCipherList.append(key[numberSpace.index(char)]) # Appending the ciphered text into the new list
        return ["".join(newCipherList), key]
    except:
        return ["Key Error: -PLease make sure you have entered all 26 letters in key",key]


def decrypt(cipher, key=None):
    if key is not None:
        newDecryptedList = []
        for char in cipher:
            newDecryptedList.append(numberSpace[key.index(char)])
        return "".join(newDecryptedList)


#-------------Function for mapping into the web page is written below----
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/encryptText', methods=['POST'])
def encryptText():
    if request.method =="POST":
        message= request.form["plainText_input"]
        messageFormated = removeMessageCharacters(message)
        key = request.form["key_input"]
        key = key.lower()
        encryptionList = encrypt(messageFormated, key)
        print(encryptionList[0], encryptionList[1])
        return render_template('encryption.html', encryptedMessage=encryptionList[0],messageFormated=messageFormated, key = encryptionList[1] )

if (__name__ =="__main__"):
    app.run(debug=True)
