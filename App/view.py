"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
from datetime import datetime
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def new_controller(mptype, loadfactor):
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
   
    control = controller.new_controller(mptype, loadfactor)
    return control


def print_menu():
    print("Bienvenido\n")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("10- Cambiar tamaño, ADT y algoritmo de ordenamiento")
    print("0- Salir")


def load_data(control, file_size, memflag=True):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    results, goalscorers, shootouts, deltadata = controller.load_data(control,file_size, memflag)

    print('Total de encuentros cargados: ' + str(results))
    print('Total de anotaciones cargadas: ' + str(goalscorers))
    print('Total de goles marcados desde el punto penal cargados: ' + str(shootouts))

    print('Tiempo de ordenamiento: ')

    print("Primeros y ultimos 3 resultados: \n")

    keys_result = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'country', 'city', 'tournament']
    table_results = print_tabulate(control['model']['results'], keys_result)
    print(table_results, "\n")

    print("Primeros y ultimos 3 anotadores: \n")

    keys_goalscorers = ['date', 'home_team', 'away_team', 'scorer', 'team', 'minute', 'penalty', 'own_goal']
    table_goalscorers = print_tabulate(control['model']['goalscorers'], keys_goalscorers)
    print(table_goalscorers, "\n")

    print("Primeros y ultimos 3 goles:\n")

    keys_shootouts = ['date', 'home_team', 'away_team', 'winner']
    table_shootouts = print_tabulate(control['model']['shootouts'], keys_shootouts)
    print(table_shootouts, "\n")
    
    print_delta_data(deltadata)
    pass

def print_delta_data(deltadata):
    if isinstance(deltadata, (list, tuple)) is True:
        print('Tiempo [ms]: ',  f"{deltadata[0]:.3f}")
        print('Memoria [kB]: ',  f"{deltadata[1]:.3f}")
    else:
        print('Tiempo [ms]: ',  f"{deltadata:.3f}")


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def choose_adt():
    print("Por favor elije el ADT que prefieras: ")
    print('1. Array List')
    print('2. Single Linked List')
    user = input("Selecciona una opción: ")
    if int(user) == 1:
        return 'ARRAY_LIST'
    elif int(user) == 2:
        return 'SINGLE_LINKED'
    else:
        return None
    
def choose_size():
    print('Por favor elija el tamaño de archivo a cargar: ')
    print('1. Small')
    print('2. Large')
    print('3. 5pct')
    print('4. 10pct')
    print('5. 20pct')
    print('6. 30pct')
    print('7. 50pct')
    print('8. 80pct')

    choice = int(input('Seleccione una opción: '))

    if choice == 1:
        return 'small'
    elif choice == 2:
        return 'large'
    elif choice == 3:
        return '5pct'
    elif choice == 4:
        return '10pct'
    elif choice == 5:
        return '20pct'
    elif choice == 6:
        return '30pct'
    elif choice == 7:
        return '50pct'
    elif choice == 8:
        return '80pct'
    else:
        return None

def choose_sort():
    print('Por favor elija el algoritmo de ordenamiento que desea:')
    print('1. Shell Sort')
    print('2. Insertion Sort')
    print('3. Selection Sort')
    print('4. Merge Sort')
    print('5. Quick Sort')

    choice = int(input('Seleccione una opción: '))

    if choice == 1:
        return 'shell'
    elif choice == 2:
        return 'insertion'
    elif choice == 3:
        return 'selection'
    elif choice == 4:
        return 'merge'
    elif choice == 5:
        return 'quick'
    else:
        return None

def choose_mapdata():
    print('Por favor elija el tipo de manejod de colisiones que desea:')
    print('1. Linear Probing')
    print('2. Chaining')
    user = input('Seleccione una opción: ')
    maptype = None
    loadfactor = None 
    if int(user) == 1:
        maptype = 'PROBING'
    elif int(user) == 2:
        maptype = 'CHAINING'
    
    user2 = float(input('Ingrese el factor de carga que desee: '))
    loadfactor = user2
    return maptype, loadfactor

def choose_memory_tracking():
    print('¿Desea medir la memoria consumida en la ejecución')
    print('1. Si/Yes')
    print('2. No')
    user = int(input('Seleccione su opción: '))

    if user == 1:
        return True
    elif user == 2:
        return False
    else:
        print('No se seleccionó una opción válida')
    

def print_tabulate(data_struct, columns):
    data = data_struct

    if data == None:
        return 'No hay datos'

    #Filtrar solo ultimos y primeros 3 datos si es muy grande la lista
    if lt.size(data_struct) > 6:
        data = controller.get_first_last_three(data_struct)
        print('Se encontraron más de 6 resultados...')

    #Lista vacía para crear la tabla
    reduced = []

    #Iterar cada línea de la lista
    for result in lt.iterator(data):
        line = []
        formato_fecha = "%Y-%m-%d"
        result['date'] = datetime.strftime(result['date'], formato_fecha)
        #Iterar las columnas para solo imprimir las deseadas
        for column in columns:

            #Creación de subtabla para el requerimiento 6
            if column == 'top_scorer':
                topscorer = []
                keys_scorer = ['name', 'goals', 'matches', 'avg_time']
                for column_scorer in keys_scorer:
                    topscorer.append(result[column][column_scorer])
                list = [keys_scorer, topscorer]
                table_scorer = tabulate(list, headers='firstrow', tablefmt='grid')
                line.append(table_scorer)

            #Creación de subtabla para el requerimiento 7
            elif column == 'last_goal':
                last_goal = []
                keys = ['date', 'tournament', 'home_team', 'away_team', 'home_score', 'away_score', 'minute', 'penalty', 'own_goal']
                for key in keys:
                    last_goal.append(result[column][key])
                list = [keys, last_goal]
                subtable = tabulate(list, headers='firstrow', tablefmt='grid')
                line.append(subtable)
            else:
                line.append(result[column])

        reduced.append(line)
    table = tabulate(reduced, headers=columns, tablefmt="grid")
    return table


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, nombre, numero_goles):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    total_scorers, total_goals, penaltis, lista_goles = controller.req_1(control, nombre, numero_goles)
    print(f"\n\nTop {numero_goles} goals:")
    print(f"Player Name {nombre}")
    if lt.size(lista_goles) < numero_goles:
      print(f"\n\nSe han encontrado solamente {lt.size(lista_goles)} goles")
      lista_goles_top = lista_goles
    else:
      print("\n\nLos siete goles son: ")
      lista_goles_top = lt.subList(lista_goles, 1, numero_goles)
    print("Total scorers: ", total_scorers)
    print("Total goals: ", total_goals)
    print("Total penaltis: ", penaltis)
    lista = []
    for gol in lt.iterator(lista_goles_top):
        lista.append(gol)
    lista_llaves = ["date", "home_team", "away_team", "team", "scorer", "minute", "own_goal", "penalty"]


    lista_valores = []
    pos = -1
    for gol in lista:
        pos += 1
        lista_valores.append([])
        for llave in lista_llaves:
            if llave == "scorer":
                lista_valores[pos].append(nombre)
            elif llave == "date":
                fecha = gol["date"].strftime("%Y-%m-%d")
                lista_valores[pos].append(fecha)
            else:
                lista_valores[pos].append(gol[llave])


    print(tabulate(lista_valores, headers=lista_llaves, tablefmt='grid'))



def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control, name, inicial, final):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    list, size, home, away, available_teams, d_time = controller.req_3(control, name, inicial, final)
    print(("="*15) + "Req No. 3 Inputs" + ("="*15))
    print('Team name:', name)
    print('Start date:', inicial)
    print('End date:', final, '\n')

    print(("="*15) + "Req No. 3 Results" + ("="*15))
    print('Total teams with available information:', str(available_teams))
    print(name, 'Total games:', str(size))
    print(name, 'Total home games:', str(home))
    print(name, 'Total away games:', str(away), '\n')

    columns = ['date', 'home_score', 'away_score', 'home_team', 'away_team', 'country', 'city', 'tournament', 'penalty', 'own_goal']
    table = print_tabulate(list, columns)
    print(table)
    d_time = f'{d_time:.3f}'
    print('Tiempo de ejecución:', str(d_time), 'ms')



def print_req_4(control, nombre, fechai, fechaf):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    res = controller.req_4(control, nombre, fechai, fechaf)
    print(res)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


control = None
file_size = None
mapdata = None

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print('¿Desea usar las opciones predeterminadas?')
            print('1. Si \n2.No')
            user = int(input('Seleccione una opción: '))

            if user == 1:
                memflag = True
                maptype = 'CHAINING'
                loadfactor = 4
                file_size = 'small'
            else:
                if file_size == None:
                    file_size = choose_size()
                
                if mapdata == None:
                    maptype, loadfactor = choose_mapdata()
                memflag = choose_memory_tracking()
            control = new_controller(maptype, loadfactor)
            print("Cargando información de los archivos ....\n")

            if memflag or not memflag:
                load_data(control, file_size, memflag)

        elif int(inputs) == 2:
            numero_goles = 5#int(input("Número (N) de goles de consulta:"))
            nombre_jugador = "Michael Ballack" #str(input("Ingrese el nombre completo del jugador:"))
            print_req_1(control, nombre_jugador, numero_goles)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            name = input('Ingrese el nombre del equipo: ')
            print('Por favor coloque las fechas en el siguiente formato: YYYY-MM-DD')
            inicial = input('Ingrese la fecha inicial: ')
            final = input('Ingrese la fecha final: ')
            print_req_3(control, name, inicial, final)

        elif int(inputs) == 5:
            nombre = "Copa América"#input("Diga el nombre del torneo: ")
            fechai = "1955-06-01"#input("Diga la fecha inicial: ")
            fechaf = "2022-06-30"#input("Diga la fecha final: ")
            print_req_4(control, nombre, fechai, fechaf)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
