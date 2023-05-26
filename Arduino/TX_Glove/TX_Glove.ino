#include "LSM6DS3.h"
#include "Wire.h"
#include "SPI.h"
#include <RadioLib.h>

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

uint16_t value1;
uint16_t value2;
uint16_t value3;
uint16_t value4;
uint16_t value5;

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


SX1276 radio = new Module(LORA_IRQ_DUMB, LORA_IRQ, RADIOLIB_NC, RADIOLIB_NC, SPI1, SPISettings(200000, MSBFIRST, SPI_MODE0));
float frequency= 869.0;
float rxBw = 250; 
int8_t pwr = 10;
uint16_t preambleLength = 16; // 8; 16;   nb of bits, must be a multiple of 8 => succession of 10101010... preambleLength = 0,8,16,24 etc
bool enableOOK =  false; //true ;     // true => OOK; false => FSK;
float freqDev = 70;           // frequency deviation :0.6 to 200.0 kHz; FreqDev + BitRate/2 <= 250 kHz must be always met.
float br = 5;                 // bit rate 1.2 to 300.0 kbps.

unsigned long time0;

LSM6DS3Core myIMU(I2C_MODE, 0x6A);

void setup() {
  Serial.begin(9600);

  //Call .beginCore() to configure the IMU
  myIMU.beginCore();

  uint8_t dataToWrite = 0;  //Temporary variable

  //Setup the accelerometer******************************
  dataToWrite = 0; //Start Fresh!
  dataToWrite |= LSM6DS3_ACC_GYRO_BW_XL_100Hz;
  dataToWrite |= LSM6DS3_ACC_GYRO_FS_XL_4g;
  dataToWrite |= LSM6DS3_ACC_GYRO_ODR_XL_104Hz;


  dataToWrite &= ~((uint8_t)LSM6DS3_ACC_GYRO_BW_SCAL_ODR_ENABLED);

  
  // Reset Modem (thank you sandeepmistry and associates)
  pinMode(LORA_IRQ_DUMB, OUTPUT);
  digitalWrite(LORA_IRQ_DUMB, LOW);

  // Hardware reset
  pinMode(LORA_BOOT0, OUTPUT);
  digitalWrite(LORA_BOOT0, LOW);

  pinMode(LORA_RESET, OUTPUT);
  digitalWrite(LORA_RESET, HIGH);
  delay(200);
  digitalWrite(LORA_RESET, LOW);
  delay(200);
  digitalWrite(LORA_RESET, HIGH);
  delay(50);

  // start SPI
  SPI1.begin();
  
  // initialize SX1276
  int16_t state =  radio.beginFSK(frequency, br, freqDev, rxBw,pwr, preambleLength,enableOOK);
}

void loop() {
  time0 = millis();
  
  myIMU.readRegisterInt16(&tempX, LSM6DS3_ACC_GYRO_OUTX_L_XL);

  myIMU.readRegisterInt16(&tempY, LSM6DS3_ACC_GYRO_OUTY_L_XL);

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

  val_flexi = 0;
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

  int state = radio.transmit((byte*)&ma_trame,  sizeof(ma_trame));

  // if (state == RADIOLIB_ERR_NONE) {
  //   // the packet was successfully transmitted
  //   Serial.println(F(" success!"));

  //   // print measured data rate
  //   Serial.print(F("[SX1276] Datarate:\t"));
  //   Serial.print(radio.getDataRate());
  //   Serial.println(F(" bps"));

  // } else if (state == RADIOLIB_ERR_PACKET_TOO_LONG) {
  //   // the supplied packet was longer than 256 bytes
  //   Serial.println(F("too long!"));

  // } else if (state == RADIOLIB_ERR_TX_TIMEOUT) {
  //   // timeout occurred while transmitting packet
  //   Serial.println(F("timeout!"));

  // } else {
  //   // some other error occurred
  //   Serial.print(F("failed, code "));
  //   Serial.println(state);

  // }

  while (millis() - time0 < 100);
}
