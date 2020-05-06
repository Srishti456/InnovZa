/*************************************************************
  Download latest Blynk library here:
    https://github.com/blynkkk/blynk-library/releases/latest

  Blynk is a platform with iOS and Android apps to control
  Arduino, Raspberry Pi and the likes over the Internet.
  You can easily build graphic interfaces for all your
  projects by simply dragging and dropping widgets.

    Downloads, docs, tutorials: http://www.blynk.cc
    Sketch generator:           http://examples.blynk.cc
    Blynk community:            http://community.blynk.cc
    Follow us:                  http://www.fb.com/blynkapp
                                http://twitter.com/blynk_app

  Blynk library is licensed under MIT license
  This example code is in public domain.

 *************************************************************
  =>
  =>          USB HOWTO: http://tiny.cc/BlynkUSB
  =>

  Rotate a servo using a slider!

  App project setup:
    Slider widget (0...180) on V3
 *************************************************************/

/* Comment this out to disable prints and save space */
#define BLYNK_PRINT SwSerial


#include <SoftwareSerial.h>
SoftwareSerial SwSerial(10, 11); // RX, TX
    
#include <BlynkSimpleStream.h>
#include <Servo.h>

// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "SwQwzjk9QbWxLIy8IjblDjQkD0IWXa81";

Servo servo1;
Servo servo2;
Servo servo3;



BLYNK_WRITE(V10)
{
   if(param.asInt())
  {

servo1.write(30);
servo1.write(0);
servo3.write(0);
    delay(1000);
}

     else
{
    
    servo1.write(50);
    servo2.write(100);
    delay(2000);
    
    servo1.write(150);
    delay(2000);
    servo1.write(50);
    delay(2000);
    servo3.write(180);
    delay(2000);
    servo2.write(10);
    delay(2000);
    
    servo3.write(30);
    delay(2000);
    servo2.write(100);
    delay(2000);
    servo1.write(30);
    delay(2000);
    
    
  }
}

BLYNK_WRITE(V11)
{
  if(param.asInt())
  {

servo1.write(30);
servo1.write(0);
servo3.write(0);
    delay(1000);
}

     else
{
    
    servo1.write(50);
    servo2.write(100);
    delay(2000);
    delay(2000);
    servo1.write(150);
    delay(2000);
    servo1.write(50);
    delay(2000);
    servo1.write(150);
    delay(2000);
    servo3.write(180);
    delay(2000);
    servo2.write(10);
    delay(2000);
    servo3.write(20);
    delay(2000);
    servo2.write(100);
    delay(2000);
    servo1.write(30);
    delay(2000);
    
    
  }
}


BLYNK_WRITE(V5)
{
  if(param.asInt())
  {


servo3.write(180);
    delay(1000);
}

     else
{
    
    
    servo3.write(10);
    delay(2000);
    
    
  }
}

BLYNK_WRITE(V3)
{
  if(param.asInt())
  {


servo1.write(180);
    delay(1000);
}

     else
{
    
    
    servo1.write(10);
    delay(2000);
    
    
  }
}


BLYNK_WRITE(V4)
{
  if(param.asInt())
  {


servo2.write(180);
    delay(1000);
}

     else
{
    
    
    servo2.write(10);
    delay(2000);
    
    
  }
}


void setup()
{
  // Debug console
  SwSerial.begin(9600);

  // Blynk will work through Serial
  // Do not read or write this serial manually in your sketch
  Serial.begin(9600);
  Blynk.begin(Serial, auth);
   servo1.attach(9);
   servo2.attach(10);
   servo3.attach(11);
}

void loop()
{
  Blynk.run();
}

