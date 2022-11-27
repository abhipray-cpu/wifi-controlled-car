from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5 import QtWebEngineWidgets
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import logging
import datetime as dt
logging.basicConfig(filename="dev.log", level=logging.INFO)
from datetime import  datetime as dt
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
    logging.error(f'{dt.now()}:failed to connect to firebase realtime database {e} ')


class Screen1(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Screen1, self).__init__(*args, **kwargs)
        uic.loadUi('controller.ui', self)
        self.setWindowTitle('Wifi car controller')
        self.ForwardLeftMotor = 0
        self.forwardRightMotor = 0
        self.backwardLeftMotor = 0
        self.backwardRightMotor = 0
        self.lightsValMotor = False
        self.speed = 0
        self.forwardBtn.clicked.connect(self.forwardPressed)
        self.backwardBtn.clicked.connect(self.backwardPressed)
        self.rightBtn.clicked.connect(self.rightPressed)
        self.leftBtn.clicked.connect(self.leftPressed)
        self.lightsBtn.clicked.connect(self.lights)
        self.left360Btn.clicked.connect(self.left_360)
        self.right360Btn.clicked.connect(self.right360)
        self.brakeBtn.clicked.connect(self.brakes)
        self.speedController.valueChanged.connect(self.adjustSpeed)
        self.switch_2.clicked.connect(self.switch)

    def switch(self):
        widget.setCurrentIndex(1)

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
        # check for corner conditions here to adjust speed
        elif event.key() == Qt.UpArrow:
            Store.child('speed').set(Store.child('speed').get() + 15)
        elif event.key() == Qt.DownArrow:
            Store.child('speed').set(Store.child('speed').get() - 15)

        elif event.key() == Qt.Key_Q:
            self.brakes()

    # in these functions set motor speeds accordingly
    def forwardPressed(self):
        print('forward btn pressed')
        try:
            Store.child('direction').set('FORWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for forward button')
            logging.error(f'{dt.now}:failed to set the values in forward function {e}')

    def leftPressed(self):
        print('left btn pressed')
        try:
            Store.child('direction').set('LEFT')
        except Exception as e:
            print(e)
            print('Failed to set values for left button')
            logging.error(f'{dt.now}:failed to set the values in left function {e}')

    def rightPressed(self):
        print('right btn pressed')
        try:
            Store.child('direction').set('RIGHT')
        except Exception as e:
            print(e)
            print('Failed to set values for right button')
            logging.error(f'{dt.now}:failed to set the values in right function {e}')

    def backwardPressed(self):
        print('back btn pressed')
        try:
            Store.child('direction').set('BACKWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for backward button')
            logging.error(f'{dt.now}:failed to set the values in backward function {e}')

    def left_360(self):
        print('left360 btn pressed')
        try:
            Store.child('direction').set('ANTI')
        except Exception as e:
            print(e)
            print('Failed to set values for left360 button')
            logging.error(f'{dt.now}:failed to set the values in left360 function {e}')

    def right360(self):
        print('right360 btn pressed')
        try:
            Store.child('direction').set('CLOCK')
        except Exception as e:
            print(e)
            print('Failed to set values for right 360 button')
            logging.error(f'{dt.now}:failed to set the values in right360 function {e}')

    def lights(self):
        print('lights btn pressed')
        val = Store.child('lights').get()
        if val == 'off':
            Store.child('lights').set('on')
        else:
            Store.child('lights').set('off')
            logging.error(f'{dt.now}:failed to set the values in lights function {e}')

    def brakes(self):
        print('brakes btn pressed')
        try:
            Store.child('direction').set('STOP')
        except Exception as e:
            print(e)
            print('Failed to set values for forward button')
            logging.error(f'{dt.now}:failed to set the values in brakes function {e}')

    def adjustSpeed(self):
        try:
            Store.child('speed').set(self.speedController.value())
            print(self.speedController.value())
        except Exception as e:
            print(e)
            print('failed to set speed value')
            logging.error(f'{dt.now}:failed to set the values in adjust speed function {e}')


class Screen2(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Screen2, self).__init__(*args, **kwargs)
        uic.loadUi('camera.ui', self)
        self.setWindowTitle('Wifi car controller')
        self.switch_2.clicked.connect(self.switch)
        self.front.clicked.connect(self.forwardPressed)
        self.back.clicked.connect(self.backwardPressed)
        self.left.clicked.connect(self.leftPressed)
        self.right.clicked.connect(self.rightPressed)
        self.back.clicked.connect(self.backwardPressed)
        self.speedContoller.valueChanged.connect(self.adjustSpeed)
        self.clockwise.clicked.connect(self.right360)
        self.anticlockwise.clicked.connect(self.left_360)
        self.flash.clicked.connect(self.lights)
        self.brake.clicked.connect(self.brakes)
        self.axis1.setMinimum(0)
        self.axis1.setMaximum(180)
        self.axis2.setMinimum(0)
        self.axis2.setMaximum(180)
        self.axis1.setValue(90)
        self.axis2.setValue(100)

        self.axis1.valueChanged.connect(self.axis1Controller)
        self.axis1.setWrapping(False)
        self.axis2.setWrapping(False)
        self.axis2.valueChanged.connect(self.axis2Controller)

    def axis1Controller(self):
        try:
            if 0 < self.axis1.value() < 100:
                Store.child('axis1').set(self.axis1.value())
                print(self.axis1.value())
        except Exception as e:
            logging.error(f'{dt.now}:failed to set the values in axis1 function {e}')

    def axis2Controller(self):
        try:
            if 0 < self.axis2.value() < 100:
                Store.child('axis2').set(self.axis2.value())
                print(self.axis2.value())
        except Exception as e:
            logging.error(f'{dt.now}:failed to set the values in axis2 function {e}')

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
        # check for corner conditions here to adjust speed
        elif event.key() == Qt.UpArrow:
            Store.child('speed').set(Store.child('speed').get() + 15)
        elif event.key() == Qt.DownArrow:
            Store.child('speed').set(Store.child('speed').get() - 15)

        elif event.key() == Qt.Key_Q:
            self.brakes()

    # in these functions set motor speeds accordingly
    def forwardPressed(self):
        print('forward btn pressed')
        try:
            Store.child('direction').set('FORWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for forward button')
            logging.error(f'{dt.now}:failed to set the values in forward function {e}')

    def leftPressed(self):
        print('left btn pressed')
        try:
            Store.child('direction').set('LEFT')
        except Exception as e:
            print(e)
            print('Failed to set values for left button')
            logging.error(f'{dt.now}:failed to set the values in left function {e}')

    def rightPressed(self):
        print('right btn pressed')
        try:
            Store.child('direction').set('RIGHT')
        except Exception as e:
            print(e)
            print('Failed to set values for right button')
            logging.error(f'{dt.now}:failed to set the values in right function {e}')

    def backwardPressed(self):
        print('back btn pressed')
        try:
            Store.child('direction').set('BACKWARD')
        except Exception as e:
            print(e)
            print('Failed to set values for backward button')
            logging.error(f'{dt.now}:failed to set the values in back function {e}')

    def left_360(self):
        print('left360 btn pressed')
        try:
            Store.child('direction').set('ANTI')
        except Exception as e:
            print(e)
            print('Failed to set values for left360 button')
            logging.error(f'{dt.now}:failed to set the values in left function {e}')

    def right360(self):
        print('right360 btn pressed')
        try:
            Store.child('direction').set('CLOCK')
        except Exception as e:
            print(e)
            print('Failed to set values for right 360 button')
            logging.error(f'{dt.now}:failed to set the values in right function {e}')

    def lights(self):
        print('lights btn pressed')
        val = Store.child('lights').get()
        if val == 'off':
            Store.child('lights').set('on')
        else:
            Store.child('lights').set('off')

    def brakes(self):
        print('brakes btn pressed')
        try:
            Store.child('direction').set('STOP')
        except Exception as e:
            print(e)
            print('Failed to set values for forward button')
            logging.error(f'{dt.now}:failed to set the values in brakes function {e}')

    def adjustSpeed(self):
        try:
            Store.child('speed').set(self.speedContoller.value())
        except Exception as e:
            print(e)
            print('failed to set speed value')
            logging.error(f'{dt.now}:failed to set the values in adjust speed function {e}')

    def switch(self):
        widget.setCurrentIndex(0)


def exitFn():
    app = QtWidgets.QApplication(sys.argv)
    try:
        Store.child('direction').set('STOP')
        Store.child('speed').set(50)
        Store.child('lights').set('off')
    except Exception as e:
        print(e)
        print('Failed to set reset values')
        logging.error(f'{dt.now}:failed to reset values in the exit function {e}')
    app.exec_()


app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
screen1 = Screen1()
screen2 = Screen2()
widget.addWidget(screen1)
widget.addWidget(screen2)
widget.setFixedWidth(1400)
widget.setFixedHeight(865)
widget.show()
sys.exit(exitFn())
