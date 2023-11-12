from errores import *

class Analizador:

    def __init__(self):
        # Estos son los digitos y palabras claves que el programa aceptara al momento de leer el "código fuente"
        tipos = ('void', 'int', 'float', 'string')
        condicionales = ('if' ,'while')
        operaciones = ('=', '+', '-', '<', '>')
        puntuales = (',', '.', '[', ']', '{', '}', '(', ')')

        # Diccionario para almacenar las variables del "código fuente"
        variables = {}

        # Lista para almacenar las variables desconocidas que se encuentren
        desconocidos = []

    # Los PRINT() de abajo tienen que ser borrados, ahorita los deje para que se entienda la idea.

    def procesar_linea(self, numLinea, linea):
        print("Linea {}: {} \n - Palabras:".format(numLinea, linea))
        for palabra in linea.split(): # De esta linea, lee cada una de sus palabras
            self.procesar_palabra(palabra)
        
    def procesar_palabra(self, palabra):
        print(palabra)