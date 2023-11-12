# Clase para crear los distintos errores que pueden generarse en el procesado del "código fuente"

class DatoSinDeclararException(Exception):
    "Ocurre cuando el dato leído no ha sido declarado"
    pass

class returnFueraDeFuncion(Exception):
    "Ocurre cuando se trata de realizar un RETURN fuera del bloque de un bloque de función válido"
    pass