from __future__ import division

import time, sys
import socket
import os
import math
from PySide import QtGui, QtCore
import pandas as pd
import numpy as np

from database import RawDataPoint, ProcessedDataPoint, Session

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
        try:
            self.conn_worker.updateUI.connect(self.changeIcon())
        except RuntimeError as e:
            pass#this is fine
        self.conn_worker.start()
        #self.changeIcon()

    #changing the icon on the broom
    def changeIcon(self):
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'connected.png')))

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
            if not os.path.exists('kermits'):
                os.mkdir('kermits')
            filename = "kermits/%s_%s_%s.kermit" % (fNameEdit.text(), lNameEdit.text(), time.clock())
            f = file(filename, "w")
            f.write(self.conn_worker.memory)
            f.close()
            self.processor = ProcessingWorking(self.conn_worker.memory, self.conn_worker.angle)
            self.processor.start()

            # Save to database
            raw_data_points = []
            while self.processor.p_data is None:
                pass
            for index, raw_data in self.processor.p_data.loc[:, range(0, 15)].iterrows():
                raw_data_points.append(RawDataPoint(*raw_data))

            processed_data_points = []
            for index, processed_data in self.processor.p_data.loc[:, [0, 'v_force', 'h_force']].iterrows():
                processed_data_points.append(ProcessedDataPoint(*processed_data, broom_angle=self.processor.angle))

            try:
                session = Session(fNameEdit.text(), raw_data_points, processed_data_points, lNameEdit.text(), notes.toPlainText())
                id = session.save()
            except RuntimeError as error:
                print(error)

            # Reset UI
            self.conn_worker.memory = None
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
    updateUI = QtCore.Signal()

    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.record = False
        self.angle = False
        self.parent = parent

    def disconnect(self):
        self.socket.close()
        self.terminate()

    def run(self):
        self.memory = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket
        try:
            lblReady.setText('Connecting...')
            self.parent.setWindowTitle('Curling Demo - (Connecting)')
            self.socket.connect((HOST, PORT)) #Connect to the broom
            #once connected...
            self.updateUI.emit()
            connected = True
            btnStart.setEnabled(True)
            btnConnect.setEnabled(False)
            btnDisconnect.setEnabled(True)
            self.parent.setWindowTitle('Curling Demo - (Connected)')
            lblReady.setText('Connected!')
        except socket.error as e:
            lblReady.setText('Unable to connect.')
            self.terminate() #You're terminated
        while True:
            try:
                res = self.socket.recv(80)
                if self.angle == True and type(self.angle) == bool:
                    if len(res.split(', ')) == 15:
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
        angle_f = [float(x) for x in angle.split(', ')]
        quo = angle_f[5] / angle_f[6]
        self.angle = np.rad2deg(np.tan(quo))
        self.p_data = None
        print "Angle tan(%d/%d (%f)): %f" % (angle_f[5], angle_f[6], quo, self.angle)

    def run(self):
        # Process out of raw format
        arr = []
        for row in self.data.split('\n'):
            try:
                print row
                cols = [int(x) for x in row.split(', ')] # Converts columns to ints
                if len(cols) == 15:
                    arr.append(cols)

            except ValueError:
                break # End of memory
        df = pd.DataFrame(arr)
        df['e1'] = (-4 / (2.13 * 300)) * (df[11] / 3.3)
        df['e2'] = (-4 / (2.13 * 300)) * (df[12] / 3.3)
        df['axial_strain'] = -0.5 * (df['e1'] + df['e2'])
        df['bending_strain'] = 0.5 * (df['e1'] - df['e2'])

        KA = 13.644
        KB = 846.972

        df['fa'] = df['axial_strain'] * KA
        df['fb'] = df['bending_strain'] * KB

        df['v_force'] = df['fa'] * np.sin(self.angle) + df['fb'] * np.cos(self.angle)
        df['h_force'] = df['fa'] * np.cos(self.angle) + df['fb'] * np.sin(self.angle)
        df.to_csv('last.csv')
        self.p_data = df





def main():

    app = QtGui.QApplication(sys.argv)
    ex = UI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
