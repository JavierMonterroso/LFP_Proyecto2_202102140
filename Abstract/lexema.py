from Abstract.abstract import Expression

class Lexema(Expression):

    def __init__(self, lexema, fila, columna, reservada, token):
        self.lexema = lexema
        self.reservada = reservada
        self.token = token
        super().__init__(fila, columna)

    def operar(self, arbol):
        return self.lexema
    
    def getLexema(self):
        return self.lexema

    def getFila(self):
        return super().getFila()
    
    def getColumna(self):
        return super().getColumna()
    
    def getReservada(self):
        return self.reservada

    def getToken(self):
        return self.token