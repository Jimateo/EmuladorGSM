# Authentication Simulation with AES Encryption

This project simulates the authentication process between a mobile device, an antenna, and an operator using AES encryption. The code demonstrates the implementation of the A3 and A8 algorithms commonly used in GSM authentication protocols.

## **Table of Contents**
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Code Overview](#code-overview)
  - [Classes](#classes)
  - [Main Process](#main-process)

## **Introduction**

This simulation illustrates how a mobile device authenticates with an antenna using the A3 and A8 algorithms. The process involves generating random values (RAND), computing response values (SRES), and using a session key (Kc) to encrypt and decrypt messages.

## **Features**

- **Mobile Class**: Handles mobile-specific operations including setting RAND, running A3 and A8 algorithms, and encrypting messages.
- **Antenna Class**: Manages IMSI, RAND, SRES, Kc, and message encryption/decryption.
- **Operator Class**: Generates RAND, retrieves Ki based on IMSI, and runs A3 and A8 algorithms to provide authentication parameters.

## **Prerequisites**

- Python 3.x
- PyCryptodome library

To install PyCryptodome, run:
```bash
pip install pycryptodome

Code Overview
Classes
Movil

__init__(self, IMSI, Ki): Initializes the mobile with IMSI and Ki.
set_RAND(self, RAND): Sets the RAND value.
a3_algorithm(self, Ki, RAND): Runs the A3 algorithm to compute SRES.
a8_algorithm(self, Ki, RAND): Runs the A8 algorithm to compute Kc.
ENC(self): Encrypts a message using Kc.
Antena

__init__(self): Initializes the antenna.
get_IMSI(self, IMSI): Sets the IMSI value.
set_SRES_(self, SRES_): Sets the SRES_ value.
set_parameters(self, RAND, SRES, Kc): Sets RAND, SRES, and Kc.
validate_authentication(self): Validates if SRES matches SRES_.
read_msg(self, msg): Reads an encrypted message.
DEC(self): Decrypts a message using Kc.
Operador

__init__(self): Initializes the operator.
get_KI(self, IMSI): Retrieves Ki based on IMSI.
generate_RAND(self): Generates a random RAND value.
a3_algorithm(self): Runs the A3 algorithm to compute SRES.
a8_algorithm(self): Runs the A8 algorithm to compute Kc.
get_parameters(self, IMSI): Returns IMSI, RAND, SRES, and Kc.
Main Process
The main script simulates the authentication process:

Mobile sends IMSI to Antenna.
Antenna requests Ki and RAND from Operator.
Operator generates RAND and computes SRES and Kc using A3 and A8 algorithms.
Parameters are sent back to Antenna.
Mobile receives RAND from Antenna, computes SRES using A3 algorithm, and sends it back to Antenna.
Antenna validates the SRES, and if correct, proceeds to encrypt a message using Kc.
Mobile encrypts a message, Antenna decrypts it, and the decrypted message is displayed.
