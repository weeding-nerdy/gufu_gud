#ifndef _MAIN_H
#define _MAIN_H

// // Library imports
#include <Arduino.h>
#include <ArduinoJson.h>
#include <Adafruit_INA260.h>

// Interface pins
#define LED_PIN 13
#define ALERT_PIN 21
#define INIT_ATTEMPTS 5
#define SERIAL_BAUD 115200
#define JSON_BUFFER_SIZE 64
#define JSON_BUFFER_SIZE_DEBUG (10 * JSON_BUFFER_SIZE)
#define I2C_BUS_SPEED (4e2 * 1e3)

// INA260 configuration
#define CONVERSION_READY_MASK 0x400
#define INA260_CONVERSION_TIME INA260_TIME_140_us
#define INA260_AVG_COUNT INA260_COUNT_4

// Protos
void alert(void);
void debug_msg(String msg);

// Reset function to simulate POR
#define RESTART_ADDR 0xE000ED0C
#define READ_RESTART() (*(volatile uint32_t *)RESTART_ADDR)
#define WRITE_RESTART(val) ((*(volatile uint32_t *)RESTART_ADDR) = (val))
#define TEENSY_POR() WRITE_RESTART(0x5FA0004)

#endif
