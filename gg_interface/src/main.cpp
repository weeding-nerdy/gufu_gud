#include "main.h"

Adafruit_INA260 ina260 = Adafruit_INA260();
bool initialized = false;

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
    debug_msg(F("Gufu Gud"));

    // Initialize the INA260
    uint8_t retries = INIT_ATTEMPTS;
    while (retries > 0) {
        if (!ina260.begin()) {
            debug_msg(F("Couldn't find INA260!"));
            retries--;
        }
        debug_msg(F("Found INA260!"));
        break;
    }

    // Configure I2C bus speed
    Wire.setClock(I2C_BUS_SPEED);

    // Set conversion and averaging parameters
    ina260.setVoltageConversionTime(INA260_CONVERSION_TIME);
    ina260.setCurrentConversionTime(INA260_CONVERSION_TIME);
    ina260.setAveragingCount(INA260_AVG_COUNT);

    // Clear any pending alerts
    ina260.MaskEnable->read();

    // Enable alert on "Conversion Ready"
    ina260.MaskEnable->write(CONVERSION_READY_MASK);

    // Attach ISR to "alert" pin from the INA260 to handle reading of the data
    attachInterrupt(digitalPinToInterrupt(ALERT_PIN), alert, FALLING); // TODO: FALLING or LOW?

    initialized = true;
}

void loop() {
    // We shouldn't get here, but just in case
    if (!initialized) {
        debug_msg(F("In loop() but INA260 not Initialized!"));
        return;
    }

    // Das blinkenlight!
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(500);

    // If we lose connection to Serial
    if (!Serial) {
        // POR to start from scratch and wait for new connection
        TEENSY_POR();
    }
}

void alert(void) {
    // NOTE: The micros() function will roll-over to zero after 4294967295 us (1h, 11m, 34.967295s)
    //       this is not compensated for.
    const uint32_t timestamp = micros();

    // Read voltage and current registers
    const float voltage = ina260.readBusVoltage();
    const float current = ina260.readCurrent();

    // Serialize and send to USB Serial port
    // NOTE: doc must fit into JSON_BUFFER_SIZE
    StaticJsonDocument<JSON_BUFFER_SIZE> doc;
    doc["v"] = voltage * 1e-3;
    doc["i"] = current * 1e-3;
    doc["t"] = timestamp * 1e-6;
    serializeMsgPack(doc, Serial);

    // Read mask register to clear alert line
    ina260.MaskEnable->read();
}

void debug_msg(String msg) {
    // Serialize and send debug message to USB Serial port
    // NOTE: doc must fit into JSON_BUFFER_SIZE_DEBUG
    StaticJsonDocument<JSON_BUFFER_SIZE_DEBUG> doc;
    doc["debug"] = true;
    doc["msg"] = msg;
    serializeMsgPack(doc, Serial);
}
