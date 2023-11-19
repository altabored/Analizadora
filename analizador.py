from errores import *
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
        self.nLinea = 0
        self.RetornoDeFuncion = False
        #funciones
        self.funciones = []
        #Validaciones
        self.validaciones = Validaciones()
#   =============================================================================================================

    def procesar_linea(self, numLinea, linea):
        self.nlinea = numLinea
        codigo = self.definir_ambito(linea)
        self.procesar_codigo(codigo)

#   =============================================================================================================

    def definir_ambito(self, codigo):
        revision = codigo.split()
        if '{' in codigo:
            if not revision[0] in self.condicionales:
                self.funciones.append(revision[0])
        if '}' in codigo:
           if self.funciones and self.funciones[-1] == "void":
                self.funciones.pop()
           else:
                if not self.RetornoDeFuncion == True:
                   self.validaciones.errorRetorno(self.nLinea)
                   self.funciones.pop() 
                else:
                    self.funciones.pop()
        for i in range(len(self.simbolos_abrir)):
            if self.simbolos_abrir[i] in codigo:
                aux = codigo.replace(self.simbolos_abrir[i], " ")
                self.ambito.append(self.nLinea)
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


        for palabra in codigo.split():

            if declaracion:
                if funcion:
                    self.codigo_procesado[prev].append(palabra)
                    funcion = False
                else:
                    if prev == "string":
                        self.codigo_procesado[prev].update({palabra : ""})
                    else:    
                        self.codigo_procesado[prev].update({palabra : 0})
                    tipo = prev
                declaracion = False

            if palabra in self.tipos:
                declaracion = True
                if palabra not in self.codigo_procesado:
                    if palabra == self.tipos[0]:
                        self.codigo_procesado.update({palabra : []})
                        funcion = True
                    elif palabra in self.condicionales:
                        declaracion = False
                        if prev == "while":
                            self.codigo_procesado.update({palabra : ["ciclo"]})  
                        else:
                            self.codigo_procesado.update({palabra : ["Condicion"]})
                    else:
                        self.codigo_procesado.update({palabra : {}})

            if asignacion:
                if tipo != "":
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
                                        self.codigo_procesado[self.tipos[i]].update({asignar : "Error"})  
                                    try: 
                                        if prev == '-':
                                            self.codigo_procesado[self.tipos[i]].update({asignar : valor - self.procesar_valor(self.tipos[i], palabra)})
                                    except Exception as e:
                                            self.validaciones.RestaIncorrecta(valor,palabra,self.nLinea)
                                            self.codigo_procesado[self.tipos[i]].update({asignar : "Error"}) 
                                    if prev == '>' or '<':
                                        self.validaciones.verificar_Condicional(asignar,palabra,self.nLinea)

                asignacion = False

            if palabra in self.operaciones:
                if palabra != '=':
                    operacion = True

                asignacion = True
                asignar = prev

            if palabra == "return":
                funcion = self.funciones[-1]
                if not funcion == 'void':
                     self.validaciones.Retorno_void(self.nLinea)
                else:   
                     retorno = True

            if retorno:
                funcion = self.funciones[-1]
                self.validaciones.switch_ErrorFunciones(funcion,valor,self.nLinea)  
                self.RetornoDeFuncion = True
                retorno = False
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