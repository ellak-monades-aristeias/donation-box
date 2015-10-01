/*
    ch_92x_interface.ino - CH-92x coin acceptor interface (AGPL3+)

    This sketch interfaces a CH-92x series coin acceptor device.
    It waits for pulses on a digital input pit and then sends
    clear-text information accordingly through any output pin 
    via SoftwareSerial.

    Copyright (C) 2014  
    by Jann Eike  Kruse,  Dimitris  Koukoulakis,  Manolis Britsolakis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/* VERSION HISTORY
*********************

2014-06-18  Jann Kruse
v. 0.1      First draft

2014-06-23  Jann Kruse
v. 0.2      Start implementing finite state machine.

2014-06-24  Jann Kruse
v. 0.3RC    Basic features are there. Ready for release after some clean-up.

2014-10-24  Jann Kruse
v. 0.5RC    Merged tested Arduino code with untested ATtiny code to work with ATtiny85. To-be tested!

*/


#include <SoftwareSerial.h>
#include "notes.h"

const char* CURRENCY = "EUR";   // Currency unit of the coin acceptor
const int   MAX_PULSES = 99;    // Not more that so many pulses make sense. Stop counting here and complain.
const int   CENT_PER_PULSE = 50;  // This many 1/100th of a currency unit are counted per pulse.
const int   BAUD = 9600;        // Baud-rate of the serial communication.

// Define here some timing constants according to the settings of the coin acceptor.
enum timing
  {
    T_MIN = 25,     // The PULSE_INPUT shourd be LOW or HIGH for at least this long, otherwise it's noise.
    T_MAX = 150,    // The PULSE_INPUT shourd be LOW or HIGH for at most this long, otherwise it's not a pulse.
  };


// Define here how the Arduino (or ATtiny) is connected.
enum cabling
  {
    STATUS_LED   = 1,  // You may connect the status LED here.         (ATtiny85 DIP pin 5 - TX+LED on Arduino)
    PULSE_INPUT  = 0,  // Connect the coin acceptor's COIN output here.(ATtiny85 DIP pin 6 - RX+LED on Arduino)
    SPEAKER      = 2,  // You may connect a beeper/speaker here.       (ATtiny85 DIP pin 7)
    SERIAL_RX    = 3,  // Serial data input from the other Arduino/PC. (ATtiny85 DIP pin 2)
    SERIAL_TX    = 4,  // Serial data output to the other Arduino/PC.  (ATtiny85 DIP pin 3)
    ON_BOARD_LED = 13, // Most Arduino boards have LED here.           (default: Arduino pin 13)
  };


// States of the finite state machine:
enum state 
  {
  // The first (negative) states are initial, before the pulse sequence starts.
    INIT          = -1, // state after power-up, reset, or after reporting a pulse sequence.
    START         = -2, // Start here wating for a pulse.
    START_CONFIRM = -3, // Input just went HIGH for the first time.

  // The next (positive) states are to count the pulses in the sequence.
    LO            =  0, // Counting pulses, input pin is LOW  (0 V).
    HI            =  1, // Counting pulses, input pin is HIGH (5 V).
    LO_CONFIRM    =  2, // Counting pulses, input pin just went LOW.
    HI_CONFIRM    =  3, // Counting pulses, input pin just went HIGH.
  };

// Enable or disable debugging features here.
const boolean DEBUG = true;
const boolean VERBOSE = false;

SoftwareSerial softSerial(SERIAL_RX, SERIAL_TX); // Use software serial for compatibility with ATtiny85.

// Variables
unsigned char pulses; // Holds the number of pulses that have been counted lately. 
unsigned long tLow;   // Holds the millis() when pin went LOW.
unsigned long tHigh;  // Holds the millis() when pin went HIGH.
state currentState;   // Holds the current state of the finite state machine.


// The setup routine runs once when you power-up the Arduino or press reset:
void setup() {
  softSerial.begin(BAUD); // Use previously defined pins to communicate at this baud rate.
  currentState = INIT;
};


// This function oscillates the given pin for the given time with the given frequency.
// This function is blocking (not like the Arduino tone() function).
void beep(char pin, unsigned int frequency, unsigned int milliseconds) {
  // Minimal frequency = 30Hz
  // Maximal frequency = 20kHz
  // Maximal duration = 65535 miliseconds = ca. 1 minute
  if (frequency < 30) frequency = 30;
  if (frequency > 20000) frequency = 20000;
  unsigned long cycles = ((unsigned long)frequency * milliseconds) / 1000 ; // cycles = frequency * seconds
  unsigned int half_period = 500000 / frequency; // half_perion = 1/2 * second / frequency
  for (unsigned long cycle = 0; cycle < cycles; cycle++) {
    digitalWrite(pin, HIGH);
    delayMicroseconds(half_period);
    digitalWrite(pin, LOW);
    delayMicroseconds(half_period);
  };
};


// This routine reports an error.
void reportError(int error) {
  switch (error) {
    default:
      beep(SPEAKER, 2000, 1000); // Beep for a second at 2kHz.
      if (VERBOSE) {softSerial.print("Error: ");softSerial.println(error);}
  };
};


// This routine reports counted pulses as coins through a serial connection.
void reportPulses(unsigned int pulses) {
  if (VERBOSE) {softSerial.print("Reporting pulses: ");softSerial.println(pulses);}
  // The below code is necessary because printf() is not available in Arduino. This code should be improved soon.
  softSerial.print(CURRENCY);
  if (pulses*CENT_PER_PULSE < 100)    softSerial.print("0");
  else                                softSerial.print(pulses*CENT_PER_PULSE/100); // 100s (full units of the currency)
                                      softSerial.print(".");
  if (pulses*CENT_PER_PULSE%100 < 10) softSerial.print("0");
                                      softSerial.println(pulses*CENT_PER_PULSE%100); // (10s and) 1s
};


// the loop routine runs over and over again forever:
void loop() {
  
  switch (currentState) {
  
    //---------------------------------------------
    case INIT:
    // ENTRY:
      pulses = 0;
      if (VERBOSE) softSerial.println("INIT");

      // Initialize digital pins.
      pinMode(ON_BOARD_LED, OUTPUT);
      pinMode(STATUS_LED,   OUTPUT);
      pinMode(SPEAKER,      OUTPUT);
      pinMode(PULSE_INPUT,  INPUT);

      ///////////////////////////////////////////////
      ////////////// DOUBLE-CHECK THE BELOW /////////
      ///////////////////////////////////////////////
//    digitalWrite(PULSE_INPUT, HIGH); // Activate internal pull-up resistor. (So it's HIGH if not connected.)
      digitalWrite(PULSE_INPUT, LOW); // Dectivate internal pull-up resistor. (So it's not HIGH when idle.)
      digitalWrite(STATUS_LED, HIGH);  // Show, we're online...

    // WAIT FOR EVENT:
      while (not (digitalRead(PULSE_INPUT) == HIGH)) {}; // Wait for pin to go HIGH.
      // EVENT HAPPENED! PIN WENT HIGH.

    //EXIT:
      tHigh = millis();
      currentState = START;
    break;


    //---------------------------------------------
    case START:
    //ENTRY:
      if (VERBOSE) softSerial.println("S");

    // WAIT FOR EVENT:
      while (digitalRead(PULSE_INPUT) == HIGH) {}; // Wait until pin goes LOW. (I.e. wait while pin stays HIGH.)
      // EVENT HAPPENED! PIN WENT LOW.

    //EXIT:
      currentState = START_CONFIRM;
    break;


    //---------------------------------------------
    case START_CONFIRM:
    //ENTRY:
      tLow = millis(); // Save system time when pin went LOW.
      if (VERBOSE) softSerial.println("SC");

    // WAIT FOR EVENT:
      while (   (digitalRead(PULSE_INPUT) == LOW) // Wait until pin goes HIGH. (Wait while pin stays LOW.)
             && (millis() - tLow <= T_MIN)) {}; // as long as time reaches minimum (confirmed LOW).
      // EVENT HAPPENED! Either the pin went HIGH again quickly (noise?) or it's a stable LOW, i.e. a pulse.

    //EXIT:
      if (millis() - tLow >= T_MIN) { // Good pulse...probably. 
        currentState = LO;
      } else {
        currentState = START;             // Bad pulse... Back to START.
      }
    break;


    //---------------------------------------------
    case LO:
    //ENTRY:
      if (DEBUG) digitalWrite(STATUS_LED, LOW);
      if (VERBOSE) softSerial.println("L");

    // WAIT FOR EVENT:
      while (   (digitalRead(PULSE_INPUT) == LOW)    // Wait while pin is stays LOW
             && (millis() - tLow <= T_MAX)) {}; // as long as time does not exceed maximum.
      // EVENT HAPPENED! Either the pin went HIGH again (end of pulse or noise) or something's wrong...

    //EXIT:
      if (millis() - tLow >= T_MAX) { // This is wrong... 
        reportError(millis() - tLow);
        currentState = INIT;
      } else {
        currentState = HI_CONFIRM;
      }
    break;


    //---------------------------------------------
    case HI_CONFIRM:
    //ENTRY:
      tHigh = millis(); // Save system time when pin went HIGH.
      if (VERBOSE) {softSerial.print("HC -");softSerial.println(millis() - tLow);}

    // WAIT FOR EVENT:
      while (   (digitalRead(PULSE_INPUT) == HIGH)   // Wait until pin goes LOW (while pin is stays HIGH)
             && (millis() - tHigh <= T_MIN)) {};  // as long as time reaches minimumim (confirmed HIGH).
      // EVENT HAPPENED! Either the pin went LOW again (noise?) or it's a stable HIGH, i.e. end of pulse.

    //EXIT:
      if (millis() - tHigh >= T_MIN) { // Good pulse... ... Count this!
        pulses = pulses +1;
        if (pulses > MAX_PULSES) {reportError(-pulses); currentState = INIT;} // Too many pulses !! ??
        if (VERBOSE) {softSerial.print("Ps:");softSerial.println(pulses);}
        currentState = HI;
      } else {                       // Bad pulse... (noise)
        currentState = LO;
      }
    break;


    //---------------------------------------------
    case HI:
    //ENTRY:
      if (DEBUG) digitalWrite(STATUS_LED, HIGH);
      if (VERBOSE) softSerial.println("H");

    // WAIT FOR EVENT:
      while (   (digitalRead(PULSE_INPUT) == HIGH)  // Wait while pin is stays HIGH (until it goes low)
             && (millis() - tHigh <= T_MAX)) {}; // as long as time does not exceed maximum.
      // EVENT HAPPENED! Either the pin went LOW again or something's wrong...

    //EXIT:
      if (millis() - tHigh >= T_MAX) { // If the pin stays high, that's the end of the pulse sequence. 
        reportPulses(pulses);
        currentState = INIT;
      } else {
        currentState = LO_CONFIRM;         // Otherwise there's (probably) another pulse (to be confirmed).
      }
    break;


    //---------------------------------------------
    case LO_CONFIRM:
    //ENTRY:
      tLow = millis(); // Save system time when pin went HIGH.
      if (VERBOSE) {softSerial.print("LC -");softSerial.println(millis() - tHigh);}

    // WAIT FOR EVENT:
      while (   (digitalRead(PULSE_INPUT) == LOW)     // Wait while pin is stays LOW
             && (millis() - tLow <= T_MIN)) {}; // as long as time reaches minimumim (confirmed LOW).
      // EVENT HAPPENED! Either the pin went HIGH again very quickly (noise?) or it's a stable LOW, i.e. a pulse.

    //EXIT:
      if (millis() - tHigh >= T_MIN) { // Stable low.
        currentState = LO;
      } else {                            // Bad pulse... Back to HI.
        currentState = HI;
      }
    break;
    
    
    //---------------------------------------------
    default:
     if (VERBOSE) softSerial.println("FELL INTO DEFAULT CASE!!!");
    break;
  };
};

