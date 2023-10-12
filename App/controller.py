﻿"""
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
 """

import config as cf
import model
import time
import csv
import tracemalloc
from datetime import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, file_size):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_structs = control['model']

    results = load_results(data_structs, file_size)
    model.sort(data_structs, 'results')
    goalscorers = load_goalscorers(data_structs, file_size)
    model.sort(data_structs, 'goalscorers')
    shootouts = load_shootouts(data_structs, file_size)
    model.sort(data_structs, 'shootouts')
    model.load_auxiliar(data_structs)

    return (results, goalscorers, shootouts)

def load_results(data_structs, file_size):

    results_file = cf.data_dir + 'football/results-utf8-' + file_size + '.csv'
    input_file = csv.DictReader(open(results_file, encoding='utf-8'))

    id = 1
    for result in input_file:

        changed = change_type(result)
        changed['id'] = id
        changed['scorers'] = 'Unknown'
        changed['winner'] = 'Unknown'
        changed['penalty'] = 'Unknown'
        changed['own_goal'] = 'Unknown'
        model.add_results(data_structs, changed)
        id += 1
    return model.data_size_list(data_structs['results'])

def load_goalscorers(data_structs, file_size):

    goalscorers_file = cf.data_dir + 'football/goalscorers-utf8-' + file_size + '.csv'
    input_file = csv.DictReader(open(goalscorers_file, encoding='utf-8'))

    id = 1
    for goalscorer in input_file:
        
        if goalscorer['minute'] == "" or goalscorer['minute'] == None:
            goalscorer['minute'] = -1
        changed = change_type(goalscorer)
        changed['id'] = id
        model.add_goalscorers(data_structs, changed)
        id += 1

    return model.data_size_list(data_structs['goalscorers'])

def load_shootouts(data_structs, file_size):

    shootouts_file = cf.data_dir + 'football/shootouts-utf8-' + file_size + '.csv'
    input_file = csv.DictReader(open(shootouts_file, encoding='utf-8'))

    id = 1
    for shootout in input_file:

        changed = change_type(shootout)
        changed['id'] = id
        model.add_shootouts(data_structs, changed)
        id += 1

    return model.data_size_list(data_structs['shootouts'])

def change_type(data):

    changed = data
    formato_fecha = "%Y-%m-%d"
    changed['date'] = datetime.strptime(data['date'], formato_fecha)
    if changed.get('home_score'):
        changed['home_score'] = int(data['home_score']) 
        changed['away_score'] = int(data['away_score'])
        
    if changed.get('scorer'):
        if changed['minute'] != 'Unknown':
            changed['minute'] = float(data['minute'])
    
    return changed


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass

def get_first_last_three(list):
    data = model.get_first_last_three(list)
    return data

def req_1(control):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
