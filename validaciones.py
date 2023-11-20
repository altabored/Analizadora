class Validaciones():
    def __init__(self):
        self.errores = []


    #Tipos
    def verificar_String(self,asignacion,valor,numLinea):
        if not isinstance(valor, str):
            self.errores.append(f"Error-Linea {numLinea}: El dato: {valor} esta asignado a '{asignacion}' corresponde a un string")
        
    def verificar_Float(self,asignacion,valor,numLinea):
        if not isinstance(valor, float):
            self.errores.append(f"Error-Linea {numLinea}: El dato: {valor} esta asignado a '{asignacion}' corresponde a un float")
     

    def verificar_Int(self,asignacion,valor,numLinea):
        if not isinstance(valor, int):
              self.errores.append(f"Error-Linea {numLinea}: El dato: {valor} esta asignado a '{asignacion}' que corresponde a un entero")

    def verificar_ExistVariable(valor):
        if not (valor in globals() or valor in locals()):return
            #raise Error_ExistVariable(valor)
     
    def verificar_Tipo(valor): 
        if not (isinstance(valor, int,float,str)): return
           # raise Error_Tipo(valor)
            
    
    def switch_case(self,tipo,asignacion,valor,numLinea):
        switch_dict = {
            'string': self.verificar_String,
            'float': self.verificar_Float,
            'int': self.verificar_Int
        }
        switch_dict.get(tipo, lambda x, y, z: None)(asignacion,valor,numLinea)

    #Asignaciones
    def SumaIncorrecta(self,valor1,valor2,numLinea): 
        self.errores.append(f"Error-Linea {numLinea}: No es posible sumar el dato:'{valor1}' con el dato:'{valor2}'")

    def RestaIncorrecta(self,valor1,valor2,numLinea): 
        self.errores.append(f"Error-Linea {numLinea}: No es posible restar el dato:'{valor1}' con el dato:'{valor2}'")

    def Retorno_void(self,numLinea): 
        self.errores.append(f"Error-Linea {numLinea}: La funcion void no retorna ningun dato")  

    def verificar_Condicional(self,valor1,valor2,numLinea): 
        if not isinstance(valor1, str) and not isinstance(valor2, str):
            self.errores.append(f"Error-Linea {numLinea}: El dato: {valor1} no se puede comparar con el dato '{valor2}' corresponde a un string")          
    
    def imprimir_Errores(self):
        for elemento in self.errores:
            print(elemento, end='\n')

    def verificar_RetornoString(self,valor,numLinea):
        if not isinstance(valor, str) :
            self.errores.append(f"Error-Linea {numLinea}: La funcion tipo String no puede retorno el dato:{valor}" )
        
    def verificar_RetornoFloat(self,valor,numLinea):
        if not isinstance(valor, float):
            self.errores.append(f"Error-Linea {numLinea}: La funcion tipo Float no puede retorno el dato:{valor}")
    
    def verificar_RetornoInt(self,valor,numLinea):
        if not isinstance(valor, int):
              self.errores.append(f"Error-Linea {numLinea}: La funcion tipo Int no puede retorno el dato:{valor}")       
    
    def switch_ErrorFunciones(self, tipo, valor, numLinea):
        switch_dict = {
            'string': self.verificar_RetornoString,
            'float': lambda x, y: self.verificar_RetornoFloat(valor, numLinea),
            'int': lambda x, y: self.verificar_RetornoInt(valor, numLinea)
        }
        switch_dict.get(tipo, lambda x, y: None)(valor, numLinea)

    def errorRetorno(self,numLinea):
        self.errores.append(f"Error-Linea {numLinea}: La funcion no retorno ningun valor")  

    def errorAlcance(self,numLinea):
        self.errores.append(f"Error-Linea {numLinea}: Alcance de funcion")  

    def falsoRetorno(self,numLinea):
        self.errores.append(f"Error-Linea {numLinea}: Return inesperado") 


    def datoNoDeclarado(self,valor, numLinea):
        self.errores.append(f"Error-Linea {numLinea}: El dato: {valor}  no declarado") 
        