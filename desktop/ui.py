import time, sys
import socket
from PySide import QtGui, QtCore

HOST = "192.168.4.1"
PORT = 23

#Class used for the UI
class UI(QtGui.QWidget):
    def __init__(self):
        super(UI, self).__init__()

        self.initUI()

    #initializes UI
    def initUI(self):

        #global variables
        global connected
        global btnSave
        global btnStart
        global prgTimer
        global btnConnect
        global btnDisconnect
        global lblReady
        global fNameEdit
        global lNameEdit
        global notes
        global btnDiscard

        #creating buttons, labels, textboxes.
        self.setWindowIcon(QtGui.QIcon('disconnected.png'))
        btnSave = QtGui.QPushButton('Save')
        btnSave.clicked.connect(self.saveDemo)
        btnDiscard = QtGui.QPushButton('Discard')
        btnDiscard.clicked.connect(self.discardDemo)
        btnStart = QtGui.QPushButton('Start')
        btnStart.clicked.connect(self.startDemo)
        btnConnect = QtGui.QPushButton('Connect')
        btnConnect.clicked.connect(self.connectToBroom)
        btnDisconnect = QtGui.QPushButton('Disconnect')
        btnDisconnect.clicked.connect(self.disconnectFromBroom)
        lblReady = QtGui.QLabel('', self)
        prgTimer = QtGui.QProgressBar(self)
        title = QtGui.QLabel('Curling Demo')
        fName = QtGui.QLabel('First Name:')
        lName = QtGui.QLabel('Last Name:')
        lblNotes = QtGui.QLabel('Notes:')
        notes = QtGui.QTextEdit()
        fNameEdit = QtGui.QLineEdit()
        lNameEdit = QtGui.QLineEdit()

        #disabling buttons
        btnStart.setEnabled(False)
        btnSave.setEnabled(False)
        btnDisconnect.setEnabled(False)
        btnDiscard.setEnabled(False)

        #adding buttons, labels, textboxes etc to UI
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(btnConnect, 2, 0, 1, 2)
        grid.addWidget(btnDisconnect, 2, 2, 1, 2)
        grid.addWidget(fName, 3, 0)
        grid.addWidget(fNameEdit, 3, 1, 1 ,3)
        grid.addWidget(lName, 4, 0)
        grid.addWidget(lNameEdit, 4, 1, 1, 3)
        grid.addWidget(lblNotes, 5, 0)
        grid.addWidget(notes, 6, 0, 1, 4)
        grid.addWidget(prgTimer, 7, 0, 1, 4)
        grid.addWidget(lblReady, 8, 0, 1, 1)
        grid.addWidget(btnDiscard, 8, 1, 1, 1)
        grid.addWidget(btnSave, 8, 2, 1, 1)
        grid.addWidget(btnStart, 8, 3, 1, 1)
        self.setLayout(grid)
        self.setGeometry(200, 200, 350, 150)
        self.setWindowTitle('Curling Demo - (Disconnected)')
        self.show()

    #method for connecting to the broom
    def connectToBroom(self):
        self.conn_worker = ConnectionWorker()
        self.conn_worker.start()

        connected = True
        btnStart.setEnabled(True)
        self.setWindowTitle('Curling Demo - (Connected)')
        self.setWindowIcon(QtGui.QIcon('connected.png'))
        btnConnect.setEnabled(False)
        btnDisconnect.setEnabled(True)

    #method for disconnecting to the broom
    def disconnectFromBroom(self):
        self.conn_worker.exit()
        self.conn_worker.socket.close()

        connected = False
        self.setWindowTitle('Curling Demo - (Disconnected)')
        self.setWindowIcon(QtGui.QIcon('disconnected.png'))
        btnStart.setEnabled(False)
        btnSave.setEnabled(False)
        btnDisconnect.setEnabled(False)
        btnConnect.setEnabled(True)

    #method for starting the demo
    def startDemo(self):

        btnStart.setEnabled(False)
        btnSave.setEnabled(False)
        btnDiscard.setEnabled(False)
        btnConnect.setEnabled(False)
        btnDisconnect.setEnabled(False)
        #time the program runs

        self.demo_worker = DemoWorker()
        self.demo_worker.updateProgress.connect(self.setProgress)
        self.demo_worker.start()

    #method for saving the demo
    def saveDemo(self):

        if fNameEdit.text() != "":
            filename = "%s_%s_%s.kermit" % (fNameEdit.text(), lNameEdit.text(), time.clock())
            f = file(filename, "w")
            f.write(self.conn_worker.memory)
            f.close()
            self.conn_worker.memory = "Angle\n"
            btnSave.setEnabled(False)
            btnDiscard.setEnabled(False)
            btnDisconnect.setEnabled(True)
            btnStart.setEnabled(True)
            prgTimer.setValue(0)
            fNameEdit.setText('')
            lNameEdit.setText('')
            notes.setText('')
            lblReady.setText('Saved!')
        else:
            lblReady.setText('First Name is Required')

    #method for discarding a demo
    def discardDemo(self):
            self.conn_worker.memory = "Angle\n"
            btnSave.setEnabled(False)
            btnDiscard.setEnabled(False)
            btnDisconnect.setEnabled(True)
            btnStart.setEnabled(True)
            prgTimer.setValue(0)
            fNameEdit.setText('')
            lNameEdit.setText('')
            notes.setText('')
            lblReady.setText('Discarded!')

    #set the progress on the progress bar
    def setProgress(self, progress):
        prgTimer.setValue(progress)
        print progress
        if progress == -5:
            self.conn_worker.angle = True
        if progress == 0:
            self.conn_worker.record = True
        if progress == 100:
            self.conn_worker.record = False

#This class is used to multithread the timer, so it doesn't freeze the UI.
class DemoWorker(QtCore.QThread):
    updateProgress = QtCore.Signal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)

    #what happens when the timer is running. 10s atm + 3 for the countdown
    def run(self):
        for i in range(1, 131):
            if i == 10:
                lblReady.setText('Ready')
            elif i == 20:
                lblReady.setText('Set')
            elif i == 30:
                lblReady.setText('Go!')
            #Sending the update to the UI.
            self.updateProgress.emit(i-30)
            time.sleep(0.1)

        btnSave.setEnabled(True)
        btnDiscard.setEnabled(True)
        btnDisconnect.setEnabled(False)

class ConnectionWorker(QtCore.QThread):
    """
    Thread for controlling the connection to the broom."""

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.record = False
        self.angle = False


    def run(self):
        self.memory = 'Angle\n'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket
        self.socket.connect((HOST, PORT)) # Connect to the broom
        while True:
            res = self.socket.recv(80)
            if self.record or self.angle:
                self.memory = "%s%s" % (self.memory, res)
            if self.record and self.angle:
                self.memory = "%s%s" % (self.memory, "Data\n")
                self.angle = False



def main():

    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
