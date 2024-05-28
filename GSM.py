from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

# Implementación ficticia de MILENAGE para la demostración
def milenage(Ki, OPc, RAND):
    # Esta es una implementación simplificada. Debes usar la implementación real del algoritmo MILENAGE.
    cipher = AES.new(Ki, AES.MODE_ECB)
    SRES = cipher.encrypt(RAND)[:4]  # Respuesta esperada
    Kc = cipher.encrypt(RAND)[:16]  # Clave de cifrado temporal
    IK = cipher.encrypt(RAND)[:16]  # Clave de integridad temporal
    AUTN = cipher.encrypt(RAND)[:16]  # Número de autenticación
    return SRES, Kc, IK, AUTN

class Movil:
    def __init__(self, IMSI, Ki, OPc):
        self.IMSI = IMSI
        self.Ki = Ki
        self.OPc = OPc
        self.RAND = None
        self.SRES_ = None
        self.Kc = None
        self.IK = None
    
    def set_RAND(self, RAND):
        self.RAND = RAND

    def authenticate(self):
        self.SRES_, self.Kc, self.IK, _ = milenage(self.Ki, self.OPc, self.RAND)

    def ENC(self, message):
        cipher = AES.new(self.Kc, AES.MODE_ECB)
        mensaje_padding = message.ljust(16, b'\0')
        msg_enc = cipher.encrypt(mensaje_padding)
        return msg_enc

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

    def DEC(self):
        cipher = AES.new(self.Kc, AES.MODE_ECB)
        msg_dec = cipher.decrypt(self.msg)
        return msg_dec

class Operador:
    def __init__(self):
        self.RAND = None
        self.Ki = None
        self.OPc = None

    def get_KI(self, IMSI):
        if IMSI == "214050000000095":
            self.Ki = b'1234567890123456'
            self.OPc = b'6543210987654321'

    def generate_RAND(self):
        self.RAND = get_random_bytes(16)

    def authenticate(self):
        SRES, Kc, IK, AUTN = milenage(self.Ki, self.OPc, self.RAND)
        return SRES, Kc

    def get_parameters(self, IMSI):
        SRES, Kc = self.authenticate()
        return IMSI, self.RAND, SRES, Kc
# ------------------------ MAIN ------------------------

IMSI = "214050000000095"
Ki = b'1234567890123456'
OPc =  b'6543210987654321'

movil = Movil(IMSI, Ki, OPc)
antena = Antena()
operador = Operador()

# Enviamos IMSI del móvil a la antena
antena.get_IMSI(movil.IMSI)

# Enviamos el IMSI de la antena al Operador para así obtener el Ki y OPc y generar los parámetros
operador.get_KI(antena.IMSI)
operador.generate_RAND()
IMSI, RAND, SRES, Kc = operador.get_parameters(antena.IMSI)

# Enviamos los parámetros a la antena
antena.set_parameters(RAND, SRES, Kc)

# Enviamos al móvil el RAND desde la antena
movil.set_RAND(antena.RAND)

# El móvil genera SRES' y se la envía a la antena
movil.authenticate()
antena.set_SRES_(movil.SRES_)

# Antena comprueba que es correcto y envía un OK
if antena.validate_authentication():
    print("El SRES generado por el móvil coincide con el obtenido de la operadora.")
    msg_encrypted = movil.ENC(b'Hola000000000000')
    antena.read_msg(msg_encrypted)
    print(f'Mensaje cifrado: {antena.msg}')
    print(f'Mensaje descifrado: {antena.DEC()}')
else:
    print("El SRES generado por el móvil no coincide con el obtenido de la operadora.")