//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                  Teste de comunicão Serial
//
//   build 17/09/2024 by Raul
//   v0.1 REV. 000
//   Arrduino IDE 2.3.3
//
//    Arduino Uno
//    LCD nKeypad Shild
//
//
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Bibliotecas
#include <SPI.h>
#include <DMD.h>
#include <TimerOne.h>
#include "SystemFont5x7.h"
#include "Arial_black_16.h"
#include "Arial14.h"

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Definições
#define DISPLAYS_ACROSS 1
#define DISPLAYS_DOWN 1

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
String RX;
String str;
char b[8];
DMD dmd(DISPLAYS_ACROSS, DISPLAYS_DOWN);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Prototipos
void ScanDMD() {
  dmd.scanDisplayBySPI();
}
void display();
void teste();
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Confiruração
void setup() {

  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  Timer1.initialize(5000);
  Timer1.attachInterrupt(ScanDMD);
  dmd.clearScreen(true);
  Serial.print("Teste comunicacao");
  teste();
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Loop Principal
void loop() {

  /*---------------------------------------  serial  -------------------------------------*/
  while (Serial.available()) {
    Serial.println(RX);
    RX = Serial.readString();  // read the incoming data as string
    display();
  }
}
void display() {
  int slen = 0;
  dmd.clearScreen(true);
  /*---------------------------------------  Display using SystemFont  -------------------------------------*/
  dmd.selectFont(SystemFont5x7);
  str = "Velo.";
  slen = str.length() + 1;
  str.toCharArray(b, slen);
  dmd.drawString(1, 0, b, slen, GRAPHICS_NORMAL);
  str = "KM/h";
  slen = str.length() + 1;
  str.toCharArray(b, slen);
  dmd.drawString(1, 8, b, slen, GRAPHICS_NORMAL);
  delay(500);
  dmd.clearScreen(true);
  //delay(100);

  /*----------------------------------  Display using  Arial14  -------------------------------------------- */
  dmd.selectFont(Arial_Black_16);
  str = RX;
  slen = str.length() + 1;
  str.toCharArray(b, slen);
  dmd.drawString(6, 1, b, slen, GRAPHICS_NORMAL);
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
void teste() {
 int slen = 0;
  dmd.clearScreen(true);
  /*---------------------------------------  Display using SystemFont  -------------------------------------*/
  dmd.selectFont(SystemFont5x7);
  str = "Em";
  slen = str.length() + 1;
  str.toCharArray(b, slen);
  dmd.drawString(1, 0, b, slen, GRAPHICS_NORMAL);
  str = "Teste";
  slen = str.length() + 1;
  str.toCharArray(b, slen);
  dmd.drawString(1, 8, b, slen, GRAPHICS_NORMAL);
  //delay(1000);
  //dmd.clearScreen(true);
  //delay(1000);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Fim