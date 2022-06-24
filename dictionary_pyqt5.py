from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets, uic, QtGui  # icon
import sys
import sqlite3

# custom functions here


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('dictionary_pyqt5.ui', self)  # pass your ui file name here

        ########## set custom icon ############
        self.setWindowIcon(QtGui.QIcon('resources/dictionary_icon.png'))
        #######################################

        # lock window resize
        width = 503
        height = 386
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        ############################

        # find the button 'PressMeBtn' is the button name
        self.searchButton = self.findChild(QtWidgets.QPushButton, 'searchButton')
        # Remember to pass the definition/method, not the return value!
        self.searchButton.clicked.connect(self.searchButtonPressed)
        
        #self.searchLabel = self.findChild(QtWidgets.QPushButton, 'searchLabel')
        #self.searchLabel.clicked.connect(self.searchButtonPressed)
        
        self.inputWord = self.findChild(QtWidgets.QLineEdit, 'inputWord')
        self.output = self.findChild(QtWidgets.QLabel,'outputLabel')

        self.show()

    def searchButtonPressed(self):
        # This is executed when the button is pressed
        
        conn = sqlite3.connect("resources/dict.db")
        c = conn.cursor()
        word = str(self.inputWord.text())
        c.execute("""SELECT T_IdeaBase.meaning, T_IdeaBase.meaningAsm, T_IdeaBase.posID FROM T_IdeaBase WHERE IdeaID =
        (SELECT T_Map_WrdASM_IdeaBase.IdeaID FROM T_Map_WrdASM_IdeaBase where WrdAsmID =
        (SELECT T_WrdASM.WrdAsmID FROM T_WrdASM WHERE (T_WrdASM.pRoman LIKE :word) OR T_WrdASM.WrdAsm LIKE :word)) """, {'word': word})
        records1 = c.fetchall()
        c.execute("""SELECT T_IdeaBase.meaning, T_IdeaBase.meaningAsm, T_IdeaBase.posID FROM T_IdeaBase WHERE IdeaID =(
        SELECT T_Map_WrdENG_IdeaBase.IdeaID FROM T_Map_WrdENG_IdeaBase where WrdEngID =
        (SELECT T_WrdENG.WrdEngID FROM T_WrdENG WHERE T_WrdENG.WrdEng LIKE :word)) LIMIT 1; """, {'word': word})
        records2 = c.fetchall()
        #print(records1)
        #print(records2)
        if len(records1)!=0:
            c.execute("""SELECT T_WrdASM.WrdAsm FROM T_WrdASM WHERE (T_WrdASM.pRoman LIKE :word) OR (T_WrdASM.WrdAsm LIKE :word) LIMIT 1; """, {'word': word})
            searchWord=c.fetchall()
            #print(searchWord)
            c.execute("""SELECT TL_POS.posEng,TL_POS.posAsm FROM TL_POS WHERE posid = """+str(records1[0][2]))
            pos=c.fetchall()
            self.output.setText(str(searchWord[0][0]) + ": " + str(pos[0][0]) + "/ "+str(pos[0][1])+"\n\n"+str(records1[0][0])+"\n" +str(records1[0][1]))
        if len(records2)!=0:
            c.execute("""SELECT T_WrdENG.WrdEng FROM T_WrdENG WHERE T_WrdENG.WrdEng LIKE :word LIMIT 1; """, {'word': word})
            searchWord=c.fetchall()
            #print(searchWord)
            c.execute("""SELECT TL_POS.posEng,TL_POS.posAsm FROM TL_POS WHERE posid = """+str(records2[0][2]))
            pos=c.fetchall()
            self.output.setText(str(searchWord[0][0]) + ": " + str(pos[0][0]) + "/ "+str(pos[0][1])+"\n\n"+str(records2[0][0])+"\n" +str(records2[0][1]))
            
        
        conn.commit()
        conn.close()


app = QtWidgets.QApplication(sys.argv)

window = Ui()
app.exec_()
