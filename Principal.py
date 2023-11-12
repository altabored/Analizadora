from io import open

linea = 1

# Por algún motivo sin el 'encoding' no lee el archivo. Ahí se quedará.
#
# El código de abajo es una prueba para verificar que el programa rescate bien las lineas del TXT,
# y que permita trabajar bien con sus respectivos valores

with open("codigo.txt", 'r', encoding="utf8") as file:

    print("\n")
    for line in file.readlines(): # Del archivo .txt, lee una linea
        print("+++++[ Linea #{} de código ]+++++\n".format(linea))
        print(line)

        print("\n*****[ Palabras de la linea #{} ]*****\n".format(linea))
        for word in line.split(): # De esta linea, lee cada una de sus palabras
            print(word)
        print("\n======================================\n")

        # Todos estos print son solo para ver que sirvan bien las partes del método, al final se quitarán

        # En base a esas palabras reescatadas, es que deberíamos de realizar la construcción del Hashtable

        linea = linea + 1