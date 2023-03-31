▪ /* 
▪ * Team Id: HB_1776
▪ * Author List: Dhanvantraj M, Madhusudhanan K, Winston Doss, Vinoth B
▪ * Filename: ESP32_code
▪ * Theme: HolA Bot (HB)
▪ * Functions: velocity(vf,vr,vl)
▪ * Global Variables: ssid,password,port,host,number,x,y,z,velx,vely,velz,w,penstatus,pos
▪ * variables> buf,i
▪ */
#include <WiFi.h>
#include <AccelStepper.h>
#include <ESP32Servo.h>


 
const char* ssid = "Galaxy M12BC54";                    //Enter your wifi hotspot ssid
const char* password =  "sondhamadatapodavakilla";               //Enter your wifi hotspot password
 
//const uint16_t port = 8090;
const uint16_t port = 8002;
const char * host = "192.168.158.72";

//number: Used to store recieved string from socket
String number="";
//x: Used to store front wheel velocity as string. Range form '0' to '650'
//y: Used to store right wheel velocity as string. Range form '0' to '650'
//z: Used to store left wheel velocity as string. Range form '0' to '650'
//w: Used to store pen up-down status. Either '0' or '1'
//velx: Used to store value of x
//vely: Used to store value of y
//velz: Used to store value of z
//penstatus:Used to store value of w
String x, y, z,velx ,vely ,velz,w,penstatus;
// pos:variable to store the servo position. Range: 90-130
int pos = 130;    

/*                     PINS DEFINITIONS                    */
#define dirPin1 14
#define stepPin1 12
#define dirPin2 4
#define stepPin2 2
#define dirPin3 15
#define stepPin3 13
#define motorInterfaceType 1

/*                       OBJECT INITILIZATIONS               */
AccelStepper stepper1(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper2(motorInterfaceType, stepPin2, dirPin2);
AccelStepper stepper3(motorInterfaceType, stepPin3, dirPin3);
Servo myservo;  // create servo object to control a servo

/*                       FUNCTIONS                            */

/*
 * FUNCTION NAME: velocity
 * INPUTS: vf,vr,vl
 * OUTPUTS: none
 * LOGIC: Takes front,left and right wheel velocity values as input and applies to motor through setspeed
 * and runspeed functions
 * EXAMPLE CALL: velocity(200.00,200.00,200.00)
 */
void velocity(float vf, float vr, float vl) {

/* Serial.println(vf);
    Serial.println(vr);
    Serial.println(vl);*/

  //Serial.println("Vel pub");
  stepper1.setSpeed(vf);
  stepper1.runSpeed();

  stepper2.setSpeed(vr);
  stepper2.runSpeed();

  stepper3.setSpeed(vl);
  stepper3.runSpeed();


}


void setup()
{
 
  //Serial.begin(115200);
 
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    //Serial.println("...");
  }
 
  //Serial.print("WiFi connected with IP: ");
  //Serial.println(WiFi.localIP());

  stepper1.setMaxSpeed(2000);
  stepper2.setMaxSpeed(2000);
  stepper3.setMaxSpeed(2000);
  myservo.attach(27);  // attaches the servo on pin 27 to the servo object
 
}
 
void loop()
{
    velx=x;
    vely=y;
    velz=z;
    velocity(velx.toFloat(), vely.toFloat(), velz.toFloat());

    if((int(millis())%500==0)){
      WiFiClient client;
      //velocity(velx.toFloat(), vely.toFloat(), velz.toFloat());
 
      if (!client.connect(host, port)) {
 
        //Serial.println("Connection to host failed");
        delay(500);
        return;
                }
        //velocity(velx.toFloat(), vely.toFloat(), velz.toFloat());
        client.print("!");
        //velocity(velx.toFloat(), vely.toFloat(), velz.toFloat());

        number=client.readStringUntil('\n');
        //velocity(velx.toFloat(), vely.toFloat(), velz.toFloat());

    //Serial.println(number);
    
    //buf:Store string as charector array
    char buf[40];
    //Serial.println(number);


    number.toCharArray(buf, 35);
    //i: Variable to increment through buf. Range:0-35
    int i = 0;

    x = "";
    y = "";
    z = "";
    w="";
    while (i < 35) {

          if (buf[i] == 'x') {
            i = i + 2;
            while (buf[i] != ' ') {
              x = x + buf[i];
              i = i + 1;
            }
    
          }
          else if (buf[i] == 'y') {
    
    
            i = i + 2;
            while (buf[i] != ' ') {
              y = y + buf[i];
              i = i + 1;
            }
    
          }
          else if (buf[i] == 'z') {
    
            i = i + 2;
            while (buf[i] != ' ') {
              z = z + buf[i];
              i = i + 1;
            }


      }
      else if (buf[i]=='w'){
        i=i+2;
        while(buf[i]!=' '){
          w = w + buf[i];
          i = i + 1;
        }
      }
      i += 1  ;

    }
    
    velx=x;
    vely=y;
    velz=z;
    penstatus=w;
    velocity(velx.toFloat(), vely.toFloat(), velz.toFloat());
    //Serial.println(velx);
    //Serial.println(vely);
    //Serial.println(velz);
    //Serial.println(penstatus);
    if(penstatus=="1")
    {
      pos=90;
    }
    else
    {
      pos=130;
    }
    myservo.write(pos);
    
    client.stop();
    }

    
    
    
 
    //Serial.println("Connected to server successful!");
    }
