from io import open
from analizador import *

class Archivo:
    def __init__(self, fichero):
        self.archivo = fichero
        self.nroLinea = 1
        self.analizador = Analizador()

    def lectura(self):
        # Por algún motivo sin el 'encoding' no lee el archivo.
        with open(self.archivo, 'r', encoding="utf8") as archivo: 

            for linea in archivo.readlines(): # Del archivo .txt, lee una line
                
                self.analizador.procesar_linea(self.nroLinea, linea)

                self.nroLinea = self.nroLinea + 1