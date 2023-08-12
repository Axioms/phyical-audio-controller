#include "Adafruit_seesaw.h"
#include <seesaw_neopixel.h>
#include <ArduinoJson.h>
#include <time.h>

#define SS_SWITCH 24 // this is the pin on the encoder connected to switch
#define SS_NEOPIX 6  // this is the pin on the encoder connected to neopixel

#define SEESAW_BASE_ADDR 0x36 // I2C address, starts with 0x36
#define DEBOUNCE_BUTTON_PRESS_MILLS 5000
#define BAUDRATE 1000000
#define ENCODER_AMOUNT 5
#define SYNC_INTERVAL 60000

/*********
 * {
 *   "a": "volume",  // Action volume/press/sync
 *   "v": 100,       // volume 0-100
 *   "p": false,     // pressed true/false
 *   "e": 0          // encoder #
 * }
 ***********/

// create 5 encoders!
Adafruit_seesaw encoders[ENCODER_AMOUNT];
// create 5 encoder pixels
seesaw_NeoPixel encoder_pixels[ENCODER_AMOUNT] = {
    seesaw_NeoPixel(1, SS_NEOPIX, NEO_GRB + NEO_KHZ800),
    seesaw_NeoPixel(1, SS_NEOPIX, NEO_GRB + NEO_KHZ800),
    seesaw_NeoPixel(1, SS_NEOPIX, NEO_GRB + NEO_KHZ800),
    seesaw_NeoPixel(1, SS_NEOPIX, NEO_GRB + NEO_KHZ800),
    seesaw_NeoPixel(1, SS_NEOPIX, NEO_GRB + NEO_KHZ800)};
void Seed();
void splitStringToVector(String msg);
bool previouslyPressed = false;
unsigned long previouslyPressedTime;
StaticJsonDocument<64> resultJson;
int32_t encoder_positions[] = {0, 0, 0, 0, 0};
bool found_encoders[] = {false, false, false, false, false};
unsigned long lastSyncTime;
void setup()
{
  Serial.begin(BAUDRATE);

  // wait for serial port to open
  while (!Serial)
  {
    delay(10);
  }

  Serial.println("Looking for seesaws!");

  for (uint8_t enc = 0; enc < sizeof(found_encoders); enc++)
  {
    // See if we can find encoders on this address
    if (!encoders[enc].begin(SEESAW_BASE_ADDR + enc) ||
        !encoder_pixels[enc].begin(SEESAW_BASE_ADDR + enc))
    {
      // Serial.print("Couldn't find encoder #");
      // Serial.println(enc);
    }
    else
    {
      // Serial.print("Found encoder + pixel #");
      // Serial.println(enc);

      uint32_t version = ((encoders[enc].getVersion() >> 16) & 0xFFFF);
      if (version != 4991)
      {
        // Serial.print("Wrong firmware loaded? ");
        // Serial.println(version);
        while (1)
        {
          delay(10);
        }
      }
      // Serial.println("Found Product 4991");

      // use a pin for the built in encoder switch
      encoders[enc].pinMode(SS_SWITCH, INPUT_PULLUP);

      // get starting position
      encoder_positions[enc] = encoders[enc].getEncoderPosition();

      // Serial.println("Turning on interrupts");
      delay(10);
      encoders[enc].setGPIOInterrupts((uint32_t)1 << SS_SWITCH, 1);
      encoders[enc].enableEncoderInterrupt();

      // set not so bright!
      encoder_pixels[enc].setBrightness(30);
      encoder_pixels[enc].show();

      found_encoders[enc] = true;
    }
  }

  Serial.println("Encoders started");
  resultJson["a"] = "sync";
  serializeJson(resultJson, Serial);
  resultJson.clear();
  Serial.println();
  delay(100);
  yield();
  pullSeedValues();
}

void loop()
{
  for (uint8_t enc = 0; enc < sizeof(found_encoders); enc++)
  {
    if (found_encoders[enc] == false)
      continue;

    int32_t new_position = encoders[enc].getEncoderPosition();
    // did we move around?

    if (new_position > 99)
    {
      encoders[enc].setEncoderPosition(100);
      new_position = encoders[enc].getEncoderPosition();
    }
    else if (new_position < 1)
    {
      encoders[enc].setEncoderPosition(0);
      new_position = encoders[enc].getEncoderPosition();
    }

    if (encoder_positions[enc] != new_position)
    {
      resultJson["a"] = "volume";
      resultJson["v"] = new_position;
      resultJson["p"] = false;
      resultJson["e"] = enc;
      serializeJson(resultJson, Serial);
      Serial.println();
      resultJson.clear();
      // Serial.print("Encoder #");
      // Serial.print(enc);
      // Serial.print(" -> ");
      // Serial.println(new_position);         // display new position
      encoder_positions[enc] = new_position;

      // change the neopixel color, mulitply the new positiion by 4 to speed it up
      encoder_pixels[enc].setPixelColor(0, Wheel((new_position * 4) & 0xFF));
      encoder_pixels[enc].show();
    }

    if (!encoders[enc].digitalRead(SS_SWITCH))
    {
      if (previouslyPressed)
      {
        if (previouslyPressedTime + DEBOUNCE_BUTTON_PRESS_MILLS <= millis())
        {
          previouslyPressed = false;
          previouslyPressedTime = 0;
        }
      }
      else
      {
        previouslyPressed = true;
        previouslyPressedTime = millis();
        resultJson["a"] = "press";
        resultJson["v"] = 0;
        resultJson["p"] = true;
        resultJson["e"] = enc;
        serializeJson(resultJson, Serial);
        Serial.println();
        resultJson.clear();
      }
    }
  }

  // Timer For Syncing Audio
  unsigned long CurrentTimeDelta = millis() - lastSyncTime;
  // Serial.println(CurrentTimeDelta);
  //  Fix timer if overflow happens
  if (CurrentTimeDelta < 0)
  {
    lastSyncTime = millis();
  }
  else if (CurrentTimeDelta > SYNC_INTERVAL)
  {
    Serial.println("Encoders started");
    resultJson["a"] = "sync";
    serializeJson(resultJson, Serial);
    resultJson.clear();
    Serial.println();
    delay(100);
    yield();
    pullSeedValues();
  }

  // don't overwhelm serial port
  yield();
  delay(10);
}

uint32_t Wheel(byte WheelPos)
{
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85)
  {
    return seesaw_NeoPixel::Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if (WheelPos < 170)
  {
    WheelPos -= 85;
    return seesaw_NeoPixel::Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return seesaw_NeoPixel::Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

void splitStringToVector(String msg)
{
  int pos;
  int j = 0;
  int k = 0;
  for (int i = 0; i < msg.length(); i++)
  {
    if (msg.charAt(i) == '|')
    {
      // Serial.println("---" + k);
      pos = atoi(msg.substring(j, i).c_str());
      encoders[k].setEncoderPosition(pos);
      encoder_pixels[k].setPixelColor(0, Wheel(((pos)*4) & 0xFF));
      j = i + 1;
      k++;
      // Serial.println(("Set Encoder #" + k + ' to POS: ' + pos));
    }
    delay(10);
  }
  pos = atoi(msg.substring(j, msg.length()).c_str());
  encoders[k].setEncoderPosition((pos)); // to grab the last value of the string
  encoder_pixels[k].setPixelColor(0, Wheel(((pos)*4) & 0xFF));
  // Serial.println("Set Encoder #" + k + ' to POS: ' + pos);
}

void pullSeedValues()
{
  Serial.println("Waiting for host...");
  while (Serial.available() == 0)
  {
  }
  String seedValues = Serial.readString();
  Serial.println("Host Reply reseaved...");
  Serial.println("Seed Values: " + seedValues.substring(1, seedValues.length() - 1));
  splitStringToVector(seedValues.substring(1, seedValues.length() - 1));
  lastSyncTime = millis();
}
