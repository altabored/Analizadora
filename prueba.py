tipos = ('void', 'int', 'float', 'string')
simbolos_abrir = ('[', '{', '(')
simbolos_cerrar = (']', '}', ')')
operaciones = ('+', '-', '<', '>')

#=============================================================

def refinadora(codigo):
    apertura = 0

    print("Limpiando simbolos de apertura")
    for i in range(len(simbolos_abrir)):
        if simbolos_abrir[i] in codigo:
            print("Si se encontró.")
            aux = codigo.replace(simbolos_abrir[i], " ")
            codigo = aux
            apertura = apertura + 1

            print(codigo)

        else:
            print("No se encontró.")

    print("\nLimpiando simbolos de cierre")
    for i in range(len(simbolos_cerrar)):
        if simbolos_cerrar[i] in codigo:
            print("Si se encontró.")
            aux = codigo.replace(simbolos_cerrar[i], " ")
            codigo = aux
            apertura = apertura - 1

            print(codigo)

        else:
            print("No se encontró.")

    if apertura is not 0:
        print("-+-+-[ La función no se ha cerrado ]-+-+-")

    return codigo
    
#=============================================================

def procesador(procesado, codigo):
    prev = ""
    tipo = ""
    asignar = ""

    declaracion = False
    asignacion = False

    for palabra in codigo.split():
        if palabra not in operaciones:
            if declaracion:
                procesado[prev].update({palabra : 0})
                declaracion = False
                tipo = prev

            if palabra in tipos:
                declaracion = True

                if palabra not in procesado:
                    procesado.update({palabra : {}})

            if asignacion:
                procesado[tipo].update({asignar : palabra})
                asignacion = False

            if palabra is '=':
                asignacion = True
                asignar = prev

        prev = palabra

#========================================================

procesado = {}

cadena_1 = "int x = (40)"
cadena_2 = "int y = [(60)]" 
cadena_3 = "string str = 'cervecita'"
cadena_4 = "float z = 155.5"

cadena_1 = refinadora(cadena_1)
cadena_2 = refinadora(cadena_2)
cadena_3 = refinadora(cadena_3)
cadena_4 = refinadora(cadena_4)

procesador(procesado, cadena_1)
procesador(procesado, cadena_2)
procesador(procesado, cadena_3)
procesador(procesado, cadena_4)

print("\nDiccionario como tal: " + str(procesado))
print("Index INT: " + str(procesado['int']))
print("Index FLOAT: " + str(procesado['float']))
print("Index STRING: " + str(procesado['string']))