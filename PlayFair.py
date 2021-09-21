import string
import re

def GetInputString():
    inputString = input()
    inputString = inputString.upper()
    inputString = inputString.replace(" ", "")

    return inputString

def ShiftChars(stopAtIndex, listToShift):#az index, amitől csúsztatni kell (visszafele pedig AMEDDIG kell)

    for curIndex in reversed(range(len(listToShift))):#visszafele végigmegyünk az elemeken
        if (curIndex == stopAtIndex):#stopAtIndex mőgé nem kell menni
            listToShift[curIndex] = listToShift[curIndex][0] + 'X'#lecseréljük X re a dupla sor 2. elemét
            break

        if (len(listToShift[len(listToShift) - 1]) == 2):#ha nem üres (egy hosszúságú) az utolsó elem, új sorba csúszik a betű
            listToShift.append(listToShift[curIndex][1])

        listToShift[curIndex] = listToShift[curIndex - 1][1] + listToShift[curIndex][0]#sor második eleme, a sor első eleme lesz #sor első eleme az előző sor második eleme lesz

    return listToShift

def GetPlainText():
    inputString = GetInputString().replace("J", "I")#I és J egyként van kezelve

    inputString = re.findall('..?', inputString)#minden 2. karakternél szétbontja

    for stringIndex in range(len(inputString)):#dupla karakterek keresése
        if (len(inputString[stringIndex]) == 2):
            if (inputString[stringIndex][0] == inputString[stringIndex][1]):
                inputString = ShiftChars(stringIndex, inputString)

    if (len(inputString[len(inputString) - 1]) % 2 != 0):#Ha páratlan a hossza, akkor nincs párja az utolsónak ézért X lesz
        inputString[len(inputString) - 1] += 'X'

    text = ""

    for index in range(len(inputString)):
        text += inputString[index][0] + inputString[index][1]

    return text

def CheckKeyWord(keyWord):
    for aIndex, aChar in enumerate(keyWord):
        for bIndex, bChar in enumerate(keyWord):
            if (aIndex != bIndex):
                if (aChar == bChar):
                    return False
    return True

def GetKeyWord():

    while True:
        print("Kulcsszó: ")
        keyWord = GetInputString()
        keyWord = keyWord.replace("J", "I")#J és I egyként van kezelve
        
        if CheckKeyWord(keyWord):
            break

        print("Nem szerepelhet két ugyanolyan betű a szóban !")
    
    return keyWord

def SetUpTable(keyWord):
    alphabet = list()

    for char in keyWord:
        if (char != 'J'):
            alphabet.append(char)#ha nem J akkor, hozzáadjuk az stringhez, amit kesőbb kiegészítünk az abc többi betüjével
        else:
            alphabet.append('I')#ha J akkor I re változtatjuk, mivel ez a betü nem fog szerepelni a táblánkban 

    for asciiChar in string.ascii_uppercase:
        if ((asciiChar not in alphabet) & (asciiChar != 'J')):#feltöltjük az abc maradék betüivel, ha még nem szerepel a stringünkben
            alphabet.append(asciiChar)

    table = [["", "", "", "", ""], 
    ["", "", "", "", ""], 
    ["", "", "", "", ""], 
    ["", "", "", "", ""], 
    ["", "", "", "", ""]]

    row = 0
    column = 0

    for index in range(len(alphabet)):#feltöltjük a mátrixot
        table[column][row] = alphabet[index]
        row += 1

        if (row == 5):#új sor kezdése
            row = 0
            column += 1

    return table

def FindIndex(element, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == element:
                return (i, j)

def SlideRowRight(firstIndex, secondIndex, text, table):

    if (firstIndex[1] + 1 <= 4):
        text += table[firstIndex[0]][firstIndex[1] + 1]
    else:
        text += table[firstIndex[0]][0]

    if (secondIndex[1] + 1 <= 4):
        text += table[secondIndex[0]][secondIndex[1] + 1]
    else:
        text += table[secondIndex[0]][0]

    return text

def SlideColumnDown(firstIndex, secondIndex, text, table):

    if (firstIndex[0] + 1 <= 4):#ha nem megy túl a tömb méretén, a következő elem értékét veszi fel
        text += table[firstIndex[0] + 1][firstIndex[1]]
    else:
        text += table[0][firstIndex[1]]#ha túlmegy az oszlop első elemét veszi fel

    if (secondIndex[0] + 1 <= 4):
        text += table[secondIndex[0] + 1][secondIndex[1]]
    else:
        text += table[0][secondIndex[1]]

    return text

def SlideRowLeft(firstIndex, secondIndex, text, table):

    if (firstIndex[1] - 1 >= 0):
        text += table[firstIndex[0]][firstIndex[1] - 1]
    else:
        text += table[firstIndex[0]][4]

    if (secondIndex[1] - 1 >= 0):
        text += table[secondIndex[0]][secondIndex[1] - 1]
    else:
        text += table[secondIndex[0]][4]

    return text

def SlideColumnUp(firstIndex, secondIndex, text, table):

    if (firstIndex[0] - 1 >= 0):
        text += table[firstIndex[0] - 1][firstIndex[1]]
    else:
        text += table[4][firstIndex[1]]

    if (secondIndex[0] - 1 >= 0):
        text += table[secondIndex[0] - 1][secondIndex[1]]
    else:
        text += table[4][secondIndex[1]]

    return text

def Encrypt(table, textToEncrypt):
    encryptedString = ""

    for textCharIndex, textChar in enumerate(textToEncrypt):
        if (textCharIndex % 2 != 0):
            continue

        firstCharIndex = FindIndex(textChar, table)
        secondCharIndex = FindIndex(textToEncrypt[textCharIndex + 1], table)

        if (firstCharIndex[1] == secondCharIndex[1]):#egy oszlopban vannak
            encryptedString = SlideColumnDown(firstCharIndex, secondCharIndex, encryptedString, table)

        elif (firstCharIndex[0] == secondCharIndex[0]):#egy sorban vannak
            encryptedString = SlideRowRight(firstCharIndex, secondCharIndex, encryptedString, table)
                

        else:#blockot alkotnak
            encryptedString += table[firstCharIndex[0]][secondCharIndex[1]]#a sor indexük felcserélődik
            encryptedString += table[secondCharIndex[0]][firstCharIndex[1]]

    return encryptedString

def Decrypt(table, plainText):
    decryptedString = ""

    for textCharIndex, textChar in enumerate(plainText):
        if (textCharIndex % 2 != 0):
            continue

        firstCharIndex = FindIndex(textChar, table)
        secondCharIndex = FindIndex(plainText[textCharIndex + 1], table)

        if (firstCharIndex[1] == secondCharIndex[1]):#egy oszlopban állnak
            decryptedString = SlideColumnUp(firstCharIndex, secondCharIndex, decryptedString, table)

        elif (firstCharIndex[0] == secondCharIndex[0]):#egy sorban állnak
            decryptedString = SlideRowLeft(firstCharIndex, secondCharIndex, decryptedString, table)
                

        else:#blockot alkotnak
            decryptedString += table[firstCharIndex[0]][secondCharIndex[1]]#sor indexük felcserélődik
            decryptedString += table[secondCharIndex[0]][firstCharIndex[1]]
            

    return decryptedString

#main
while True:
    print("Titkosítás/Dekódolás(T/D): ")
    inputString = GetInputString()

    if (inputString == "T"):

        print("Titkosítandó szöveg: ")
        stringToEncrypt = GetPlainText()#plaintext feldarabolása és szerkesztése

        table = SetUpTable(GetKeyWord())#tábla létrehozása

        print(Encrypt(table, stringToEncrypt))

        break

    elif (inputString == "D"):
        print("Dekódolandó szöveg: ")
        inputString = GetInputString()

        table = SetUpTable(GetKeyWord())

        print(Decrypt(table, inputString))

        break

    print("Helytelen formátum.")