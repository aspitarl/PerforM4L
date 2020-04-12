 #include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define pi 3.14159

#define PIN 6
#define stripseg  29
#define striptot  436

int stripNarr[] = {28,29,30,29, 29,29,30,28};

#define numstrips sizeof(stripNarr)/2

int striplocarr[numstrips] = {0};

int selectall[numstrips] = {1,1,1,1, 1,1,1,1};

int stripsel[numstrips] = {0}; 
int stripsel_R[numstrips] = {0,0,0,0, 1,1,1,1};
int stripsel_L[numstrips]  = {1,1,1,1, 0,0,0,0};
int stripsel_mid[numstrips]  = {1,1,0,0, 1,1,0,0};
int stripsel_outer[numstrips]  = {0,0,1,1, 0,0,1,1};



// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)

Adafruit_NeoPixel strip = Adafruit_NeoPixel(striptot, PIN, NEO_GRB + NEO_KHZ800);

uint16_t rainoff[5] = {10, 1, 13, 27, 6};
uint16_t rainpos = 0;

String presetname = "";
String timestring;
String donereadingstr;
unsigned long time1 = 0;
unsigned long time2 = 0;
unsigned long time3 = 0;   
unsigned long dtime23 = 0;
    
int LFO = 0;
int Colorin = 0;
int EnvFollow1  = 0;
int EnvFollow2  = 0;
int General = 0;
int preset = 0;
int midi = 0;
int text = 1;

int LFO_d = 0;
int Colorin_d = 0;
int EnvFollow1_d  = 0;
int EnvFollow2_d  = 0;
int General_d = 0;
int preset_d = 0;
int midi_d = 0;
int text_d = 1;

int cr_d = 0;

float LFOfloat = 0.0;

char serialdummy;
    
int midiprev = 0; //check if midi c

int rainposarray[numstrips] = {0};

int k;
  
void setup() {

  Serial.begin(19200); // open the arduino serial port

  strip.begin(); 
  strip.setBrightness(255);
  strip.show(); // Initialize all pixels to 'off'

        for(k = 1; k<=numstrips ; k++){
        striplocarr[k] = striplocarr[k-1]+stripNarr[k-1]; 
        }
        
        for(k = 0; k<=numstrips ; k++){
        rainposarray[k] = 0;
        }
}

void loop() {
    if (Serial.available() > 0){
        time1 = millis();
        
        LFO_d = Serial.parseInt();
        Colorin_d = Serial.parseInt();
        EnvFollow1_d = Serial.parseInt();
        EnvFollow2_d = Serial.parseInt();
        General_d = Serial.parseInt();
        preset_d = Serial.parseInt();
        midi_d = Serial.parseInt();
        text_d = Serial.parseInt();
        cr_d = Serial.read();
        
        if (cr_d  == 10) {
            LFO = constrain(LFO_d, 0, 255);
            Colorin = constrain(Colorin_d, 0, 255);
            EnvFollow1 = constrain(EnvFollow1_d, 0, 255);
            EnvFollow2 = constrain(EnvFollow2_d, 0, 255);
            General = constrain(General_d, 0, 255);
            preset = constrain( preset_d, 0, 255);
            midi = constrain(midi_d, 0, 255);
            text = constrain(text_d, 0, 255);
                
            LFO = LFO-128;
            LFOfloat = (((float)LFO)+0.5)/128.0;
            
            time2 = millis();
            
            switch(text)
            {
                case 0:
                    timestring = " ";
                    break;
                case 1:
                    timestring = "Preset: " + presetname + "  Time 1-2: " + String(time2-time1) + + " Time 1-3:" + String(dtime23);
                    break;
                case 2:
                    timestring = "Preset: " + presetname + "  LFO: " +String (LFO)+ " Color: " +String (Colorin) + " E1:  " +String (EnvFollow1)+ " E2: " +String (EnvFollow2) + " General: " +String (General) +  " midi:" +String (midi);
                    break;
                default:
                    timestring = "Preset: " + presetname + "  Time 1-2: " + String(time2-time1) + + " Time 1-3:" + String(dtime23);
                    break;
            }
            
            switch(preset)
            {
                case 0:
                    presetname = "ColorBrightWhite";
                    ColorBrightWhite(selectall, Colorin+LFO, EnvFollow1, General,10,0);
                    strip.show();
                    break;
                case 1:
                    presetname = "ColorAndBars";
                    ColorBrightWhite(selectall, Colorin, EnvFollow1, General,0,0);
                    Bars(selectall, EnvFollow2, General);
                    strip.show();
                    break;
                
                  
                case 2:
                    presetname = "Hits";
                    int i;

                    if ( midi == 0){
                        ColorBrightWhite(stripsel_L,Colorin+LFO,  EnvFollow2, 0,0,0);
                        ColorBrightWhite(stripsel_R,Colorin+LFO, 0, 0,0,0);
                    }
                    else if (midi == 1){
                        ColorBrightWhite(stripsel_outer,Colorin+LFO, 0, 0,0,0);
                        ColorBrightWhite(stripsel_mid,Colorin+LFO, EnvFollow2, 0,0,0);
                    }
                    else if (midi == 2){
                        ColorBrightWhite(stripsel_L,Colorin+LFO, 0, 0,0,0);
                        ColorBrightWhite(stripsel_R,Colorin+LFO, EnvFollow2, 0,0,0);
                    }
                    //NU_hits(Colorin, midi , EnvFollow2, 0 );
                    strip.show();
                    break;

                            
                case 3:
                    presetname = "Drop1";
                    ColorBrightWhite(selectall, Colorin+LFO, EnvFollow1, General,10,0);
                    strip.show();
                    break;
                case 4:
                    presetname = "Drop2";
                    ColorBrightWhite(selectall, Colorin+LFO, EnvFollow1, 0,50,General);
                    strip.show();
                    break;
                case 5:
                    presetname = "Solo";
                    ColorBrightWhite(selectall, Colorin+LFO, EnvFollow2, 0,25,General);
                    strip.show();
                    break;

                //Not used yet
                case 9:
                    presetname = "SplitColorBars";
                    ColorBrightWhite(stripsel_R, Colorin, EnvFollow1, General,0,0);
                    ColorBrightWhite(stripsel_L, 0, 0, 0,0,0);
                    Bars(stripsel_L, EnvFollow2, 0 );
                    strip.show();
                    //NU_verse_split(Colorin, LFO, EnvFollow1, EnvFollow2 );
                    break;                   
                case 10:
                    presetname = "Rain";  
                    advancerain();
                    ColorBrightWhite(selectall, Colorin+LFO, EnvFollow2, 0,70,0);  
                    Rain(selectall, 0, EnvFollow1 ,255, rainposarray);
                    strip.show();
                    break;
                case 11:
                    presetname = "Rain 3 wide";  
                    advancerain();
                    ColorBrightWhite(selectall, Colorin+LFO, EnvFollow2, 0,70,0);  
                    Rain_wide(selectall, 0, EnvFollow1 ,255, rainposarray, 3);
                    strip.show();
                    break;
                case 12:
                    presetname = "SingleStrip";  
                    advancerain();
                    ColorBrightWhite(selectall, Colorin, EnvFollow2, 0,70,0);  
                    SingleStrip(midi, Colorin+50, EnvFollow2, 0) ;
                    strip.show();
                    break;
               case 13:
                    presetname = "LFOphase";
                    ColorBrightWhite(selectall, Colorin, EnvFollow1, General,30, LFOfloat);
                    strip.show();
                    break;
                default:
                    presetname = "wheeltest";
                    wheeltest(General);
                    //firsttest(100);
                    break;
        }   
            
            time3 = millis();
            dtime23 = time3-time2;
            
            Serial.println(timestring);

        }
        else{  
            //didn't get return character
            Serial.println("Read Error");
            delay(1000);
            while(Serial.available() > 0){
                serialdummy = Serial.read();
                delay(1);
            }
        }
    }
}


void ColorBrightWhite( int stripselect[],uint16_t basecolor, float bright, float whiteamnt, int spatialLFOamt, float spatialLFOkvec) 
{
    //Formerly NU_Intro
    //1: Base color
    //2: Color Brightness
    //3: Whiteness

    uint32_t color = Wheelwhitebright((basecolor) & 255, bright,  whiteamnt);
    int newbasecolor = basecolor;
     
    uint16_t i ;
    uint16_t j ;
    uint16_t loc ;
    for( j=0; j<numstrips; j++){
        if(stripselect[j] == 1 ){
            if(spatialLFOamt != 0){
                newbasecolor = (basecolor + int(spatialLFOamt*cos((spatialLFOkvec*5)*(j/float(numstrips))*2*pi))) & 255;
                color = Wheelwhitebright(newbasecolor & 255, bright,  whiteamnt );                
            }
            for( i=0; i<stripNarr[j]; i++) {
                loc = striplocarr[j]+stripNarr[j] - i-1;
                //----Action----
                strip.setPixelColor(loc, color);
            }
        }
    }   
    
}


void Bars(int stripselect[], uint16_t barsloc, uint16_t barscolor) 
{
    uint32_t bars = Wheel(barscolor);

    barsloc = (uint16_t)((((float)barsloc)/255)   *stripseg);

    uint16_t i ;
    uint16_t j ;
    uint16_t loc ;
    for( j=0; j<numstrips; j++){
        if(stripselect[j] == 1 ){  
              for( i=0; i<stripNarr[j]; i++) {
                    loc = striplocarr[j]+stripNarr[j] - i-1;
                    //----Action----
                    if(i < barsloc ){
                        strip.setPixelColor(loc, bars);
                    }
              }
        } 
    }
    
}


void Rain(int stripselect[],uint16_t basecolor, float bright, float whiteamnt,  int rainposarray[]) 
{  

//For some insane reason this function cannot becalled twice and you have to make a duplicate with a different name. 
    uint32_t color = Wheelwhitebright((basecolor) & 255, bright,  whiteamnt);

    uint16_t i ;
    uint16_t j ;
    uint16_t loc ;
    for( j=0; j<numstrips; j++){
        if(stripselect[j] == 1 ){  
              for( i=0; i<stripNarr[j]; i++) {
                    loc = striplocarr[j]+stripNarr[j] - i-1;
                    //----Action----
                    if(i == (rainposarray[j]%stripseg)){
                        strip.setPixelColor(loc, color);
                    }
              }
        } 
    }
    
} 


void Rain_wide(int stripselect[],uint16_t basecolor, float bright, float whiteamnt,  int rainposarray[], int wide) 
{  

//For some insane reason this function cannot becalled twice and you have to make a duplicate with a different name. 
    uint32_t color = Wheelwhitebright((basecolor) & 255, bright,  whiteamnt);

    uint16_t i ;
    uint16_t j ;
    uint16_t loc ;

    
    for( j=0; j<numstrips; j++){
        if(stripselect[j] == 1 ){  
              for( i=0; i<stripNarr[j]; i++) {
                    loc = striplocarr[j]+stripNarr[j] - i-1;
                    //----Action----
                    //if(i == (rainposarray[j]%stripNarr[j]) || i == ((rainposarray[j]%stripNarr[j])+1) || i == ((rainposarray[j]%stripNarr[j])-1))
                    if(abs(i - (rainposarray[j]%stripNarr[j])) <  wide )
                    {
                      strip.setPixelColor(loc, color);
                    }
              }
        } 
    }
    
} 

void SingleStrip( int stripnum, uint16_t basecolor, float bright_strip,  float whiteamnt) 
{
uint16_t i ;
uint16_t j ;
uint16_t loc ;

uint32_t color_strip = Wheelwhitebright((basecolor+LFO+100) & 255, bright_strip,  whiteamnt );

for( j=0; j<numstrips; j++){
    for( i=0; i<stripNarr[j]; i++) {
        loc = striplocarr[j]+stripNarr[j] - i-1;
            if(j == stripnum){
                strip.setPixelColor(loc, color_strip);
            }
        } 
    }
    
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


void firsttest(uint16_t color) 
{
  for(uint16_t j=0; j<numstrips; j++){
    
        strip.setPixelColor(striplocarr[j], color);    
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


void advancerain()
{
              for(k = 0; k<numstrips ; k++)
            {
                if( (k==midi || k == (midi + 5) || k == (midi + 10)) && (midi != midiprev) )
                {
                    if(midi != midiprev){
                      rainposarray[midi] = 0;
                      rainposarray[midi+5] = 0;
                      rainposarray[midi+10] = 0;
                    }                  
                }
                else
                {
              rainposarray[k] = rainposarray[k] +1;
                }
            }
          midiprev = midi; 
}



