#ifndef _MAIN_H
#define _MAIN_H

// // Library imports
// #include <Arduino.h>
// #include <Adafruit_INA260.h>

// Interface pins
const uint8_t ledPin = 13;
const uint8_t alertPin = 21;

// Protos
void alert(void);

// Reset function to simulate POR
#define RESTART_ADDR 0xE000ED0C
#define READ_RESTART() (*(volatile uint32_t *)RESTART_ADDR)
#define WRITE_RESTART(val) ((*(volatile uint32_t *)RESTART_ADDR) = (val))
#define TEENSY_POR() WRITE_RESTART(0x5FA0004)

#endif
