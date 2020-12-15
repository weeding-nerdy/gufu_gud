#include <Arduino.h>
#include <ArduinoJson.h>
#include <Adafruit_INA260.h>

#include "main.h"

Adafruit_INA260 ina260 = Adafruit_INA260();
volatile bool ledState = true;

void setup() {
    // Every embedded system needs an LED
    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, HIGH);

    // Configure serial port
    Serial.begin(115200);

    // Wait until serial port is opened
    while (!Serial) { delay(10); }
    Serial.println("Gufu Gud");// INA260 Test");

    // Initilize the INA260
    if (!ina260.begin()) {
        Serial.println("Couldn't find INA260 chip");
        while (1);
    }
    Serial.println("Found INA260");// chip");

    // Configure I2C bus speed
    uint16_t i2c_speed_khz = 400;
    Wire.setClock(i2c_speed_khz * 1000);

    // Set conversion and averaging parameters
    ina260.setVoltageConversionTime(INA260_TIME_558_us);
    ina260.setCurrentConversionTime(INA260_TIME_558_us);
    ina260.setAveragingCount(INA260_COUNT_1);

    // Clear any pending alerts
    ina260.MaskEnable->read();

    // Enable alert on "Conversion Ready"
    ina260.MaskEnable->write(0x0400);

    // Attach ISR to "alert" pin from the INA260 to handle reading of the data
    attachInterrupt(digitalPinToInterrupt(alertPin), alert, FALLING); // TODO: FALLING or LOW?
}

void loop() {
    // Das blinkenlight!
    if (ledState) {
        digitalWrite(ledPin, LOW);
        ledState = false;
    } else {
        digitalWrite(ledPin, HIGH);
        ledState = true;
    }
    delay(100);

    // If we lose connection to Serial
    if (!Serial) {
        // POR to start from scratch and wait for new connection
        TEENSY_POR();
    }
}

void alert(void) {
    uint32_t alert_ts = micros();

    // Read voltage and current registers
    float voltage = ina260.readBusVoltage();
    float current = ina260.readCurrent();

    // Serialize and send to USB Serial port
    StaticJsonDocument<128> doc;
    doc["v"] = voltage / 1000.0;
    doc["i"] = current / 1000.0;
    doc["t"] = alert_ts / 1000000.0;
    serializeMsgPack(doc, Serial);

    // // Format seperator
    // Serial.println(0x5AA5);

    // Read mask register to clear alert line
    ina260.MaskEnable->read();
}
