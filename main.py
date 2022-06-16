from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

try:
    print(os.environ['DATABASE_URI'])
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./configKey.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': f"{os.environ['DATABASE_URI']}"
    })
    # declaring the collection objects
    Store = db.reference('/bot')

except Exception as e:
    print(e)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('controller.ui', self)
        self.setWindowTitle('Wifi car controller')
        self.ForwardLeftMotor=0
        self.forwardRightMotor=0
        self.backwardLeftMotor=0
        self.backwardRightMotor=0
        self.lightsValMotor=False
        self.speed=0
        self.forwardBtn.clicked.connect(self.forwardPressed)
        self.backwardBtn.clicked.connect(self.backwardPressed)
        self.rightBtn.clicked.connect(self.rightPressed)
        self.leftBtn.clicked.connect(self.leftPressed)
        self.lightsBtn.clicked.connect(self.lights)
        self.left360Btn.clicked.connect(self.left_360)
        self.right360Btn.clicked.connect(self.right360)
        self.brakeBtn.clicked.connect(self.brakes)
        self.speedController.valueChanged.connect(self.adjustSpeed)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.forwardPressed()
        elif event.key() == Qt.Key_S:
            self.backwardPressed()
        elif event.key() == Qt.Key_A:
            self.leftPressed()
        elif event.key() == Qt.Key_D:
            self.rightPressed()
        elif event.key() == Qt.Key_1:
            self.lights()
        elif event.key() == Qt.Key_2:
            self.left_360()
        elif event.key() == Qt.Key_3:
            self.right360()
        #check for corner conditions here to adjust speed
        elif event.key() == Qt.UpArrow:
            Store.child('speed').set(Store.child('speed').get()+15)
        elif event.key()==Qt.DownArrow:
            Store.child('speed').set(Store.child('speed').get() - 15)

        elif event.key() == Qt.Key_Q:
            self.brakes()


    #in these functions set motor speeds accordingly
    def forwardPressed(self):
        print('forward btn pressed')
        try:
            Store.child('backwardLeft').set('FORWARD')
            Store.child('backwardRight').set('FORWARD')
            Store.child('forwardLeft').set('FORWARD')
            Store.child('forwardRight').set('FORWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for forward button')
    def leftPressed(self):
        print('left btn pressed')
        try:
            Store.child('backwardLeft').set('BACKWARD')
            Store.child('backwardRight').set('FORWARD')
            Store.child('forwardLeft').set('BACKWARD')
            Store.child('forwardRight').set('FORWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for left button')

    def rightPressed(self):
        print('right btn pressed')
        try:
            Store.child('backwardLeft').set('FORWARD')
            Store.child('backwardRight').set('BACKWARD')
            Store.child('forwardLeft').set('FORWARD')
            Store.child('forwardRight').set('BACKWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for right button')

    def backwardPressed(self):
        print('back btn pressed')
        try:
            Store.child('backwardLeft').set('BACKWARD')
            Store.child('backwardRight').set('BACKWARD')
            Store.child('forwardLeft').set('BACKWARD')
            Store.child('forwardRight').set('BACKWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for backward button')

    def left_360(self):
        print('left360 btn pressed')
        try:
            Store.child('backwardLeft').set('STOP')
            Store.child('backwardRight').set('BACKWARD')
            Store.child('forwardLeft').set('BACKWARD')
            Store.child('forwardRight').set('BACKWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for left360 button')


    def right360(self):
        print('right360 btn pressed')
        try:
            Store.child('backwardLeft').set('BACKWARD')
            Store.child('backwardRight').set('STOP')
            Store.child('forwardLeft').set('BACKWARD')
            Store.child('forwardRight').set('BACKWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for right 360 button')

    def lights(self):
        print('lights btn pressed')
        val=Store.child('lights').get()
        if val=='off':
          Store.child('lights').set('on')
        else:
           Store.child('lights').set('off')

    def brakes(self):
        print('brakes btn pressed')
        try:
            Store.child('backwardLeft').set('STOP')
            Store.child('backwardRight').set('STOP')
            Store.child('forwardLeft').set('STOP')
            Store.child('forwardRight').set('STOP')
        except Exception as e:
            print(e)
            print('Failed to set values for forward button')

    def adjustSpeed(self):
        try:
            Store.child('speed').set(self.speedController.value())
        except Exception as e:
            print(e)
            print('failed to set speed value')






def main():
    app = QtWidgets.QApplication(sys.argv)
    main=MainWindow()
    main.show()
    sys.exit(exitFn())


def exitFn():
    app = QtWidgets.QApplication(sys.argv)
    try:
        Store.child('backwardLeft').set('STOP')
        Store.child('backwardRight').set('STOP')
        Store.child('forwardLeft').set('STOP')
        Store.child('forwardRight').set('STOP')
        Store.child('speed').set(50)
        Store.child('lights').set('off')
    except Exception as e:
        print(e)
        print('Failed to set reset values')
    app.exec_()


if __name__ == '__main__':
    main()