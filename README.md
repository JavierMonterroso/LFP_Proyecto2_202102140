<img src='https://user-images.githubusercontent.com/36779113/128587817-1a6c2fdc-d106-4dd3-b092-104c8299bded.png' background='white'>


## Universidad de San Carlos de Guatemala, Abril 2023
## Facultad de Ingeniería
## Escuela de Ciencias y Sistemas
## Laboratorio de Lenguajes Formales y de Programación B+


| TABLA DE DATOS  | 
| ------------- | 
| Carné:    202102140|
| Nombre:    Javier Andrés Monterroso García|




# Manual Técnico


Para realizar la práctica se usó el lenguaje de programación de Python. La aplicación consiste en realizar un software de tipo visual donde se podrá cargar un archivo de texto, posteriormente, se realizará un análisis léxicos y sintácticos sobre el contenido del archivo, a su vez, con el contenido se crearán sentencias de bases de datos.  


Para la elaboración del proyecto 2 se implementó el paradigma de programación POO, a su vez se utilizaron clases abstractas. Para poder crear clases abstractas en Python es necesario importar la clase ABC y el decorador abstractmethod del modulo abc (Abstract Base Classes). Un módulo que se encuentra en la librería estándar del lenguaje, por lo que no es necesario instalar. Así para definir una clase privada solamente se tiene que crear una clase heredada de ABC con un método abstracto. A su vez se implementó el paradigma de programación POO

![](https://i.imgur.com/hPahS26.jpg)

Para elaborar la interfaz gráfica se utilizó Tkinter, la cual es una librería del lenguaje de programación Python. Para hacer uso de Tkinter se debe de importar las diferentes funciones de la librería.

![](https://i.imgur.com/MQUqFig.jpg)

Para la elaboración de las ventanas se deberá de realizar lo siguiente:

![](https://i.imgur.com/IFo28FH.png)

Se hace uso de la Programación Orientada a Objetos, creando clases que serán nuestras ventanas, dentro de cada ventana existen funciones.

Al igular self.PP con Tk(), se podrá acceder a los diferentes métodos. El método “title” permite colocar un título a la ventana y el método “geometry” permite indicar las dimensiones de la ventana y la posición donde se desea que aparezca en pantalla.

También existen diferentes componentes para colocar en las ventas, tales como, botones, cajas de texto, tablas y demás elementos. Para colocar los componentes se tiene que escribir el nombre del componente, posterior se abren paréntesis, el
primer parámetro que escribe es el nombre de la ventana donde se quiere que aparezca, luego se pueden agregar otros parámetros como, el tamaño de letra de
los componentes, fuente de texto, estado del componente y demás cosas. 

![](https://i.imgur.com/auhsPwW.png)

Para trasladarnos de ventana a ventana se utiliza el siguiente código:

![](https://i.imgur.com/OXgQvWz.png)

Se tiene que destruir la ventana en la que actualmente nos encontramos, posterior, se manda a llamar la clase o ventana a la cual nos queremos dirigir. Estos códigos se guardan en funciones y dichas funciones se agregan a nuestros botones, existe un parámetro en los botones donde se puede colocar el nombre de nuestras funciones, se puede visualizar en la siguiente imagen:

![](https://i.imgur.com/j1DmJng.png)

<br>
<br>

## Analizador léxico

### Tabla de tokens

| Número| Token | Patron|
| ----------- | -----------|-----------|
| 1| CrearBD | CreaBD |
| 2| EliminarBD | EliminarBD |
| 3| CrearColeccion | CrearColeccion |
| 4| EliminarColeccion | EliminarColeccion |
| 5| InsertarUnico | InsertarUnico |
| 6| ActualizarUnico | ActualizarUnico |
| 7| EliminarUnico | EliminarUnico |
| 8| BuscarTodo | BuscarTodo |
| 9| BuscarUnico | BuscarUnico |
| 10| nueva | nueva |
| 11| $set | set |
| 12| Coma | , |
| 13| PuntoComa | ; |
| 14| Relación | = |
| 15| ParentesisAbre | ( |
| 16| ParentesisCierre | ) |
| 17| Parámetro | " |
| 18| Puntos | : |
| 19| LlaveAbre | { |
| 20| LlaveCierra | } |
| 21| ID | [a-zA-Z0-9_][a-zA-Z0-9_]^* |
| 22| Comentarios | //.*|
| 23| String | "[^"]*" |


Para programar el analizador léxico, se tomó como base el siguiente AFD:

![](https://i.imgur.com/X7asepC.png)

El estado inicial del autómata (q0) es nuestro método analisis_lexico, para acceder al siguiente estado (q1) se necesita proporcionar una cadena.

![](https://i.imgur.com/7pWwyJ1.png) ![](https://i.imgur.com/kGixZLg.png)

![](https://i.imgur.com/7DZenhD.png) ![](https://i.imgur.com/dkl66Wh.png)


Dentro del estado q1, se definieron diversas variables, entre ellas dos variables llamadas n_linea y n_columna, las cuales son esenciales para ubicar donde se encuentra cada lexema.

Al recibir la cadena en el estado q1, se procede a ir al estado q2, para ir a dicho estado solo se necesita un carácter de la cadena. Para acceder a un solo carácter de la cadena, se codifica el nombre de la variable, seguido de corchetes, entre los corchetes colocamos la variable puntero, la cual tiene un valor de cero, por lo que nos devolverá el primer carácter. Se podría decir que la variable cadena se vuelve una lista y podemos acceder a los elementos de la lista indicando la posición, loselementos de la lista son todos los caracteres que componen la cadena.

![](https://i.imgur.com/OvWkxwy.png) ![](https://i.imgur.com/ewZ6dFv.png)

Al recibir un carácter en el estado q2, podemos ir de dicho estado a 6 posibles estados. Se analiza el carácter recibido por q2, y dependiendo del carácter nos dirigimos a alguno de los 9 estados.

![](https://i.imgur.com/QX5NLJL.png) ![](https://i.imgur.com/vy0tp9Z.png)

![](https://i.imgur.com/A5PgZ5u.png) ![](https://i.imgur.com/WfHpEY6.png)


![](https://i.imgur.com/t7Ef2e5.png) ![](https://i.imgur.com/RbXc3MY.png)


![](https://i.imgur.com/NxqfOto.png) ![](https://i.imgur.com/J6QIYhw.png)


![](https://i.imgur.com/85xoCFF.png) ![](https://i.imgur.com/amEXpm1.png)


![](https://i.imgur.com/bktxKbH.png) ![](https://i.imgur.com/J9TMO6m.png)


![](https://i.imgur.com/ApeQ8Qy.png) ![](https://i.imgur.com/f7aGdVP.png)

![](https://i.imgur.com/dFZRR7B.png) ![](https://i.imgur.com/VXHGh5Q.png)

![](https://i.imgur.com/MYA77yU.png) ![](https://i.imgur.com/6w2hq9z.png)




Cada if o elif representa los posibles estados donde se puede ir el carácter, dicho carácter se encuentra en la variable char. Dependiendo a donde se dirija se realizarán cosas diferentes, una de ellas es la suma de filas y columnas porque no todos los estados suman a la variable n_linea, solo el estado q5, ya que dicho carácter es un salto de línea. La suma del número de columnas también puede ser diferente, al acceder al estado q4, ya que dicho carácter es una tabulación siempre se sumará 4 columnas a la variable n_columna, en los demás estados la suma de columnas dependerá del largo del lexema que se forme.

Cuando el carácter no sea aceptado por el autómata es cuando identificamos los errores léxicos, por lo que, nos dirigimos al estado q22 donde guardaremos los errores léxicos en una lista, se guardará el lexema, el número de fila y columna donde se encuentra. Cuando el carácter sea aceptado por el autómata se guardarán los lexemas reconocidos en una lista, guardando el lexema, el número de fila y columna donde se encuentra.

Cuando ya se haya analizado toda la cadena de entrada, nos dirigimos al estado q23, en dicho estado se retornará la lista de lexemas que se identificaron y una lista de errores léxicos. 

También hay estados que permiten identificar comentarios, ya sea de una línea o de varias líneas. El estado q8 reconoce los comentarios de una línea y el estado q9 reconoce los comentarios de diversas líneas, en ambos casos los lexemas no se guardan en la lista de lexemas, pero tampoco se guardan en la lista de errores léxicos.

El estado inicial es q0 y el estado q23 es el estado final.

<br>
<br>

## Analizador sintáctico

Gramática libre de contexto utilizada para el análisis sintáctico:

init : instrucciones


instruccion : crearDB ;
------------ | eliminarDB ;
------------ | crearColeccion ;
------------ | eliminarColeccion ;
------------ | insertarUnico ;
------------ | actualizarUnico ;
------------ | eliminarUnico ;
------------ | buscarTodo ;
------------ | buscarUnico ;

crearDB : CrearDB ID = nueva CrearDB ( )

eliminarDB : EliminarDB ID = nueva EliminarDB ( )

crearColeccion : CrearColecion ID = nueva CreaColeccion ( STRING )

eliminarColeccion : EliminarColeccion ID = nueva EliminarColeccion ( STRING )

insertarUnico : InsertarUnico ID = nueva InsertarUnico ( STRING, STRING, STRING )

actualizarUnico : ActualizarUnico ID = nueva ActualizarUnico ( STRING, STRING )

eliminarUnico : EliminarUnico ID = nueva EliminarUnico ( STRING )

buscarTodo : BuscarTodo ID = nueva BuscarTodo ( STRING )

buscarUnico : BuscarUnico ID = nueva BuscarUnico ( STRING )



<br>
<br>
<br>
<br>
<br>


# Manual de Usuario
El programa cuenta con una sola ventana que contiene el menú principal. Desde dicha ventana se encuentran todas las funcionalidades del proyecto. 

![](https://i.imgur.com/m392jxR.png)

<br>
<br>
<br>


## Botones de la ventana y sus funcionalidades


* ![](https://i.imgur.com/DsLR8SO.png) : El botón al iniciar el programa no tendrá ninguna funcionalidad, se tiene que presionar primeramente el botón de "Abrir", posteriormente se podrá utilizar sin ningún inconveniente. Lo que realiza dicho botón es limpiar el área de texto donde se escribe el contenido de los archivos que se cargan en el programa. Antes de borrar el contenido se preguntará al usuario si desea guardar, en dado caso se desea guardar, se le pedirá al usuario el nombre que se desea colocar al archivo y el lugar donde se guardará.

* ![](https://i.imgur.com/lnXgqnv.png) : El botón será el que habilité a los demás botones, ya que este permite acceder al explorador de archivos y cargar el contenido en el área de texto de entrara del archivo que eligió el usuario. 

* ![](https://i.imgur.com/YIDXZ7E.png) : El botón será el que nos permita guardar los cambios que se hicieron en el archivo que el usuario seleccionó.

* ![](https://i.imgur.com/zsdBEv2.png) : El botón será el que nos permita guardar el contenido que se encuentra en el área de texto de entrada en un archivo diferente del que se abrió.

* ![](https://i.imgur.com/gvap8rO.png) : El botón cerrará la ventana principal.

* ![](https://i.imgur.com/2KVMY3D.png) : El botón inicialmente no se encontrará habilitado, ya que primeramente se necesita cargar un archivo, posteriormente, se podrá utilizar dicho botón sin ningún inconveniente. La funcionalida del botón es analizar el contenido del archivo tanto léxicamente como sintácticamente, luego se generará una imagen donde se podrá visualizar los errores encontrados, indicando el lexema que el automata no identificó, la fila y columna donde se encuentra. 

* ![](https://i.imgur.com/T0RL9yB.png) : El botón inicialmente no se encontrará habilitado, ya que primeramente se necesita cargar un archivo, posteriormente, se podrá utilizar dicho botón sin ningún inconveniente. La funcionalida del botón es analizar el contenido del archivo y verificar los tokens encontrados, posterior se generará un imagen para visualizar la información.
