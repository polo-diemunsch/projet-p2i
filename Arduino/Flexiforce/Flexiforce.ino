uint8_t pin_flexi1 = A1;
uint8_t pin_flexi2 = A2;
uint8_t pin_flexi3 = A3;
uint8_t pin_flexi4 = A4;
uint8_t pin_flexi5 = A5;

float v_ref = 0.480;
uint16_t seuil = 500;

uint16_t value;
byte val_flexi


void setup() {
  Serial.begin(9600);
}

void loop() {
  val_flexi = 0
  value1 = analogRead(pin_flexi1);
  value2 = analogRead(pin_flexi2);
  value3 = analogRead(pin_flexi3);
  value4 = analogRead(pin_flexi4);
  value5 = analogRead(pin_flexi5);
  
  if (value1 > seuil) {
      val_flexi += 1;
  }
  if (value2 > seuil) {
      val_flexi += 2;
  }
  if (value3 > seuil) {
      val_flexi += 4;
  }
  if (value4 > seuil) {
      val_flexi += 8;
  }
  if (value5 > seuil) {
      val_flexi += 16;
  }


  delay(100);
}