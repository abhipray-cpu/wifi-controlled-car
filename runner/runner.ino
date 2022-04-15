//in this sketch we will be fetching data from firebase
//then will send data to uno usin serial communication
#include <SoftwareSerial.h>
#include<ESP8266WiFi.h>
#include<FirebaseESP8266.h>
#define WIFI_SSID "Heavy Driver"
#define WIFI_PASSWORD "maakabhosda"
#define FIREBASE_AUTH "J7zZWSjFYt1VW2h3Y6SgGz8JW7okCe1qrYYEnEe0"
#define FIREBASE_HOST "channel-relay-control-3a865-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define  Rx_PIN  4   // D2
#define  Tx_PIN 0    // D3

FirebaseJson json;
FirebaseData fbdo;
//initializing the serial communication object
SoftwareSerial mySerial(Rx_PIN, Tx_PIN);//rx tx
#define Gate A0 // Please ignore. This is only to activate ext power to transmitter

//***************************************
const byte numCharsSlave = 64;
char receivedSlaveChars[numCharsSlave];
char tempSlaveChars[numCharsSlave];        // temporary array for use when parsing

// variables to hold the parsed data
char messageFromSlave[numCharsSlave] = {0};
int integer1Slave = 0;
float float1Slave = 0.0;
int integer2Slave;
boolean newData = false; // invert this on Slave arduino

static boolean recvInProgress = false;
static byte ndx = 0;
char startMarker = '<';
char endMarker = '>';
char rc;
//***************************************
unsigned long currentMillis1 = 0;
unsigned long previousMillis1 = 0;
long interval1 = 150;  
void setup()
{
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
   Serial.println();
   Serial.print("Connected with IP: ");
   Serial.println(WiFi.localIP());
   Serial.println(); 
   Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
   Serial.println("WIFI Bot controlled bot is all your to play with");
  delay(700);
 }

void loop()
{
  currentMillis1 = millis();
  if (currentMillis1 - previousMillis1 > interval1)
  {
   previousMillis1 = currentMillis1;
   sendDataToSlave ();
  }
  }


//this will send serial data to arduino UNO
void sendDataToSlave () {

  String motor1=sendMotor1();
  String motor2=sendMotor2();
  String motor3=sendMotor3();
  String motor4=sendMotor4();
  String lights=sendlight();
  int speedval=sendSpeed();
  mySerial.print('<');
  mySerial.print("Master text");
  mySerial.print(",");
  mySerial.print("Motor1");
  mySerial.print(",");
  mySerial.print(motor1);
  mySerial.print(",");
  mySerial.print("Motor2");
  mySerial.print(",");
  mySerial.print(motor2);
  mySerial.print(",");
  mySerial.print("Motor3");
  mySerial.print(",");
  mySerial.print(motor3);
  mySerial.print(",");
  mySerial.print("Motor4");
  mySerial.print(",");
  mySerial.print(motor4);
  mySerial.print(",");
  mySerial.print("lights");
  mySerial.print(",");
  mySerial.print(lights);
  mySerial.print(",");
  mySerial.print("speed");
  mySerial.print(",");
  mySerial.print(speedval);
  mySerial.print('>');
  
}


//these fuctions will send serial data to arudino uno
String sendMotor1()
{
   //getting the motor directions
      if (Firebase.getString(fbdo, "/bot/forwardLeft")){
           Serial.print("FORWARDLEFTMOTOR:");
           Serial.println(fbdo.stringData());
           return fbdo.stringData();
      }
    
    else{
      Serial.println("Failed to update data for forward left motor");
        Serial.println(fbdo.errorReason().c_str());
    }
  
  }
String sendMotor2()
{
   //getting the motor directions
      if (Firebase.getString(fbdo, "/bot/forwardRight")){
           Serial.print("FORWARDLEFTMOTOR:");
           Serial.println(fbdo.stringData());
           return fbdo.stringData();
      }
    
    else{
      Serial.println("Failed to update data for forward right motor");
        Serial.println(fbdo.errorReason().c_str());
    }
  
  }

String sendMotor3()
{
   //getting the motor directions
      if (Firebase.getString(fbdo, "/bot/backwardLeft")){
           Serial.print("FORWARDLEFTMOTOR:");
           Serial.println(fbdo.stringData());
           return fbdo.stringData();
      }
    
    else{
      Serial.println("Failed to update data for backward left motor");
        Serial.println(fbdo.errorReason().c_str());
    }
  
  }

String sendMotor4()
{
   //getting the motor directions
      if (Firebase.getString(fbdo, "/bot/backwardRight")){
           Serial.print("FORWARDLEFTMOTOR:");
           Serial.println(fbdo.stringData());
           return fbdo.stringData();
      }
    
    else{
      Serial.println("Failed to update data for backward right motor");
        Serial.println(fbdo.errorReason().c_str());
    }
  
  }


int sendSpeed()
{
   //getting the motor directions
      if (Firebase.getInt(fbdo, "/bot/speed")){
           Serial.print("FORWARDLEFTMOTOR:");
           Serial.println(fbdo.intData());
           return fbdo.intData();
      }
    
    else{
      Serial.println("Failed to update data for speed");
        Serial.println(fbdo.errorReason().c_str());
    }
  
  }
String sendlight()
{
   //getting the motor directions
      if (Firebase.getString(fbdo, "/bot/lights")){
           Serial.print("FORWARDLEFTMOTOR:");
           Serial.println(fbdo.stringData());
           return fbdo.stringData();
      }
    
    else{
      Serial.println("Failed to update data for light");
        Serial.println(fbdo.errorReason().c_str());
    }
  
  }
