 #include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define pi 3.14159

#define PIN 3


// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)

Adafruit_NeoPixel strip = Adafruit_NeoPixel(30, PIN, NEO_GRB + NEO_KHZ800);

int x = 0;
int y = 0;
int z = 0;
int nl = 0;
char string[] ="";

char serialdummy;

unsigned long LFO = 0;

int inv255 = 1/255;

int period = 1000;

uint16_t k;
  
void setup() {

  Serial.begin(9600); // open the arduino serial port
  //Serial.begin(9600); // open the arduino serial port

  strip.begin(); 
  strip.setBrightness(80);
  strip.show(); // Initialize all pixels to 'off'

}

void loop() {

  

  // read from port 1, send to port 0:
  if (Serial.available()>3) {
    x = 2*Serial.read();
    y = 2*Serial.read();
    z = 2*Serial.read();
    nl = Serial.read();
    

   LFO = sin((2*pi*millis())/period);
    
    NU_intro((x+(20*LFO))&255, (y)&255, 0);

   if(nl != 10){
      
          while(Serial.available() > 0 && nl != 10)
          {
            nl = Serial.read();
            //delay(1);
          }
   }
  }


}





void NU_intro(uint16_t basecolor, float bright, float whiteamnt) 
{
  uint16_t i ; 

  uint32_t color = Wheelwhitebright((basecolor) & 255, bright,  whiteamnt);
  
    for(i=0; i< strip.numPixels(); i++) { 
       strip.setPixelColor(i, color); 
    }
    strip.show();

}




//Functions



void wheeltest(uint16_t color) 
{
  uint16_t i ;  
    for(i=0; i< strip.numPixels(); i++) { 
       strip.setPixelColor(i, Wheel(color)); 
    } 
    strip.show();
} 




uint32_t Wheel(byte WheelPos) 
{
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

uint32_t Wheelwhite(byte WheelPos, float whiteamnt) 
{
  float wa = whiteamnt/255;
  float ca = 1 - wa;
  
  WheelPos = 255 - WheelPos;

  if(WheelPos < 85) {
    return strip.Color(ca*(255 - WheelPos * 3) + whiteamnt   , whiteamnt    ,     (ca*WheelPos * 3)  + whiteamnt   );
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(whiteamnt, (ca*WheelPos * 3)  + whiteamnt, ca*(255 - WheelPos * 3) + whiteamnt);
  }
  WheelPos -= 170;
  return strip.Color((ca*WheelPos * 3)  + whiteamnt, ca*(255 - WheelPos * 3) + whiteamnt, whiteamnt);
}


uint32_t Wheelbright(byte WheelPos, float bright) 
{
  bright = bright/255;
  
  WheelPos = 255 - WheelPos;

  if(WheelPos < 85) {
    return strip.Color(bright*(255 - WheelPos * 3), 0, bright*(WheelPos * 3));
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, bright*(WheelPos * 3), bright*(255 - WheelPos * 3));
  }
  WheelPos -= 170;
  return strip.Color(bright*(WheelPos * 3), bright*(255 - WheelPos * 3), 0);
}


uint32_t Wheelwhitebright(byte WheelPos, float bright, float whiteamnt ) 
{
  
  float ca = 1 -(whiteamnt/255);
  bright = bright /255;
  
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
  

    
    return strip.Color( (ca*(255 - WheelPos * 3) + whiteamnt)*bright   , whiteamnt*bright    ,     ((ca*WheelPos * 3)  + whiteamnt)*bright   );
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(whiteamnt*bright ,         ((ca*WheelPos * 3)  + whiteamnt)*bright,         (ca*(255 - WheelPos * 3) + whiteamnt)*bright);
  }
  WheelPos -= 170;
  return strip.Color(((ca*WheelPos * 3)  + whiteamnt)*bright,      (ca*(255 - WheelPos * 3) + whiteamnt)*bright ,       whiteamnt*bright);
}





