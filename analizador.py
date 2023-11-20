from validaciones import *

class Analizador:

    def __init__(self):
        # Esta es la simbología permitida para la lectura de los códigos fuente.
        self.tipos = ('void', 'int', 'float', 'string')
        self.condicionales = ('if' ,'while')
        self.operaciones = ('=', '+', '-', '<', '>')
        self.puntuales = (',', '.')
        self.simbolos_abrir = ('[', '{', '(')
        self.simbolos_cerrar = (']', '}', ')')

        # Diccionario para almacenar las variables y procesar el "código fuente".
        self.codigo_procesado = {}

        # Variable auxiliar para el conteo de la línea que se está procesando.
        self.nlinea = 0

        # Lista para almacenar los valores de línea donde se realiza apertura de paréntesis.
        self.ambito = []

        # Lista para almacenar las funciones incluidas en el programa.
        self.funciones = []

        # Apartado de validaciones.
        self.validaciones = Validaciones()
        self.RetornoDeFuncion = False

#   =============================================================================================================

    def procesar_linea(self, numLinea, linea):
        """Método para el procesado de la línea del código fuente, donde va definiendo de a pocos el alcance de
        las funciones del programa. Aparte de procesar el código para almacenarlo en el diccionario 
        'codigo_procesado'.
        
        Argumentos clave:
        numLinea -- representa la línea del código que esta siendo procesado;
        linea -- es la línea de código que será procesada.
        """

        self.nlinea = numLinea
        codigo = self.definir_ambito(linea)
        self.procesar_codigo(codigo)

#   =============================================================================================================

    def definir_ambito(self, codigo):
        """Método encargado de ir definiendo el alcance de las funciones del programa, al procesar las lineas,
        buscar los carácteres puntuales y los simbolos de apertura y cierre, para que los procese, y vaya
        purificando el código resultante para que pueda ser leído en la función 'procesar_codigo'."""

        if self.puntuales[0] in codigo:
                aux = codigo.replace(self.puntuales[0], " ")
                codigo = aux

        revision = codigo.split()
        if '{' in codigo:
                self.funciones.append(revision[0])
        if '}' in codigo:
           if self.funciones and self.funciones[-1] == "void":
                self.funciones.pop()
           elif self.funciones[-1] in self.condicionales:
                self.funciones.pop() 
           else:
                if not self.RetornoDeFuncion:
                   self.validaciones.errorRetorno(self.nlinea)
                   self.funciones.pop() 
        for i in range(len(self.simbolos_abrir)):
            if self.simbolos_abrir[i] in codigo:
                aux = codigo.replace(self.simbolos_abrir[i], " ")
                self.ambito.append(self.nlinea)
                codigo = aux
        for i in range(len(self.simbolos_cerrar)):
            if self.simbolos_cerrar[i] in codigo:
                aux = codigo.replace(self.simbolos_cerrar[i], " ")
                self.ambito.pop()
                codigo = aux
        return codigo

#   =============================================================================================================

    def procesar_codigo(self, codigo):
        """Método encargado de procesar el código purificado resultante de la función 'definir_ambito', al procesar la
        linea, buscar los carácteres condicionales y de operaciones, además de los tipos de función, y realizar las
        asignaciones y operaciones necesarias para poder procesarlas correctamente a la tabla de simbolos."""

        prev = ""
        tipo = ""
        asignar = ""

        declaracion = False
        asignacion = False
        operacion = False
        funcion = False
        retorno = False


        for palabra in codigo.split(): # Lee la línea de código palabra por palabra.
            if declaracion: # Verifica si la "variable" anterior es una declaración.
                if funcion: # Verifica si se está declarando una función.
                    self.codigo_procesado[prev].append(palabra)
                    funcion = False
                else: # Si no se esta declarando una función, entonces declara una variable.
                    if prev == "string":
                        self.codigo_procesado[prev].update({palabra : ""})
                    else:    
                        self.codigo_procesado[prev].update({palabra : 0})
                    tipo = prev
                declaracion = False

            # Verifica si la palabra procesada es algún tipo de función, o si es un simbolo condicional.
            if palabra in self.tipos or palabra in self.condicionales:
                declaracion = True
                if palabra not in self.codigo_procesado: # Si la palabra no ha sido declarada en el diccionario como un tipo de función.
                    if palabra == self.tipos[0]:
                        self.codigo_procesado.update({palabra : []})
                        funcion = True
                    elif palabra in self.condicionales: # Si la palabra es una palabra condicional.
                        declaracion = False
                        if prev == "while":
                            self.codigo_procesado.update({palabra : ["ciclo"]})  
                        else:
                            self.codigo_procesado.update({palabra : ["Condicion"]})
                    else:
                        self.codigo_procesado.update({palabra : {}})

            # Verifica si la palabra procesada es una valor de asignación.
            if asignacion:
                if tipo != "":
                     self.codigo_procesado[tipo].update({asignar : self.procesar_valor(tipo, palabra)})
                     self.validaciones.switch_case(tipo,asignar,self.procesar_valor(tipo, palabra),self.nlinea)
                else:
                        for i in range(len(self.tipos)):
                            if self.tipos[i] in self.codigo_procesado and asignar in self.codigo_procesado[self.tipos[i]]:
                                valor = self.codigo_procesado[self.tipos[i]].get(asignar)

                                if valor == 0 or valor == "":
                                    self.codigo_procesado[self.tipos[i]].update({asignar : self.procesar_valor(self.tipos[i], palabra)})
                                    self.validaciones.switch_case(self.tipos[i],asignar,self.procesar_valor(self.tipos[i], palabra),self.nlinea)  
                                elif prev == '>' or  prev =='<':
                                    self.validaciones.verificar_Condicional(self.procesar_valor(self.tipos[i],asignar),self.procesar_valor(self.tipos[i],palabra),self.nlinea)
                                else:
                                    if not operacion:
                                        self.codigo_procesado[self.tipos[i]].update({asignar : valor})  
                                        self.validaciones.switch_case(self.tipos[i],asignar,valor,self.nlinea)   
                                    else:
                                        try:
                                            if prev == '+':
                                                self.codigo_procesado[self.tipos[i]].update({asignar : valor + self.procesar_valor(self.tipos[i], palabra)})  
                                        except Exception as e:
                                            self.validaciones.SumaIncorrecta(valor,palabra,self.nlinea)
                                            self.codigo_procesado[self.tipos[i]].update({asignar : "Error"})  
                                        try: 
                                            if prev == '-':
                                                self.codigo_procesado[self.tipos[i]].update({asignar : valor - self.procesar_valor(self.tipos[i], palabra)})
                                        except Exception as e:
                                                self.validaciones.RestaIncorrecta(valor,palabra,self.nLinea)
                                                self.codigo_procesado[self.tipos[i]].update({asignar : "Error"}) 
                asignacion = False

            # Verifica si la palabra es algún simbolo de operación.
            if palabra in self.operaciones:
                if palabra != '=':
                    operacion = True

                asignacion = True
                asignar = prev

            # Verifica si la función de retorno tiene algún valor
            if retorno:
                funcion = self.funciones[-1]
                self.validaciones.switch_ErrorFunciones(funcion,self.procesar_valor(funcion,palabra),self.nlinea)  
                self.RetornoDeFuncion = True
                retorno = False
    
            # Define si la palabra es una función de retorno
            if palabra == "return":
                if len(self.funciones) == 0:
                    self.validaciones.falsoRetorno(self.nlinea)
                else: 
                   funcion = self.funciones[-1]
                   if funcion == 'void':
                        self.validaciones.Retorno_void(self.nlinea)
                        self.RetornoDeFuncion = True
                   else:   
                         retorno = True

            prev = palabra

#   =============================================================================================================

    def procesar_valor(self, tipo, dato):
        """Función encargada de procesar el valor de las variables para verificar si están siendo declaradas de
        forma correcta."""
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

    def errorAlcanceFuncion(self,numLinea):
        self.validaciones.errorAlcance(numLinea)