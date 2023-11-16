from Variable import *
import archivo

fichero = "codigo.txt"

proyecto = archivo.Archivo(fichero)
proyecto.lectura()

proyecto.mostrar_diccionario()


valor = 'x' 
proyecto.Search(valor)
