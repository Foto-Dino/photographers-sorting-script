from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

class MyFrame(QWidget):

    dName = ""
    sendDirec = Signal(str)

    def __init__(self,parent=None):

        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls:
            event.accept()
            event.mimeData().urls()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        print(files)
        for f in files:
            print(f)
            self.sendDirec.emit(f)

    def getDirec(self):
        print(self.dName," Heres my dName")
        return self.dName
