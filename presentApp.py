from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import (QFileDialog, QMessageBox)
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file,client,tools
from PySide2.QtCore import *
from PySide2.QtGui import *
import sounddevice as sd
from scipy.io.wavfile import write
import argparse
import tempfile
from queue import Queue
import sys
import os

import sounddevice as sd
import soundfile as sf
import numpy  
assert numpy 
import random
import string
import signal
import time
import threading

signal.signal(signal.SIGINT, signal.SIG_DFL)
recordFlag = True

def int_or_str(text):
        """Helper function for argument parsing."""
        try:
                return int(text)
        except ValueError:
                return text

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
parser.add_argument(
        'filename', nargs='?', metavar='FILENAME',
        help='audio file to store recording to')
parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
        '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
        '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)


work_directory_path = os.getcwd()
print("PATH: "+work_directory_path)

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(872, 792)
        Frame.setStyleSheet("background-color: rgb(46, 52, 54);\n"
"background-color: rgb(0, 0, 0);")
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(170, 140, 61, 61))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("arrow.png"))
        self.label.setObjectName("label")
        self.choose_file_button = QtWidgets.QPushButton(Frame)
        self.choose_file_button.setGeometry(QtCore.QRect(40, 40, 291, 61))
        self.choose_file_button.setStyleSheet("background-color: rgb(211, 215, 207);\n"
"color: rgb(8, 99, 17);\n"
"font: 81 20pt \"Open Sans\";")
        self.choose_file_button.setObjectName("choose_file_button")
        self.id_number_label = QtWidgets.QTextBrowser(Frame)
        self.id_number_label.setGeometry(QtCore.QRect(70, 220, 231, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.id_number_label.sizePolicy().hasHeightForWidth())
        self.id_number_label.setSizePolicy(sizePolicy)
        self.id_number_label.setStyleSheet("color: rgb(8, 99, 17);\n"
"font: 18pt \"Open Sans\";")
        self.id_number_label.setObjectName("id_number_label")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(390, 650, 61, 61))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("arrowRight.png"))
        self.label_2.setObjectName("label_2")
        self.share_button = QtWidgets.QPushButton(Frame)
        self.share_button.setEnabled(False)
        self.share_button.setGeometry(QtCore.QRect(20, 460, 331, 61))
        self.share_button.setStyleSheet("background-color: rgb(211, 215, 207);\n"
"color: rgb(8, 99, 17);\n"
"font: 81 26pt \"Open Sans\";")
        self.share_button.setObjectName("share_button")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setGeometry(QtCore.QRect(170, 360, 61, 61))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("arrow.png"))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Frame)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(20, 650, 331, 61))
        self.pushButton.setStyleSheet("background-color: rgb(211, 215, 207);\n"
"color: rgb(8, 99, 17);\n"
"font: 81 26pt \"Open Sans\";")
        self.pushButton.setObjectName("pushButton")
        self.will_share_file = QtWidgets.QTextBrowser(Frame)
        self.will_share_file.setGeometry(QtCore.QRect(350, 40, 441, 61))
        self.will_share_file.setStyleSheet("color: rgb(8, 99, 17);\n"
"background-color: rgb(138, 226, 52);\n"
"font: 16pt \"Open Sans\";\n"
"background-color: rgb(187, 248, 123);")
        self.will_share_file.setText("")
        self.will_share_file.setObjectName("will_share_file")

        self.pause_and_share = QtWidgets.QPushButton(Frame)
        self.pause_and_share.setEnabled(False)
        self.pause_and_share.setGeometry(QtCore.QRect(490, 650, 311, 61))
        self.pause_and_share.setStyleSheet("background-color: rgb(211, 215, 207);\n"
"color: rgb(8, 99, 17);\n"
"font: 81 24pt \"Open Sans\";\n"
"font: 81 26pt \"Open Sans\";")
        self.pause_and_share.setText("Pause and Share")
        self.pause_and_share.setObjectName("pause_and_share")
        self.label_4 = QtWidgets.QLabel(Frame)
        self.label_4.setGeometry(QtCore.QRect(170, 560, 61, 61))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("arrow.png"))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "PresentApp-Desktop"))
        self.choose_file_button.setText(_translate("Frame", "Choose File  To Share"))
        self.id_number_label.setText(_translate("Frame", "<html><head/><body><p align=\"center\">Document ID</p></body></html>"))
        self.share_button.setText(_translate("Frame", "Share"))
        self.pushButton.setText(_translate("Frame", "Start Audio Record"))
        self.choose_file_button.clicked.connect(self.openFileNameDialog)
        self.share_button.clicked.connect(self.share)
        self.pushButton.clicked.connect(self.recording)
        self.pause_and_share.clicked.connect(self.pause_share)

    def openFileNameDialog(self):
        self.id_number_label.clear()
        self.will_share_file.clear()
        word = ""
        filename = ""
        _translate = QtCore.QCoreApplication.translate
        global path
        path = QFileDialog.getOpenFileName()
        filename = '<span style=\" color: #000;\">''</span>'
        print("path: ", path[0])
        filename = path[0].split('/')
        print("File name: ",filename[-1])
        filename = '<span style=\" color: #000;\">%s</span>'%filename[-1]
        self.will_share_file.append("        "+filename)
        self.share_button.setEnabled(True)
        global ID
        letters = string.ascii_lowercase
        ID = ''.join(random.choice(letters) for i in range(8))
        word = '<html><head/><body><p align=\"center\">%s</p></body></html>'%ID
        self.id_number_label.append(word)

    def share(self):
        print("share button", path)
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

        except ImportError:
            flags = None

        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        store = file.Storage('storage.json')
        creds = store.get()

        if not creds or creds.invalid:
            print('make new p data file')
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store, flags) \
                    if flags else tools.run(flow,store)

        DRIVE = build('drive','v3', http=creds.authorize(Http()))

        send_file = "'" + path[0] + "'"
        print("SEND FILE", send_file)   #bunun yerine ID ile gönderecek

        FILES = (
            send_file
        )

        for file_title in FILES:
            file_name = file_title
            metadata = {
                'name': str(ID)+path[0],    #File'ın isminin verildiği yer
                'mimeType': None
            }

        print("Metadata: ",metadata)
        res = DRIVE.files().create(body=metadata,media_body=path[0]).execute()
        
        print("Bitti")
        self.pushButton.setEnabled(True)
        
    def pause_share(self):
            global args
            global y
            global recordFlag
            recordFlag = False
            """print('\nRecording finished: ' + repr(args.filename))
            print("pause_and_share")
            global path
            path = QFileDialog.getOpenFileName()
            filename = '<span style=\" color: #000;\">''</span>'
            print("path: ", path[0])
            filename = path[0].split('/')
            print("File name: ",filename[-1])
            filename = '<span style=\" color: #000;\">%s</span>'%filename[-1]
            self.will_share_file.append(filename)
            self.share_button.setEnabled(True)
            letters = string.ascii_lowercase
            ID = ''.join(random.choice(letters) for i in range(8))

            word = '<span style=\" font: 81 31pt \"Open Sans\" color: #b90505;\">%s</span>' % ID
            self.id_number_label.append(word)"""

            
            self.id_number_label.clear()
            self.will_share_file.clear()

            letters = string.ascii_lowercase
            ID = ''.join(random.choice(letters) for i in range(8))

            word = '<span style=\" font: 81 31pt \"Open Sans\" color: #b90505;\">%s</span>' % ID
            self.id_number_label.append(word)
            self.will_share_file.append("        "+args.filename)
            #print("Filename: "+args.filename)

            #Share kısmı. Fonksiyon çağırırken değişkenler lazım olacaktı
            #diye fonksiyonu çağırmadım. Fonksiyonu tekrar yazdım.
            global work_directory_path
            path = work_directory_path + "/" + args.filename
            print("share button", path)
            try:
                import argparse
                flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

            except ImportError:
                flags = None

            SCOPES = 'https://www.googleapis.com/auth/drive.file'
            store = file.Storage('storage.json')
            creds = store.get()

            if not creds or creds.invalid:
                print('make new p data file')
                flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
                creds = tools.run_flow(flow, store, flags) \
                        if flags else tools.run(flow,store)

            DRIVE = build('drive','v3', http=creds.authorize(Http()))

            send_file = "'" + path + "'"
            print("SEND FILE", send_file)   #bunun yerine ID ile gönderecek

            FILES = (
                send_file
            )

            for file_title in FILES:
                file_name = file_title
                metadata = {
                    'name': str(ID)+path,    #File'ın isminin verildiği yer
                    'mimeType': None
                }

            print("Metadata: ",metadata)
            res = DRIVE.files().create(body=metadata,media_body=path).execute()
            
            print("Bitti")

    def recording(self):
        self.pause_and_share.setEnabled(True)
        self.pushButton.setEnabled(False)
        global args
        global ID
        global recordSend
        q = Queue()


        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                file=sys.stderr
                print(status)
            q.put(indata.copy())
        def thread_function(self):
            print("hello")
            
        def record_audio(self):
            if args.samplerate is None:
                device_info = sd.query_devices(args.device, 'input')
                args.samplerate = int(device_info['default_samplerate'])
            newID = str(ID)
            if args.filename is None:
                args.filename = tempfile.mktemp(prefix=newID,
                                                suffix='.wav', dir='')
            with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                            channels=args.channels, subtype=args.subtype) as file:
                with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                    channels=args.channels, callback=callback):
                    while True:
                        global recordFlag
                        file.write(q.get())
                        if(recordFlag == False):
                                break
        
        x = threading.Thread(target=thread_function, args=(1,))
        x.start()
        global stop_threads
        global y
        y = threading.Thread(target=record_audio, args =(2, ))
        y.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
