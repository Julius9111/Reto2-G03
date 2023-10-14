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
        'official_teams': None
    }
    data_structs['results'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)
    data_structs['goalscorers'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)
    data_structs['shootouts'] = lt.newList(datastructure='ARRAY_LIST', cmpfunction=compare_id)
    data_structs['teams'] = mp.newMap(numelements=160, maptype='CHAINING', loadfactor=4, cmpfunction=compare_map_name)
    data_structs['tournaments'] = mp.newMap(numelements=80, maptype='CHAINING', loadfactor=4, cmpfunction=compare_map_name)
    data_structs['scorers'] = mp.newMap(numelements=500, maptype='CHAINING', loadfactor=4, cmpfunction=compare_map_name)
    
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
        if data['scorers'] != 'Unknown':
            for scorer in lt.iterator(data['scorers']):
                add_scorer(data_structs, scorer['name'], data)
    

def add_team(data_structs, teamname, result):
    teams = data_structs['teams']

    try:
        entry = mp.get(teams, teamname)
        if entry:
            listresults = me.getValue(entry)
            lt.addLast(listresults, result)
        else:
            results = lt.newList('ARRAY_LIST', compare_name)
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
            results = lt.newList('ARRAY_LIST', compare_name)
            lt.addLast(results, result)
            mp.put(tournaments, name, results)
    except Exception:
        return None

def add_scorer(data_structs, scorer, result):
    
    scorers = data_structs['scorers']

    try:
        entry = mp.get(scorers, scorer)
        if entry:
            listscorers = me.getValue(entry)
            lt.addLast(listscorers, result)
        else:
            results = lt.newList('ARRAY_LIST', compare_name)
            lt.addLast(results, result)
            mp.put(scorers, scorer, results)
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



def req_1(nombre, numero_goles, control):
    """
    Función que soluciona el requerimiento 1
    """
    
    return control


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


def cmp_partidos_by_fecha_y_pais(result1, result2):
    """
    Devuelve verdadero (True) si la fecha del resultado1 es menor que en el resultado2,
    en caso de que sean iguales tenga el nombre de la ciudad en que se disputó el partido,
    de lo contrario devuelva falso (False).
    Args:
    result1: información del primer registro de resultados FIFA que incluye 
    “date” y el “country” 
    result2: información del segundo registro de resultados FIFA que incluye 
    “date” y el “country” 
    """
    #TODO: Crear función comparadora para ordenar
    fecha1 = result1['date']
    fecha2 = result2['date']

    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        hscore1 = result1['home_score']
        hscore2 = result2['home_score']

        if hscore1 > hscore2:
            return True
        elif hscore1 < hscore2:
            return False
        else:
            ascore1 = result1['away_score']
            ascore2 = result2['away_score']
            if ascore1 > ascore2:
                return True
            else: 
                return False

def cmp_goalscorers(scorer1, scorer2):

    fecha1 = scorer1['date']
    fecha2 = scorer2['date']

    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
    else:
        min1 = (scorer1['minute'])
        min2 = (scorer2['minute'])

        if min1 > min2:
            return True
        elif min1 < min2:
            return False
        else:
            player1 = scorer1['scorer'].lower()
            player2 = scorer2['scorer'].lower()
            if player1 > player2:
                return True
            else:
                return False

def cmp_shootouts(shoot1, shoot2):

    fecha1 = shoot1["date"]
    fecha2 = shoot2["date"]

    if fecha1 > fecha2:
        return True
    elif fecha1 < fecha2:
        return False
        
    else: 
        nombre_1_local = shoot1["home_team"].lower()
        nombre_2_local = shoot2["home_team"].lower()

        if nombre_1_local > nombre_2_local:
            return True
        elif nombre_1_local < nombre_1_local:
            return False
        
        else:
            nombre_1_visitante = shoot1["away_team"].lower()
            nombre_2_visitante = shoot2["away_team"].lower()

            if nombre_1_visitante > nombre_2_visitante:
                return True
            elif nombre_1_visitante < nombre_1_visitante:
                return False

def cmp_name(team1, team2):

    t1 = team1['name'].lower()
    t2 = team2['name'].lower()

    if t1 < t2:
        return True
    else:
        return False
    
def cmp_stats(team1, team2):
    points1 = team1['total_points']
    points2 = team2['total_points']

    if points1 > points2:
        return True
    elif points1 < points2:
        return False
    else:
        difgoals1 = team1['goal_difference']
        difgoals2 = team2['goal_difference']
        if difgoals1 > difgoals2:
            return True
        elif difgoals1 < difgoals2:
            return False
        else:
            penaltgoals1 = team1['penalty_points']
            penaltygoals2 = team2['penalty_points']
            if penaltgoals1 > penaltygoals2:
                return True
            elif penaltgoals1 < penaltygoals2:
                return False
            else:
                matches1 = team1['matches']
                matches2 = team2['matches']
                if matches1 < matches2:
                    return True
                elif matches1 > matches2:
                    return False
                else:
                    owngoals1 = team1['own_goals']
                    owngoals2 = team2['own_goals']
                    if owngoals1 < owngoals2:
                        return True
                    else:
                        return False
                    
def cmp_top_scorer(scorer1, scorer2):
    if scorer1['goals'] > scorer2['goals']:
        return True
    elif scorer1['goals'] < scorer2['goals']:
        return False
    else:
        if scorer1['avg_time'] < scorer2['avg_time']:
            return True
        elif scorer1['avg_time'] > scorer2['avg_time']:
            return False
        else:
            if scorer1['name']  < scorer2['name']:
                return True
            else:
                return False
    
def cmp_cities(city1, city2):
    if city1['meetings'] > city2['meetings']:
        return True
    elif city1['meetings'] < city2['meetings']:
        return False
    else:
        if city1['name'] < city2['name']:
            return True
        else:
            return False

def cmp_scorer_points(scorer1, scorer2):
    if scorer1['total_points'] > scorer2['total_points']:
        return True
    elif scorer1['total_points'] < scorer2['total_points']:
        return False
    else:
        if scorer1['total_goals'] > scorer2['total_goals']:
            return True
        elif scorer1['total_goals'] < scorer2['total_goals']:
            return False
        else:
            if scorer1['penalty_goals'] > scorer2['penalty_goals']:
                return True
            elif scorer1['penalty_goals'] < scorer2['penalty_goals']:
                return False
            else:
                if scorer1['own_goals'] < scorer2['own_goals']:
                    return True
                elif scorer1['own_goals'] > scorer2['own_goals']:
                    return False
                else:
                    if scorer1['avg_time'] < scorer2['avg_time']:
                        return True
                    elif scorer1['avg_time'] > scorer2['avg_time']:
                        return False
                    else:
                        if scorer1['name'] < scorer2['name']:
                            return True
                        else:
                            return False                    

def cmp_year(year1, year2):
    if year1['name'] > year2['name']:
        return True
    else:
        return False


def sort(data_structs, name):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    if name == 'results':
        merg.sort(data_structs['results'], cmp_partidos_by_fecha_y_pais)
    elif name == 'goalscorers':
        merg.sort(data_structs['goalscorers'], cmp_goalscorers)
    elif name == 'shootouts':
        merg.sort(data_structs['shootouts'], cmp_shootouts)