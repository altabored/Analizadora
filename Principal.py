from Variable import *
import archivo

fichero = "codigo.txt"

proyecto = archivo.Archivo(fichero)
proyecto.lectura()
proyecto.imprimir_Errores()

proyecto.mostrar_diccionario()


valor = 'int' 
proyecto.Search(valor)


