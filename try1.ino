#include <HardwareSerial.h>
#include <AccelStepper.h>


HardwareSerial SerialPort(2);


String msg = "0";

#define dirPin1 14
#define stepPin1 12
#define dirPin2 4
#define stepPin2 2
#define dirPin3 15
#define stepPin3 13
#define motorInterfaceType 1


AccelStepper stepper1(motorInterfaceType, stepPin1, dirPin1);
AccelStepper stepper2(motorInterfaceType, stepPin2, dirPin2);
AccelStepper stepper3(motorInterfaceType, stepPin3, dirPin3);

String number, x, y, z,velx ,vely ,velz;


void velocity(float vf, float vr, float vl) {

/* Serial.println(vf);
    Serial.println(vr);
    Serial.println(vl);*/

  //Serial.println("Vel pub");
  stepper1.setSpeed(vf);
  stepper1.runSpeed();

  stepper2.setSpeed(vr);
  stepper2.runSpeed();

  stepper3.setSpeed(-vl);
  stepper3.runSpeed();


}

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  //Serial.begin(9600);
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);
    
 
  stepper1.setMaxSpeed(500);
  stepper2.setMaxSpeed(500);
  stepper3.setMaxSpeed(500);
}

// the loop function runs over and over again forever
void loop() {
  //Serial.println(SerialPort.available());
  if (SerialPort.available()) {
    number =  SerialPort.readStringUntil('\n');
    char buf[40];
    //Serial.println(number);


    number.toCharArray(buf, 30);
    int i = 0;

    x = "";
    y = "";
    z = "";
    while (i < 30) {

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
      i += 1  ;

    }
    
    
   //velocity(x.toFloat(), y.toFloat(), z.toFloat());
   
    
 
    
    
    


  }
  else
  {
    //Serial.println("Not connected");
    velx=x;
    vely=y;
    velz=z;
    velocity(velx.toFloat(), vely.toFloat(), velz.toFloat());
  }
}
