byte seg[2][4] = {{11, 10, 9, 8}, {7, 6, 5, 4}};
byte binario[10][4] = {
  {0, 0, 0, 0}, 
  {0, 0, 0, 1}, 
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 1, 0, 0},
  {0, 1, 0, 1},
  {0, 1, 1, 0},
  {0, 1, 1, 1},
  {1, 0, 0, 0}, 
  {1, 0, 0, 1}
};
  


void setup() {
   Serial.begin(9600);
  Serial.println("Readly");
  for (int j = 0; j < 2; j++){
    for (int i = 0; i<4 ;i++)
      pinMode(seg[j][i], OUTPUT);
  }
}

void loop() {
  Serial.println("cont");
  for (int o = 0; o < 10; o++){
    Serial.println(o);
    for (int j = 0; j < 10; j++){
      for (int i = 0; i < 4 ;i++){
        Serial.println(i);
        digitalWrite(seg[0][i], binario[o][i]);
        digitalWrite(seg[1][i], binario[j][i]);
        
      }

      delay(800);
    }
  }
}