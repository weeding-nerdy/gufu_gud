#include "main.h"

Adafruit_INA260 ina260 = Adafruit_INA260();
bool initialized = false;
volatile bool ledState = true;

void setup() {
    // Every embedded system needs an LED
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, HIGH);

    // Configure serial port
    Serial.begin(SERIAL_BAUD);

    // Wait until serial port is opened
    while (!Serial) {
        delay(10);
    }
    Serial.println("Gufu Gud");

    // Initilize the INA260
    if (!ina260.begin()) {
        Serial.println("Couldn't find INA260!");
        return;
    }
    Serial.println("Found INA260!");

    // Configure I2C bus speed
    Wire.setClock(I2C_BUS_SPEED);

    // Set conversion and averaging parameters
    ina260.setVoltageConversionTime(INA260_TIME_558_us);
    ina260.setCurrentConversionTime(INA260_TIME_558_us);
    ina260.setAveragingCount(INA260_COUNT_1);

    // Clear any pending alerts
    ina260.MaskEnable->read();

    // Enable alert on "Conversion Ready"
    ina260.MaskEnable->write(CONVERSION_READY_ADDRESS);

    // Attach ISR to "alert" pin from the INA260 to handle reading of the data
    attachInterrupt(digitalPinToInterrupt(ALERT_PIN), alert, FALLING); // TODO: FALLING or LOW?

    initialized = true;
}

void loop() {
    if (!initialized) {
        return;
    }

    // Das blinkenlight!
    if (ledState) {
        digitalWrite(LED_PIN, LOW);
    } else {
        digitalWrite(LED_PIN, HIGH);
    }

    ledState = !ledState;
    delay(100);

    // If we lose connection to Serial
    if (!Serial) {
        // POR to start from scratch and wait for new connection
        TEENSY_POR();
    }
}

void alert(void) {
    const uint32_t timestamp = micros();

    // Read voltage and current registers
    const float voltage = ina260.readBusVoltage();
    const float current = ina260.readCurrent();

    // Serialize and send to USB Serial port
    StaticJsonDocument<128> doc;
    doc["v"] = voltage / 1000.0;
    doc["i"] = current / 1000.0;
    doc["t"] = timestamp / 1000000.0;
    serializeMsgPack(doc, Serial);

    // Format seperator
    // Serial.println(0x5AA5);

    // Read mask register to clear alert line
    ina260.MaskEnable->read();
}
