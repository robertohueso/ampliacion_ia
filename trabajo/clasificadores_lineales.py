# ==========================================================
# Ampliación de Inteligencia Artificial. Tercer curso. 
# Grado en Ingeniería Informática - Tecnologías Informáticas
# Curso 2016-17
# Trabajo práctico
# ===========================================================

# --------------------------------------------------------------------------
# Autor del trabajo:
#
# APELLIDOS: HUESO GOMEZ
# NOMBRE: ROBERTO
#
# ----------------------------------------------------------------------------


# *****************************************************************************
# HONESTIDAD ACADÉMICA Y COPIAS: un trabajo práctico es un examen, por lo que
# debe realizarse de manera individual. La discusión y el intercambio de
# información de carácter general con los compañeros se permite (e incluso se
# recomienda), pero NO AL NIVEL DE CÓDIGO. Igualmente el remitir código de
# terceros, OBTENIDO A TRAVÉS DE LA RED o cualquier otro medio, se considerará
# plagio. 

# Cualquier plagio o compartición de código que se detecte significará
# automáticamente la calificación de CERO EN LA ASIGNATURA para TODOS los
# alumnos involucrados. Por tanto a estos alumnos NO se les conservará, para
# futuras convocatorias, ninguna nota que hubiesen obtenido hasta el
# momento. SIN PERJUICIO DE OTRAS MEDIDAS DE CARÁCTER DISCIPLINARIO QUE SE
# PUDIERAN TOMAR.  
# *****************************************************************************


# IMPORTANTE: NO CAMBIAR EL NOMBRE NI A ESTE ARCHIVO NI A LAS CLASES Y MÉTODOS
# QUE SE PIDEN

# NOTA: En este trabajo no se permite usar scikit-learn

# ====================================================
# PARTE I: MODELOS LINEALES PARA CLASIFICACIÓN BINARIA
# ====================================================

# En esta primera parte se pide implementar en Python los siguientes
# clasificadores BINARIOS, todos ellos vistos en el tema 5.

# - Perceptron umbral
# - Regresión logística minimizando el error cuadrático:
#      * Versión batch
#      * Versión estocástica (regla delta)
# - Regresión logística maximizando la verosimilitud:
#      * Versión batch
#      * Versión estocástica


# --------------------------------------------
# I.1. Generando conjuntos de datos aleatorios
# --------------------------------------------

# Previamente a la implementación de los clasificadores, conviene tener
# funciones que generen aleatoriamente conjuntos de datos fictícios. 
# En concreto, se pide implementar estas dos funciones:

# * Función genera_conjunto_de_datos_l_s(rango,dim,n_datos): 

#   Debe devolver dos listas X e Y, generadas aleatoriamente. La lista X debe
#   tener un número total n_datos de elelemntos, siendo cada uno de ellos una
#   lista (un ejemplo) de dim componentes, con valores entre -rango y rango. El
#   conjunto Y debe tener la clasificación binaria (1 o 0) de cada ejemplo del
#   conjunto X, en el mismo orden. El conjunto de datos debe ser linealmente
#   separable.

#   SUGERENCIA: generar en primer lugar un hiperplano aleatorio (mediante sus
#   coeficientes, elegidos aleatoriamente entre -rango y rango). Luego generar
#   aleatoriamente cada ejemplo de igual manera y clasificarlo como 1 o 0
#   dependiendo del lado del hiperplano en el que se situe. Eso asegura que el
#   conjunto de datos es linealmente separable.


# * Función genera_conjunto_de_datos_n_l_s(rango,dim,size,prop_n_l_s=0.1):

#   Como la anterior, pero el conjunto de datos debe ser no linealmente
#   separable. Para ello generar el conjunto de datos con la función anterior
#   y cambiar de clase a una proporción pequeña del total de ejemplos (por
#   ejemplo el 10%). La proporción se da con prop_n_l_s. 

import random
import numpy as np

def genera_conjunto_de_datos_l_s(rango,dim,n_datos):
#Conjuntos linealmente separables
    hiperplano = np.random.uniform(-rango, rango, dim)
    X = np.random.uniform(-rango, rango, (n_datos, dim))
    Y = np.empty(n_datos)
    for i, sample in enumerate(X):
        if np.inner(hiperplano, sample) >= 0:
            Y[i] = 1
        else:
            Y[i] = 0
    Y = Y.astype('int')
    return X, Y

#Conjuntos no linealmente separables
def genera_conjunto_de_datos_n_l_s(rango,dim,size,prop_n_l_s=0.1):
    X, Y = genera_conjunto_de_datos_l_s(rango, dim, size)
    elementos_a_modificar = random.sample(range(size), int(prop_n_l_s*size))
    for i in elementos_a_modificar:
        if Y[i] == 0:
            Y[i] = 1
        else:
            Y[i] = 0
    return X, Y

# -----------------------------------
# I.2. Clases y métodos a implementar
# -----------------------------------

# En esta sección se pide implementar cada uno de los clasificadores lineales
# mencionados al principio. Cada uno de estos clasificadores se implementa a
# través de una clase python, que ha de tener la siguiente estructura general:

# class NOMBRE_DEL_CLASIFICADOR():

#     def __init__(self,clases,normalizacion=False):

#          .....
         
#     def entrena(self,entr,clas_entr,n_epochs,rate=0.1,
#                 pesos_iniciales=None,
#                 rate_decay=False):

#         ......

#     def clasifica_prob(self,ej):


#         ......

#     def clasifica(self,ej):


#         ......
        

# Explicamos a continuación cada uno de estos elementos:

# * NOMBRE_DEL_CLASIFICADOR:
# --------------------------


#  Este es el nombre de la clase que implementa el clasificador. 
#  Obligatoriamente se han de usar cada uno de los siguientes
#  nombres:

#  - Perceptrón umbral: 
#                       Clasificador_Perceptron
#  - Regresión logística, minimizando L2, batch: 
#                       Clasificador_RL_L2_Batch
#  - Regresión logística, minimizando L2, estocástico: 
#                       Clasificador_RL_L2_St
#  - Regresión logística, maximizando verosimilitud, batch: 
#                       Clasificador_RL_ML_Batch
#  - Regresión logística, maximizando verosimilitud, estocástico: 
#                       Clasificador_RL_ML_St



# * Constructor de la clase:
# --------------------------

#  El constructor debe tener los siguientes argumentos de entrada:

#  - Una lista clases con los nombres de las clases del problema de
#    clasificación, tal y como aparecen en el conjunto de datos. 
#    Por ejemplo, en el caso del problema de las votaciones, 
#    esta lista sería ["republicano","democrata"]

#  - El parámetro normalizacion, que puede ser True o False (False por
#    defecto). Indica si los datos se tienen que normalizar, tanto para el
#    entrenamiento como para la clasificación de nuevas instancias.  La
#    normalización es una técnica que suele ser útil cuando los distintos
#    atributos reflejan cantidades numéricas de muy distinta magnitud.
#    En ese caso, antes de entrenar se calcula la media m_i y la desviación
#    típica d_i en cada componente i-esima (es decir, en cada atributo) de los
#    datos del conjunto de entrenamiento.  A continuación, y antes del
#    entrenamiento, esos datos se transforman de manera que cada componente
#    x_i se cambia por (x_i - m_i)/d_i. Esta misma transformación se realiza
#    sobre las nuevas instancias que se quieran clasificar.  NOTA: se permite
#    usar la biblioteca numpy para calcular la media, la desviación típica, y
#    en general para cualquier cálculo matemático.



# * Método entrena:
# -----------------

#  Este método es el que realiza el entrenamiento del clasificador. 
#  Debe calcular un conjunto de pesos, mediante el correspondiente
#  algoritmo de entrenamiento. Describimos a continuación los parámetros de
#  entrada:  

#  - entr y clas_entr, son los datos del conjunto de entrenamiento y su
#    clasificación, respectivamente. El primero es una lista con los ejemplos,
#    y el segundo una lista con las clasificaciones de esos ejemplos, en el
#    mismo orden. 

#  - n_epochs: número de veces que se itera sobre todo el conjunto de
#    entrenamiento.

#  - rate: si rate_decay es False, rate es la tasa de aprendizaje fija usada
#    durante todo el aprendizaje. Si rate_decay es True, rate marca una cota
#    mínima de la tasa de aprendizaje, como se explica a continuación. 

#  - rate_decay, indica si la tasa de aprendizaje debe disminuir a medida que
#    se van realizando actualizaciones de los pases. En concreto, si
#    rate_decay es True, la tasa de aprendizaje que se usa en cada
#    actualización se debe de calcular con la siguiente fórmula:
#       rate_n= rate_0 + (2/n**(1.5)) 
#    donde n es el número de actualizaciones de pesos realizadas hasta el
#    momento, y rate_0 es la cantidad introducida en el parámetro rate
#    anterior.   
#
#  - pesos_iniciales: si es None, se indica que los pesos deben iniciarse
#    aleatoriamente (por ejemplo, valores aleatorios entre -1 y 1). Si no es
#    None, entonces se debe proporcionar la lista de pesos iniciales. Esto
#    puede ser útil para continuar el aprendizaje a partir de un aprendizaje
#    anterior, si por ejemplo se dispone de nuevos datos.    

#  NOTA: En las versiones estocásticas, y en el perceptrón umbral, en cada
#  epoch recorrer todos los ejemplos del conjunto de entrenamiento en un orden
#  aleatorio distinto cada vez.  


# * Método clasifica_prob:
# ------------------------

#  El método que devuelve la probabilidad de pertenecer a la clase (la que se
#  ha tomado como clase 1), calculada para un nuevo ejemplo. Este método no es
#  necesario incluirlo para el perceptrón umbral.


        
# * Método clasifica:
# -------------------
    
#  El método que devuelve la clase que se predice para un nuevo ejemplo. La
#  clase debe ser una de las clases del problema (por ejemplo, "republicano" o
#  "democrata" en el problema de los votos).  


# Si el clasificador aún no ha sido entrenado, tanto "clasifica" como
# "clasifica_prob" deben devolver una excepción del siguiente tipo:

class ClasificadorNoEntrenado(Exception):
    pass

#  NOTA: Se aconseja probar el funcionamiento de los clasificadores con
#  conjuntos de datos generados por las funciones del apartado anterior. 

# Ejemplo de uso:

# ------------------------------------------------------------

# Generamos un conjunto de datos linealmente separables, 
# In [1]: X1,Y1,w1=genera_conjunto_de_datos_l_s(4,8,400)

# Lo partimos en dos trozos:
# In [2]: X1e,Y1e=X1[:300],Y1[:300]

# In [3]: X1t,Y1t=X1[300:],Y1[300:]

# Creamos el clasificador (perceptrón umbral en este caso): 
# In [4]: clas_pb1=Clasificador_Perceptron([0,1])

# Lo entrenamos con elprimero de los conjuntos de datos:
# In [5]: clas_pb1.entrena(X1e,Y1e,100,rate_decay=True,rate=0.001)

# Clasificamos un ejemplo del otro conjunto, y lo comparamos con su clase real:
# In [6]: clas_pb1.clasifica(X1t[0]),Y1t[0]
# Out[6]: (1, 1)

# Comprobamos el porcentaje de aciertos sobre todos los ejemplos de X2t
# In [7]: sum(clas_pb1.clasifica(x) == y for x,y in zip(X1t,Y1t))/len(Y1t)
# Out[7]: 1.0

# Repetimos el experimento, pero ahora con un conjunto de datos que no es
# linealmente separable: 
# In [8]: X2,Y2,w2=genera_conjunto_de_datos_n_l_s(4,8,400,0.1)

# In [8]: X2e,Y2e=X2[:300],Y2[:300]

# In [9]: X2t,Y2t=X2[300:],Y2[300:]

# In [10]: clas_pb2=Clasificador_Perceptron([0,1])

# In [11]: clas_pb2.entrena(X2e,Y2e,100,rate_decay=True,rate=0.001)

# In [12]: clas_pb2.clasifica(X2t[0]),Y2t[0]
# Out[12]: (1, 0)

# In [13]: sum(clas_pb2.clasifica(x) == y for x,y in zip(X2t,Y2t))/len(Y2t)
# Out[13]: 0.82
# ----------------------------------------------------------------

#Funciones auxiliares

def normalizaDataset(dataset):
    media = np.mean(dataset, axis = 0)
    desviacion = np.std(dataset, axis = 0)
    

#Clases
class Clasificador():
    def __init__(self, clases, normalizacion = False):
        self.clases = clases
        self.normalizacion = normalizacion
        self.entrenado = False

    def entrena(self, entr, clas_entr, n_epochs, rate = 0.1,
                pesos_iniciales = None, rate_decay = False):
        pass

    def clasifica_prob(self, ej):
        pass

    def clasifica(self, ej):
        pass



#Clasificador Perceptron---------------------------------------------------
class Clasificador_Perceptron(Clasificador):
    def __init__(self, clases, normalizacion = False):
        super().__init__(clases, normalizacion)
        self.pesos = None
    
    def entrena(self, entr, clas_entr, n_epochs, rate = 0.1,
                pesos_iniciales = None, rate_decay = False):
        
        #Normalizacion
        if self.normalizacion:
            self.media = np.mean(entr, axis = 0)
            self.desviacion = np.std(entr, axis = 0)
            entr = (entr - self.media) / self.desviacion
        
        #Inicializar pesos
        if pesos_iniciales is None:
            pesos_iniciales = np.random.uniform(-1, 1, len(entr[0]))
        self.pesos = pesos_iniciales
        
        self.entrenado = True

        #Entrenamiento
        rate_n = rate
        n = 1
        for i in range(n_epochs):
            for ej, clase in zip(entr, clas_entr):
                if rate_decay:
                    rate_n = rate + (2 / n**1.5)
                    n += 1
                self.pesos = self.pesos + rate_n * ej * (clase - self.umbral(ej))

    def umbral(self, ej):
        if np.inner(self.pesos, ej) >= 0:
            return 1
        else:
            return 0

    def clasifica(self, ej):
        if not self.entrenado:
            raise ClasificadorNoEntrenado
        else:
            if self.normalizacion:
                ej = (ej - self.media) / self.desviacion
            return self.umbral(ej)

#Clasificador regresion logistica min L2 batch-----------------------------
class Clasificador_RL_L2_Batch(Clasificador):
    def __init__(self, clases, normalizacion = False):
        super().__init__(clases, normalizacion)
        self.pesos = None
    
    def entrena(self, entr, clas_entr, n_epochs, rate = 0.1,
                pesos_iniciales = None, rate_decay = False):
        
        #Normalizacion
        if self.normalizacion:
            self.media = np.mean(entr, axis = 0)
            self.desviacion = np.std(entr, axis = 0)
            entr = (entr - self.media) / self.desviacion
        
        #Inicializar pesos
        if pesos_iniciales is None:
            pesos_iniciales = np.random.uniform(-1, 1, len(entr[0]))
        self.pesos = pesos_iniciales
        
        self.entrenado = True

        #Entrenamiento
        rate_n = rate
        n = 1
        for i in range(n_epochs):
            if rate_decay:
                rate_n = rate + (2 / n**1.5)
                n += 1
            gradiente = np.zeros(len(entr[0]))
            for ej, clase in zip(entr, clas_entr):
                o = self.sigmoide(ej)
                gradiente += (clase - o) * o * (1 - o) * ej
            gradiente = -2 * gradiente
            self.pesos = self.pesos - rate_n * gradiente

    def sigmoide(self, ej):
        wx = np.inner(self.pesos, ej)
        return 1 / (1 + np.exp(-wx))

    def clasifica_prob(self,ej):
        if not self.entrenado:
            raise ClasificadorNoEntrenado
        #Normalizacion
        if self.normalizacion:
            ej = (ej - self.media) / self.desviacion
        #Clasificacion
        return self.sigmoide(ej)

    def clasifica(self, ej):
        if not self.entrenado:
            raise ClasificadorNoEntrenado
        if self.clasifica_prob(ej) >= 0.5:
            return 1
        else:
            return 0

#Clasificador regresion logistica L2 St--------------------------------
class Clasificador_RL_L2_St(Clasificador_RL_L2_Batch):
    
    def entrena(self, entr, clas_entr, n_epochs, rate = 0.1,
                pesos_iniciales = None, rate_decay = False):
        
        #Normalizacion
        if self.normalizacion:
            self.media = np.mean(entr, axis = 0)
            self.desviacion = np.std(entr, axis = 0)
            entr = (entr - self.media) / self.desviacion
        
        #Inicializar pesos
        if pesos_iniciales is None:
            pesos_iniciales = np.random.uniform(-1, 1, len(entr[0]))
        self.pesos = pesos_iniciales
        
        self.entrenado = True

        #Entrenamiento
        rate_n = rate
        n = 1
        for i in range(n_epochs):
            for ej, clase in zip(entr, clas_entr):
                if rate_decay:
                    rate_n = rate + (2 / n**1.5)
                    n += 1
                o = self.sigmoide(ej)
                self.pesos = self.pesos + rate_n * (clase-o) * ej * o * (1-o)

#Clasificador regresion logistica ML Batch--------------------------------
class Clasificador_RL_ML_Batch(Clasificador_RL_L2_Batch):
    
    def entrena(self, entr, clas_entr, n_epochs, rate = 0.1,
                pesos_iniciales = None, rate_decay = False):
        
        #Normalizacion
        if self.normalizacion:
            self.media = np.mean(entr, axis = 0)
            self.desviacion = np.std(entr, axis = 0)
            entr = (entr - self.media) / self.desviacion
        
        #Inicializar pesos
        if pesos_iniciales is None:
            pesos_iniciales = np.random.uniform(-1, 1, len(entr[0]))
        self.pesos = pesos_iniciales
        
        self.entrenado = True

        #Entrenamiento
        rate_n = rate
        n = 1
        for i in range(n_epochs):
            if rate_decay:
                rate_n = rate + (2 / n**1.5)
                n += 1
            gradiente = np.zeros(len(entr[0]))
            for ej, clase in zip(entr, clas_entr):
                o = self.sigmoide(ej)
                gradiente += (clase - o) * ej
            self.pesos = self.pesos + rate_n * gradiente

#Clasificador regresion logistica ML St--------------------------------
class Clasificador_RL_ML_St(Clasificador_RL_L2_Batch):
    
    def entrena(self, entr, clas_entr, n_epochs, rate = 0.1,
                pesos_iniciales = None, rate_decay = False):
        
        #Normalizacion
        if self.normalizacion:
            self.media = np.mean(entr, axis = 0)
            self.desviacion = np.std(entr, axis = 0)
            entr = (entr - self.media) / self.desviacion
        
        #Inicializar pesos
        if pesos_iniciales is None:
            pesos_iniciales = np.random.uniform(-1, 1, len(entr[0]))
        self.pesos = pesos_iniciales
        
        self.entrenado = True

        #Entrenamiento
        rate_n = rate
        n = 1
        for i in range(n_epochs):
            for ej, clase in zip(entr, clas_entr):
                if rate_decay:
                    rate_n = rate + (2 / n**1.5)
                    n += 1
                o = self.sigmoide(ej)
                self.pesos = self.pesos + rate_n * (clase-o) * ej

# --------------------------
# I.3. Curvas de aprendizaje
# --------------------------

# Se pide mostrar mediante gráficas la evolución del aprendizaje de los
# distintos algoritmos. En concreto, para cada clasificador usado con un
# conjunto de datos generado aleatoriamente con las funciones anteriores, las
# dos siguientes gráficas: 

# - Una gráfica que indique cómo evoluciona el porcentaje de errores que
#   comete el clasificador sobre el conjunto de entrenamiento, en cada epoch.    
# - Otra gráfica que indique cómo evoluciona el error cuadrático o la log
#   verosimilitud del clasificador (dependiendo de lo que se esté optimizando
#   en cada proceso de entrenamiento), en cada epoch.

# Para realizar gráficas, se recomiendo usar la biblioteca matplotlib de
# python: 

import matplotlib.pyplot as plt


# Lo que sigue es un ejemplo de uso, para realizar una gráfica sencilla a 
# partir de una lista "errores", que por ejemplo podría contener los sucesivos
# porcentajes de error que comete el clasificador, en los sucesivos epochs: 


# plt.plot(range(1,len(errores)+1),errores,marker='o')
# plt.xlabel('Epochs')
# plt.ylabel('Porcentaje de errores')
# plt.show()

# Basta con incluir un código similar a este en el fichero python, para que en
# la terminal de Ipython se genere la correspondiente gráfica.

# Se pide generar una serie de gráficas que permitan explicar el
# comportamiento de los algoritmos, con las distintas opciones, y con
# conjuntos separables y no separables. Comentar la interpretación de las
# distintas gráficas obtenidas. 

# NOTA: Para poder realizar las gráficas, debemos modificar los
# algoritmos de entrenamiento para que ademas de realizar el cálculo de los
# pesos, también calcule las listas con los sucesivos valores (de errores, de
# verosimilitud,etc.) que vamos obteniendo en cada epoch. Esta funcionalidad
# extra puede enlentecer algo el proceso de entrenamiento y si fuera necesario
# puede quitarse una vez se realize este apartado.










# ==================================
# PARTE II: CLASIFICACIÓN MULTICLASE
# ==================================

# Se pide implementar algoritmos de regresión logística para problemas de
# clasificación en los que hay más de dos clases. Para ello, usar las dos
# siguientes aproximaciones: 

# ------------------------------------------------
# II.1 Técnica "One vs Rest" (Uno frente al Resto)
# ------------------------------------------------

#  Esta técnica construye un clasificador multiclase a partir de
#  clasificadores binarios que devuelven probabilidades (como es el caso de la
#  regresión logística). Para cada posible valor de clasificación, se
#  entrena un clasificador que estime cómo de probable es pertemecer a esa
#  clase, frente al resto. Este conjunto de clasificadores binarios se usa
#  para dar la clasificación de un ejemplo nuevo, sin más que devolver la
#  clase para la que su correspondiente clasificador binario da una mayor
#  probabilidad. 

#  En concreto, se pide implementar una clase python Clasificador_RL_OvR con
#  la siguiente estructura, y que implemente el entrenamiento y la
#  clasificación como se ha explicado. 

# class Clasificador_RL_OvR():

#     def __init__(self,class_clasif,clases):

#        .....
#     def entrena(self,entr,clas_entr,n_epochs,rate=0.1,rate_decay=False):

#        .....

#     def clasifica(self,ej):

#        .....            

#  Excepto "class_clasif", los restantes parámetros de los métodos significan
#  lo mismo que en el apartado anterior, excepto que ahora "clases" puede ser
#  una lista con más de dos elementos. El parámetro class_clasif es el nombre
#  de la clase que implementa el clasificador binario a partir del cual se
#  forma el clasificador multiclase.   

#  Un ejemplo de sesión, con el problema del iris:

# ---------------------------------------------------------------
# In [28]: from iris import *

# In [29]: iris_clases=["Iris-setosa","Iris-virginica","Iris-versicolor"]

# Creamos el clasificador, a partir de RL binaria estocástico:
# In [30]: clas_rlml1=Clasificador_RL_OvR(Clasificador_RL_ML_St,iris_clases)

# Lo entrenamos: 
# In [32]: clas_rlml1.entrena(iris_entr,iris_entr_clas,100,rate_decay=True,rate=0.01)

# Clasificamos un par de ejemplos, comparándolo con su clase real:
# In [33]: clas_rlml1.clasifica(iris_entr[25]),iris_entr_clas[25]
# Out[33]: ('Iris-setosa', 'Iris-setosa')

# In [34]: clas_rlml1.clasifica(iris_entr[78]),iris_entr_clas[78]
# Out[34]: ('Iris-versicolor', 'Iris-versicolor')
# ----------------------------------------------------------------




# ------------------------------------------------
# II.1 Regresión logística con softmax 
# ------------------------------------------------


#  Se pide igualmente implementar un clasificador en python que implemente la
#  regresión multinomial logística mdiante softmax, tal y como se describe en
#  el tema 5, pero solo la versión ESTOCÁSTICA.

#  En concreto, se pide implementar una clase python Clasificador_RL_Softmax 
#  con la siguiente estructura, y que implemente el entrenamiento y la 
#  clasificación como seexplica en el tema 5:

# class Clasificador_RL_Softmax():

#     def __init__(self,clases):

#        .....
#     def entrena(self,entr,clas_entr,n_epochs,rate=0.1,rate_decay=False):

#        .....

#     def clasifica(self,ej):

#        .....            





# ===========================================
# PARTE III: APLICACIÓN DE LOS CLASIFICADORES
# ===========================================

# En este apartado se pide aplicar alguno de los clasificadores implementados
# en el apartado anterior,para tratar de resolver tres problemas: el de los
# votos, el de los dígitos y un tercer problema que hay que buscar. 

# -------------------------------------
# III.1 Implementación del rendimiento
# -------------------------------------

# Una vez que hemos entrenado un clasificador, podemos medir su rendimiento
# sobre un conjunto de ejemplos de los que se conoce su clasificación,
# mediante el porcentaje de ejemplos clasificados correctamente. Se ide
# definir una función rendimiento(clf,X,Y) que calcula el rendimiento de
# clasificador concreto clf, sobre un conjunto de datos X cuya clasificación
# conocida viene dada por la lista Y. 
# NOTA: clf es un objeto de las clases definidas en
# los apartados anteriores, que además debe estar ya entrenado. 


# Por ejemplo (conectando con el ejemplo anterior):

# ---------------------------------------------------------
# In [36]: rendimiento(clas_rlml1,iris_entr,iris_entr_clas)
# Out[36]: 0.9666666666666667
# ---------------------------------------------------------




# ----------------------------------
# III.2 Aplicando los clasificadores
# ----------------------------------

#  Obtener un clasificador para cada uno de los siguientes problemas,
#  intentando que el rendimiento obtenido sobre un conjunto independiente de
#  ejemplos de prueba sea lo mejor posible. 

#  - Predecir el partido de un congresista en función de lo que ha votado en
#    las sucesivas votaciones, a partir de los datos en el archivo votos.py que
#    se suministra.  

#  - Predecir el dígito que se ha escrito a mano y que se dispone en forma de
#    imagen pixelada, a partir de los datos que están en el archivo digidata.zip
#    que se suministra.  Cada imagen viene dada por 28x28 píxeles, y cada pixel
#    vendrá representado por un caracter "espacio en blanco" (pixel blanco) o
#    los caracteres "+" (borde del dígito) o "#" (interior del dígito). En
#    nuestro caso trataremos ambos como un pixel negro (es decir, no
#    distinguiremos entre el borde y el interior). En cada conjunto las imágenes
#    vienen todas seguidas en un fichero de texto, y las clasificaciones de cada
#    imagen (es decir, el número que representan) vienen en un fichero aparte,
#    en el mismo orden. Será necesario, por tanto, definir funciones python que
#    lean esos ficheros y obtengan los datos en el mismo formato python en el
#    que los necesitan los algoritmos.

#  - Cualquier otro problema de clasificación (por ejemplo,
#    alguno de los que se pueden encontrar en UCI Machine Learning repository,
#    http://archive.ics.uci.edu/ml/). Téngase en cuenta que el conjunto de
#    datos que se use ha de tener sus atríbutos numéricos. Sin embargo,
#    también es posible transformar atributos no numéricos en numéricos usando
#    la técnica conocida como "one hot encoding".   


#  Nótese que en cualquiera de los tres casos, consiste en encontrar el
#  clasificador adecuado, entrenado con los parámetros y opciones
#  adecuadas. El entrenamiento ha de realizarse sobre el conjunto de
#  entrenamiento, y el conjunto de validación se emplea para medir el
#  rendimiento obtenido con los distintas combinaciones de parámetros y
#  opciones con las que se experimente. Finalmente, una vez elegido la mejor
#  combinación de parámetros y opciones, se da el rendimiento final sobre el
#  conjunto de test. Es importante no usar el conjunto de test para decididir
#  sobre los parámetros, sino sólo para dar el rendimiento final.

#  En nuestro caso concreto, estas son las opciones y parámetros con los que
#  hay que experimentar: 

#  - En primer lugar, el tipo de clasificador usado (si es batch o
#    estaocástico, si es basado en error cuadrático o en verosimilitud, si es
#    softmax o OvR,...)
#  - n_epochs: el número de epochs realizados influye en el tiempo de
#    entrenamiento y evidentemente también en la calidad del clasificador
#    obtenido. Con un número bajo de epochs, no hay suficiente entrenamiento,
#    pero también hay que decir que un número excesivo de epochs puede
#    provocar un sobreajuste no deseado. 
#  - El valor de "rate" usado. 
#  - Si se usa "rate_decay" o no.
#  - Si se usa normalización o no. 

# Se pide describir brevemente el proceso de experimentación en cada uno de
# los casos, y finalmente dar el clasificador con el que se obtienen mejor
# rendimiento sobre el conjunto de test correspondiente.

# Por dar una referencia, se pueden obtener clasificadores para el problema de
# los votos con un rendimiento sobre el test mayor al 90%, y para los dígitos
# un rendimiento superior al 80%.  
