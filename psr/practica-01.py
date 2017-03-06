## AIA
## Problemas de Satisfacción de Restricciones
## Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
## ===================================================================

## En esta práctica vamos a programar el algoritmo de backtracking
## combinado con consistencia de arcos AC3 y la herística MRV. Al
## final se incluye el ejercicio evaluable propuesto: el algoritmo de
## reparación heurística con la heurística de mínimos conflictos.

import random, copy

## ===================================================================
## Representación de problemas de satisfacción de restricciones
## ===================================================================

##   Definimos la clase PSR que servirá para representar problemas de
## satisfacción de restricciones.

## La clase tiene tener cuatro atributos:
## - variables: una lista con las variables del problema.
## - dominios: un diccionario que asocia a cada variable su dominio,
##      una lista con los valores posibles.
## - restricciones: un diccionario que asigna a cada tupla de
##      variables la restricción que relaciona a esas variables.
## - vecinos: un diccionario que asigna a cada variables una lista con
##      las variables con las que tiene una restricción asociada.

## El constructor de la clase recibe los valores de los atributos
## "dominios" y "restricciones". Los otros dos atributos se definen a
## partir de éstos valores.

## NOTA IMPORTANTE: Supondremos en adelante que todas las
## restricciones son binarias y que existe a lo sumo una restricción
## por cada par de variables.

class PSR:
    """Clase que describe un problema de satisfacción de
    restricciones, con los siguientes atributos:
       variables     Lista de las variables del problema
       dominios      Diccionario que asigna a cada variable su dominio
                     (una lista con los valores posibles)
       restricciones Diccionario que asocia a cada tupla de variables
                     involucrada en una restricción, una función que,
                     dados valores de los dominios de esas variables,
                     determina si cumplen o no la restricción.
                     IMPORTANTE: Supondremos que para cada combinación
                     de variables hay a lo sumo una restricción (por
                     ejemplo, si hubiera dos restricciones binarias
                     sobre el mismo par de variables, consideraríamos
                     la conjunción de ambas). 
                     También supondremos que todas las restricciones
                     son binarias
        vecinos      Diccionario que representa el grafo del PSR,
                     asociando a cada variable, una lista de las
                     variables con las que comparte restricción.

    El constructor recibe los valores de los atributos dominios y
    restricciones; los otros dos atributos serán calculados al
    construir la instancia."""

    def __init__(self, dominios, restricciones):
        """Constructor de PSRs."""

        self.dominios = dominios
        self.restricciones = restricciones
        self.variables = list(dominios.keys())

        vecinos = {v: [] for v in self.variables}
        for v1, v2 in restricciones:
            vecinos[v1].append(v2)
            vecinos[v2].append(v1)
        self.vecinos = vecinos

## ===================================================================
## Ejercicio 1
## ===================================================================

##   Definir una función n_reinas(n), que recibiendo como entrada un
## número natural n, devuelva una instancia de la clase PSR,
## correspondiente al problema de las n-reinas.

## Ejemplos:

## >>> psr_n4 = n_reinas(4)
## >>> psr_n4.variables
## [1, 2, 3, 4]
## >>> psr_n4.dominios
## {1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4]}
## >>> psr_n4.restricciones
## {(1, 2): <function <lambda> at ...>,
##  (1, 3): <function <lambda> at ...>,
##  (1, 4): <function <lambda> at ...>,
##  (2, 3): <function <lambda> at ...>,
##  (3, 4): <function <lambda> at ...>,
##  (2, 4): <function <lambda> at ...>}
## >>> psr_n4.vecinos
## {1: [2, 3, 4], 2: [1, 3, 4], 3: [1, 2, 4], 4: [1, 2, 3]}
## >>> psr_n4.restricciones[(1,4)](2,3)
## True
## >>> psr_n4.restricciones[(1,4)](4,1)
## False
import itertools

def n_reinas(n):
    #Crea dominios
    dominios = {}
    for i in range(1, n + 1):
        dominios[i] = list(range(1, n + 1))
    #Crea restricciones
    permutaciones = itertools.permutations(dominios.keys(), 2)
    permutaciones = list(map(lambda x : tuple(sorted(x)), permutaciones))
    rest_keys = list(set(permutaciones))
    restricciones = {}
    for key in rest_keys: 
        restricciones[key] = lambda x, y, i = key[0], j = key[1]: (x != y) and abs(x - y) != abs(i - j)
    return PSR(dominios, restricciones)

## ===================================================================
## Parte II: Algoritmo de consistencia de arcos AC3
## ===================================================================

##   En esta parte vamos a definir el algoritmo de consistencia de arcos
## AC3 que, dado un problema de satisfacción de restricciones,
## devuelva una representación equivalente que cumple la propiedad de
## ser arco consistente (y que usualmente tiene dominios más
## reducidos.)

#   Dado un PSR, un arco es una restricción cualquiera del problema,
# asociada con una de las variables implicadas en la misma, a la que
# llamaremos variable distinguida.

## ===================================================================
## Ejercicio 2
## ===================================================================

##   Definir una función restriccion_arco que, dado un PSR, la
## variable distinguida de un arco y la variable asociada; devuelva
## una función que, dado un elemento del dominio de la variable
## distinguida y otro de la variable asociada, determine si verifican
## la restricción asociada al arco.

## Ejemplos:

## >>> restriccion_arco(psr_n4, 1, 2)
## <function n_reinas.<locals>.n_reinas_restriccion.<locals>.<lambda>
## at 0x7fdfa13d30d0>
## >>> restriccion_arco(psr_n4, 1, 2)(1, 4)
## True
## >>> restriccion_arco(psr_n4, 1, 2)(3, 2)
## False
        
## ===================================================================
## Ejercicio 3
## ===================================================================

##   Definir una función arcos que, dado un PSR, devuelva el conjunto
## de todos los arcos asociados a las restricciones del
## problema. Utilizaremos las tuplas para representar a los arcos
## siendo el primer elemento de la tupla la variable distinguida y el
## segundo la variable asociada.
		      
## Ejemplo:

## >>> arcos(psr_n4)
## [(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3),
##  (2, 4), (4, 2), (1, 4), (4, 1)]

## ===================================================================
## Ejercicio 4
## ===================================================================

##   Definir una función AC3 que, recibiendo como entrada un PSR y un
## diccionario que a cada variable del problema le asigna un dominio;
## aplique el algoritmo de consistencia de arcos AC3 a los dominios
## recibidos (ver tema 1).

## NOTA: La función AC3 debe actualizar los dominios de forma
## destructiva (es decir, después de ejecutar la llamada el
## diccionario recibido debe quedar actualizado).

## Ejemplos:

## >>> dominios = {1:[2,4],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}
## >>> AC3(psr_n4, dominios)
## >>> dominios
## {1: [2, 4], 2: [1, 4], 3: [1, 3], 4: [1, 3, 4]}

## >>> dominios = {1:[1],2:[1,2,3,4],3:[1,2,3,4],4:[1,2,3,4]}
## >>> AC3(psr_n4,dominios)
## >>> dominios
## {1: [], 2: [], 3: [], 4: []}

## >>> dominios = {1:[1,2,3,4],2:[3,4],3:[1,4],4:[1,2,3,4]}
## >>> AC3(psr_n4,dominios)
## >>> dominios
## {1: [2], 2: [4], 3: [1], 4: [3]}

## ===================================================================
## Parte III: Algoritmo de backtracking con AC3 y MRV
## ===================================================================

## En esta parte vamos a definir el algoritmo de backtracking para
## solucionar PSRs. Incorporaremos también AC3 y la heurística MRV
## para decidir la siguiente variable a asignar (tema 1).
## Este algoritmo recursivo genera un árbol de búsqueda en
## profundidad. Cada nodo del árbol de búsqueda queda definido por:
## * una asignación de valores a algunas de las variables del problema
##   (consistente con las restricciones)
## * los dominios de las variables que aún quedan por asignar (en los
##   que se han eliminado aquellos valores que no son consistentes con
##   la asignación que se tiene hasta el momento).
## Tanto la asignación como los dominios se representarán mediante
## diccionarios cuyas claves serán las variables.

## ===================================================================
## Ejercicio 5
## ===================================================================

## Definir una función MRV que, dada una lista con las variables
## pendientes de asignar y un diccionario con los dominios actuales de
## todas las variables; devuelva una variable para que sea la
## siguiente variable a asignar siguiendo el criterio MRV (es decir,
## escoger entre las pendientes de asignar aquella con menos valores
## de su dominio consistentes con los ya asignados, deshaciendo
## empates aleatoriamente).

## Ejemplos:

## >>> MRV([2, 3, 4], {1: [2], 2: [4], 3: [1, 3], 4: [1, 3, 4]})
## 2
## >>> MRV([2, 3, 4], {1: [2], 2: [3, 4], 3: [2, 4], 4: [2, 3]})
## 3
## >>> MRV([2, 3, 4], {1: [2], 2: [3, 4], 3: [2, 4], 4: [2, 3]})
## 2

## ===================================================================
## Ejercicio 6
## ===================================================================

##   Definir una función psr_backtracking_AC3_MRV que, recibiendo un
## problema de satisfacción de restricciones, le aplique el
## algoritmo de backtracking (recursivo) con AC3, utilizando MRV como
## estrategia para seleccionar en cada paso la siguiente variable a
## asignar.

## NOTA: Respecto al orden para considerar los posibles valores de una
## variable, tomarlos en el orden en el que aparecen en la lista de
## valores del dominio.

## ===================================================================
## Ejercicio 7
## ===================================================================

##   En este ejercicio no se pide ninguna función. Tan sólo comprobar
## el algoritmo anterior resolviendo diversas instancias del problema
## de las n_reinas. Para visualizar las soluciones, puede ser útil la
## siguiente función:

def dibuja_tablero_n_reinas(asig):
    def cadena_fila(i,asig):
        cadena="|"
        for j in range (1,n+1):
            if asig[i]==j:
                cadena += "X|"
            else:
                cadena += " |"
        return cadena
    n=len(asig)
    print("+"+"-"*(2*n-1)+"+")
    for i in range(1,n):
        print(cadena_fila(i,asig))
        print("|"+"-"*(2*n-1)+"|")
    print(cadena_fila(n,asig))
    print("+"+"-"*(2*n-1)+"+")

## Ejemplos:

## >>> dibuja_tablero_n_reinas(psr_backtracking_AC3_MRV(n_reinas(4)))
## +-------+
## | | |X| |
## |-------|
## |X| | | |
## |-------|
## | | | |X|
## |-------|
## | |X| | |
## +-------+

## >>> dibuja_tablero_n_reinas(psr_backtracking_AC3_MRV(n_reinas(6)))
## +-----------+
## | | | | |X| |
## |-----------|
## | | |X| | | |
## |-----------|
## |X| | | | | |
## |-----------|
## | | | | | |X|
## |-----------|
## | | | |X| | |
## |-----------|
## | |X| | | | |
## +-----------+

## >>> dibuja_tablero_n_reinas(psr_backtracking_AC3_MRV(n_reinas(8)))
## +---------------+
## | | | | | | | |X|
## |---------------|
## | | | |X| | | | |
## |---------------|
## |X| | | | | | | |
## |---------------|
## | | |X| | | | | |
## |---------------|
## | | | | | |X| | |
## |---------------|
## | |X| | | | | | |
## |---------------|
## | | | | | | |X| |
## |---------------|
## | | | | |X| | | |
## +---------------+

## >>> dibuja_tablero_n_reinas(psr_backtracking_AC3_MRV(n_reinas(14)))
## +---------------------------+
## | | | | | | | | | | | | | |X|
## |---------------------------|
## | | | | | | | | | | | |X| | |
## |---------------------------|
## | | | | | | | | | |X| | | | |
## |---------------------------|
## | | | | | | | |X| | | | | | |
## |---------------------------|
## | | |X| | | | | | | | | | | |
## |---------------------------|
## | | | | |X| | | | | | | | | |
## |---------------------------|
## | |X| | | | | | | | | | | | |
## |---------------------------|
## | | | | | | | | | | |X| | | |
## |---------------------------|
## |X| | | | | | | | | | | | | |
## |---------------------------|
## | | | | | |X| | | | | | | | |
## |---------------------------|
## | | | | | | | | | | | | |X| |
## |---------------------------|
## | | | | | | | | |X| | | | | |
## |---------------------------|
## | | | | | | |X| | | | | | | |
## |---------------------------|
## | | | |X| | | | | | | | | | |
## +---------------------------+

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

## ###################################################################
## Implementación del algoritmo de reparación heurística (con la
## heurística de mínimos conflictos), para resolver problemas de
## satisfacción de restricciones
## ###################################################################
    
## La implementación que sigue debe hacerse de manera general, y en
## ningún caso dependiente de un PSR concreto, utilizando la clase PSR
## proporcionada (no es necesario que incluya los métodos propuestos
## en los ejercicios de la práctica, aunque pueden ser de
## utilidad). Representar las asignaciones como diccionarios que
## asocien a las variables del problema un elmento del dominio de las
## mismas.

## Los ejemplos que se mostrarán corresponden al PSR 4-reinas. 

## ###################################################################
## (1)  Definir una función crea_asignacion_inicial que, dado un PSR,
## devuelva una asignación aleatoria; es decir, un diccionario que
## asocie a cada variable del problema un elemento de su dominio.

## >>> crea_asignacion_inicial(psr_n4)
## {1: 2, 2: 1, 3: 4, 4: 1}

## ###################################################################
## (2) Definir una función restricciones_incumplidas que, dado un PSR
## y una asignación; devuelva un diccionario que asocie a cada
## variable (con dominio múltiple) el número de restricciones
## incumplidas en las que participa (respecto de la asignación
## recibida).

## >>> dibuja_tablero_n_reinas({1: 3, 2: 1, 3: 1, 4: 2})
## +-------+
## | | |X| |
## |-------|
## |X| | | |
## |-------|
## |X| | | |
## |-------|
## | |X| | |
## +-------+
## >>> restricciones_incumplidas(psr_n4, {1: 3, 2: 1, 3: 1, 4: 2})
## {1: 1, 2: 1, 3: 3, 4: 1}

## >>> dibuja_tablero_n_reinas({1: 3, 2: 3, 3: 1, 4: 2})
## +-------+
## | | |X| |
## |-------|
## | | |X| |
## |-------|
## |X| | | |
## |-------|
## | |X| | |
## +-------+
## >>> restricciones_incumplidas(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2})
## {1: 2, 2: 1, 3: 2, 4: 1}

## ###################################################################
## (3) Definir una función selecciona_variable que, dado un PSR, una
## asignación y una variable; devuelva la variable (con dominio
## múltiple) que participa en el mayor número de restricciones
## incumplidas (distinta de la variable que se recibe). En caso de
## empate seleccionar aleatoriamente entre todas las que se
## corresponden con el valor máximo.

## >>> restricciones_incumplidas(psr_n4, {1: 3, 2: 1, 3: 1, 4: 2})
## {1: 1, 2: 1, 3: 3, 4: 1}
## >>> selecciona_variable(psr_n4, {1: 3, 2: 1, 3: 1, 4: 2}, 1)
## 3
## >>> selecciona_variable(psr_n4, {1: 3, 2: 1, 3: 1, 4: 2}, 3)
## 4
## >>> selecciona_variable(psr_n4, {1: 3, 2: 1, 3: 1, 4: 2}, 3)
## 1
## >>> selecciona_variable(psr_n4, {1: 3, 2: 1, 3: 1, 4: 2}, None)
## 3

## ###################################################################
## (4) Definir una función cantidad_conflictos que, dados un PSR, una
## asignación, una variable (con dominio múltiple) y un valor del
## dominio de la variable; calcule el número de restricciones
## incumplidas en las que aparece dicha variable (respecto de una
## asignación igual a la que se recibe como entrada, excepto que la
## variable indicada tiene asignado el valor indicado).

## >>> dibuja_tablero_n_reinas({1: 3, 2: 3, 3: 1, 4: 2})
## +-------+
## | | |X| |
## |-------|
## | | |X| |
## |-------|
## |X| | | |
## |-------|
## | |X| | |
## +-------+
## >>> cantidad_conflictos(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 3, 2)
## 2
## >>> cantidad_conflictos(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 3, 3)
## 3
## >>> cantidad_conflictos(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 3, 4)
## 1

## ###################################################################
## (5) Definir una función nuevo_valor que, dado un PSR, una
## asignación y una variable (con dominio múltiple); devuelva un valor
## del dominio de la variable (distinto del que tiene asociado en la
## asignación), seleccionado aleatoriamente de entre los valores que
## menos conflictos crearían respecto de las restricciones del
## problema.

## >>> dibuja_tablero_n_reinas({1: 3, 2: 3, 3: 1, 4: 2})
## +-------+
## | | |X| |
## |-------|
## | | |X| |
## |-------|
## |X| | | |
## |-------|
## | |X| | |
## +-------+
## >>> nuevo_valor(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 3)
## 4

## >>> cantidad_conflictos(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 1, 1)
## 1
## >>> cantidad_conflictos(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 1, 2)
## 2
## >>> cantidad_conflictos(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 1, 4)
## 1
## >>> nuevo_valor(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 1)
## 4
## >>> nuevo_valor(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2}, 1)
## 1

## ###################################################################
## (6) Definir una función es_solucion que, dado un PSR y una
## asignación, determine si la asignación es una solución del PSR.

## >>> es_solucion(psr_n4, {1: 3, 2: 3, 3: 1, 4: 2})
## False
## >>> es_solucion(psr_n4, {1: 3, 2: 1, 3: 4, 4: 2})
## True

## ###################################################################
## (7) Definir una función reparacion_heuristica que, dado un PSR y un
## número de iteraciones, aplique el algoritmo de reparación
## heurística con la heurística de mínimos conflictos. El argumento
## iteraciones proporciona el número de asignaciones máximo que se
## pueden generar (por defecto, usar 1000 iteraciones).

## Si no se encuentra solución en el número máximo de iteraciones, la
## función debe devolver None. En caso contrario, debe devolver la
## solución encontrada junto con el número de iteraciones que han sido
## necesarias para encontrarla.

## Como ejemplos, usar la implementación para resolver el problema
## n-reinas hasta el mayor n en el que se pueda realizar en un tiempo
## razonable. 

# >>> reparacion_heuristica(psr_n4)
# ({1: 3, 2: 1, 3: 4, 4: 2}, 4)

## ###################################################################
