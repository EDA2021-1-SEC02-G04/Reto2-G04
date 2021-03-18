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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Los videos con más likes por categoria")


def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog()


def loadData(catalog):
    
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)


def printResults(videos, sample):
    size = lt.size(videos)
    if size > sample:
        print("Los ", sample, " videos con más views son:")
        i=1
        while i <= sample:
            video = lt.getElement(videos,i)
            print("Trending date: "+ video["trending_date"]+ ' Titulo: ' + video['title'] + " Canal: "
            + video["channel_title"]+  " Fecha de publicación: "
            + video["publish_time"]+" views: " + video["views"]  + " likes: "+video["likes"] +" dislikes: " +video["dislikes"])

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categorias'])))
        print('Paises cargados: ' + str(lt.size(catalog['paises'])))

    elif int(inputs[0]) == 2:
        numeroT=int(input("¿Que tan grande quiere que sea el top? "))
        categoria= input("Indique la categoria que desea analizar: ").lower()
        print("Cargando videos con más views ....")
        result = controller.sortLikes(catalog,categoria)
        printResults(result)

    else:
        sys.exit(0)
sys.exit(0)
