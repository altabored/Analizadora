from io import open
import os
from analizador import *

class Archivo:
    def __init__(self, fichero):
        self.archivo = fichero
        self.nroLinea = 1
        self.analizador = Analizador()

    def lectura(self):
        """ Este método se encarga de realizar la lectura del archivo .txt, procesandolo
        línea por línea.""" 
        with open(self.archivo, 'r', encoding="utf8") as archivo: 
            for linea in archivo.readlines(): # Del archivo .txt, lee una línea
                self.analizador.procesar_linea(self.nroLinea, linea) # Se procesa la línea
                self.nroLinea = self.nroLinea + 1 # Incrementa el contador de la línea

    def imprimirFuncion(self):
        """Método encargado de imprimir el código fuente en la terminal."""
        print("\n \u001b[32m - Codigo Analizado - \u001b[37m")
        dirname = os.path.dirname(__file__)
        num = 0
        with open(dirname+'\\'+ self.archivo, 'r', encoding="utf8") as file:
            for line in file:
                num +=1
                print("{}:      {}".format(num, line), end="")
        file.close()              

    def imprimir_Errores(self):
        """Método encargado de imprimr los errores presentes durante el procesado del código fuente."""
        self.analizador.imprimirErrores()

    def mostrar_diccionario(self):
        """Método encargado de imprimr el diccionario resultante del procesado del código fuente."""
        print("\n\n \u001b[32m - Diccionario Procesado - \u001b[37m" + str(self.analizador.codigo_procesado) + "\n")

    def Search(self, valor):
        self.analizador.Search(valor)

    def remove(self, key):
        self.analizador.remove(key) 
