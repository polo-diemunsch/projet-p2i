#include "Fixed16FFT.h"

uint8_t pin_micro = A0;
unsigned long time0;
unsigned long time1;

const int offset = 336;
const int N = 512;
float frequency;

five_frequencies ma_trame;

fixed_t data[N];
int i = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  time0 = micros();
}

void loop() {

  data[i] = analogRead(pin_micro) - offset;
  // data[i] = analogRead(pin_micro);

  if (i == N-1) {
    time1 = micros();
    
    i = -1;
    
    run_fft();
    // delay(400);
    // Serial.println(time1 - time0);

    time0 = micros();

    // for (int j = 0; j < 256; j++) {
    //   Serial.print(data[j]);
    //   Serial.print(", ");
    // }
    // Serial.println();

    // for (int j = 0; j < 256; j++) {
    //   Serial.print(data_fft[j]);
    //   Serial.print(", ");
    // }
    // Serial.println();
  }
  
  i++;
}

void run_fft() {
  frequency = (float)N * 1000000.0 / (float)(time1 - time0);
  // Serial.print(F("Fréquence d'échantillonnage : "));
  // Serial.print(frequency);
  // Serial.println(F(" Hz"));

  Fixed16FFT FFT = Fixed16FFT();
  FFT.fft(data, N);
  
  // Serial.print(F("Fréquence principale du signal audio : "));
  // Serial.println(FFT.modulus(data, N, frequency));
  // Serial.println(F(" Hz"));
  // Serial.println();

  ma_trame = FFT.five_max_frequencies(data, N, frequency);
  Serial.write((byte*)&ma_trame, sizeof(ma_trame));

  // Serial.print(ma_trame.frequencies[0]);
  // Serial.print(" ");
  // Serial.print(ma_trame.frequencies[1]);
  // Serial.print(" ");
  // Serial.print(ma_trame.frequencies[2]);
  // Serial.print(" ");
  // Serial.print(ma_trame.frequencies[3]);
  // Serial.print(" ");
  // Serial.print(ma_trame.frequencies[4]);
  // Serial.println();
  // Serial.println();
}
