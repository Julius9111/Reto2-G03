"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {
        'results': None,
        'goalscorers': None,
        'shootouts': None,
        'scorers': None,
        'teams': None,
        'tournaments': None,
        'official_results': None,
        'official_teams': None
    }
    data_structs['results'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)
    data_structs['goalscorers'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)
    data_structs['shootouts'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)
    data_structs['teams'] = mp.newMap(numelements=160, maptype='CHAINING', loadfactor=4, cmpfunction=compare_map_name)
    data_structs['tournaments'] = mp.newMap(numelements=80, maptype='CHAINING', loadfactor=4, cmpfunction=compare_map_name)
    
    return data_structs


# Funciones para agregar informacion al modelo

def add_results(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista results
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs['results'], data)
    return data_structs

def add_goalscorers(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista goalscorers
    """
    #TODO: Crear la función para agregar elementos a una lista

    #Añadir a data_struct goalscorers
    lt.addLast(data_structs['goalscorers'], data)

    #Obtención de datos para buscar el partido que coincide en results
    date = data['date']
    hometeam = data['home_team'].lower()
    awayteam = data['away_team'].lower()

    if data['scorer'] == '' or data['scorer'] == None:
        return data_structs

    #Posición del partido que coincide en results
    pos_result = binary_search_general(data_structs['results'], date, hometeam, awayteam)
    if pos_result != -1:

        #Cambio de datos según los obtenidos en goalscorers
        result = lt.getElement(data_structs['results'], pos_result)

        scorer = {'team': data['team'], 'name': data['scorer'], 'minute': data['minute'], 'own_goal': data['own_goal'], 'penalty': data['penalty']}
        if result['scorers'] == 'Unknown' and data['scorer'] != '':
            result['scorers'] = lt.newList('ARRAY_LIST', cmpfunction=compare_name)

        lt.addLast(result['scorers'], scorer)

        #Cambiar penalty si hay información
        if result['penalty'] == 'Unknown':
            result['penalty'] = scorer['penalty']
        else:
            if result['penalty'] == 'False' and scorer['penalty'] == 'True':
                result['penalty'] == 'True'
        
        #Cambiar own_goal si hay información
        if result['own_goal'] == 'Unknown':
            result['own_goal'] = scorer['own_goal']
        else:
            if result['own_goal'] == 'False' and scorer['own_goal'] == 'True':
                result['own_goal'] == 'True'
        
        lt.changeInfo(data_structs['results'], pos_result, result)
    return data_structs

def add_shootouts(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista shootouts
    """
    #TODO: Crear la función para agregar elementos a una lista

    #Añadir información al data_struct shootouts
    lt.addLast(data_structs['shootouts'], data)

    #Datos para encontrar el archivo que coincide en results
    date = data['date']
    hometeam = data['home_team'].lower()
    awayteam = data['away_team'].lower()

    #Posición del partido que coincide en results
    pos_result = binary_search_general(data_structs['results'], date, hometeam, awayteam)

    if pos_result != -1:
        result = lt.getElement(data_structs['results'], pos_result)
        result['winner'] = data['winner']

        #Actualizar la información en el data_struct results
        lt.changeInfo(data_structs['results'], pos_result, result)
    return data_structs

def load_auxiliar(data_structs):
    """
    Función para crear las estructuras de datos auxiliares
    """
    #Recorrer cada linea de resultados para crear estructuras auxiliares
    for data in lt.iterator(data_structs['results']):
        add_team(data_structs, data['home_team'], data)
        add_team(data_structs, data['away_team'], data)
    

def add_team(data_structs, teamname, result):
    teams = data_structs['teams']

    try:
        entry = mp.get(teams, teamname)
        if entry:
            listresults = me.getValue(entry)
            lt.addLast(listresults, result)
        else:
            results = lt.newList('ARRAY_LIST')
            lt.addLast(results, result)
            mp.put(teams, teamname, results)
    except Exception:
        return None
    
def add_tourn(data_structs, name, result):
    tournaments = data_structs['tournaments']

    try:
        entry = mp.get(tournaments, name)
        if entry:
            listresults = me.getValue(entry)
            lt.addLast(listresults, result)
        else:
            results = lt.newList('ARRAY_LIST')
            lt.addLast(results, result)
            mp.put(tournaments, name, results)
    except Exception:
        return None

# Funciones para creacion de datos

def new_data(data):
    pass


# Funciones de consulta

def get_first_last_three(list):
    """
    Retorna una lista con los tres primeros y tres últimos elementos
    """
    filtered = lt.newList("ARRAY_LIST")
    for i in range(1, 4):
        lt.addLast(filtered, lt.getElement(list, i))
    for i in range(-2, 1):
        lt.addLast(filtered, lt.getElement(list, i))

    return filtered


def data_size_list(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    return lt.size(data_structs)

def binary_search_general(data_structs, date, hometeam, awayteam):

    """
    Retorna la posición del partido en el que coinciden la fecha, el equipo local y el equipo visitante
    """

    low = 1
    high = lt.size(data_structs)

    while low <= high:
        mid = (low + high) // 2
        result = lt.getElement(data_structs, mid)
        datemid = result['date']
        if datemid < date:
            high = mid -1
        elif datemid > date:
            low = mid + 1
        else:
            hometeam_mid = result['home_team'].lower()
            if hometeam_mid < hometeam:
                high = mid - 1
            elif hometeam_mid > hometeam:
                low = mid + 1
            else:
                awayteam_mid = result['away_team'].lower()
                if awayteam_mid < awayteam:
                    high = mid - 1
                elif awayteam_mid > awayteam:
                    low = mid + 1
                else:
                    return mid
    return -1



def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare_id(data_1, data_2):
    """
    Función encargada de comparar dos datos por id
    """
    #TODO: Crear función comparadora de la lista
    if data_1['id'] > data_2['id']:
        return 1
    elif data_1['id'] < data_2['id']:
        return -1
    else:
        return 0
    
def compare_map_name(data1, data2):
    dataentry = me.getKey(data2)
    if data1 > dataentry:
        return 1
    elif data1 < dataentry:
        return -1
    else:
        return 0

def compare_name(team1, team2):
    """
    Función encargada de comparar dos datos por nombre
    """
    t1 = team1.lower()
    t2 = team2['name'].lower()

    if t1 > t2:
        return 1
    elif t1 < t2:
        return -1
    else:
        return 0

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
