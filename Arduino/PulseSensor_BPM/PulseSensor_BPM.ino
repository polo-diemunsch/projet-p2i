
/*  PulseSensor Starter Project and Signal Tester
 *  The Best Way to Get Started  With, or See the Raw Signal of, your PulseSensor.com™ & Arduino.
 *
 *  Here is a link to the tutorial
 *  https://pulsesensor.com/pages/code-and-guide
 *
 *  WATCH ME (Tutorial Video):
 *  https://www.youtube.com/watch?v=RbB8NSRa5X4
 *
 *
-------------------------------------------------------------
1) This shows a live human Heartbeat Pulse.
2) Live visualization in Arduino's Cool "Serial Plotter".
3) Blink an LED on each Heartbeat.
4) This is the direct Pulse Sensor's Signal.
5) A great first-step in troubleshooting your circuit and connections.
6) "Human-readable" code that is newbie friendly."

*/


//  Variables
int PulseSensorPurplePin = 0;        // Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
int LED = LED_BUILTIN;   //  The on-board Arduion LED

bool actif = false;
bool prec = false;
int battement = 0;
int compteur = 0;
int BPM;


int Signal;                // holds the incoming raw data. Signal value can range from 0-1024
int Threshold = 1000;       // Determine which Signal to "count as a beat", and which to ingore.


// The SetUp Function:
void setup() {
  pinMode(LED,OUTPUT);         // pin that will blink to your heartbeat!
   Serial.begin(9600);         // Set's up Serial Communication at certain speed.

}

// The Main Loop Function
void loop() {

  Signal = analogRead(PulseSensorPurplePin);  // Read the PulseSensor's value.
                                              // Assign this value to the "Signal" variable.
   if (prec != actif) {
     prec = actif;
     if (prec == true){
       battement += 1;
     }
   }
                       // Send the Signal value to Serial Plotter.


   if(Signal > Threshold){                          // If the signal is above "550", then "turn-on" Arduino's on-Board LED.
     actif = true;
   } 
   else {
     actif = false;               //  Else, the sigal must be below "550", so "turn-off" this LED.
   }
compteur += 1;
if (compteur == 75){
BPM = battement *8;
battement = 0;
compteur = 0;  
}
Serial.print(compteur);
Serial.print(", ");
Serial.println(BPM);

delay(100);


}
