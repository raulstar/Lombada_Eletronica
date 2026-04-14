#include <FastLED.h>
 
// How many leds in your strip?
#define NUM_LEDS 1
 
 
#define DATA_PIN 18
 
 
// Define the array of leds
CRGB leds[NUM_LEDS];
 
void setup() { 
    // Uncomment/edit one of the following lines for your leds arrangement.
    // ## Clockless types ##
    FastLED.addLeds<WS2816, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
}
 
void loop() { 
  // Turn the LED on, then pause
  leds[0] = CRGB::Red;
  FastLED.show();
  delay(500);
  // Now turn the LED off, then pause
  leds[0] = CRGB::Black;
  FastLED.show();
  delay(500);
}