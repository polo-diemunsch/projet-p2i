#include "LSM6DS3.h"
#include "Wire.h"
#include "SPI.h"

typedef struct
{
  int16_t accelero_x;
  int16_t accelero_y;
  uint8_t frequence_cardiaque;
  byte pression_doigts;
} Trame_t;

Trame_t ma_trame;

uint8_t pin_flexi1 = A1;
uint8_t pin_flexi2 = A2;
uint8_t pin_flexi3 = A3;
uint8_t pin_flexi4 = A4;
uint8_t pin_flexi5 = A5;

float v_ref = 0.480;
uint16_t seuil = 500; // Voir pour modifier le Threshold

uint16_t value;

int PulseSensorPurplePin = 0;

bool actif = false;
bool prec = false;
int battement = 0;
int compteur = 0;
int BPM;

int Signal;
int Threshold = 1000;

int16_t tempX;
int16_t tempY;

byte val_flexi;


LSM6DS3Core myIMU(I2C_MODE, 0x6A);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  //Call .beginCore() to configure the IMU
  if (myIMU.beginCore() != 0) {
      Serial.print("\nDevice Error.\n");
  } else {
      Serial.print("\nDevice OK.\n");
  }

  uint8_t dataToWrite = 0;  //Temporary variable

  //Setup the accelerometer******************************
  dataToWrite = 0; //Start Fresh!
  dataToWrite |= LSM6DS3_ACC_GYRO_BW_XL_100Hz;
  dataToWrite |= LSM6DS3_ACC_GYRO_FS_XL_4g;
  dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_104Hz;


  dataToWrite &= ~((uint8_t)LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLED);

}

void loop() {


  myIMU.readRegisterInt16(&tempX, LSM6DS3_ACC_GYRO_OUTX_L_XL)

  myIMU.readRegisterInt16(&tempY, LSM6DS3_ACC_GYRO_OUTY_L_XL)

  Signal = analogRead(PulseSensorPurplePin);

   if (prec != actif) {
     prec = actif;
     if (prec == true){
       battement += 1;
     }
   }



   if(Signal > Threshold){
     actif = true;
   }
   else {
     actif = false;
   }
  compteur += 1;
  if (compteur == 75){
  BPM = battement *8;
  battement = 0;
  compteur = 0;
  }

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

  ma_trame.accelero_x = tempX;
  ma_trame.accelero_y = tempY;
  ma_trame.frequence_cardiaque = BPM;
  ma_trame.pression_doigts = val_flexi;

  delay(100);

}
