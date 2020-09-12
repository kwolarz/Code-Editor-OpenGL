from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os

# ------------- Zmienne globalne ------------------
# głowna lista programu (lista list), zawiera w sobie listy odpowiadające za dany wiersz
# ilosc tych list odpowiada ilości wierszy w programie
characters = []
characters.append([]) # dodawnia pierwszego wiersza

# lista w której zapisywane są pozycje słów kluczowych (lista list), zawiera w sobie listy odpowiadające za dany wiersz
# ilosc tych list odpowiada ilości wierszy w programie
keywordPositions = []
keywordPositions.append([])

# zmienne odpowaidające za szerokość i wysokość okna
w, h= 800, 600

# aktualna liczba wierszy edytora
row = 0

# ostatni widoczny wiersz edytora - uzywane do obsługi scrollowania
lastVisisbleRow = 39

# pozycja kursora - wiersze
coursorRow = row

# pozycja kursora - kolumny
coursorColumn = 0

# ------------- Obsługa plików ------------------
def saveFile():
    global row
    file = open('file.txt', 'w+')
    for r in range(row + 1):
        if r == row:                    # jeśli ostatnia linia nie dodawaj znaku nowej linii
            file.write(listToString(characters[r]))
        else:
            file.write(listToString(characters[r]) + '\n')

    file.close()


def openFile():
    global row

    if os.path.isfile('file.txt'):       # sprawdzenie czy taki plik istnieje, jeśli nie - tworzy taki plik
        characters.clear()
        keywordPositions.clear()

        with open('file.txt', 'r') as file:
            if os.stat('file.txt').st_size == 0:   # w przypadku gdy plik jest pusty dodawana jest pusta lista
                characters.append([])
                keywordPositions.append([])

            else:
                for i, line in enumerate(file):
                    characters.append([])
                    characters[i] = list(line.replace('\n', ''))
                    keywordPositions.append([])
                    checkIfSyntax(listToString(characters[i]), i)
                    specialCharSyntax(listToString(characters[i]), i) 
                    row = i

            file.close()

    else:
        file = open('file.txt', 'w+')

# ------------- Podświetlanie składni kodu ------------------
# metoda odpoiwadająca za zamianę listy char'ów w jeden string
def listToString(listOfChar):
    word = ''
    for w in listOfChar:
        word += w

    return word

# metoda odpowaidająca za znajdowanie wielu słów kluczowych w jednym stringu
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1


# metoda odpowiadająca za znajdowanie słów kluczowych w danym stringu
# metoda dostaje cały wiersz, szuka w nim począteku oraz końca słowa kluczowego
# następnie sprawdza czy słowo kluczowe nie jest częścią jakiegoś wyrazu 
# metoda kończy się dodaniem pozycji liter do listy pozycji słów kluczowych w danym wierszu
def checkIfSyntax(text, row):
    keywordPositions[row].clear()
    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
    startOfKeyword = None
    for keyword in keywords:
        startOfKeyword = text.find(keyword)
        if keyword in text:
            endOfKeyword = len(keyword) + startOfKeyword
            if (startOfKeyword == 0 or characters[row][startOfKeyword - 1].isspace()) and characters[row][endOfKeyword].isspace():
                for i in range(startOfKeyword, endOfKeyword):
                    if i not in keywordPositions[row]:
                        keywordPositions[row].append(i)

            
# metoda odpowiadająca za znajdowaanie pojedyńczych znaków do podświetlenia
def specialCharSyntax(text, row):
    keywords = [':', ';', '"', "'", '[', ']', '{', '}', '(', ')', '=']
    # startOfKeyword = None
    for keyword in keywords:
        positions = list(find_all(text, keyword))

        keywordPositions[row].extend(positions)


# ------------- Obsługa zachowań po naciśnięciu przycisków ------------------
# metoda odpowaidająca za obsługę klawiszy kierunkowych na klawiaturze
def arrowHandler(key, x, y):
    global coursorRow, row, coursorColumn, h, lastVisisbleRow
    
    if key == GLUT_KEY_UP:
        if coursorRow > 0:
            coursorRow -= 1
            if lastVisisbleRow > 39 and coursorRow < lastVisisbleRow - 38:  # obsługa scrollowania
                h -= 15
                lastVisisbleRow -= 1

            if coursorColumn > len(characters[coursorRow]):
                coursorColumn = len(characters[coursorRow])

    elif key == GLUT_KEY_DOWN:
        if row > coursorRow:

            if row > lastVisisbleRow:           # obsługa scrollowania
                if coursorRow >= lastVisisbleRow - 1:
                    h += 15
                    lastVisisbleRow += 1

            coursorRow += 1
            if coursorColumn > len(characters[coursorRow]):
                coursorColumn = len(characters[coursorRow])


    elif key == GLUT_KEY_LEFT:
        if coursorColumn > 0:
            coursorColumn -= 1

    elif key == GLUT_KEY_RIGHT:
        if len(characters[coursorRow]) > coursorColumn:
            coursorColumn += 1

    print('row = ', row, 'coursor = ', coursorRow, 'last visible = ', lastVisisbleRow)
    
    return None


# metoda odpowiadająca za obsługę klawiatury
def handler(key, x, y):
    global row, coursorRow, coursorColumn, h, lastVisisbleRow
    
    if key == b'\x7f':           # usuwanie znaków (backspace)
        if coursorColumn > 0:
            coursorColumn -= 1 

        if len(characters[coursorRow]) == 0:
            if row > 0:
                characters.pop(coursorRow)
                keywordPositions.pop(coursorRow)
                row -= 1
                if row or coursorRow > row: 
                    coursorRow -= 1
                coursorColumn = len(characters[coursorRow])
                
        else:
            characters[coursorRow].pop(coursorColumn)
            keywordPositions[coursorRow].pop(coursorColumn)

    elif key==b'\r':            # nowa linia (enter/return)
        if row > lastVisisbleRow - 1:
            if coursorRow == row:
                h += 15
                lastVisisbleRow += 1

        coursorRow += 1
        row += 1
        characters.insert(coursorRow, [])
        keywordPositions.insert(coursorRow, [])
        characters[coursorRow] = characters[coursorRow - 1][coursorColumn:]
        characters[coursorRow - 1] = characters[coursorRow - 1][:coursorColumn]
        coursorColumn = 0

    elif key == b'\t':        # tabulator
        for _ in range(4):
            characters[coursorRow].insert(coursorColumn, ' ')
            coursorColumn += 1

    elif key == b'\x13':      # kombinacja CTRL + f
        saveFile()

    elif key == b'\x0f':      # kombinacja CTRL + s
        openFile()

    else:                     # kazdy inny znak zostanie dodany do listy oraz narysowany
        characters[coursorRow].insert(coursorColumn, key.decode('UTF-8'))
        coursorColumn += 1

    print(characters)

    checkIfSyntax(listToString(characters[coursorRow]), coursorRow)
    specialCharSyntax(listToString(characters[coursorRow]), coursorRow)  

    return None

# ------------- Rysowanie elementów na ekranie ------------------
# metoda odpowaidająca za rysowanie tekstu w oknie edytora
def glut_print(x, y, font, text, r, g, b):
    blending = False 
    if glIsEnabled(GL_BLEND):
        blending = True

    #glEnable(GL_BLEND)
    glColor3f(r, g, b)
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

    if not blending:
        glDisable(GL_BLEND) 


# zmienna słuąca do stworzenia animowanego kursora
index = 0
# metoda odpowiadająca za rysowanie elemntów w oknie edytora
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    global index
    index += 1

    # rysowanie numeru wiersza
    for i in range(row + 1):
        glut_print(10, (h-15) - (15 * i), GLUT_BITMAP_HELVETICA_10, str(i), 0.99 , 0.9 , 0.05)

    # rysowanie znaków na bazie listy
    for charRow in range(row+1):
        for pos, char in enumerate(characters[charRow]):
            if pos in keywordPositions[charRow]:
                glut_print(33 + 10*pos, (h - 15) - (15 * (charRow)), GLUT_BITMAP_9_BY_15, char, 0, 0.7, 0.95)
            else:
                glut_print(33 + 10*pos, (h - 15) - (15 * (charRow)), GLUT_BITMAP_9_BY_15, char, 1.0 , 1.0 , 1.0)

    # rysowanie oraz animizacja kursora
    if index > 0 and index < 40:
        glut_print(33 + 10*coursorColumn, (h - 15) - (15 * (coursorRow)), GLUT_BITMAP_HELVETICA_18, "|", 0 , 0 , 0)
    elif index == 80:
        index = 0
    else:
        glut_print(33 + 10*coursorColumn, (h - 15) - (15 * (coursorRow)), GLUT_BITMAP_HELVETICA_18, "|", 0.99 , 0.9 , 0.05)

    glutSwapBuffers()

# ------------- Inicjalizacja środowiska ------------------
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(w, h)
    glutInitWindowPosition(560, 240)
    wind = glutCreateWindow("OpenGL Code Editor")
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(handler)
    glutSpecialFunc(arrowHandler)
    glutMainLoop()

if __name__ == "__main__":
    main()