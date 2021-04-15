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
    catalog['trending'] = mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    catalog['categorias'] = mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    catalog['paises'] = mp.newMap(15,maptype="PROBING",loadfactor=0.5)
    catalog['pais_trending'] = mp.newMap(1000,maptype="PROBING",loadfactor=0.5)
    catalog['categoria_trending'] = mp.newMap(1000,maptype="PROBING",loadfactor=0.5)
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
    addTrending(catalog['trending'],video)
    for categoria in categorias:
        tr=traduccion(categoria.strip(),catalog)
        addCategoriaVideo(catalog['categorias'], tr,categoria.strip(), video)
    for pais in paises:
        addPaisVideo(catalog['paises'], pais.strip(), video,tr)

    
def trending_en_mapas(catalog):
    videos_trending=mp.valueSet(catalog['trending'])
    for video in lt.iterator(videos_trending):
        tr=traduccion(video['category_id'].strip(),catalog)
        addPaisVideo(catalog['pais_trending'],  video['country'].strip(), video,tr)
        addCategoriaVideo(catalog['categoria_trending'], tr,video['category_id'].strip(), video)
def addListaCategorias(catalog, categoria):
    """
    Adiciona una categoria a la lista de categorias
    """
    cat = newCategoria(categoria['name'].strip().lower(), categoria['id'])
    mp.put(catalog['categorias'],categoria["name"].strip().lower(),cat)
    mp.put(catalog['traduccion'],categoria["id"],categoria["name"].strip().lower())

def addCategoriaVideo(catalog, nombre_categoria,id_cat,video):
    """
    Adiciona un categoria a la lista de categorias
    """

    
    categorias_mapa = catalog
    existecat = mp.contains(categorias_mapa, nombre_categoria)
    if existecat:
        pareja = mp.get(categorias_mapa, nombre_categoria)
        categoria=me.getValue(pareja)
        lt.addLast(categoria["videos"], video)
    else:
        cat = newCategoria(nombre_categoria, id_cat)
        lt.addLast(cat["videos"], video)
        mp.put(categorias_mapa, nombre_categoria,cat)

def addPaisVideo(catalog, nombre_pais, video,tr):
    """
    Adiciona un pais a lista de paises, la cual guarda referencias
    a los videos de dicho pais
    """
    paises_mapa = catalog
    existepais = mp.contains(paises_mapa,nombre_pais)
    if existepais:
        pareja = mp.get(paises_mapa, nombre_pais)
        pais=me.getValue(pareja)
        addCategoriaVideo(pais['categorias'], tr,video['category_id'], video)
        lt.addLast(pais["videos"], video)
    else:
        pais = newPais(nombre_pais)
        addCategoriaVideo(pais['categorias'], tr,video['category_id'], video)
        lt.addLast(pais["videos"], video)
        mp.put(paises_mapa, nombre_pais,pais)

def addTrending(trending_map,video):
    video_nombre=video['title']
    existe_video =  mp.contains(trending_map,video_nombre)
    if existe_video:
        pareja=mp.get(trending_map,video_nombre)
        vid=me.getValue(pareja)
        dias=vid['trending']
        dias+=1
        vid['trending']=dias
        mp.put(trending_map,video_nombre,vid)
    else:
        trending = newTrending(video)
        mp.put(trending_map,video_nombre, trending)

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
    pais['categorias'] = mp.newMap(100,maptype="PROBING",loadfactor=0.5)
    pais['videos'] = lt.newList('ARRAY_LIST')
    return pais

def newTrending(video):

    trending = {'id':None, 'name': None, 'channel':None, "categoria":None, 'pais': None, "trending":None}
    trending['video_id']=video['video_id']
    trending['title'] = video['title']
    trending['channel_title'] = video['channel_title']
    trending['category_id'] = video['category_id']
    trending['country'] = video['country']
    trending['trending']=1
    return trending
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


def tags_en_lista(tag,lista,catalog):
    nueva_lista=lt.newList(datastructure='ARRAY_LIST',cmpfunction=cmpVideosByLikes)
    for video in lt.iterator(lista):
        if tag in video["tags"]:
            lt.addLast(nueva_lista,video)
    return nueva_lista

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
def cmpVideosByViews(video1, video2):
    
    if (float(video1['views']) > float(video2['views'])):
        return True
    else:
        return False

def comparetrending(trending1, trending2):
    if (trending1['title'].strip() == trending2['name'].strip()):
        return 0
    return -1

def cmpVideosByTrending(video1, video2):
    
    if (float(video1['trending']) > float(video2['trending'])):
        return True
    else:
        return False
# Funciones de ordenamiento
def sortLikes(catalog,categoria):
    
    categorias=obtener_videos_categoria(catalog,categoria)

    lista_categoria=categorias['videos']
    
    sorted_list = ms.sort(lista_categoria, cmpVideosByLikes)
    return sorted_list

def sort_con_tags(tag,catalog,nombre_pais):
    
    pais=catalog['paises']
    prelistap=mp.get(pais,nombre_pais)
    listap=me.getValue(prelistap)
    lista_pais=listap['videos']
    lista_tags=tags_en_lista(tag,lista_pais,catalog)
    sorted_list = ms.sort(lista_tags, cmpVideosByLikes)
    return sorted_list

def sortVideos(catalog,nombre_pais,categoria):
    pais=catalog['paises']
    filtro_uno=mp.get(pais,nombre_pais)
    filtro_unovalue=me.getValue(filtro_uno)
    filtro_dos=filtro_unovalue["categorias"]
    filtro_tres=mp.get(filtro_dos,categoria)
    filtro_tresvalue=me.getValue(filtro_tres)
    lista_ordenar=filtro_tresvalue['videos']
    tamaño=lt.size(lista_ordenar)
    sub_list = lt.subList(lista_ordenar, 1, tamaño)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpVideosByViews)
    return sorted_list

def trending_categoria(catalog,categoria):
    categorias_map=catalog['categoria_trending']
    cat=mp.get(categorias_map,categoria)
    lista_videos=me.getValue(cat)['videos']
    tamaño=lt.size(lista_videos)
    sub_list = lt.subList(lista_videos, 1, tamaño)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpVideosByTrending)
    return sorted_list

def trending_pais(catalog,pais):
    pai = catalog['pais_trending']
    pa=mp.get(pai,pais)
    lista_videos=me.getValue(pa)['videos']
    tamaño=lt.size(lista_videos)
    sub_list = lt.subList(lista_videos, 1, tamaño)
    sub_list = sub_list.copy()
    sorted_list = ms.sort(sub_list, cmpVideosByTrending)
    return sorted_list