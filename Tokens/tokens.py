class Tokens():
    
    def __init__(self, numeroCorrelativo, token, numeroToken, lexema, patron, reservada):
        self.numeroCorrelativo = numeroCorrelativo
        self.token = token
        self.numeroToken = numeroToken
        self.lexema = lexema
        self.patron = patron
        self.reservada = reservada
    
    def getCorrelativo(self):
        return self.numeroCorrelativo

    def getToken(self):
        return self.token

    def getNumeroToken(self):
        return self.numeroToken
    
    def getLexema(self):
        return self.lexema

    def getPatron(self):
        return self.patron

    def getReservada(self):
        return self.reservada

    