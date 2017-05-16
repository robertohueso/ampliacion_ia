## AIA
## Búsqueda con adversario
## Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
## ===================================================================

## En esta práctica vamos a implementar los algoritmos minimax y
## minimiax con poda alfa beta para decidir el siguiente movimiento en
## un problema de búsqueda con adversario.

## ==================================================================
## Representación de problemas de búsqueda con adversario
## ==================================================================

## Recuérdese que según lo que se ha visto en clase, la implementación
## de la representación de un juego consiste en:

## * Representar estados y movimientos mediante alguna una estructura
##   de datos.
## * Definir: es_estado_final(_), es_estado_ganador(_,_,_),
##   movimientos(_), aplica(_,_), f_utilidad(_,_), y f_evaluacion(_,_)
## * Definir: estado_inicial, minimo_valor y maximo_valor

## ==================================================================
## Ejercicio 1
## ==================================================================

##   Definir en python una clase Juego que represente un problema de
## búsqueda con adversario. La clase debe tener los siguientes
## atributos:

## - estado_inicial: Estado inicial del juego.
## - estado_final: Estado final del juego (si es único).
## - maximo_valor: Cota superior de los valores de la función de
##   evaluación estática
## - minimo_valor: Cota inferior de los valores de la función de
##   evaluación estática

## y los siguientes métodos:

## - movimientos(estado): Lista de movimientos aplicables al 'estado'.
## - aplica(movimiento,estado): Estado resultado de aplicar el
##   'movimiento' al 'estado'.
## - es_estado_final(estado): Comprueba si el 'estado' es un estado
##   final del juego. Por defecto compara con el estado final.
## - es_estado_ganador(estado,turno,jugador): Comprueba si el
##   'jugador' gana el juego en el 'estado' cuando le toca al jugador
##   'turno'.
## - f_evaluacion(estado,turno): Devuelve el valor asociado al
##   'estado' cuando le toca jugar al jugador 'turno'. Por defecto
##   está definida como la función de utilidad para los estados
##   finales y 0 en caso cualquier otro caso.
## - str_estado(estado): Devuelve una repesentación en forma de cadena
##   de texto del 'estado'.
## - str_movimiento(movimiento): Devuelve una repesentación en forma
##   de cadena de texto del 'movimiento'.

##   El constructor de la clase recibe el estado inicial, el estado
## final, en caso de que éste sea único y los valores máximo y mínimo
## de la función de evaluación (por defecto, infinito y -infinito
## respectivamente).
import math

class Juego():
    def __init__(self, e_inicial, e_final, eval_max = math.inf,
                 eval_min = -math.inf):
        self.estado_inicial = e_inicial
        self.estado_final = e_final
        self.eval_max = eval_max
        self.eval_min = eval_min

    def movimientos(self, estado):
        pass

    def aplica(self, movimiento, estado):
        pass

    def es_estado_final(self, estado):
        pass

    def es_estado_ganador(self, estado, turno, jugador):
        pass

    def f_evaluacion(self, estado, turno):
        pass

    def str_estado(self, estado):
        pass

    def str_movimiento(self, movimiento):
        pass


## ==================================================================
## NIM
## ==================================================================

## Recordemos el juego del Nim visto en clase. Inicialmente se dispone
## de una pila de N fichas. En cada jugada, el jugador tiene que
## elegir 1, 2 ó 3 fichas. El jugador que coja la última pieza pierde.
        
## ==================================================================
## Ejercicio 2
## ==================================================================

##   Definir una función nim(n), que recibiendo como entrada un número
## natural n, devuelva la instancia de la clase Juego correspondiente
## al juego del Nim que inicia la partida con n piezas sobre la mesa.

##   Utilizar como función de evaluación estática la siguiente: Si el
## resto de dividir entre 4 el número de piezas del estado es igual a
## 1 entonces, si es el turno de 'MAX' devolver -1 y si es el turno de
## 'MIN', devolver 1. Si el resto de dividir entre 4 el número de
## piezas del estado es distinto de 1 entonces, si es el turno de
## 'MAX' devolver 1 y si es el turno de 'MIN', devolver -1.

## >>> juego_nim = nim(17)
## >>> juego_nim.estado_inicial
## 17
## >>> juego_nim.es_estado_final(3)
## False
## >>> juego_nim.movimientos(2)
## [2, 1]
## >>> juego_nim.movimientos(17)
## [3, 2, 1]
## >>> juego_nim.aplica(17, 3)
## 14

class Nim(Juego):
    def __init__(self, e_inicial, e_final, eval_max = math.inf,
                 eval_min = -math.inf):
        super().__init__(e_inicial, e_final, eval_max, eval_min)

    def movimientos(self, estado):
        if estado >= 3:
            return [-1, -2, -3]
        elif estado == 2:
            return [-1, -2, -3]
        else:
            return [-1]

    def aplica(self, movimiento, estado):
        return estado + movimiento

    def es_estado_final(self, estado):
        if estado == 0:
            return True
        else:
            return False

    def es_estado_ganador(self, estado, turno, jugador):
        if estado == self.estado_final and turno == jugador:
            return True
        else:
            return False

    def f_evaluacion(self, estado, turno):
        if estado % 4 == 1:
            if turno == 'MAX':
                return self.eval_min
            else:
                return self.eval_max
        else:
            if turno == 'MAX':
                return self.eval_max
            else:
                return self.eval_min

    def str_estado(self, estado):
        return str(estado)

    def str_movimiento(self, movimiento):
        return str(movimiento)


def nim(n):
    return Nim(n, 0, 1, -1)

## ===================================================================
## Algoritmo de decision minimax
## ===================================================================

##   En esta parte vamos a implementar el algoritmo de toma de
## decisiones minimax.

## ==================================================================
## Ejercicio 3
## ==================================================================

##   Implementar el procedimiento de decisión minimax visto en
## clase. Para ello definir las siguientes funciones:

## - minimax: Dado un juego, un estado del juego y un valor de
##   profundidad, devuelve el movimiento (aplicable a dicho estado en
##   el que tiene que jugar 'MAX', con mejor valor minimax de entre
##   todas las opciones disponibles) y el estado que resulta al
##   aplicar dicho movimiento.

## - valor_minimax: Dado un juego, un estado del juego, el jugador que
##   tiene el turno y un valor de profundidad, devuelve el valor
##   minimax obtenido como el valor de la función de evaluación
##   estática si se ha alcanzado la cota de profundidad, el estado es
##   final o no hay movimientos aplicables al estado; o el mejor de
##   los valores minimax de los estados sucesores (el máximo si juega
##   'MAX' o el mínimo si juega 'MIN').

## - maximizador: Dado un juego, un estado, una lista de movimientos
##   aplicables a dicho estado (sucesores) y un valor de profundidad,
##   devuelve el máximo de los valores minimax de los estados
##   obtenidos aplicando cada uno de los movimientos al estado
##   proporcionado.

## - minimizador: Dado un juego, un estado, una lista de movimientos
##   aplicables a dicho estado (sucesores) y un valor de profundidad,
##   devuelve el mínimo de los valores minimax de los estados
##   obtenidos aplicando cada uno de los movimientos al estado
##   proporcionado.

def maximizador(juego, estado, movimientos, profundidad):
    max_val = juego.eval_min
    for mov in movimientos:
        sucesor = juego.aplica(mov, estado)
        valor_actual = valor_minimax(juego, sucesor, 'MIN', profundidad)
        if valor_actual > max_val:
            max_val = valor_actual
    return max_val

def minimizador(juego, estado, movimientos, profundidad):
    min_val = juego.eval_max
    for mov in movimientos:
        sucesor = juego.aplica(mov, estado)
        valor_actual = valor_minimax(juego, sucesor, 'MAX', profundidad)
        if valor_actual < min_val:
            min_val = valor_actual
    return min_val

def valor_minimax(juego, estado, turno, profundidad):
    movimientos = juego.movimientos(estado)
    if juego.es_estado_final(estado) or profundidad == 0 or \
       len(movimientos) == 0: 
        return juego.f_evaluacion(estado, turno)
    else:
        if turno == 'MAX':
            return maximizador(juego, estado, movimientos, profundidad - 1)
        else:
            return minimizador(juego, estado, movimientos, profundidad - 1)

def minimax(juego, estado, profundidad):
    max_val = juego.eval_min
    decision = 0
    for mov in juego.movimientos(estado):
        sucesor = juego.aplica(mov, estado)
        valor_actual = valor_minimax(juego, sucesor, 'MIN', profundidad - 1)
        if valor_actual > max_val:
            max_val = valor_actual
            decision = mov
    return decision, juego.aplica(decision, estado)


## ##################################################################

## >>> from juego import *
## >>> control(juego_nim, 'MAX', [minimax, 5])
## Estado  : 17
## Jugador : MAX
## Mi turno.
## Estado  : 16
## Jugador : MIN
## Los movimientos permitidos son:
##       Quitar 3 (0)
##       Quitar 2 (1)
##       Quitar 1 (2)
## Tu turno: 0
## Estado  : 13
## Jugador : MAX
## Mi turno.
## Estado  : 12
## Jugador : MIN
## Los movimientos permitidos son:
##       Quitar 3 (0)
##       Quitar 2 (1)
##       Quitar 1 (2)
## Tu turno: 0
## Estado  : 9
## Jugador : MAX
## Mi turno.
## Estado  : 8
## Jugador : MIN
## Los movimientos permitidos son:
##       Quitar 3 (0)
##       Quitar 2 (1)
##       Quitar 1 (2)
## Tu turno: 0
## Estado  : 5
## Jugador : MAX
## Mi turno.
## Estado  : 4
## Jugador : MIN
## Los movimientos permitidos son:
##       Quitar 3 (0)
##       Quitar 2 (1)
##       Quitar 1 (2)
## Tu turno: 0
## Estado  : 1
## Jugador : MAX
## Mi turno.
## Estado  : 0
## Jugador : MIN
## El humano ha ganado

## ###################################################################
## Los siguientes apartados se proponen como ejercicio de programación
## que contará para la evaluación de la asignatura. Se podrá entregar
## a través de la página de la asignatura, en el formulario a tal
## efecto que estará disponible junto a la ficha de alumno.
## ###################################################################
## HONESTIDAD ACADÉMICA Y COPIAS: la realización de los ejercicios es
## un trabajo personal, por lo que deben completarse por cada
## estudiante de manera individual.  La discusión y el intercambio de
## información de carácter general con los compañeros se permite (e
## incluso se recomienda), pero NO AL NIVEL DE CÓDIGO. Igualmente el
## remitir código de terceros, obtenido a través de la red o cualquier
## otro medio, se considerará plagio.

## Cualquier plagio o compartición de código que se detecte
## significará automáticamente la calificación de CERO EN LA
## ASIGNATURA para TODOS los alumnos involucrados. Por tanto a estos
## alumnos NO se les conservará, para futuras convocatorias, ninguna
## nota que hubiesen obtenido hasta el momento. Independientemente de
## otras acciones de carácter disciplinario que se pudieran tomar.
## ###################################################################

## ##################################################################
## D O D G E M
## ##################################################################

##  Este juego, inventado por Colin Vout, se juega en un tablero
##  *ORDEN* x *ORDEN* (*ORDEN* > 2), con *ORDEN*-1 fichas blancas y
##  *ORDEN*-1 negras. El estado inicial del tablero donde B
##  representa una ficha blanca y N una negra sería, para un tablero
##  3x3:

##        +---+---+---+
##        | N |   |   |
##        +---+---+---+
##        | N |   |   |
##        +---+---+---+
##        |   | B | B |
##        +---+---+---+

##  Las fichas negras mueven una posición a la derecha, arriba o
##  abajo,las blancas una posición arriba, derecha o izquierda. El
##  propósito del juego es sacar las fichas del tablero (las negras
##  por la derecha y las blancas por arriba). En cada casilla sólo
##  puede haber una ficha y gana el que primero saque sus fichas del
##  tablero (o impida que el contrario pueda mover).

##  Función de evaluación:
## ------------------------

## Función de evaluación estática:

## Valora el que las negras muevan a la derecha y arriba y que las
## blancas muevan arriba y a la derecha asignando valores apropiados
## a cada casilla del tablero. También valora bloquear una posición
## del contrario colocando en la fila (o columna) que lleva al borde
## del tablero correspondiente. (Todo desde el punto de vista de las
## negras). Por ejemplo, para el juego de orden 3 los siguientes
## tableros reflejan los valores que se obtendrían por cada pieza
## dependiendo de la posición que ocupen en el tablero.
    
##  blancas                       negras              
##  Fuera: 45           		 Fuera: 45           
##  Tablero: -30  -35  -40		 Tablero: 10  25  40
##           -15  -20  -25		           5  20  35
##            -0   -5  -10		           0  15  30 

## ------------------------------------------------------------------
## Ejercicio 1
## ------------------------------------------------------------------

## Definir la clase DODGEM que implemente la representación del juego
## descrito y permita jugar para distintos tamaños de tablero.

## >>> juego = dodgem(3, 'blancas')
## >>> control(juego, 'MAX', [minimax, 5])
## Estado  : Mueven las blancas
##    +---+---+---+
##  2 | N |   |   |
##    +---+---+---+
##  1 | N |   |   |
##    +---+---+---+
##  0 |   | B | B |
##    +---+---+---+
##      0   1   2   

## Jugador : MAX
## Mi turno.
## Estado  : Mueven las negras
##    +---+---+---+
##  2 | N |   |   |
##    +---+---+---+
##  1 | N | B |   |
##    +---+---+---+
##  0 |   |   | B |
##    +---+---+---+
##      0   1   2   

## Jugador : MIN
## Los movimientos permitidos son:
##       Mover la ficha 1 hacia abajo (0)
##       Mover la ficha 2 hacia la derecha (1)
## Tu turno: 0
## Estado  : Mueven las blancas
##    +---+---+---+
##  2 | N |   |   |
##    +---+---+---+
##  1 |   | B |   |
##    +---+---+---+
##  0 | N |   | B |
##    +---+---+---+
##      0   1   2   

## Jugador : MAX
## Mi turno.
## Estado  : Mueven las negras
##    +---+---+---+
##  2 | N | B |   |
##    +---+---+---+
##  1 |   |   |   |
##    +---+---+---+
##  0 | N |   | B |
##    +---+---+---+
##      0   1   2   

## Jugador : MIN
## Los movimientos permitidos son:
##       Mover la ficha 1 hacia la derecha (0)
##       Mover la ficha 1 hacia arriba (1)
##       Mover la ficha 2 hacia abajo (2)
## Tu turno: 0
## Estado  : Mueven las blancas
##    +---+---+---+
##  2 | N | B |   |
##    +---+---+---+
##  1 |   |   |   |
##    +---+---+---+
##  0 |   | N | B |
##    +---+---+---+
##      0   1   2   

## Jugador : MAX
## Mi turno.
## Estado  : Mueven las negras
##    +---+---+---+
##  2 | N | B |   |
##    +---+---+---+
##  1 |   |   | B |
##    +---+---+---+
##  0 |   | N |   |
##    +---+---+---+
##      0   1   2   

## Jugador : MIN
## Los movimientos permitidos son:
##       Mover la ficha 1 hacia la derecha (0)
##       Mover la ficha 1 hacia arriba (1)
##       Mover la ficha 2 hacia abajo (2)
## Tu turno: 0
## Estado  : Mueven las blancas
##    +---+---+---+
##  2 | N | B |   |
##    +---+---+---+
##  1 |   |   | B |
##    +---+---+---+
##  0 |   |   | N |
##    +---+---+---+
##      0   1   2   

## Jugador : MAX
## Mi turno.
## Estado  : Mueven las negras
##    +---+---+---+
##  2 | N | B | B |
##    +---+---+---+
##  1 |   |   |   |
##    +---+---+---+
##  0 |   |   | N |
##    +---+---+---+
##      0   1   2   

## Jugador : MIN
## Los movimientos permitidos son:
##       Mover la ficha 1 hacia la derecha (0)
##       Mover la ficha 1 hacia arriba (1)
##       Mover la ficha 2 hacia abajo (2)
## Tu turno: 0
## Estado  : Mueven las blancas
##    +---+---+---+
##  2 | N | B | B |
##    +---+---+---+
##  1 |   |   |   |
##    +---+---+---+
##  0 |   |   |   |
##    +---+---+---+
##      0   1   2   

## Jugador : MAX
## Mi turno.
## Estado  : Mueven las negras
##    +---+---+---+
##  2 | N | B |   |
##    +---+---+---+
##  1 |   |   |   |
##    +---+---+---+
##  0 |   |   |   |
##    +---+---+---+
##      0   1   2   

## Jugador : MIN
## Los movimientos permitidos son:
##       Mover la ficha 2 hacia abajo (0)
## Tu turno: 0
## Estado  : Mueven las blancas
##    +---+---+---+
##  2 |   | B |   |
##    +---+---+---+
##  1 | N |   |   |
##    +---+---+---+
##  0 |   |   |   |
##    +---+---+---+
##      0   1   2   

## Jugador : MAX
## Mi turno.
## Estado  : Mueven las negras
##    +---+---+---+
##  2 |   |   |   |
##    +---+---+---+
##  1 | N |   |   |
##    +---+---+---+
##  0 |   |   |   |
##    +---+---+---+
##      0   1   2   

## Jugador : MIN
## Los movimientos permitidos son:
##       Mover la ficha 2 hacia la derecha (0)
##       Mover la ficha 2 hacia abajo (1)
##       Mover la ficha 2 hacia arriba (2)
## Tu turno: 0
## Estado  : Mueven las blancas
##    +---+---+---+
##  2 |   |   |   |
##    +---+---+---+
##  1 |   | N |   |
##    +---+---+---+
##  0 |   |   |   |
##    +---+---+---+
##      0   1   2   

## Jugador : MAX
## El humano ha ganado
## >>>

        
## ------------------------------------------------------------------
## Ejercicio 2
## ------------------------------------------------------------------

##   Implementar el algoritmo de toma de decisiones minimax con poda
##   alfabeta.

## - alfa_beta: Dado un juego, un estado del juego y una cota de
##   profundidad, devuelve el movimiento (y el estado que resulta al
##   aplicarlo) del juego aplicable a dicho estado con el que tiene que
##   jugar 'MAX'. El movimiento con mejor valor minimax de entre todas
##   las opciones disponibles.

