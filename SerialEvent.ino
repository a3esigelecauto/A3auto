//othor : Loïc Boillod
//date : 02/05/2019
//title : Uart communication and control motor functions with Arduino uno.
#include <PWM.h>

int pin_motor_speed = 9; //the pin that the motor for speed is attached to.
int pin_motor_direction = 10; //the pin that the motor for direction is attached to.
int32_t frequency = 62; //frequency (in Hz)
int message;
uint8_t error = 0;
int flag=0;
const unsigned int TRIG_PIN=13;
const unsigned int ECHO_PIN=12;

const int messages_len=8; //sets the number of bytes of the messages betaween arduino and RaspberryPi.
byte readed_message[messages_len];
int distance=0;
void setup() {  
    Serial.begin(115200); //sets the baud rate (bit/s)
    Serial.setTimeout(0);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    InitTimersSafe(); //initialize all timers except for 0, to save time keeping functions
    bool motor_speed_success = SetPinFrequencySafe(pin_motor_speed, frequency); //sets the frequency for the specified pin  
    bool motor_direction_success = SetPinFrequencySafe(pin_motor_direction, frequency); //sets the frequency for the specified pin  
    pwmWriteHR(pin_motor_direction, 5500);//sets the angle of the weels at the mid.
    pwmWriteHR(pin_motor_speed, 6000); //sets the speed of the weels at 0.
    delay(3000);
}
uint8_t speed_motor(uint16_t final_speed){ //final_speed betwen 0 and 100.
    final_speed=(final_speed*20)+6000; //convertion 
    if ((final_speed<=8000) && (final_speed>=5000)){
      pwmWriteHR(pin_motor_speed, final_speed);//set the PWM
    return 0;
    }
    return 1; //error value
}
uint8_t direction_motor(uint16_t final_angle){ //final_angle betwen 0(right), 50(mid) and 100(left)  
    final_angle=(final_angle*22)+5000; //convertion
    if ((final_angle<=7200) && (final_angle>=5000)){
      pwmWriteHR(pin_motor_direction, final_angle); //set the PWM 
    return 0; 
    }
    return 1; //error value
}

uint8_t backward(){ //final_speed betwen 0 and 100.
      pwmWriteHR(pin_motor_speed, 3000);//set the PWM
    return 0;
    }
uint8_t read_message(void){
  if (Serial.available()) {     
    message=Serial.read();
    return 0;   
  }
  return 1; //error value
}
int uls() 
{ digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  

 const unsigned long duration= pulseIn(ECHO_PIN, HIGH,15);
 int distance= duration/29/2;
 if(duration==0){
   return 0;
   } 
  else{
      return distance ;
  }
 }
void loop() {
  flag++;
   if (Serial.available())  {
    message = Serial.parseInt();
      if ((message > 100) &&(message<200)) {
    
      speed_motor(message-100);
    }
    else if ((message>200) &&(message<255)){
      backward();
    }
    else if ((message<100) &&){
      direction_motor(message);
  }}
  
  if (flag>=10){
    flag=0;
  distance=uls();
  if(distance==0){
    //Serial.println(distance);
  }}delay(20);
  
}
