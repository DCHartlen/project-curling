import time, sys
import socket
import os
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
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'disconnected.png')))
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
        logo = QtGui.QPixmap(95, 45)
        logo.load(os.path.join('images', 'logo.png'))
        lblLogo = QtGui.QLabel(self)
        lblLogo.setPixmap(logo)
        title = QtGui.QLabel('Curling Demo')
        fName = QtGui.QLabel('First Name:')
        lName = QtGui.QLabel('Last Name:')
        lblNotes = QtGui.QLabel('Notes:')
        notes = QtGui.QTextEdit()
        fNameEdit = QtGui.QLineEdit()
        lNameEdit = QtGui.QLineEdit()

        #fonts
        titleFont = QtGui.QFont()
        titleFont.setPointSize(14)
        title.setFont(titleFont)

        buttonFont = QtGui.QFont()
        buttonFont.setPointSize(11)
        btnConnect.setFont(buttonFont)
        btnDisconnect.setFont(buttonFont)
        btnDiscard.setFont(buttonFont)
        btnSave.setFont(buttonFont)
        btnStart.setFont(buttonFont)

        lblFont = QtGui.QFont()
        lblFont.setPointSize(11)
        lblReady.setFont(lblFont)
        prgTimer.setFont(lblFont)
        fName.setFont(lblFont)
        lName.setFont(lblFont)
        notes.setFont(lblFont)
        lblNotes.setFont(lblFont)
        fNameEdit.setFont(lblFont)
        lNameEdit.setFont(lblFont)

        #background
        btnStart.setStyleSheet('QPushButton {background-color: #aeffae; }')

        #disabling buttons
        btnStart.setEnabled(False)
        btnSave.setEnabled(False)
        btnDisconnect.setEnabled(False)
        btnDiscard.setEnabled(False)

        #adding buttons, labels, textboxes etc to UI
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lblLogo,1,0)
        grid.addWidget(title, 1, 1)
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
        self.setGeometry(200, 200, 450, 400)
        self.setWindowTitle('Curling Demo - (Disconnected)')
        self.show()

    #method for connecting to the broom
    def connectToBroom(self):
        self.conn_worker = ConnectionWorker(self) # Pass the parent so it can ifConnected
        self.conn_worker.start()

    def ifConnected(self):
        connected = True
        btnStart.setEnabled(True)
        self.setWindowTitle('Curling Demo - (Connected)')
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'connected.png')))
        btnConnect.setEnabled(False)
        btnDisconnect.setEnabled(True)


    #method for disconnecting to the broom
    def disconnectFromBroom(self):
        self.conn_worker.disconnect()

        connected = False
        self.setWindowTitle('Curling Demo - (Disconnected)')
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'disconnected.png')))
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
            self.processor = ProcessingWorking(self.conn_worker.memory, conn_worker.angle)
            self.processor.start()
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
        #print progress
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

    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.record = False
        self.angle = False
        self.parent = parent

    def disconnect(self):
        self.socket.close()
        self.terminate()

    def run(self):
        # self.memory = 'Angle\n'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket
        try:
            lblReady.setText('Connecting...')
            self.socket.connect((HOST, PORT)) #Connect to the broom
            #once connected...
            self.parent.ifConnected()
            lblReady.setText('Connected!')
        except socket.error as e:
            lblReady.setText('Unable to connect.')
            self.terminate() #You're terminated

        while True:
            try:
                res = self.socket.recv(80)
                if self.angle == True:
                    self.angle = res
                if self.record:
                    self.memory = "%s%s" % (self.memory, res)
            except socket.error as e:
                lblReady.setText('Unable to connect.')
                self.terminate() #You're terminated

class ProcessingWorking(QtCore.QThread):
    def __init__(self, data, angle):
        QtCore.QThread.__init__(self)
        self.data = data
        self.angle_frame = angle

    def run(self):
        # Process out of raw format
        for row in self.data.split('\n'):
            cols = [int(x) for x in row.split(', ')] # Converts columns to ints
            print cols



def main():

    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
