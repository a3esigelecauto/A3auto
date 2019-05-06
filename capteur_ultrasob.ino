const unsigned int TRIG_PIN=13; // trigger sur le pin 13
const unsigned int ECHO_PIN=12; // echo sur le pin 12 
const unsigned int BAUD_RATE=9600; //vitesse de transmission du capteur, 9600 bits/secondes

void setup() {
  pinMode(TRIG_PIN, OUTPUT); 
  pinMode(ECHO_PIN, INPUT);  
  Serial.begin(BAUD_RATE);  
}

void loop() {
  digitalWrite(TRIG_PIN, LOW); //envoie + retour du signal  
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); 
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  

 const unsigned long duration= pulseIn(ECHO_PIN, HIGH); // variable pour le délais aller/retour du signal
 int distance= duration/58; //Le SRF05 fournit une impulsion d'écho proportionnelle à la distance. Si la largeur de l'impulsion est
                            //mesurée en µS alors une division par 58 donnera la distance en cm 

 if(duration==0){
   Serial.println("pas de réponse");
   } 
  else{
      Serial.print("Distance de l'object:");
      Serial.println(distance);
      Serial.println(" cm");
  }
 delay(100);
 }
