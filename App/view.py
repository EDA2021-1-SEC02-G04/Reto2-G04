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
    print("3- Videos con más views en un pais y categoria")
    print("4- Video con mayor tiempo en trending de un pais")
    print("5- Video que más dias ha sido trending en una categoria")
    print("6- Videos con más likes en un pais con un tag en especifico")
    print("0- Salir")

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


def printResultslike(videos, sample):
    size = lt.size(videos)
    if size > sample:
        print("Los ", sample, " videos con más views son:")
        i=1
        while i <= sample:
            video = lt.getElement(videos,i)
            print("Trending date: "+ video["trending_date"]+ ' Titulo: ' + video['title'] + " Canal: "
            + video["channel_title"]+  " Fecha de publicación: "
            + video["publish_time"]+" views: " + video["views"]  + " likes: "+video["likes"] +" dislikes: " +video["dislikes"])
            i+=1
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
            i+=1
def printTags(videos, sample):
    size = lt.size(videos)
    if size > sample:
        print("Los ", sample, " videos con más likes son:")
        i=1
        while i <= sample:
            video = lt.getElement(videos,i)
            print(' Titulo: ' + video['title'] + " Canal: "
            + video["channel_title"]+  " Fecha de publicación: "
            + video["publish_time"]+" views: " + video["views"]  + " likes: "+video["likes"] +" dislikes: " +video["dislikes"]+" Tags:: " +video["tags"]+" Pais: "+video["country"])
            i+=1
            
def print_categoria_trending(result):
    video=lt.getElement(result,1)
    print('Titulo: ' + video['title'] + " Canal: "
            + video["channel_title"]+  " Categoria_id: "
            + str(video['category_id'])+" Días Trending: " + str(video["trending"])+" Pais: "+video['country'])


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        answer=controller.loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str(lt.size(catalog['categorias'])))
        print('Paises cargados: ' + str(lt.size(catalog['paises'])))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")

    elif int(inputs[0]) == 2:
        numeroT=int(input("¿Que tan grande quiere que sea el top? "))
        categoria= input("Indique la categoria que desea analizar: ").lower()
        print("Cargando videos con más views ....")
        result = controller.sortLikes(catalog,categoria)
        printResultslike(result,numeroT)
    elif int(inputs[0]) == 3:
        numeroT=int(input("¿Que tan grande quiere que sea el top? "))
        pais= input("Indique el pais que desea analizar: ").lower()
        categoria= input("Indique la categoria que desea analizar: ").lower()
        print("Cargando videos con más views ....")
        answer = controller.sortVideos(catalog,pais,categoria)
        printResults(answer[0],numeroT)
        print("Tiempo [ms]: ", f"{answer[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[2]:.3f}")
    elif int(inputs[0]) == 4:
        pais= input("Indique el pais que desea analizar: ").lower()
        print("Cargando video con más dias en trending en un pais ....")
        result = controller.trending_pais(catalog,pais)
        print_categoria_trending(result[2])
        print("Tiempo [ms]: ", f"{result[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{result[1]:.3f}")
    elif int(inputs[0]) == 5:
        categoria= input("Indique la categoria que desea analizar: ").lower()
        print("Cargando video con más dias en trending en una categoria ....")
        result = controller.trending_categoria(catalog,categoria)
        print_categoria_trending(result[2])
        print("Tiempo [ms]: ", f"{result[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{result[1]:.3f}")

    elif int(inputs[0]) == 6:
        print("Cargando videos con más likes de un tag en especifico ....")
        tag=input("Indique el tag: ")
        pais= input("Indique el pais que desea analizar: ").lower()
        answer=controller.sort_con_tags(tag,catalog,pais)
        numeroT=int(input("¿Que tan grande quiere que sea el top? "))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
         "Memoria [kB]: ", f"{answer[1]:.3f}")
        printTags(answer[2],numeroT)
        
    else:
        sys.exit(0)
sys.exit(0)
