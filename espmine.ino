#include <HardwareSerial.h>

HardwareSerial SerialPort(2);  //if using UART2

char number  = ' ';

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);
  SerialPort.begin(115200,SERIAL_8N1,16,17);
  Serial.println("Serial monitor started:");
  
  pinMode(2, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  Serial.println("Dada");
  delay(1000);
  Serial.println(SerialPort.available());
  if (SerialPort.available())
  {
    char number = SerialPort.read();
    Serial.println(number);
    if (int(number)%2 == 0) {
      digitalWrite(2, LOW);
    }
    if (int(number)%2 == 1) {
      digitalWrite(2, HIGH);
    }
  } 
}
