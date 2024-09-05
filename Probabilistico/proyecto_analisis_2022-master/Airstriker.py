#Proyecto Programado 2
#Jennifer Alvarado Brenes y Brenda Badilla Rodríguez
#Semestre II - 2022
import time
import retro
from random import randint, uniform,random

env = retro.make(game='Airstriker-Genesis', record=False)

env.reset()

done = False #Indica si el juego se acabó (true)

movCorrectos = [] #Aquí se almacenan los movimientos correctos

inicio = True #Indica si el juego inició
lineasEjecutadas=0
c=0
a=0
iteraciones=0
def dormir():
    time.sleep(0.0002)

nivel1 = True
inicioTiempo=time.time()
#Las variables se miden a partir de aquí, que inicia el algoritmo en sí

while nivel1:
    iteraciones+=1
    env.render()
    probDisparo = random()

    action = [0, 0, 0, 0, 0, 0, randint(0,1), randint(0,1), 0, 1, 0, 0]
#             0=B
#             1
#             2
#             3
#             4=arriba
#             5=abajo
#             6=izquierda
#             7=derecha
#             8=A
#             9
#             10
#             11

    #Se verifica el nivel

    ob, rew, done, info = env.step(action)
    #Si se encuentra en el nivel 2, apaga el juego, para efecto de la revisión
    if info["lives"]==4:
        print("\nNivel 1 Completado")
        nivel1=False

    dormir()
    a+=2
    #Comparaciones de los if:
    c+=6
    lineasEjecutadas+=6
    #Indica cuando el juego se reinicia, hace los movimientos correctos registrados hasta el momento.
    if inicio and info['gameover'] ==9:
        a+=1
        inicio = False
        lineasEjecutadas+=2
        for i in range(len(movCorrectos)):
            lineasEjecutadas +=4
            env.render()
            a+=1
            ob, rew, done, info = env.step(movCorrectos[i])
            dormir()
            c+=1
            if info['gameover'] ==2:
                lineasEjecutadas +=1
                break

    #lineas de los if:
    lineasEjecutadas +=4
    #Indica si el juego está activo y agrega el movimiento
    if info['gameover'] ==9:
        lineasEjecutadas +=1
        a+=1
        movCorrectos.append(action)
    #Indica si la nave explotó, se reinicia el juego
    if info['gameover'] ==2:
        lineasEjecutadas +=3
        a+=2
        inicio = True
        obs = env.reset()
        c+=1
        #En caso de que la cantidad de movimientos correctos ya sea considerablemente grande
        #pero la nave explotó, se eliminan los últimos 10 movimientos, de forma que se pueda
        #corregir el rumbo de la nave antes del error.
        if (len(movCorrectos)>100):
            lineasEjecutadas +=1
            for e in range(20):
                lineasEjecutadas +=1
                movCorrectos.pop(len(movCorrectos)-e-1)

    #La probabilidad de disparo se bajó a un 30%, si en el movimiento random con disparo se tiene éxito
    #se añade a los movimientos correctos.
    if probDisparo <= 0.30:
        a+=1
        action = [randint(0, 1), 0, 0, 0, 0, 0, randint(0, 1), randint(0, 1), 0, 1, 0, 0]
        #             0=B
        #             1
        #             2
        #             3
        #             4=arriba
        #             5=abajo
        #             6=izquierda
        #             7=derecha
        #             8=A
        #             9
        #             10
        #             11
        a+=1
        ob, rew, done, info = env.step(action)
        dormir()
        c+=1
        lineasEjecutadas +=4
        if info['gameover'] == 9:
            lineasEjecutadas +=1
            a+=1
            movCorrectos.append(action)

    if done:
        lineasEjecutadas +=1
        a+=1
        obs = env.reset()

    #Mediciones
    if iteraciones==10 or iteraciones==50 or iteraciones==100 or iteraciones==200 or iteraciones==500 or iteraciones==1000 or iteraciones==3000:
        print("\nIteraciones: ", iteraciones)
        print("Asignaciones: ", a)
        print("Comparaciones: ", c)
        print("Lineas ejecutadas: ", lineasEjecutadas)
        print("Tiempo de ejecucion: ", time.time()-inicioTiempo)

env.close()