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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de videos. Crea una lista vacia para guardar
    todos los videos, adicionalmente, crea una lista vacia para las categorias. Retorna el catalogo inicializado.
    """
    catalog = {'videos': None,
               'categorias': None,'paises': None, 'trending':None}

    catalog['videos'] = lt.newList(datastructure="ARRAY_LIST")
    catalog['categorias'] = mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    catalog['paises'] = mp.newMap(15,maptype="PROBING",loadfactor=0.5)
    catalog['trending'] = mp.newMap(1000,maptype="PROBING",loadfactor=0.5)
    catalog['id'] = mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    catalog["traduccion"]=mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    return catalog




# Funciones para agregar informacion al catalogo
def traduccion(categoria,catalog):
    x=mp.get(catalog["traduccion"],categoria)
    return me.getValue(x)
def addVideo(catalog, video):
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], video)
    paises = video['country'].split(",")
    categorias = video['category_id'].split(",")
    for pais in paises:
        addPaisVideo(catalog, pais.strip(), video)
    for categoria in categorias:
        tr=traduccion(categoria.strip(),catalog)
        addCategoriaVideo(catalog, tr, video)

def addListaCategorias(catalog, categoria):
    """
    Adiciona una categoria a la lista de categorias
    """
    cat = newCategoria(categoria['name'].strip().lower(), categoria['id'])
    mp.put(catalog['categorias'],categoria["name"].strip().lower(),cat)
    mp.put(catalog['traduccion'],categoria["id"],categoria["name"].strip().lower())

def addCategoriaVideo(catalog, nombre_categoria,video):
    """
    Adiciona un categoria a la lista de categorias
    """
    #cat = newCategoria(categoria['name'], categoria['id'])
    #lt.addLast(catalog['categorias'], cat)
    
    categorias_mapa = catalog['categorias']
    existecat = mp.contains(categorias_mapa, nombre_categoria)
    if existecat:
        pareja = mp.get(categorias_mapa, nombre_categoria)
        categoria=me.getValue(pareja)
        lt.addLast(categoria["videos"], video)

def addPaisVideo(catalog, nombre_pais, video):
    """
    Adiciona un pais a lista de paises, la cual guarda referencias
    a los videos de dicho pais
    """
    paises_mapa = catalog['paises']
    existevid = mp.contains(paises_mapa,nombre_pais)
    if existevid:
        pareja = mp.get(paises_mapa, nombre_pais)
        pais=me.getValue(pareja)
        lt.addLast(pais["videos"], video)
    else:
        pais = newPais(nombre_pais)
        lt.addLast(pais["videos"], video)
        mp.put(paises_mapa, nombre_pais,pais)

    
"""
def addTrending(trending_lista,video):
    video
    posvideo = lt.isPresent(trending_lista, video)
    if posvideo > 0:
        vid=lt.getElement(trending_lista, posvideo)
        dias=vid['trending']
        dias+=1
        vid['trending']=dias
        lt.changeInfo(trending_lista,posvideo,vid)
    else:
        trending = newTrending(video,trending_lista)
        lt.addLast(trending_lista, trending)
"""
# Funciones para creacion de datos
def newCategoria(name, id):
    """
    Esta estructura almacena las categorias con sus id respectivos.
    """
    categoria = {'name': '', 'id': '', "videos": None}
    categoria['name'] = name.lower().strip()
    categoria['id'] = id
    categoria['videos'] = lt.newList('ARRAY_LIST')
    return categoria

def newPais(name):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    pais = {'name': "", "categorias":None, "videos":None}
    pais['name'] = name.lower()
    pais['categorias'] = lt.newList('ARRAY_LIST')
    pais['videos'] = lt.newList('ARRAY_LIST')
    return pais
"""
def newTrending(video,catalog):
    
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    
    trending = {'id':None, 'name': None, 'channel':None, "categoria":None, 'pais': None, "trending":None}
    trending['id']=video['video_id']
    trending['name'] = video['title']
    trending['channel'] = video['channel_title']
    trending['categoria'] = video['category_id']
    trending['pais'] = video['country']
    trending['trending']=1
    return trending
"""
# Funciones de consulta
def obtener_videos_categoria(catalog,categoria):
    posvideo = mp.contains(catalog['categorias'], categoria)
    
    
    if posvideo:
        pais = mp.get(catalog['categorias'],categoria)
        return me.getValue(pais) 
    
    return None


# Funciones utilizadas para comparar elementos dentro de una lista
def cmpVideosByLikes(video1, video2):
    
    
    if (float(video1['likes']) > float(video2['likes'])):
        return True
    else:
        return False

# Funciones de ordenamiento
def sortLikes(catalog,categoria):
    
    categorias=obtener_videos_categoria(catalog,categoria)

    lista_categoria=categorias['videos']
    
    sorted_list = ms.sort(lista_categoria, cmpVideosByLikes)
    return sorted_list