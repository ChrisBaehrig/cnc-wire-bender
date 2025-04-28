//------------------------
//Release V4.1 IO
//------------------------

//Releses:
//V1.0 Serielle Schnittstelle empfängt CHAR und schreibt die Zeichen wieder auf die Serielle Schnittstelle und das LCD
//V1.1 Auswerten der Empfangenen CHAR auf Schnittstelle und speichern von Parameter und Attribut
//V1.2 Übergabe erweitern und testen und einbinden der Zeilennummer 
//V2.0 Einbinden ein Stepper mit eigener Funktion und test. Versuch hat die Bib Accelstepper ausgeschlossen.
//V2.1 Erweiterung alle Stepper änderung value_1 auf long
//V2.2 Einbinden Servosteuerung
//V2.21 Anpassungen an Python Terminal
//V2.22 Debugging nach erstem Test ( Drehrichtung Z, Servo eistellungen,
//V2.3 Freigabeschalter einbinden display erweitert (Zeile 1: row, command / Zeile 2: value_1, value_2 / Zeile 3: value_3, value_4 / Zeile: 4: Status, Kommentar)
//V2.4 Stop mit Kippschalter
//V2.5 Pin UP DOWN optimieren
//V3.0 Debug, 
//V4.0 Neuer Biegekopf installiert mit Servoansteuerung
//V4.1 Verbesserte Servo ansteuerung mit grad

/*Releasplanung:  
//V5.0 Überarbeiteter Benderkopf und elektronik in code einbinden

*/
#include <Arduino.h>
#include <Servo.h>
#include <LiquidCrystal.h> 

// Function prototypes
void getDataFromPC();
void parseData();
void replyToPC();
void showCommandLCD();
void run_stepper(int pin_pul, int pin_dir, int steps, int stepper_speed);
void move_pin(int pin_target);
void wait_taster(int input_pin);
void LockMotor();
void DebugMode(int mode);

// Global variables and objects
char prog_version[20] = "V5.0 Work";

//Config LCD
const int rs = 40, en = 41, d4 =46, d5 = 47, d6= 48, d7 = 49;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//Config Serial
const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
bool readInProgress = false;
bool newDataFromPC = false;

//Config Recaived Data
int row = 0;
int command = 0;
long value_1 = 0;
long value_2 = 0;
long value_3 = 0;
long value_4 = 0;

//Config Hardware,Pins
const int xaxis_pul = 2;
const int xaxis_dir = 3;
const int yaxis_pul = 4;
const int yaxis_dir = 5;
const int zaxis_pul = 6;
const int zaxis_dir = 7;
const int move_pin_out1 = 18;
const int move_pin_out2 = 19;
const int button_next_step = 15;  
const int switch_debug_mode = 16;
const byte interrupt_pin_switch1 = 20;
const byte interrupt_pin_switch2 = 21;

volatile int motor_lock = 0;
byte debug_mode = true;

//Config Stepper
const int pulse_width = 20;
int pulse_delay = 500;

// Function definitions
void LockMotor() {
  if (digitalRead(interrupt_pin_switch1) == HIGH) {
    motor_lock = 1;
    Serial.println("Secure switch 1 --> Motor locked"); 
    lcd.setCursor(0, 3);
    lcd.print("Secure switch 1");
  }
  else if (digitalRead(interrupt_pin_switch2) == HIGH) {
    motor_lock = 2;
    Serial.println("Secure switch 2 --> Motor locked"); 
    lcd.setCursor(0, 3);
    lcd.print("Secure switch 2");
  }
  else {
    motor_lock = 0;
    Serial.println("Motor-Free"); 
    lcd.setCursor(0, 3);
    lcd.print("Free ");
  }
}

void getDataFromPC() {
  // receive data from PC and save it into inputBuffer
  //Beispiel aus https://forum.arduino.cc/index.php?topic=225329.msg1810764#msg1810764
    
  if(Serial.available() > 0) {
    char x = Serial.read();

    // the order of these IF clauses is significant   
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//--------------------------------------------------------------------------------------------------------------
//=====================================================SETUP==================================================
//--------------------------------------------------------------------------------------------------------------  
void setup() {
  //Config Pins
  pinMode(xaxis_pul, OUTPUT); 
  pinMode(xaxis_dir, OUTPUT); 
  pinMode(yaxis_pul, OUTPUT); 
  pinMode(yaxis_dir, OUTPUT);
  pinMode(zaxis_pul, OUTPUT); 
  pinMode(zaxis_dir, OUTPUT);
  pinMode(move_pin_out1, OUTPUT);
  pinMode(move_pin_out2, OUTPUT);
  pinMode(button_next_step, INPUT_PULLUP); 
  pinMode(switch_debug_mode, INPUT_PULLUP);
  pinMode(interrupt_pin_switch1, INPUT_PULLUP);
  pinMode(interrupt_pin_switch2, INPUT_PULLUP);

  //Interrupt
  attachInterrupt(digitalPinToInterrupt(interrupt_pin_switch1), LockMotor, RISING);
  attachInterrupt(digitalPinToInterrupt(interrupt_pin_switch2), LockMotor, RISING);

  //Config Serial
  Serial.begin(9600); // set the baud rate
  Serial.println("-*-*-*-*-*-*-*-NEW CONNECTION-*-*-*-*-*-*-*-");
  Serial.print("Version: ");   
  Serial.println(prog_version); 
  Serial.println("<Arduino is ready>"); 

  //Config Display
  lcd.begin(20, 4); // Achtung HiL hat nur (16, 2), alle anderen Zeichen werden auf HiL abgeschnitten
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Version: ");
  lcd.setCursor(9, 0);
  lcd.print(prog_version);
  lcd.setCursor(0, 1);
  lcd.print("Arduino is ready"); 


}
//--------------------------------------------------------------------------------------------------------------
//=====================================================LOOP=================================
//

void loop() {

  getDataFromPC();

  if (newDataFromPC) {   
    //Debug Mode from switch
    DebugMode(digitalRead(switch_debug_mode));
    showCommandLCD();
  
    switch (command) { //TODO: byte wäre auch möglich statt integer
      case 1: //Bender (X-Achse)
        if (debug_mode == true){
          wait_taster(button_next_step); 
        }
        run_stepper(xaxis_pul, xaxis_dir, value_1, value_2);
        break;
  
      case 2: //Turn (Y-Achse)
        if (debug_mode == true){
          wait_taster(button_next_step); 
        }
        run_stepper(yaxis_pul, yaxis_dir, value_1, value_2);
        break;

      case 3: //Feeder (Z-Achse)
        if (debug_mode == true){
          wait_taster(button_next_step); 
        }
        run_stepper(zaxis_pul, zaxis_dir, value_1 * -1, value_2); //value_1 invent because different turning direction
        break;

      case 4: //Linear Motor Pin move up = 1 down = 0
        if (debug_mode == true){
          wait_taster(button_next_step); 
        }
        move_pin(value_1);
        break;

      case 5: //Wait for taster
        wait_taster(button_next_step);
        break;

      case 8: //Wait in ms
        lcd.setCursor(0, 3);
        lcd.print("Wait ms");
        Serial.println("Wait ms");
        delay(value_1); //wait in ms (1000 = 1 second) 
        break;

      case 9: //Change Debug Mode
        DebugMode(value_1);
        break;
          
      default:
        Serial.println("Error: Wrong Command at Seriel in");  
        break;    
    }
    replyToPC(); 
  }
  
  newDataFromPC = false;
}

//============FUNCTIONS=============================

void parseData() {                         // split the data into its parts
    
  char * strtokIndx;                       // this is used by strtok() as an index

  strtokIndx = strtok(inputBuffer,",");    // get the first part - the string
  row = atoi(strtokIndx);                  // convert this part to an integer
  
  strtokIndx = strtok(NULL, ",");          // this continues where the previous call left off
  command = atoi(strtokIndx);              // convert this part to an integer
  
  strtokIndx = strtok(NULL, ",");          // this continues where the previous call left off
  value_1 = atol(strtokIndx);              // convert this part to an integer

  strtokIndx = strtok(NULL, ",");          // this continues where the previous call left off
  value_2 = atol(strtokIndx);              // convert this part to an integer

  strtokIndx = strtok(NULL, ",");          // this continues where the previous call left off
  value_3 = atol(strtokIndx);              // convert this part to an integer
  
  strtokIndx = strtok(NULL, ",");          // this continues where the previous call left off
  //value_4 = atof(strtokIndx);            // for float; Beim Test sind Fehler aufgefallen. sind zu vermeiden. 
  value_4 = atol(strtokIndx);              // convert this part to an integer
}

//=============

void replyToPC() {
  Serial.print("<");
  Serial.print(row);
  Serial.print(", ");
  Serial.print(command);
  Serial.print(", ");
  Serial.print(value_1);
  Serial.print(", ");
  Serial.print(value_2);  
  Serial.print(", ");
  Serial.print(value_3);
  Serial.print(", ");
  Serial.print(value_4); 
  Serial.println(">");
}

//============

void showCommandLCD() { // Bei Text lcd.write sonst lcd.print 
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Row");
  lcd.setCursor(3, 0);
  lcd.print(row);
  lcd.setCursor(8, 0);
  lcd.print("Com");
  lcd.setCursor(11, 0);
  lcd.print(command);
  lcd.setCursor(0, 1);
  lcd.print(value_1);
  lcd.setCursor(9, 1);
  lcd.print(value_2);
  lcd.setCursor(0, 2);
  lcd.print(value_3);
  lcd.setCursor(9, 2);
  lcd.print(value_4);
}

//============

void run_stepper(int pin_pul, int pin_dir, int steps, int stepper_speed) { //Max. 6kHZ möglich
  Serial.println("Stepper is running");
  Serial.print("Status Motorlock before running: ");
  Serial.println(motor_lock); 
  

  //Output Direktion 
  if (steps > 0) {
    digitalWrite(pin_dir, HIGH);
  }
  else {
    digitalWrite(pin_dir, LOW);
  }
  //Calculation delay from frequancy
  pulse_delay = (1000000 / stepper_speed) - pulse_width; //Example:1/2000*1000000-20=480

  long steps_abs = abs(steps) ;
  
  int i = 0;
  while (i < steps_abs && motor_lock == 0) {
    digitalWrite(pin_pul, HIGH);
    delayMicroseconds (pulse_width); 
    digitalWrite(pin_pul, LOW);
    delayMicroseconds (pulse_delay); 
    i++;
  }
  Serial.print("Status Motorlock after stopping: ");
  Serial.println(motor_lock); 
  
  delay(10);
}

//============

void move_pin (int pin_target) {
  Serial.print("Bender Pin is moving to target: ");
  Serial.println(pin_target);  

  if (pin_target == 1){
    digitalWrite(move_pin_out1, LOW);
    digitalWrite(move_pin_out2, HIGH);
  }
  else {
    digitalWrite(move_pin_out1, HIGH);
    digitalWrite(move_pin_out2, LOW);
  }

  delay(1000);
}


void wait_taster (int input_pin){
  lcd.setCursor(0, 3);
  lcd.print("Wait for taster  ");
  Serial.println("Wait for taster");
  
  while(digitalRead(input_pin)==HIGH){}  //wait until taster
  lcd.setCursor(0, 3);
  lcd.print("Taster is pressed"); 
  Serial.println("Taster pressed"); 

  motor_lock = false;
  Serial.println("Motor-Free"); 
  lcd.setCursor(15, 0);
  lcd.print("Free");

}

void DebugMode(int mode){
  if (mode == 1){
    debug_mode = true;
    Serial.println("DEBUG MODE: ON"); 
    lcd.setCursor(11, 3);
    lcd.print("Debug ON");
  }
  else {
    debug_mode = false;
    Serial.println("DEBUG MODE: OFF"); 
    lcd.setCursor(11, 3);
    lcd.print("Debug OFF");
  }
}
