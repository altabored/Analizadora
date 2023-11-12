from io import open
from analizador import *

nroLinea = 1
analizador = Analizador()

# Por algún motivo sin el 'encoding' no lee el archivo.
with open("codigo.txt", 'r', encoding="utf8") as archivo: 

    for linea in archivo.readlines(): # Del archivo .txt, lee una line
        
        analizador.procesar_linea(nroLinea, linea)

        nroLinea = nroLinea + 1