from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

class Movil:
    def __init__(self, IMSI, Ki):
        self.IMSI = IMSI
        self.Ki = Ki
        self.RAND = None
        self.SRES_ = None
        self.Kc = None
    
    def set_RAND(self, RAND):
        self.RAND = RAND

    # Implementación del Algoritmo A3
    def a3_algorithm(self, Ki, RAND):
        cipher = AES.new(Ki, AES.MODE_ECB)
        SRES_ = cipher.encrypt(RAND)[:4]  # SRES será de 32 bits (4 bytes)
        self.SRES_ = SRES_
    
    # Implementación del Algoritmo A8
    def a8_algorithm(self, Ki, RAND):
        cipher = AES.new(Ki, AES.MODE_ECB)
        Kc = cipher.encrypt(RAND)[:8]  # Kc será de 64 bits (8 bytes)
        self.Kc = Kc

    # Implementación de la función ENC
    def ENC(self):
        cipher = AES.new(self.Kc + self.Kc, AES.MODE_ECB)
        msg = cipher.encrypt(b'Hola000000000000')
        return msg

class Antena:

    def __init__(self):
        self.IMSI = None
        self.RAND = None
        self.SRES = None
        self.Kc = None     
        self.SRES_ = None
        self.msg = None

    def get_IMSI(self, IMSI):
        self.IMSI = IMSI
    
    def set_SRES_(self, SRES_):
        self.SRES_ = SRES_

    def set_parameters(self, RAND, SRES, Kc):
        self.RAND = RAND
        self.SRES = SRES
        self.Kc = Kc

    def validate_authentication(self):
        return self.SRES == self.SRES_
    
    def read_msg(self, msg):
        self.msg = msg

    # Implementación de la función ENC
    def DEC(self):
        cipher = AES.new(self.Kc + self.Kc, AES.MODE_ECB)
        msg_dec = cipher.decrypt(self.msg)
        return msg_dec

class Operador: 

    def __init__(self):
        self.RAND = None
        self.Ki = None

    def get_KI(self, IMSI):
        if IMSI == "214050000000095":
            self.Ki = b'1234567890123456'
    
    def generate_RAND(self):
        self.RAND = get_random_bytes(16)

    # Implementación del Algoritmo A3
    def a3_algorithm(self):
        cipher = AES.new(self.Ki, AES.MODE_ECB)
        SRES = cipher.encrypt(self.RAND)[:4]  # SRES será de 32 bits (4 bytes)
        return SRES
    
    # Implementación del Algoritmo A8
    def a8_algorithm(self):
        cipher = AES.new(self.Ki, AES.MODE_ECB)
        Kc = cipher.encrypt(self.RAND)[:8]  # Kc será de 64 bits (8 bytes)
        return Kc    

    def get_parameters(self, IMSI):
        SRES = self.a3_algorithm()
        Kc = self.a8_algorithm() 
        return IMSI, self.RAND, SRES, Kc

# ------------------------ MAIN ------------------------

IMSI = "214050000000095"
Ki = b'1234567890123456'

movil = Movil(IMSI,Ki)
antena = Antena()
operador = Operador()

# Enviamos IMSI del móvil a la antena
antena.get_IMSI(movil.IMSI)

# Enviamos el IMSI de la antena al Operador para así obtener el Ki y generamos los parámetros
operador.get_KI(antena.IMSI)
operador.generate_RAND()
IMSI, RAND, SRES, Kc = operador.get_parameters(antena.IMSI)

# Enviamos los parámetros a la antena
antena.set_parameters(RAND, SRES, Kc)

# Enviamos al móvil el RAND desde la antena
movil.set_RAND(antena.RAND)

# El móvil genera SRES' y se la envía a la antena
movil.a3_algorithm(movil.Ki, movil.RAND)
antena.set_SRES_(movil.SRES_)

# Antena comprueba que es correcto y envía un OK
if antena.validate_authentication():
    
    print("El SRES generado por el móvil coincide por el obtenido de la operadora.")
    movil.a8_algorithm(movil.Ki, movil.RAND)
    antena.read_msg(movil.ENC())
    print(f'Mensaje cifrado: {antena.msg}')
    print(f'Mensaje descifrado: {antena.DEC()}')

else:
    print("El SRES generado por el móvil no coincide por el obtenido de la operadora.")

