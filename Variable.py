class Variable:
    
    def __init__(self, type, nombre, value, scope): 
        self.type = type
        self.nombre = nombre
        self.value = value
        self.scope = scope
        
    #---------------------------------------

    def __repr__(self):
        return f"{self.type}  {self.nombre} = {self.value}"
    
    def getNombre(self):
        return self.nombre
    
    def getValue(self):
        return self.value


    def getType(self):
        return self.type

    def getNombre(self):
        return self.nombre

    def getScope(self):
        return self.scope
    
   #---------------------------------------

    def setNombre(self, nom):
        self.nombre = nom 

    def setValue(self, valor):
        self.value = valor    

    def setType(self, tipo):
        self.type = tipo

    def setScope(self, alc):
        self.scope = alc