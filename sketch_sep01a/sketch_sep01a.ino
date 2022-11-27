//this code is for controlling a 4 wheeled bot using 
// L293D H bridge motor driver vir node mcu
// usign the firebase realtime database
#include<ESP8266WiFi.h>
#include<FirebaseESP8266.h>
//wifi credentials
#define WIFI_SSID "Amber-Prajjwal"
#define WIFI_PASSWORD "chalajaabsdk"
#define FIREBASE_AUTH "J7zZWSjFYt1VW2h3Y6SgGz8JW7okCe1qrYYEnEe0"
#define FIREBASE_HOST "channel-relay-control-3a865-default-rtdb.asia-southeast1.firebasedatabase.app/"
FirebaseData firebaseData;
FirebaseJson json;
FirebaseData fbdo;
String forwardLeftVal="STOP";
String forwardRightVal="STOP";
String backwardLeftVal="STOP";
String backwardRightVal="STOP";
String lightsVal="off";
int speedVal=30;
void setup() {
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
  delay(1000);
  Serial.println("Let's have some fun with the bot!");
}

void loop() {
  // put your main code here, to run repeatedly:
// reading teh values from the database
forwardLeftVal = forwardLeft();
forwardRightVal = forwardRight();
backwardLeftVal = backwardLeft();
backwardRightVal = backwardRight();
lightsVal = Lights();
speedVal = Speed();

// the interval will be 1s
delay(1000);
}

// these functions will fetch the values from the real time database
String forwardLeft()
{
  if (Firebase.getString(firebaseData, "/bot/forwardLeft")){
    Serial.print("State of forward left wheel:");
    Serial.println(firebaseData.stringData());
    return firebaseData.stringData();
    
     }
     else
     {
      return "STOP";
      }
  }
String forwardRight()
{
  if (Firebase.getString(firebaseData, "/bot/forwardRight")){
    Serial.print("State of forward left wheel:");
    Serial.println(firebaseData.stringData());
    return firebaseData.stringData();
    
     }
     else
     {
      return "STOP";
      }
  }
String backwardLeft()
{
  if (Firebase.getString(firebaseData, "/bot/backwardLeft")){
    Serial.print("State of forward left wheel:");
    Serial.println(firebaseData.stringData());
    return firebaseData.stringData();
    
     }
     else
     {
      return "STOP";
      }
  }
String backwardRight()
{
  if (Firebase.getString(firebaseData, "/bot/backwardRight")){
    Serial.print("State of forward left wheel:");
    Serial.println(firebaseData.stringData());
    return firebaseData.stringData();
    
     }
     else
     {
      return "STOP";
      }
  }
int Speed()
{
  if (Firebase.getInt(firebaseData, "/bot/speed")){
    Serial.print("The speed of the bot:");
    Serial.println(firebaseData.intData());
    return firebaseData.intData();
    
     }
     else
     {
      return 30;
      }
}
String Lights()
{
  if (Firebase.getString(firebaseData, "/bot/lights")){
    Serial.print("The Lights are:");
    Serial.println(firebaseData.stringData());
    return firebaseData.stringData();
    
     }
     else
     {
      return "off";
      }
  }
  
