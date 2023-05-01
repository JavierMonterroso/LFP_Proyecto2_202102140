from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser as wb
from analizador_lexico_sintactico import *
import os

class Pantalla_Principal():

    global lista_lexemas, lista_errores_lexicos, lista_tokens

    def __init__(self):
        self.PP = Tk()
        self.PP.resizable(False, False)
        self.PP.title("Proyecto 2")
        self.PP.geometry("1150x800+225+20")
        self.PP.configure(bg = "#0a516d")
        self.ventana()
    
    def ventana(self):

        global textEntrada, salida, existente, analisis, tokens
        existente = False

        self.Frame = Frame(height=1200, width=1100)
        self.Frame.config(bg = "#018790")
        self.Frame.pack(padx=5, pady=10)

        #BOTONES ENCABEZADOS
        Button(self.Frame, text="Nuevo", command=self.nuevo, font=("Comic Sans MS",12), width=8, fg = "#ffffff", bg = "#0a516d").place(x=50, y=40)
        Button(self.Frame, text="Abrir", command=self.abrir, font=("Comic Sans MS",12), width=8, fg = "#ffffff", bg = "#0a516d").place(x=250, y=40)
        Button(self.Frame, text="Guardar", command=self.guardar, font=("Comic Sans MS",12), width=8, fg = "#ffffff", bg = "#0a516d").place(x=450, y=40)
        Button(self.Frame, text="Guardar como", command=self.guardar_como, font=("Comic Sans MS",12), width=12, fg = "#ffffff", bg = "#0a516d").place(x=650, y=40)
        Button(self.Frame, text="Salir", command=self.salir, font=("Comic Sans MS",12), width=8, fg = "#ffffff", bg = "#0a516d").place(x=860, y=40)

        Label(self.Frame, text="Entrada:", font=('Comic Sans MS',15), width=15, bg = "#018790", fg = "#ffffff").place(x=0, y=120)
        textEntrada = Text(self.Frame, width=50, height=35)
        textEntrada.place(x=30, y=160)

        Label(self.Frame, text="Salida:", font=('Comic Sans MS',15), width=15, bg = "#018790", fg = "#ffffff").place(x=400, y=120)
        salida = Text(self.Frame, width=50, height=35)
        salida.place(x=460, y=160)

        #BOTONES LATERALES
        analisis = Button(self.Frame, text="Analisis", command=self.analisis, font=("Comic Sans MS",15), width=10, fg = "#ffffff", bg = "#0a516d")
        analisis.place(x=920, y=350)
        tokens = Button(self.Frame, text="Tokens", command=self.token, font=("Comic Sans MS",15), width=10, fg = "#ffffff", bg = "#0a516d")
        tokens.place(x=920, y=450)
        
        #Estado de los componentes
        textEntrada.config(state=DISABLED)
        salida.config(state=DISABLED)
        analisis.config(state=DISABLED)
        tokens.config(state=DISABLED)

        

        self.Frame.mainloop()
    
    def abrir(self):
        try:
            textEntrada.delete('1.0', END)
            global archivo
            global existente
            global lecturaGlobal
            existente = True
            archivo = filedialog.askopenfilename(title="Abrir")
            contenidoAbrir = open(archivo, "r+")
            lecturaGlobal = contenidoAbrir.read()
            contenidoAbrir.close()
            textEntrada.config(state=NORMAL)
            textEntrada.insert(END, lecturaGlobal)
            analisis.config(state=NORMAL)

        except:
            existente = False
            messagebox.showinfo("Mensaje", "Existen problemas para cargar el archivo")
            textEntrada.config(state=DISABLED)

    def nuevo(self):
        global existente
        
        if existente:
            guardar = messagebox.askyesno(message="¿Desea guardar los cambios antes de limpiar el editor?", title="Título")

            if guardar:

                
                existente = False
                
                file = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")],defaultextension=".txt")
                fob=open(file,'w')
                lectura = textEntrada.get('1.0', END)
                fob.write(lectura)
                fob.close()
    
                textEntrada.delete('1.0', END)
                messagebox.showinfo("Mensaje", "Se ha guardado el archivo con éxito")
                
            else:
                existente = False
                textEntrada.delete('1.0', END)

        else:
            messagebox.showinfo("Mensaje", "No se encuentra abierto algún archivo")

        textEntrada.config(state=DISABLED)

    def guardar(self):
        global existente

        if existente:
            contenidoAbrir = open(archivo, "w")
            lectura = textEntrada.get('1.0', END)
            contenidoAbrir.write(lectura)
            messagebox.showinfo("Mensaje", "Se han guardado los cambios con éxito")
        else:
            messagebox.showinfo("Mensaje", "No se encuentra abierto algún archivo")

    def guardar_como(self):
        global existente
        
        if existente:
            existente = False
            file = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")],defaultextension=".txt")
            fob=open(file,'w')
            lectura = textEntrada.get('1.0', END)
            fob.write(lectura)
            fob.close()
            messagebox.showinfo("Mensaje", "Se ha guardado el archivo con éxito")

        else:
            messagebox.showinfo("Mensaje", "No se encuentra abierto algún archivo")

    def salir(self):
        self.PP.destroy()

    def analisis(self):

        global lista_lexemas, lista_errores_lexicos, lista_tokens, lecturaGlobal
        lista_lexemas, lista_errores_lexicos, lista_tokens, lista_lexemas_traduccion, errorLexico = analisis_lexico(lecturaGlobal)
        seguimiento = init_instrucciones(lista_lexemas, lista_tokens)

        if len(lista_errores_lexicos) == 0 and seguimiento:
            messagebox.showinfo("Mensaje", "No existen errores en el archivo")
            dataTraduccion = traduccion(lista_lexemas_traduccion)
            nuevoArchivo = f'{archivo}_Traduccion.txt'
            contenidoAbrir = open(nuevoArchivo, "w")
            contenidoAbrir.write(dataTraduccion)
            messagebox.showinfo("Mensaje", "Se ha creado el archivo con éxito")

        else:
            self.errores()
        tokens.config(state=NORMAL)


    def token(self):
        data = ""
        data += "digraph G {\n"
        data += '\tnode [fontname="Helvetica,Arial,sans-serif"]\n'
        data += '\tedge [fontname="Helvetica,Arial,sans-serif"]\n'
        data += '\ta0 [shape=none label=<\n'
        data += '\t<TABLE border="0" cellspacing="8" cellpadding="10" style="rounded" bgcolor="black">\n'

        data += '\t\t<TR>\n'
        data += f'\t\t<TD bgcolor="white"> </TD>\n'
        data += f'\t\t<TD bgcolor="white">Token</TD>\n'
        data += f'\t\t<TD bgcolor="white">Patron</TD>\n'
        data += '\t\t</TR>\n'

        contadorToken = 0
        for token in lista_tokens:
            contadorToken += 1
            data += '\t\t<TR>\n'
            data += f'\t\t<TD bgcolor="white">{contadorToken}</TD>\n'
            data += f'\t\t<TD bgcolor="white">{token.getToken()}</TD>\n'
            data += f'\t\t<TD bgcolor="white">{token.getPatron()}</TD>\n'
            data += '\t\t</TR>\n'
        
        data += '\t</TABLE>>];'
        data += '}'
    
        with open('Lista_Tokens.dot', 'w') as f:         
            f.write(data)

        os.system('dot -Tpng Lista_Tokens.dot -o Lista_Tokens.png')

        wb.open_new("Lista_Tokens.png")
    
    def errores(self):
        global lista_lexemas, lista_errores_lexicos, lista_tokens
        data = ""
        data += "digraph G {\n"
        data += '\tfontname="Helvetica,Arial,sans-serif"\n'
        data += '\tnode [fontname="Helvetica,Arial,sans-serif"]\n'
        data += '\tedge [fontname="Helvetica,Arial,sans-serif"]\n'
        data += '\ta0 [shape=none label=<\n'
        data += '\t<TABLE border="0" cellspacing="8" cellpadding="10" style="rounded" bgcolor="black">\n'

        data += '\t\t<TR>\n'
        data += f'\t\t<TD bgcolor="white"> </TD>\n'
        data += f'\t\t<TD bgcolor="white">Tipo</TD>\n'
        data += f'\t\t<TD bgcolor="white">Fila</TD>\n'
        data += f'\t\t<TD bgcolor="white">Columna</TD>\n'
        data += f'\t\t<TD bgcolor="white">Lexema</TD>\n'
        data += '\t\t</TR>\n'

        contadorError = 0
        for error in lista_errores_lexicos:
            contadorError += 1
            data += '\t\t<TR>\n'
            data += f'\t\t<TD bgcolor="white">{contadorError}</TD>\n'
            data += f'\t\t<TD bgcolor="white">{error.getTipo()}</TD>\n'
            data += f'\t\t<TD bgcolor="white">{error.getFila()}</TD>\n'
            data += f'\t\t<TD bgcolor="white">{error.getColumna()}</TD>\n'
            data += f'\t\t<TD bgcolor="white">{error.getLexema()}</TD>\n'
            data += '\t\t</TR>\n'
        
        data += '\t</TABLE>>];'
        data += '}'
    
        with open('lista_errores_lexicos.dot', 'w') as f:         
            f.write(data)


        lista_errores_lexicos

        os.system('dot -Tpng lista_errores_lexicos.dot -o lista_errores_lexicos.png')

        wb.open_new("lista_errores_lexicos.png")

Pantalla_Principal()      


