import os
import webbrowser as wb
from Abstract.lexema import *
from Errores.errores import *
from Tokens.tokens import Tokens


#TOKENS
tokens = [
    Tokens(0, 'CrearBD', 0, '', 'CrearBD', True),
    Tokens(0, 'EliminarBD', 0, '', 'EliminarBD', True),
    Tokens(0, 'CrearColeccion', 0, '', 'CrearColeccion', True),
    Tokens(0, 'EliminarColeccion', 0, '', 'EliminarColeccion', True),
    Tokens(0, 'InsertarUnico', 0, '', 'InsertarUnico', True),
    Tokens(0, 'ActualizarUnico', 0, '', 'ActualizarUnico', True),
    Tokens(0, 'EliminarUnico', 0, '', 'EliminarUnico', True),
    Tokens(0, 'BuscarTodo', 0, '', 'BuscarTodo', True),
    Tokens(0, 'BuscarUnico', 0, '', 'BuscarUnico', True),
    Tokens(0, 'nueva', 0, '', 'nueva', True),
    Tokens(0, '$set', 0, '', '$set', True),
    Tokens(0, 'Coma', 0, '', ',', True),
    Tokens(0, 'PuntoComa', 0, '', ';', True),
    Tokens(0, 'Relacion', 0, '', '=', True),
    Tokens(0, 'Parentesisabre', 0, '', '(', True),
    Tokens(0, 'Parentesiscierra', 0, '', ')', True),
    Tokens(0, 'Parametro', 0, '', '"', False),
    Tokens(0, 'puntos', 0, '', ':', True),
    Tokens(0, 'Llaveabre', 0, '', '{', True),
    Tokens(0, 'Llavecierra', 0, '', '}', True),
    Tokens(0, 'ID', 0, '', '[a-zA-Z0-9_]^*', False),
    Tokens(0, 'Comentarios', 0, '', '//.*', False),
    Tokens(0, 'String', 0, '', '"[^"]*"', False)
    

]


reserverd = {
    'CrearBD'                   : 'CrearBD',
    'EliminarBD'                : 'EliminarBD',
    'CrearColeccion'            : 'CrearColeccion',
    'EliminarColeccion'         : 'EliminarColeccion',
    'InsertarUnico'             : 'InsertarUnico',
    'ActualizarUnico'           : 'ActualizarUnico',
    'EliminarUnico'             : 'EliminarUnico',
    'BuscarTodo'                : 'BuscarTodo',
    'BuscarUnico'               : 'BuscarUnico',
    'nueva'                     : 'nueva',
    '$set'                      : '$set',
    'separacion'                : ';',
    'Relacion'                  : '=',
    'Parentesisabre'            : '(',
    'Parentesiscierra'          : ')',
    'Comilla'                   : '"',
    'puntos'                    : ':',
    'Llaveabre'                 : '{',
    'Llavecierra'               : '}',
}


global contadorSintactico
global n_linea
global n_columna
global lista_lexemas
global lista_auxiliar
global lista_errores_lexicos
global lista_tokens
global lista_errores_sintacticos

n_linea = 1
n_columna = 1
lista_lexemas = []
lista_errores_lexicos = []
lista_tokens = []
lista_errores_sintacticos = []

def analisis_lexico(cadena):
    

    global n_linea
    global n_columna
    global lista_lexemas
    global lista_tokens
    global lista_errores_lexicos

    lista_lexemas = []
    lista_errores_lexicos = []
    lista_tokens = []
    lista_errores_sintacticos = []

    lexema = ''
    puntero = 0
    n_linea = 1
    n_columna = 1
    errorLexico = 0
    
    

    while cadena:

        

        char = cadena[puntero]
        puntero += 1


        
        if char == '\"':
            l = Lexema(char, n_linea, n_columna, True, "Parametro")
            lista_lexemas.append(l)

            if lista_tokens == []:
                lista_tokens.append(Tokens(0, 'Parametro', 0, '', '"', False))  
            else:
                guardar = True
                for token in lista_tokens:
                    if token.getToken() == "Parametro":
                        guardar = False
                        break  
                
                if guardar:
                    lista_tokens.append(Tokens(0, 'Parametro', 0, '', '"', False))


            if cadena[puntero + 1].isalnum():
                lexema, cadena = armar_lexema_string(cadena[puntero:])
                if lexema and cadena:
                    n_columna += 1
                    l = Lexema(lexema, n_linea, n_columna, False, "String")
                    lista_lexemas.append(l)
                    n_columna += len(lexema)
                    puntero = 0

                            
            #----------------------
            else:
                n_columna += 1
                cadena = cadena[1:]
                puntero = 0
            
            if lista_tokens == []:
                lista_tokens.append(Tokens(0, 'String', 0, '', '"[^"]*"', False))  
            else:
                guardar = True
                for tok in lista_tokens:
                    if tok.getToken() == 'String':
                        guardar = False
                        break  
                
                if guardar:
                    lista_tokens.append(Tokens(0, 'String', 0, '', '"[^"]*"', False))
                    
        
        elif char == '\t':
            n_columna += 4
            cadena = cadena[4:]
            puntero = 0
        
        elif char == '\n':
            cadena = cadena[1:]
            puntero = 0
            n_linea += 1
            n_columna = 1
        

        elif char == '{' or char == '}' or char == ',' or char == ':' or char == ';' or char == '=' or char == '(' or char == ')':
            
            l = Lexema(char, n_linea, n_columna, True, "caracter")
            lista_lexemas.append(l)
            n_columna += 1
            cadena = cadena[1:]
            puntero = 0

        
            for token in tokens:
                if token.getPatron() == char:
                    break

            if lista_tokens == []:
                lista_tokens.append(token)  
            else:
                guardar = True
                for tok in lista_tokens:
                    if tok.getPatron() == char:
                        guardar = False
                        break  
                
                if guardar:
                    lista_tokens.append(token)

        
        elif char == ' ' or char == '\r':
            n_columna += 1
            cadena = cadena[1:]
            puntero = 0
        
        elif char.isalpha() or char == '_' or char == '$':

            lexema, cadena = armar_lexema(cadena[puntero - 1:])
            

            if lexema and cadena:

                for token in tokens:

                    if token.getPatron() == lexema:


                        if lista_tokens == []:
                            lista_tokens.append(token)  
                        else:
                            guardar = True
                            for tok in lista_tokens:
                                if tok.getPatron() == lexema:
                                    guardar = False
                                    break  
                            
                            if guardar:
                                lista_tokens.append(token)
                        
                        l = Lexema(lexema, n_linea, n_columna, True, token.getToken())
                        lista_lexemas.append(l)
                        n_columna += len(lexema) 
                        puntero = 0
                        entrar = False
                        break

                    else:
                        entrar = True
                        
                if entrar:
                    

                    if lista_tokens == []:
                        lista_tokens.append(Tokens(0, 'ID', 0, '', '[a-zA-Z0-9_]^*', False))   
                    else:
                        guardar = True
                        for tok in lista_tokens:
                            if tok.getToken() == "ID":
                                guardar = False
                                break  
                
                    if guardar:
                        lista_tokens.append(Tokens(0, 'ID', 0, '', '[a-zA-Z0-9_]^*', False))   
                          
                    
                    l = Lexema(lexema, n_linea, n_columna, True, "ID")
                    lista_lexemas.append(l)
                    n_columna += len(lexema)
                    puntero = 0

        elif char == '-':
            lexema, cadena = comentario(cadena[puntero - 1:])
            puntero = 0

            if lista_tokens == []:
                lista_tokens.append(Tokens(0, 'Comentarios', 0, '', '//.*', False))  
            else:
                guardar = True
                for tok in lista_tokens:
                    if tok.getToken() == 'Comentarios':
                        guardar = False
                        break  
                
                if guardar:
                    lista_tokens.append(Tokens(0, 'Comentarios', 0, '', '//.*', False))
        
        elif char == '/':
            lexema, cadena, contadorFila = comentario_lineas(cadena[puntero - 1:])
            n_linea += (contadorFila-1)
            puntero = 0

        else:
            lista_errores_lexicos.append(Errores(char, n_linea, n_columna, "Lexico"))
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1
            errorLexico += 1
        
        
    
    return lista_lexemas, lista_errores_lexicos, lista_tokens, lista_lexemas, errorLexico

def armar_lexema(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ''
    puntero = ''
    for char in cadena:
        puntero += char
        
        if char == ' ' or char == '\n' or char == '\"' or char == '(' or char == ')':
            return lexema, cadena[len(puntero)-1:]
        else:
            lexema += char

    return None, None

def armar_lexema_string(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ''
    puntero = ''
    for char in cadena:
        puntero += char
        
        if char == '\"' :
            return lexema, cadena[len(puntero)-1:]
        else:
            lexema += char
    
    return None, None

def comentario(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ''
    puntero = ''
    for char in cadena:
        puntero += char
        
        if char == '\n' :
            return lexema, cadena[len(puntero)-1:]
        else:
            lexema += char
    
    return None, None   

def comentario_lineas(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ''
    puntero = ''
    contador = 0
    contadorFila = 1
    
    for char in cadena:
        puntero += char
        
        if char == '\n':
            contadorFila += 1

        if char == '*' and cadena[contador + 1] == '/' and cadena[contador + 2] == '\n' or char == '*' and cadena[contador + 1] == '/' and cadena[contador + 2] == ' ':
            lexema += char
            lexema += cadena[contador + 1]
            return lexema, cadena[len(lexema):], contadorFila
        else:
            lexema += char
            contador += 1
    
    return None, None    



#ANALISIS SINTÁCTICO

def init_instrucciones(lexemas, tokens):
    
    global contadorSintactico

    while lexemas: 
        lexema = lexemas.pop(0)
        if lexema.getLexema().lower() == "crearBD".lower():
            crearBD(lexemas, lexema)

        elif lexema.getLexema().lower() == "eliminarBD".lower():
            eliminarBD(lexemas, lexema)

        elif lexema.getLexema().lower() == "crearColeccion".lower():
            crearColeccion(lexemas, lexema)

        elif lexema.getLexema().lower() == "eliminarColeccion".lower():
            eliminarColeccion(lexemas, lexema)

        elif lexema.getLexema().lower() == "insertarUnico".lower():
            insertarUnico(lexemas, lexema)

        elif lexema.getLexema().lower() == "actualizarUnico".lower():
            actualizarUnico(lexemas, lexema)

        elif lexema.getLexema().lower() == "eliminarUnico".lower():
            eliminarUnico(lexemas, lexema)

        elif lexema.getLexema().lower() == "buscarTodo".lower():
            buscarTodo(lexemas, lexema)

        elif lexema.getLexema().lower() == "buscarUnico".lower():
            buscarUnico(lexemas, lexema)
        
    if len(lista_errores_sintacticos) == 0:
        seguimiento = True
    else:
        seguimiento = False

    return seguimiento

def crearBD(lexemas, primero):
    global lista_errores_sintacticos, contadorSintactico
    
    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == ")":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None
    

def eliminarBD(lexemas, primero):
    global lista_errores_sintacticos

    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == ")":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None


def crearColeccion(lexemas, primero):
    global lista_errores_sintacticos
   
    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getToken() == 'String':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == ")":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None

def eliminarColeccion(lexemas, primero):
    global lista_errores_sintacticos

    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
        
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getToken() == 'String':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == ")":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None

def insertarUnico(lexemas, primero):
    global lista_errores_sintacticos

    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getToken() == 'String':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getLexema() == ',':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        

    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == '{':
        
        while lexema.getLexema() == ',' or lexema.getLexema() == '{':
            lexema = lexemas.pop(0)
            if lexema.getLexema() == '"':
                lexema = lexemas.pop(0)
                if lexema.getToken() == 'String':
                    lexema = lexemas.pop(0)
                    if lexema.getLexema() == '"':
                        lexema = lexemas.pop(0)
                        if lexema.getLexema() == ':':
                            lexema = lexemas.pop(0)
                            if lexema.getLexema() == '"':
                                lexema = lexemas.pop(0)
                                if lexema.getToken() == 'String':
                                    lexema = lexemas.pop(0)
                                    if lexema.getLexema() == '"':
                                        lexema = lexemas.pop(0)
                                    else:
                                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                        lexema = lexemas.pop(0)
                                else:
                                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                    lexema = lexemas.pop(0)
                            else:
                                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                lexema = lexemas.pop(0)
                        else:
                            lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                            lexema = lexemas.pop(0)
                    else:
                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                        lexema = lexemas.pop(0)
                else:
                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                    lexema = lexemas.pop(0)
            else:
                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))      
                lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == "}":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == ')':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None

def actualizarUnico(lexemas, primero):
    global lista_errores_sintacticos

    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getToken() == 'String':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == ',':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '{':
        
        while lexema.getLexema() == ',' or lexema.getLexema() == '{':
            lexema = lexemas.pop(0)
            if lexema.getLexema() == '"':
                lexema = lexemas.pop(0)
                if lexema.getToken() == 'String':
                    lexema = lexemas.pop(0)
                    if lexema.getLexema() == '"':
                        lexema = lexemas.pop(0)
                        if lexema.getLexema() == ':':
                            lexema = lexemas.pop(0)
                            if lexema.getLexema() == '"':
                                lexema = lexemas.pop(0)
                                if lexema.getToken() == 'String':
                                    lexema = lexemas.pop(0)
                                    if lexema.getLexema() == '"':
                                        lexema = lexemas.pop(0)
                                    else:
                                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                        lexema = lexemas.pop(0)                              
                                else:
                                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                    lexema = lexemas.pop(0)
                            else:
                                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                lexema = lexemas.pop(0)
                        else:
                            lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                            lexema = lexemas.pop(0) 
                    else:
                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                        lexema = lexemas.pop(0)

                else:
                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                    lexema = lexemas.pop(0)
            else:
                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                lexema = lexemas.pop(0)      
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "}":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == ',':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == "{":
        while lexema.getLexema() == "{" or lexema.getLexema() == ",":
            lexema = lexemas.pop(0)
            if lexema.getLexema() == '$set':
                lexema = lexemas.pop(0)
                if lexema.getLexema() == ':':
                    lexema = lexemas.pop(0)
                    if lexema.getLexema() == '{':
                        lexema = lexemas.pop(0)
                        if lexema.getLexema() == '"':
                            lexema = lexemas.pop(0)
                            if lexema.getToken() == 'String':
                                lexema = lexemas.pop(0)
                                if lexema.getLexema() == '"':
                                    lexema = lexemas.pop(0)
                                    if lexema.getLexema() == ':':
                                        lexema = lexemas.pop(0)
                                        if lexema.getLexema() == '"':
                                            lexema = lexemas.pop(0)
                                            if lexema.getToken() == 'String':
                                                lexema = lexemas.pop(0)
                                                if lexema.getLexema() == '"':
                                                    lexema = lexemas.pop(0)
                                                    if lexema.getLexema() == '}':
                                                        lexema = lexemas.pop(0)
                                                    else:
                                                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                                        lexema = lexemas.pop(0)
                                                else:
                                                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                                    lexema = lexemas.pop(0)
                                            else:
                                                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                                lexema = lexemas.pop(0)
                                        else:
                                            lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                            lexema = lexemas.pop(0)
                                    else:
                                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                        lexema = lexemas.pop(0)
                                else:
                                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                    lexema = lexemas.pop(0)
                            else:
                                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                lexema = lexemas.pop(0)
                        else:
                            lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                            lexema = lexemas.pop(0)
                    else:
                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                        lexema = lexemas.pop(0)
                else:
                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                    lexema = lexemas.pop(0)
            else:
                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getLexema() == "}":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == ')':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None

def eliminarUnico(lexemas, primero):
    global lista_errores_sintacticos

    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getToken() == 'String':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == ',':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '{':
        
        while lexema.getLexema() == ',' or lexema.getLexema() == '{':
            lexema = lexemas.pop(0)
            if lexema.getLexema() == '"':
                lexema = lexemas.pop(0)
                if lexema.getToken() == 'String':
                    lexema = lexemas.pop(0)
                    if lexema.getLexema() == '"':
                        lexema = lexemas.pop(0)
                        if lexema.getLexema() == ':':
                            lexema = lexemas.pop(0)
                            if lexema.getLexema() == '"':
                                lexema = lexemas.pop(0)
                                if lexema.getToken() == 'String':
                                    lexema = lexemas.pop(0)
                                    if lexema.getLexema() == '"':
                                        lexema = lexemas.pop(0)
                                    else:
                                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                        lexema = lexemas.pop(0)
                                else:
                                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                    lexema = lexemas.pop(0)
                            else:
                                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                                lexema = lexemas.pop(0)
                        else:
                            lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                            lexema = lexemas.pop(0)
                    else:
                        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                        lexema = lexemas.pop(0)
                else:
                    lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
                    lexema = lexemas.pop(0)
            else:
                lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))      
                lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)


    if lexema.getLexema() == "}":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == ')':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None

def buscarTodo(lexemas, primero):
    global lista_errores_sintacticos
   
    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getToken() == 'String':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == ")":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None

def buscarUnico(lexemas, primero):
    global lista_errores_sintacticos
   
    lexema = lexemas.pop(0)
    if lexema.getToken() == "ID":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "=":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "nueva":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == primero.getLexema():
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    
    if lexema.getLexema() == "(":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getToken() == 'String':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == '"':
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
    
    if lexema.getLexema() == ")":
        lexema = lexemas.pop(0)
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)

    if lexema.getLexema() == ";":
        return None
    else:
        lista_errores_sintacticos.append(Errores(lexema.getLexema(), lexema.getFila(), lexema.getColumna(), "Sintactico"))
        lexema = lexemas.pop(0)
        return None





        

    

# for token in tokens:
#     print(token.getToken())





entrada = '''CrearBD ejemplo = nueva CrearBD();}
--- Actualizar s
EliminarBD elimina = nueva EliminarBD();
CrearBD ejemplo2 = nueva CrearBD();
CrearColeccion colec = nueva CrearColeccion("NombreColeccion");
EliminarColeccion eliminacolec = nueva EliminarColeccion("NombreColeccion");
InsertarUnico insertadoc = nueva InsertarUnico("NombreColeccion", 
"
{
 "nombre" : "Obra Literaria",
 "autor" : "Jorge Luis"
 }
");

ActualizarUnico actualizadoc = nueva ActualizarUnico("NombreColeccion",
"
{
 "nombre" : "Obra Literaria"
},
{
 $set : {"autor" : "Mario Vargas"}
}
"   );
EliminarUnico eliminadoc = nueva EliminarUnico("NombreColeccion",
"
{
 "nombre" : "Obra Literaria"
}
");

/* 
Be
T
*/

BuscarTodo todo = nueva BuscarTodo ("NombreColeccion");
BuscarUnico todo = nueva BuscarUnico ("NombreColeccion");'''

# entrada = '''"
# {
#  "nombre" : "Obra Literaria",
#  "autor" : "Jorge Luis"
#  }
# ");
# '''



def traduccion(sd):
    data = ""

    while sd:   
        lexema = sd.pop(0)
        if lexema.getLexema().lower() == "CrearBD".lower():

            lexema = sd.pop(0)
            data += f'''use('{lexema}');\n'''
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
       
        elif lexema.getLexema().lower() == "EliminarBD".lower():

            data += f'''db.dropDatabase();\n'''
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
              

        elif lexema.getLexema().lower() == "CrearColeccion".lower():

            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            data += f'''db.createCollection('{lexema}');\n'''
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)

        elif lexema.getLexema().lower() == "EliminarColeccion".lower():
            
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            data += f'''db.{lexema}.drop();\n'''
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)

        elif lexema.getLexema().lower() == "InsertarUnico".lower():
            print("")        

        elif lexema.getLexema().lower() == "ActualizarUnico".lower():
            print("")

        elif lexema.getLexema().lower() == "EliminarUnico".lower():
            print("")

        elif lexema.getLexema().lower() == "BuscarTodo".lower():

            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            data += f'''db.{lexema}.find();\n'''
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)


        elif lexema.getLexema().lower() == "BuscarUnico".lower():
            
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            data += f'''db.{lexema}.findOne();\n'''
            lexema = sd.pop(0)
            lexema = sd.pop(0)
            lexema = sd.pop(0)
    
    return data





# print("-------------------------------")
# for item in lista1:
#     print(item.getLexema())

# print("-------------------------------")
# for item in lista2:
#     print(item.getLexema())

# print("-------------------------------")
# for item in lista3:
#     print(item.getToken())

# print("-------------------------")
# for item in returnLista:
#     print(item.getLexema())
#     print(item.getFila())
#     print(item.getColumna())
#     print("-------------------------")





