#include <RadioLib.h>

SX1276 radio = new Module(LORA_IRQ_DUMB, LORA_IRQ, RADIOLIB_NC, RADIOLIB_NC, SPI1, SPISettings(200000, MSBFIRST, SPI_MODE0));
float frequency= 869.0;
float rxBw = 250; 
int8_t pwr = 10;
uint16_t preambleLength = 16; // 8; 16;   nb of bits, must be a multiple of 8 => succession of 10101010... preambleLength = 0,8,16,24 etc
bool enableOOK =  false; //true ;     // true => OOK; false => FSK;
float freqDev = 70;           // frequency deviation :0.6 to 200.0 kHz; FreqDev + BitRate/2 <= 250 kHz must be always met.
float br = 5;                 // bit rate 1.2 to 300.0 kbps.

// number of bytes of ma_trame
const int size_ma_trame = 6;

byte byteArr[size_ma_trame];

void setup() {
  Serial.begin(115200);
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
  int state = radio.receive(byteArr, size_ma_trame);

  if (state == RADIOLIB_ERR_NONE) {
    // packet was successfully received

    // print the data of the packet
    Serial.write((byte*)&byteArr, sizeof(byteArr));
    Serial.println();
    // for(int i; i < 15; i++) {
    //   Serial.print(byteArr[i]);
    // }
    // Serial.println();
  }
}
