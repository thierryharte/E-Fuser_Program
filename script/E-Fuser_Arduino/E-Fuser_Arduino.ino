#include <Wire.h> //Library for I2C communication with lpGBT

//Array, that receives commands
const byte numChars = 64;
char charArray[numChars];

boolean newData = false;
boolean debug = false;

char lpGBT1 = (char) 0;
char lpGBT2 = (char) 0;
char lpGBT3 = (char) 0;
char lpGBT4 = (char) 0;

int timestamp;

//===============

//We set up serial with baudrate: 115200
//@Wire.begin() starts communication port for lpGBT
//@pinMode() sets up the line to enable the fuse-switch
void setup() {
    Serial.begin(115200);
    Wire.begin();
    Wire.setClock(400000);
    
    pinMode(A0, OUTPUT);
    pinMode(A1, OUTPUT);
    pinMode(A2, OUTPUT);
    pinMode(A3, OUTPUT);

    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    
    while(!Serial){
      }
    delay(10);
}

//===============

//Looping constantly to get a new command.
//recv_command() tries to fill the command Array
//If command is found it is decoded.
//@newData: is boolean, true if new command here.
void loop() {
    recv_command();
    if (newData == true){
      decode_data(charArray);
      newData = false;
    }
}

//===============

//Function to receive a command.
//If something in the serial is available, the startMarker is searched for.
//Characters between startMarker and endMarker are stored in charArray
void recv_command() {
    static boolean active = false; //determines if we are currently getting a command
    static byte ndx = 0; //index where in charArray we are
    char startMarker = '<';
    char rc; //always newest received byte
    while (Serial.available() > 0 && newData == false) {
        
        rc = Serial.read();

        if (active == true) { //active communication (between startMarker and endMarker)
            while(ndx<5) {
              delay(1);
              charArray[ndx] = rc;
              rc = Serial.read();
              ndx++;
            }
              charArray[ndx] = '\0'; // terminate the string
              active = false;
              ndx = 0;
              newData = true;
            }
        else if (rc == startMarker) { //beginn communication
            active = true;
        }
    }
}

//===============

void decode_data(char chars[]) {
  /*Expected pattern of chars:
   * 1 Byte Mode of command (W: writing/reading, R: reading, F: toggle fuses on and off)
   * 1 Byte Address
   * 2 Bytes Register
   * 1 Byte Value to register
   */
  switch (chars[0]) {
    case 'A': //writing and reading command
      writeReg(chars);
      readReg(chars);
    case 'W': //writing command
      writeReg(chars);
      break;
    case 'R': //reading command
      readReg(chars);
      break;
    case 'F': //fuse the lpGBT
      doFuse(chars);
      break;
    case 'C': //to set the correct fusing pins to the correct lpGBT
      mapPins(chars);
      break;
    case 'P':
      switchPower(chars[1]);
      break;
    case 'B':
      switchBootCNF(chars[1]);
      break;
    case 'T':
      testFuse(chars[1]);
      break;
    default:
      Serial.print('<');
      Serial.print(chars[0]);
      Serial.print("Unknown mode");
      break;
  }
}

//Write a register on lpGBT
void writeReg(char chars[]){
  Wire.beginTransmission((byte)chars[1]);
  for(int i = 2; i<5;i++){
    Wire.write((byte)chars[i]);
    }
  Wire.endTransmission();

  if(debug==true){
    Serial.print('<');
    Serial.print("Mode: W ");
    Serial.print("Address: ");
    Serial.print((byte)chars[1],HEX);
    Serial.print(" Register: ");
    for(int i = 2; i<4;i++){
      Serial.print((byte)chars[i],HEX);
    }
    Serial.print(" Value: ");
    Serial.print((byte)chars[4],HEX);
    Serial.print(" Sent command as BinStream: ");
    for(int i = 1; i<5;i++){
      Serial.print((byte)chars[i], BIN);
    }
  }

}

//===============

//Read from a register of lpGBT
void readReg(char chars[]){
  char success;
  byte returned;
  Wire.beginTransmission((byte)chars[1]);
  Wire.write((byte) chars[2]);
  Wire.write((byte) chars[3]);
  success = Wire.endTransmission();
  returned = Wire.requestFrom(chars[1],1);
  
  Serial.print('<');
  if(debug==true){
    Serial.print("Mode: R ");
    Serial.print("Address: ");
    Serial.print(chars[1], BIN);
    Serial.print(" Register High: ");
    Serial.print((byte) chars[2],HEX);
    Serial.print(" Register Low: ");
    Serial.print((byte) chars[3],HEX);
    Serial.print(" Success: ");
    Serial.print(success, HEX);
    Serial.print(" Answer : ");
    Serial.print(Wire.read(),HEX);
    Serial.print(" Amount: ");
    Serial.print(returned);
    Serial.print(" Sent command as BinStream: ");
    for(int i = 1; i<4;i++){
      Serial.print((byte)chars[i], BIN);
      }
    }
  else{
    Serial.print((byte)Wire.read(),HEX);
  }
}


//===============

void doFuse(char chars[]){
  int pinName = findPin(chars[1]);
  
  bool finished = false;
  int timestamp = 0;
  int totaltime = 0;

//  writeReg(chars); //Start command for fusing - comes from python program
//  while(finished==false and ontime < 1000){
//    finished == fuseStatus(chars[1]); //Read the fuse status register
//    ontime = micros() - timestamp;
//    }

  do {
    timestamp = micros();
    digitalWrite(pinName,HIGH); //Turn on Fuse
    writeReg(chars);
    delay(1);
    digitalWrite(pinName,LOW); //Turn off Fuses
    timestamp = micros()-timestamp;
    stopFuse(chars);
    totaltime += timestamp;
    finished == fuseStatus(chars[1]); //Read the fuse status register
  } while (finished==false and totaltime < 5000);
  
  Serial.print('<');
  if(totaltime > 5000){
    Serial.print("Timeout ");
    }
  else{
    Serial.print("Fusing successful ");
    }
  Serial.print(totaltime);
  }

//===============

// Reads the status of the FUSESTATUS Register
bool fuseStatus(char device){
  byte returned;
  byte fusedone = 2;
  byte fusebusy = 1;

  char fusestatus[3];
  
  fusestatus[0] = device;
  fusestatus[1] = (char) 1;
  fusestatus[2] = (char) 177; //for the case of a lpGBT_V1
//  fusestatus[2] = (char) 161; //for the case of a lpGBT_V0
  
  Wire.beginTransmission((byte)fusestatus[0]);
  Wire.write((byte) fusestatus[1]);
  Wire.write((byte) fusestatus[2]);
  Wire.endTransmission();
  Wire.requestFrom(fusestatus[0],1);
  returned = (byte)Wire.read();

  if(returned == fusedone){
    return true;
    }
  else{
    return false;
    }
}

//===============

void stopFuse(char chars[]){
  char stopfuse[4];
  
  stopfuse[0] = chars[1];
  stopfuse[1] = chars[2];
  stopfuse[2] = chars[3];
  stopfuse[3] = (char) 192;

  Wire.beginTransmission((byte)stopfuse[0]);
  Wire.write((byte) stopfuse[1]);
  Wire.write((byte) stopfuse[2]);
  Wire.write((byte) stopfuse[3]);
  Wire.endTransmission();
  
  }

void mapPins(char chars[]){
  int pin = 0;
  switch (chars[3]){
    case 1:
      pin = 1;
      lpGBT1 = chars[1];
      Serial.print('<');
      Serial.print("Map ");
      Serial.print(chars[1], HEX);
      Serial.print(" to pin number ");
      Serial.print(pin, HEX);
      break;
    case 2:
      pin = 2;
      lpGBT2 = chars[1];
      Serial.print('<');
      Serial.print("Map ");
      Serial.print(chars[1], HEX);
      Serial.print(" to pin number ");
      Serial.print(pin, HEX);
      break;
    case 3:
      pin = 3;
      lpGBT3 = chars[1];
      Serial.print('<');
      Serial.print("Map ");
      Serial.print(chars[1], HEX);
      Serial.print(" to pin number ");
      Serial.print(pin, HEX);
      break;
    case 4:
      pin = 4;
      lpGBT4 = chars[1];
      Serial.print('<');
      Serial.print("Map ");
      Serial.print(chars[1], HEX);
      Serial.print(" to pin number ");
      Serial.print(pin, HEX);
      break;
    default:
      Serial.print('<');
      Serial.print((byte) chars[3]);
      Serial.print("Bad pin number");
      break;
    }
  }

//===============

int findPin(char lpGBT){
  if(lpGBT==lpGBT1){
    return A3;
    }
  else if(lpGBT==lpGBT2){
    return A2;
    }
  else if(lpGBT==lpGBT3){
    return A1;
    }
  else if(lpGBT==lpGBT4){
    return A0;
    }
  }

//===============

void switchPower(char onoff){
  if(onoff == 1){
    digitalWrite(3,LOW);
    Serial.print("<Power switched on");
    }
  else{
    digitalWrite(3,HIGH);
    Serial.print("<Power switched off");
    }
  }
  
//===============

void switchBootCNF(char onoff){
    if(onoff == 1){
    digitalWrite(2,LOW);
    Serial.print("<BOOTCNF0 pulled up");
    }
  else{
    digitalWrite(2,HIGH);
    Serial.print("<BOOTCNF0 pulled down");
    }
  }

//===============

void testFuse(char lpGBT){
  int pinName = 0;
  pinName = findPin(lpGBT);

  Serial.print("<Test Fuse for lpGBT: ");
  Serial.print(lpGBT, HEX);
  Serial.print(" pin Number: ");
  Serial.print(pinName);
  
  digitalWrite(pinName,HIGH);
  delay(1);
  digitalWrite(pinName,LOW);
}
