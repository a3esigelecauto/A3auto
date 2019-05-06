// author MBANA Marlin
// date: 06/05/2019
// title: gestion de la motorisation
#include <Servo.h> 
 

Servo myservo;     

Servo moteur;

char info;        

char info1;       

void setup(){


  myservo.attach(10);        // relier le servo au pin9

  moteur.attach(9);  // relier le moteur au pin10

  Serial.begin(250000);      // pour baud-rate

  moteur.write(1500);

  delay(4000);            //temps d'initialisation

}



void loop(){



if (Serial.available()) {

  info=Serial.read();

   if(info=='i')

{ moteur.writeMicroseconds(1500);

 

}

  else if(info=='m')

{ moteur.writeMicroseconds(1500);

 myservo.write(135);

}



else if(info=='f')

{

  moteur.writeMicroseconds(1500);

}



else if (info=='q')

{

  myservo.write(135); 

}

else if(info=='d')

{

   myservo.write(45);

}

else if(info=='c')

{

  myservo.write(90);

}



else if(info=='z')

{

  moteur.writeMicroseconds(1595);



}

else

{ 

  moteur.write(1350);

}

}

}
