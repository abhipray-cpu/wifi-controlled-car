
#include<Servo.h>
#include<ESP8266WiFi.h>
#include<FirebaseESP8266.h>
#define ENA   14          // Enable/speed motors Right        GPIO14(D5)
#define ENB   12          // Enable/speed motors Left         GPIO12(D6)
#define IN_1  15          // L298N in1 motors Rightx          GPIO15(D8)
#define IN_2  13          // L298N in2 motors Right           GPIO13(D7)
#define IN_3  2           // L298N in3 motors Left            GPIO2(D4)
#define IN_4  0           // L298N in4 motors Left            GPIO0(D3)

int speedCar = 800;         // 400 - 1023.
int speed_Coeff = 3;

#define WIFI_SSID "Amber-Prajjwal"
#define WIFI_PASSWORD "chalajaabsdk"
#define FIREBASE_AUTH "J7zZWSjFYt1VW2h3Y6SgGz8JW7okCe1qrYYEnEe0"
#define FIREBASE_HOST "channel-relay-control-3a865-default-rtdb.asia-southeast1.firebasedatabase.app/"


FirebaseData firebaseData;
FirebaseJson json;
FirebaseData fbdo;

Servo myServo1;
Servo myServo2;

void setup()
{
  Serial.begin(115200);
pinMode(ENA,OUTPUT);
pinMode(ENB,OUTPUT);
pinMode(IN_1,OUTPUT);
pinMode(IN_2,OUTPUT);
pinMode(IN_3,OUTPUT);
pinMode(IN_4,OUTPUT);
analogWrite(ENA,0);
analogWrite(ENB,0);
digitalWrite(IN_1,LOW);
digitalWrite(IN_2,LOW);
digitalWrite(IN_3,LOW);
digitalWrite(IN_4,LOW);
Serial.println("Starting our bot!!");
myServo1.attach(16); //this is the axis1
myServo2.attach(5); //this is the axis2
myServo1.write(0);
myServo2.write(0); 
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
 }

void loop()
{
  moveAxis1();
moveAxis2();
speedFn();
      Serial.println("Moving bot in the back direction!");
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
    delay(10000);
     Serial.print("Moving bot in FORWARD direction!");
     digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
   
    delay(10000);
       Serial.print("Moving bot in  LEFT direction!");
        digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
      
     delay(10000);
       Serial.print("Moving bot in RIGHT direction!");
       
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
     
      delay(10000);
      Serial.println("Stopping the bot!");
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
    
    delay(10000);
    
 delay(10000);
    digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
  delay(10000);
     

 }
void moveAxis1()
{
    if (Firebase.getInt(firebaseData, "/bot/axis1")){
    myServo1.write(firebaseData.intData()); 
     } 
  }

void moveAxis2()
{
  if (Firebase.getInt(firebaseData, "/bot/axis2")){
    myServo2.write(firebaseData.intData());
     }
  } 

 void speedFn(){
  if (Firebase.getInt(firebaseData, "/bot/speed")){
    speedCar = firebaseData.intData();
   
     }
  }

void goAhead(){ 

      
  }

void goBack(){ 

      
  }

void goRight(){ 

  }

void goLeft(){

     
  }

void goAheadRight(){
      
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar/speed_Coeff);
 
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar);
   }

void goAheadLeft(){
      
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, speedCar/speed_Coeff);
  }

void goBackRight(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar/speed_Coeff);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar);
  }

void goBackLeft(){ 

      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, speedCar);

      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, speedCar/speed_Coeff);
  }

void stopRobot(){  

      
 }
