from errores import *

class Analizador:

    def __init__(self):
        # Estos son los digitos y palabras claves que el programa aceptara al momento de leer el "código fuente"
        self.tipos = ('void', 'int', 'float', 'string')
        self.condicionales = ('if' ,'while')
        
        self.operaciones = ('+', '-', '<', '>')
        self.puntuales = (',', '.')
        self.simbolos_abrir = ('[', '{', '(')
        self.simbolos_cerrar = (']', '}', ')')

        # Diccionario para almacenar las variables del "código fuente"
        self.variables = {}

        # Lista para almacenar las variables desconocidas que se encuentren
        self.desconocidos = []

    # Los PRINT() de abajo tienen que ser borrados, ahorita los deje para que se entienda la idea.

    def procesar_linea(self, numLinea, linea):
        for palabra in linea.split(): # De esta linea, lee cada una de sus palabras
            self.procesar_palabra(palabra)
        
    def procesar_palabra(self, palabra):
        if palabra in self.tipos:
            print(palabra)