from io import open
import os
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

                numLinea = self.nroLinea

                self.nroLinea = self.nroLinea + 1

                print(self.analizador.codigo_procesado)
            
            if len(self.analizador.ambito) != 0:
                self.analizador.errorAlcanceFuncion(numLinea)


    def imprimirFuncion(self):
        print("\n \u001b[32m-Codigo Analizado\u001b[37m")
        dirname = os.path.dirname(__file__)
        num = 0
        with open(dirname+'\\'+ self.archivo, 'r', encoding="utf8") as file:
            for line in file:
                num +=1
                print("{}:      {}".format(num, line), end="")
        file.close()              

    def imprimir_Errores(self):
        self.analizador.imprimirErrores()

    def mostrar_diccionario(self):
        self.analizador.mostrar_diccionario()


    def Search(self, valor):
        self.analizador.Search(valor)

    def remove(self, key):
        self.analizador.remove(key) 
