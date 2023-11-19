from errores import *
from Variable import *
from validaciones import *

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

        #Añadido
        #Numero de linea:
        self.nLinea = 0
        self.operacion = False
        self.errorFuncion = False
        self.funcion = False
        self.condicional = False
        self.declaracion = False
        self.asignacion = False
        self.prev = ""
        self.tipo = ""
        self.asignar = ""
        self.valor = ""
        #funciones
        self.funciones = []
        #Validaciones
        self.validaciones = Validaciones()
#   =============================================================================================================
    def procesar_linea(self, numLinea, linea):
        self.nLinea = numLinea
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
            #else:
                #if(self.errorFuncion == True):
                     #self.funciones.pop() #Aqui deberia haber un error
                #else:
                    #self.funciones.pop()
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
    def procesar_codigo(self, linea):
        for palabra in linea.split():
            if self.declaracion:   
                self.procesar_declaracion(palabra)
            elif palabra in self.tipos or palabra in self.condicionales:
                self.procesar_inicio(palabra)
            elif palabra == "return":
                self.procesar_return(palabra)
            elif self.asignacion:
                self.procesar_asignacion(palabra)
            elif palabra in self.operaciones:
                self.procesar_operaciones(palabra)
            self.prev = palabra
        
            
            #else:
            #Aqui va el error de objeto no declarado
#   ============================================================================================================= 
    def procesar_inicio(self,palabra):
        self.declaracion = True
        if palabra not in self.codigo_procesado:
            if palabra == self.tipos[0]: 
                self.codigo_procesado.update({palabra : []})
                self.funcion = True
            elif palabra in self.condicionales:
                self.declaracion = False
                if self.prev == "while":
                    self.codigo_procesado.update({palabra : ["ciclo"]})  
                else:
                    self.codigo_procesado.update({palabra : ["Condicion"]})
            else:
                self.codigo_procesado.update({palabra : {}})
    
#   ============================================================================================================= 
    def procesar_declaracion(self,palabra):
        if self.funcion:
             self.codigo_procesado[self.prev].append(palabra)
             self.funcion = False
        else:
            if self.prev == "string":
                self.codigo_procesado[self.prev].update({palabra : ""}) #Representacion de los corchetes añadidos anteriormente
            else:    
                self.codigo_procesado[self.prev].update({palabra : 0})
                self.tipo = self.prev 
        self.declaracion = False
#   =============================================================================================================

    def procesar_asignacion(self,palabra):
        if self.tipo != "": #declarando
            self.codigo_procesado[self.tipo].update({self.asignar : self.procesar_valor(self.tipo, palabra)})
            self.validaciones.switch_case(self.tipo,self.asignar,self.procesar_valor(self.tipo, palabra),self.nLinea)       
        else: #asignando
            for i in range(len(self.tipos)):
                if self.tipos[i] in self.codigo_procesado and self.asignar in self.codigo_procesado[self.tipos[i]]:
                    self.valor = self.codigo_procesado[self.tipos[i]].get(self.asignar)#llave
   
                if  self.valor == 0 or self.valor == "":                     
                    self.codigo_procesado[self.tipos[i]].update({self.asignar : self.procesar_valor(self.tipos[i], palabra)})
                    self.validaciones.switch_case(self.tipos[i],self.asignar,self.procesar_valor(self.tipos[i], palabra),self.nLinea)  
                else:
                    if not self.operacion:
                        self.codigo_procesado[self.tipos[i]].update({self.asignar : self.valor})  
                        self.validaciones.switch_case(self.tipos[i],self.asignar,self.valor,self.nLinea)   
                    else:
                        try:
                            if self.prev == '+':
                                self.codigo_procesado[self.tipos[i]].update({self.asignar : self.valor + self.procesar_valor(self.tipos[i], palabra)})  
                        except Exception as e:
                            self.validaciones.SumaIncorrecta(self.valor,palabra,self.nLinea)
                            self.codigo_procesado[self.tipos[i]].update({self.asignar : "Error"})  
                        try: 
                            if self.prev == '-':
                                self.codigo_procesado[self.tipos[i]].update({self.asignar : self.valor - self.procesar_valor(self.tipos[i], palabra)})
                        except Exception as e:
                            self.validaciones.RestaIncorrecta(self.valor,palabra,self.nLinea)
                            self.codigo_procesado[self.tipos[i]].update({self.asignar : "Error"}) 
                        if self.prev == '>' or '<':
                            self.validaciones.verificarCondicional(self.asignar,palabra,self.nLinea)
        self.tipo = ""
        self.asignacion = False
#   =============================================================================================================
    def procesar_return(self,codigo):
        funcion = self.funciones[-1]
        if not funcion == 'void':
            #aqui se hace una revision si no esta malo
            
            return
        #aqui deberia haber un error en caso de Void-return
#   =============================================================================================================

    def procesar_operaciones(self,palabra):
        if palabra != '=':
            self.operacion = True          
        self.asignacion = True
        self.asignar = self.prev #Aqui agarra la variable
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