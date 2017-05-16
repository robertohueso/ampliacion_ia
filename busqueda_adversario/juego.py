### juego.py
### Procedimiento de control de un juego.
###===================================================================

from minimax import *

###*******************************************************************
### Funciones y variables externas
###*******************************************************************

### Procedentes de la clase Juego:
### estado_inicial
###    => estado inicial del juego.
### es_estado_final(ESTADO)
###    => True, si  ESTADO es final; False en caso contrario.
### es_estado_ganador(ESTADO, TURNO, JUGADOR)
###    => True, si y sólo si en el ESTADO, cuando le toca mover al
###       jugador TURNO, el JUGADOR ha ganado la partida.
### movimientos(ESTADO)
###    => Lista con las representaciones de los movimientos aplicables
###       al ESTADO.
### aplica(MOVIMIENTO, ESTADO)
###    => Aplica el MOVIMIENTO al ESTADO para generar un nuevo estado.

###*******************************************************************
### § Procedimientos de control de juegos.
###*******************************************************************

### Los nodos del árbol, NODO_J, de desarrollo del juego serán
### diccionarios con 3 campos: ESTADO, JUGADOR y VALOR.

### ESTADO describirá la situación del juego, JUGADOR valdrá MAX, si
###   le toca jugar al ordenador, o MIN, si le toca jugar al humano, y
###   VALOR almacenará el valor de la situación del juego.

### crea_nodo_j_inicial(JUEGO, JUGADOR)
### Valor: El NODO_J asociado al estado_inicial del juego, en el que
###   el JUGADOR comienza la partida.

def crea_nodo_j_inicial (juego, jugador):
    return {'estado' : juego.estado_inicial, 'jugador' : jugador}

### escribe_nodo_j(NODO_J)
### Efecto: Escribe en pantalla los campos ESTADO y JUGADOR del NODO_J.

def escribe_nodo_j (juego, nodo_j):
  print('Estado  : {0}\nJugador : {1}'.format(juego.str_estado(nodo_j['estado']),
                                              nodo_j['jugador']))
  

### control(JUEGO, JUGADOR_INICIAL, PROCEDIMIENTO)
### Efecto: Controla el desarrollo de un juego.
### Procedimiento:
### 1. crear el nodo de juego inicial con JUGADOR_INICIAL como jugador
###    que comienza la partida.
### 2. Si el estado_inicial del JUEGO es un estado final,
###    2.1 analizar el final para el nodo de juego inicial
###    2.2 en caso contrario,
###        2.2.1 Si el JUGADOR_INICIAL es MAX,
###              2.2.1.1 procesar la jugada de la máquina.
###              2.2.1.2 en caso contrario, procesar la jugada del
###                      humano.

def control(juego, jugador_inicial, procedimiento = [minimax, 5]):
  nodo_j_inicial = crea_nodo_j_inicial(juego, jugador_inicial)
  if juego.es_estado_final(juego.estado_inicial):
    analiza_final(juego, nodo_j_inicial)
  else:
    if jugador_inicial == 'MAX':
      jugada_maquina(juego, procedimiento, nodo_j_inicial)
    else:
      jugada_humana(juego, procedimiento, nodo_j_inicial)

### analiza_final(JUEGO, NODO_J)
### Efecto: Escribe en pantalla el NODO_J y si gana la máquina,
###   escribe en pantalla "La maquina ha ganado", si gana el humano,
###   escribe en pantalla "El humano ha ganado", en caso contrario
###   escribe en pantalla "Empate".

def analiza_final(juego, nodo_j):
  escribe_nodo_j(juego, nodo_j)
  if juego.es_estado_ganador(nodo_j['estado'], nodo_j['jugador'], 'MAX'):
     print('La maquina ha ganado')
  elif juego.es_estado_ganador(nodo_j['estado'], nodo_j['jugador'], 'MIN'):
    print('El humano ha ganado')
  else:
    print('Empate')

### escribe_movimientos(movimientos)
### Efecto: Escribe en pantalla la lista de los movimientos

def escribe_movimientos(juego, movimientos):
    print('Los movimientos permitidos son:')
    numero = 0
    for m in movimientos:
        print('      {0} ({1})'.format(juego.str_movimiento(m), numero))
        numero += 1

### jugada_humana(JUEGO, PROCEDIMIENTO, NODO_J)
### Efecto: Procesa la jugada humana.
### Procedimiento:
### 1. Escribe en pantalla el NODO_J
### 2. Escribe en pantalla la lista de los movimientos posibles
### 3. Solicita del jugador humano una jugada, se trata de un número que
###    representa el movimiento que el humano quiere hacer.
### 4. Si el dato introducido por el jugador humano es un número que se
###    corresponde con una posición en la lista de movimientos posibles, hacer:
###    4.1.1 Aplicar el movimiento elegido al estado del NODO_J, creando un
###          NUEVO_ESTADO.
###          4.1.2.1.1 Crear el nodo SIGUIENTE con el NUEVO_ESTADO y en el que
###                    el jugador es MAX. 
###          4.1.2.1.2 Si el NUEVO_ESTADO es un estado final,
###                    4.1.2.1.2.1 analizar el nodo final 
###                    4.1.2.1.2.2 en caso contrario, procesar la jugada de la
###                                máquina. 
###    4.2 en caso contrario hacer,
###        4.2.1 Escribir en pantalla que la elección es incorrecta.
###        4.2.2 Procesar la jugada del humano.

def jugada_humana(juego, procedimiento, nodo_j):
  escribe_nodo_j(juego, nodo_j)
  movimientos_posibles = juego.movimientos(nodo_j['estado'])
  escribe_movimientos(juego, movimientos_posibles)
  m = int(input('Tu turno: '))
  if (-1 < m <  len(movimientos_posibles)):
    nuevo_estado = juego.aplica(movimientos_posibles[m], nodo_j['estado'])
    siguiente = {'estado' : nuevo_estado, 'jugador' : 'MAX'}
    if juego.es_estado_final(nuevo_estado):
      analiza_final(juego, siguiente)
    else:
      jugada_maquina(juego, procedimiento, siguiente)
  else:
    print('  {} es ilegal.'.format(m))
    jugada_humana(juego, procedimiento, nodo_j)

### jugada_maquina(JUEGO, PROCEDIMIENTO, NODO_J)
### Efecto: Procesa la jugada de la máquina.
### Procedimiento:
### 1. Escribe en pantalla el NODO_J
### 2. Aplica el PROCEDIMIENTO de decisión al NODO_J y determina el nodo
###    SIGUIENTE 
### 3. Si el estado del nodo SIGUIENTE es un estado final,
###    3.1 analizar el nodo final SIGUIENTE
###    3.2 en caso contrario, procesar la jugada humana.

def jugada_maquina(juego, procedimiento, nodo_j):
  escribe_nodo_j(juego, nodo_j)
  print('Mi turno.')
  movimiento, estado = aplica_decision(juego, procedimiento, nodo_j)
  if juego.es_estado_final(estado):
    analiza_final(juego, {'estado': estado, 'jugador': 'MIN'})
  else:
    jugada_humana(juego, procedimiento, {'estado': estado, 'jugador': 'MIN'})

def aplica_decision(juego, procedimiento, nodo_j):
  return procedimiento[0](juego, nodo_j['estado'], procedimiento[1])
