from errores import *
from Variable import *
from validaciones import *

from collections import deque

class Analizador:

    def __init__(self):
        # Estos son los digitos y palabras claves que el programa aceptara al momento de leer el "código fuente"
        self.tipos = ('void', 'int', 'float', 'string')
        self.condicionales = ('if' ,'while')
        
        self.operaciones = ('=', '+', '-', '<', '>')
        self.puntuales = (',', '.')
        self.simbolos_abrir = ('[', '{', '(')
        self.simbolos_cerrar = (']', '}', ')')

        # Diccionario para almacenar las variables del "código fuente"
        self.codigo_procesado = {}

        # Lista para almacenar los valores de línea donde se realiza apertura de paréntesis.
        self.ambito = []

        #Numero de linea:
        self.nLinea = 0

        #Validaciones
        self.validaciones = Validaciones()
        #self.comprobacionDeErrores = False



#   =============================================================================================================

    def procesar_linea(self, numLinea, linea):
        self.nLinea = numLinea
        codigo = self.definir_ambito(linea, numLinea)
        self.procesar_codigo(codigo)

#   =============================================================================================================

    def definir_ambito(self, codigo, numLinea): #Esto es para funciones
        
        for i in range(len(self.simbolos_abrir)):
            if self.simbolos_abrir[i] in codigo:
                aux = codigo.replace(self.simbolos_abrir[i], " ")
                self.ambito.append(numLinea)
                codigo = aux

        for i in range(len(self.simbolos_cerrar)):
            if self.simbolos_cerrar[i] in codigo:
                aux = codigo.replace(self.simbolos_cerrar[i], " ")
                self.ambito.pop()
                codigo = aux

        return codigo

#   =============================================================================================================


    def procesar_codigo(self, codigo):

        prev = ""
        tipo = ""
        asignar = ""

        declaracion = False
        asignacion = False
        operacion = False
        funcion = False
        retorno = False

        for palabra in codigo.split(): #prev siempre agarra el anterior

            if declaracion: #Cuando se asigna una variable a un tipo de dato
                if funcion:
                    self.codigo_procesado[prev].append(palabra)
                    funcion = False
                else:
                    if prev == "string":
                        self.codigo_procesado[prev].update({palabra : ""}) #Representacion de los corchetes añadidos anteriormente
                    else:    
                        self.codigo_procesado[prev].update({palabra : 0})
                    tipo = prev 
                declaracion = False

            if palabra in self.tipos:
                declaracion = True #Se da cuenta que es una declaracion
                if palabra not in self.codigo_procesado:
                    if palabra == self.tipos[0]: #Si es funcion entre aqui
                        self.codigo_procesado.update({palabra : []})
                        funcion = True
                    else:
                        self.codigo_procesado.update({palabra : {}}) #Esto para añadir


            if palabra == "return":
                retorno = True
                continue

            if asignacion:
                if tipo != "":
                        if retorno:
                               self.codigo_procesado[tipo].update({"return": self.procesar_valor(tipo, palabra)})
                               retorno = False
                        else:
                            self.codigo_procesado[tipo].update({asignar : self.procesar_valor(tipo, palabra)})
                            self.validaciones.switch_case(tipo,asignar,self.procesar_valor(tipo, palabra),self.nLinea)       
                else:
                    for i in range(len(self.tipos)):
                        if self.tipos[i] in self.codigo_procesado and asignar in self.codigo_procesado[self.tipos[i]]:
                            valor = self.codigo_procesado[self.tipos[i]].get(asignar)
   
                            if valor == 0 or valor == "":                     
                                    self.codigo_procesado[self.tipos[i]].update({asignar : self.procesar_valor(self.tipos[i], palabra)})
                                    self.validaciones.switch_case(self.tipos[i],asignar,self.procesar_valor(self.tipos[i], palabra),self.nLinea)  
                            else:
                                if not operacion:
                                       self.codigo_procesado[self.tipos[i]].update({asignar : valor})  
                                       self.validaciones.switch_case(self.tipos[i],asignar,valor,self.nLinea)   
                                else:
                                    try:
                                        if prev == '+':
                                            self.codigo_procesado[self.tipos[i]].update({asignar : valor + self.procesar_valor(self.tipos[i], palabra)})  
                                    except Exception as e:
                                        self.validaciones.SumaIncorrecta(valor,palabra,self.nLinea)
                                        self.codigo_procesado[self.tipos[i]].update({asignar : valor + palabra})  
                                    try: 
                                        if prev == '-':
                                            self.codigo_procesado[self.tipos[i]].update({asignar : valor - self.procesar_valor(self.tipos[i], palabra)})
                                    except Exception as e:
                                        self.validaciones.RestaIncorrecta(valor,palabra,self.nLinea)
                                        self.codigo_procesado[self.tipos[i]].update({asignar : valor + "-"+ palabra})  
                asignacion = False

            if palabra in self.operaciones:
                if palabra != '=':
                    operacion = True
                    
                asignacion = True
                asignar = prev #Aqui agarra la variable

            prev = palabra

#   =============================================================================================================

    def procesar_valor(self, tipo, dato):
        try:
            valor = 0
            if tipo == 'int':
                valor = int(dato)
            else:
                valor = float(dato)
            return valor
        except:
            return dato
        
#   =============================================================================================================
    
    def imprimirErrores(self):
        self.validaciones.imprimir_Errores()

#   =============================================================================================================



    def funcion_hash(self, id):
        aux = 0
        for i in id:
            aux += ord(i)
        return aux % 20


    def insertar_en_diccionario(self, v):
        key = self.funcion_hash(v.nombre)
        self.codigo_procesado[key] = v


    def mostrar_diccionario(self):
        print("\nContenido del diccionario codigo_procesado:")
        print("Key\t\tValor")
        print("------------------------------")
        for key, value in self.codigo_procesado.items():
            print(f"{key}\t\t{value}") 


    


    def Search(self, valor):
        hash_value = self.funcion_hash(valor)
        
        # Verificar si la clave hash está presente en el diccionario
        if hash_value in self.codigo_procesado:
            resultado_busqueda = self.codigo_procesado[hash_value]
            print(f"\nElemento encontrado en la dirección de memoria: {hex(id(resultado_busqueda))}")
        else:
            print("\nElemento no encontrado.")

                

    def get_attributes(self, key):
        hash_key = self.funcion_hash(key)
        if hash_key in self.codigo_procesado:
            return self.codigo_procesado[hash_key]
        else:
            return None

    def remove(self, key):
        hash_key = self.hash_func(key)
        if hash_key in self.codigo_procesado:
            del self.codigo_procesado[hash_key]           