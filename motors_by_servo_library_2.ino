//othor : MBANA MARLIN

//date : 06/05/2019

//title : Uart communication and control motor functions with Arduino uno.


#include <Servo.h>

Servo motor_speed;     

Servo motor_direction;


int32_t frequency = 62; //frequency (in Hz)

int message;

uint8_t error = 0;

int flag=0;

const unsigned int TRIG_PIN=13;

const unsigned int ECHO_PIN=12;



const int messages_len=8; //sets the number of bytes of the messages between arduino and RaspberryPi.

byte readed_message[messages_len];

int distance=0;

void setup() {  
    motor_direction.attach(10);        // attaches the servo on pin 10 to the servo object

    motor_speed.attach(9);  // attaches the motor on pin 10 to the motor object


    Serial.begin(115200); //sets the baud rate (bit/s)

    Serial.setTimeout(0);

    pinMode(TRIG_PIN, OUTPUT);

    pinMode(ECHO_PIN, INPUT);

    motor_speed.write(1500);

    motor_direction.write(90);

    delay(3000);

}

uint16_t speed_motor(uint16_t final_speed){ 

   if ((final_speed>=1400) && (final_speed<=10000)){

      motor_speed.write(final_speed);
    return 0;

    }

    return 1; //error value

}

uint8_t direction_motor(uint8_t final_angle){ //final_angle between 0 and 180  

    if ((final_angle<=180) && (final_angle>=0)){

      motor_direction.write(final_angle);

    return 0; 

    }

    return 1; //error value

}



uint16_t backward(void){ 

     motor_speed.write(1400);

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

      if ((message > 50) &&(message<140)) {
        
      direction_motor(message);

    }


    else if ((message>=1400)&&(message<=2000)){

      speed_motor(message);

  }
   else if ((message>=500)&&(message<=1000)){
    
      backward();}
      
     
   }

  

  if (flag>=10){

    flag=0;

  distance=uls();

  if(distance==0){

    //Serial.println(distance);

  }}delay(20);

  

 
}
