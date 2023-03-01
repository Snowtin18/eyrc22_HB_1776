#include <WiFi.h>
#include <WiFiClient.h>
//#include <ESP8266WiFi.h>
#include <HardwareSerial.h>

HardwareSerial SerialPort(2);  //if using UART2
//
//
// WiFi credentials
const char* ssid = "Galaxy M12BC54";                    //Enter your wifi hotspot ssid
const char* password =  "sondhamadatapodavakilla";               //Enter your wifi hotspot password
const uint16_t port = 8002;
//const char * server = "192.168.102.72";                   //Enter the ip address of your laptop after connecting it to wifi hotspot
IPAddress server(192,168,102,72);


char incomingPacket[80];
WiFiClient client;


String msg = "0";


void setup(){
   
  Serial.begin(9600);                          //Serial to print data on Serial Monitor
  SerialPort.begin(115200,SERIAL_8N1,16,17);        //Serial to transfer data between ESP and AVR. The Serial connection is inbuilt.
  //client.setInsecure();
  
  //Connecting to wifi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

  int n = WiFi.scanNetworks();
  for(int i=0;i<n;i++)
  {
    Serial.println(WiFi.SSID(i));
  }
}


void loop() {
  Serial.println(client.connect(server, port));
  
  if (!client.connect(server, port)) {
    Serial.println("Connection to host failed");
    delay(200);
    return;
  }

  while(1){
      msg = client.readStringUntil('\n');         //Read the message through the socket until new line char(\n)
      client.print("Hello from ESP32!");          //Send an acknowledgement to host(laptop)
      Serial.println("DADAA");
      Serial.println(msg);                        //Print data on Serial monitor
      SerialPort.println(msg);                       //Send data to AVR
      SerialPort.flush();
    }
}
