import webbrowser
from myframe import MyFrame
import script
import sys
import Logo
from PySide6.QtCore import Qt
import time
import os
import platform
import subprocess
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import loadUiType
from PySide6.QtWidgets import QFileDialog,QMessageBox,QApplication, QWidget
from numpy import empty
from PySide6.QtCore import QThread, Signal,QFile


app=QApplication(sys.argv)
if getattr(sys,'frozen',False):
    os.chdir(sys._MEIPASS)
dName=""
emptyStr = ""
global new_path
#form,call=
# DONE loadUiType returning None? why is that
# its because pyside6-uic is not accessable over path
#
form, call=loadUiType("AppUI.ui")
form3, call3=loadUiType("splash.ui")
form1, call1=loadUiType("processing.ui")
form2, call2=loadUiType("processed.ui")

class SplashScreen(call3,form3):
    def __init__(self):
        #super(call3,self).__init__()
        super().__init__()
        self.setWindowTitle("Foto Dino")
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.setFixedWidth(850)
        self.setFixedHeight(580)
        self.setupUi(self)



class myApp(call,form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # print(width)
        #self.setOutput.clicked.connect(self.setDirec)
        self.browseButton.clicked.connect(self.askD)
        self.setOutput.clicked.connect(self.savingPath)
        self.proceedButton.clicked.connect(self.onClick)

        # use standard desktop https://stackoverflow.com/questions/34275782/how-to-get-desktop-location
        global desktop
        if platform.system() == "Windows":
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        else:
            desktop = os.path.join(os.path.expanduser('~/Desktop')) 


        

    def change(self):
        self.main = ProcessingPage()
        self.main.show()
        self.close()

      
    #Getting directory from button click.
    def askD(self):
        global dName
        dName = str(QFileDialog.getExistingDirectory(None, "Select Directory", desktop))
        self.direcText.setText(dName)
        # print("directory: ",dName)

    def savingPath(self,):
        global savingD
        #QMessageBox.information(self,"Select Folder","Select folder where you want to save files", QMessageBox.Ok, QMessageBox.Ok)
        savingD = str(QFileDialog.getExistingDirectory(None, "Select Directory", desktop))
        self.label_3.setText(savingD)

    #Getting directory from drop event of myframe.
    def setDirec(self,directory):
        # print ("Directory",directory)
        global dName
        dName = directory
        self.direcText.setText(dName)


    #Changing UI to Processing
    def onClick(self):
        print(savingD, dName)
        if (dName != emptyStr):
            self.change()
        else:
            eMsg = QMessageBox()
            eMsg.setIcon(QMessageBox.Critical)
            eMsg.setWindowTitle('Error')
            eMsg.setText("No Folder Selected!")
            eMsg.exec()



class ProcessingPage(call1,form1):
    def __init__(self):
        super(call1, self).__init__()
        self.setupUi(self)
        #Making a thread for executing script
        self.organize = External()
        self.runScript()
        
    
    def runScript(self):
        self.organize.countChanged.connect(self.onCountChanged)
        self.organize.finished.connect(self.onFinished)
        self.organize.start()
    
    #Getting values from script for progress bar
    def onCountChanged(self, value):
        self.pBar.setValue(value[0])
        self.iLabel.setText(value[1])
    
    
    def onFinished(self):
        #self.main = ProcessedPage(self.organize.event_dir,self.organize.event_dir_lis)

        self.main = ProcessedPage(self.organize.new_path, self.organize.event_dir_lis)


        self.main.setWindowTitle("Foto Dino")
        self.setWindowIcon(QIcon('resources/dino-new.png')) 
        self.main.show()
        self.close()

class ProcessedPage(call2,form2):
    def __init__(self,event_dir,event_lis):
        super(call2, self).__init__()
        self.event_dir=event_dir
        self.event_lis1 = event_lis
        # print(self.event_lis1)
        # for items in self.event_lis1:
        #     os.mkdir(os.path.join(items+'/','final sets'))
        #     os.mkdir(os.path.join(items+'/final sets','preview'))
        # print("EVENT DIRECTORY: "+self.event_dir)
        self.setupUi(self)
        self.nextButton.clicked.connect(self.change)
        self.dashboardButton.clicked.connect(self.toDashboard)
	
        #self.eLabel.setText(self.event_dir)
	
        self.viewButton.clicked.connect(self.openDirec)

    def change(self):
        self.main = myApp()
        self.main.setWindowTitle("Foto Dino")
        self.setWindowIcon(QIcon('resources/dino-new.png')) 
        self.main.show()
        self.close()

    def toDashboard(self):
        webbrowser.open('https://drive.google.com/drive/u/2/folders/1VLBdvKhYt3Faw5UVPCLGWb1op1YZXDx4')
    
    def openDirec(self):
        # webbrowser.open(self.event_dir)
        # https://stackoverflow.com/questions/6631299/python-opening-a-folder-in-explorer-nautilus-finder
        # show folder containing the clients
        final_output_path = self.event_dir
        # show folder containing the event
        final_output_path = savingD

        if platform.system() == "Windows":
            os.startfile(final_output_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", final_output_path])
        else:
            subprocess.Popen(["xdg-open", final_output_path])
        


class External(QThread):
    countChanged = Signal(list)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.event_dir = None
        self.event_dir_lis = None
        self.new_path = None
    
    def run(self):
        print("Here is saving directory", savingD)
        #self.event_dir_lis, self.event_dir, new_path = script.mainFunc(self,dName, savingD)

        self.new_path = script.mainFunc(self, dName, savingD)



if __name__ == '__main__':
    splash = SplashScreen()
    splash.show()
    time.sleep(2)
    splash.close()
    ex = myApp()
    ex.setWindowTitle("Foto Dino")
    ex.setWindowIcon(QIcon('resources/dino-new.png')) 
    ex.show()
    sys.exit(app.exec_())