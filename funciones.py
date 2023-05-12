import re
import random
from os import system
from datetime import datetime

"1"
def parser_csv(path:str)->list:
    '''
    Brief: Guarda a los personajes con sus caracteristicas en una lista con diccionarios
    Parameters: path ->  Direccion del archivo.
    Return: retorna una lista con diccionarios con los atributos de los personajes.
    '''
    coleccion = []
    with open(path,"r",encoding="utf-8") as archivo:
        for personaje in archivo:
            personaje = personaje.strip() #CON EL STRIP ME ASEGURO DE QUE NO HAYA ESPACIOS VACIOS
            lectura = re.split(r",|\n|\|\$%", personaje) #
            key = {}
            key["ID"] = int(lectura[0])
            key["nombre"] = lectura[1]
            key["raza"] = lectura[2]
            key["poder_de_pelea"] = int(lectura[3]) #CASTEO LOS TIPOS DE DATOS NUMERICOS A ENTEROS
            key["poder_de_defensa"] = int(lectura[4])
            key["habilidades"] = lectura[5:] #A PARTIR DE LA POSICION 5 SON HABILIDADES
            coleccion.append(key)
        return coleccion


def separar_mas_de_una_raza(lista:list)->None:
    '''
    Brief: Separa y crea una lista cuando el personaje tiene mas de una raza
    parameters: lista -> es la lista a iterar 
    return: no retorna nada
    '''
    for personaje in lista:
        if re.search(r"e-H|n-H", personaje["raza"]):
            personaje["raza"] = re.split(r"-", personaje["raza"])

"2" 
def listar_tipos(lista:list,dato)->list:
    "LISTA UN TIPO DE DATO Y LO DEVUELVE EN UNA LISTA SIN VALORES REPETIDOS"
    listado = []
    for personaje in lista:
        if type(personaje[dato]) == list:
            for i in personaje[dato]:
                i = i.strip()
                listado.append(i)
        else:
            listado.append(personaje[dato])

    listado = set(listado)
    listado = list(listado)
    return listado

def contar_tipos(lista:list,dato:str)->dict:

    lista_tipos = listar_tipos(lista,dato)
    coleccion_cantidad = {}
    for tipo in lista_tipos:
        if tipo not in coleccion_cantidad:
            coleccion_cantidad[tipo] = 0
    for personaje in lista:
        dato_obtenido = personaje[dato]
        if type(dato_obtenido) == list:
            for i in dato_obtenido:
                nombre_sin_espacio_final = sacar_espacios_al_final(i)
                coleccion_cantidad[nombre_sin_espacio_final] += 1
        else :
            coleccion_cantidad[dato_obtenido] += 1
    return coleccion_cantidad

"3"
def listar_personajes_por_raza(lista:list,dato="raza")->list:
    lista_de_razas = listar_tipos(lista,dato)
    for raza in lista_de_razas:
        print("-----------")
        print(raza)
        print("-----------")
        for personaje in lista:
            if type(personaje["raza"]) == list:
                for i in personaje["raza"]:
                    if i == raza:
                        print(f'NOMBRE: {personaje["nombre"]} | PODER DE PELEA: {personaje["poder_de_pelea"]}')
            elif personaje["raza"] == raza:
                print(f'NOMBRE: {personaje["nombre"]} | PODER DE PELEA: {personaje["poder_de_pelea"]}')


"4"

def dividir(dividendo:int, divisor:int)-> float:
    if divisor == 0:
        resultado = 0
    else:
        resultado = dividendo/divisor
        resultado = float(resultado)
        return resultado

def calcular_promedio_ataque_defensa(poder_pelea:int,poder_defensa:int)->float:
    suma = poder_pelea + poder_defensa
    promedio = dividir(suma,2)
    return promedio

def imprimir_habilidades(lista:list):
    print("Lista de habilidades:")
    habilidades = listar_tipos(lista, "habilidades")
    for habilidad in habilidades:
        print(habilidad)

def buscar_personajes_por_habilidad(lista:list):
    respuesta = input("Ingrese una habilidad: ").upper()
    encontro_habilidad = False 
    listado = []
    diccionario = {}
    for personaje in lista:
        habilidades = personaje["habilidades"]
        for habilidad in habilidades:
            habilidad = habilidad.strip()
            if re.search(f"^{respuesta}$",habilidad.upper()):
                encontro_habilidad = True
                diccionario["ID"]: personaje["ID"]
                diccionario["nombre"] = personaje["nombre"]
                diccionario["raza"] = personaje["raza"]
                diccionario["poder_de_pelea"] = personaje["poder_de_pelea"]
                diccionario["poder_de_defensa"] = personaje["poder_de_defensa"]
                diccionario["habilidades"] = personaje["habilidades"]
                listado.append(diccionario)
    if not encontro_habilidad :
        print ("ERROR, NO SE ENCONTRO LA HABILIDAD")
    else:
        return listado

def listar_personajes_por_habilidad(lista:list)->None:
    personaje_con_habilidad = buscar_personajes_por_habilidad(lista)
    for personaje in personaje_con_habilidad:
        nombre = personaje["nombre"]
        raza = personaje["raza"]
        poder_pelea = personaje["poder_de_pelea"]
        poder_defensa = personaje["poder_de_defensa"]
        promedio = calcular_promedio_ataque_defensa(poder_pelea,poder_defensa)
        print(f"NOMBRE: {nombre}\tRAZA: {raza}\tPROMEDIO ATQ/DEF: {promedio}")
        print("--------------------------------------------------------------")
    respuesta = input("¿Buscar otra habilidad ? (si/no): ")
    if respuesta.lower() == "si":
        listar_personajes_por_habilidad(lista)
    if respuesta.lower() == "no":
        respuesta = input("¿Volver al menu principal ? (si/no): ")
        if respuesta.lower() == "si":
            menu_principal("DBZ.csv")
        else:
            print("Gracias por jugar...")

"5"
def seleccionar_personaje_usuario(lista:list)->int:
    while True:
        for personaje in lista:
            id = personaje["ID"]
            nombre = personaje["nombre"]
            print(f"{id} ---> {nombre}")
        respuesta = input("Seleccione su personaje: ")
        if validar_entero(respuesta) and int(respuesta) > 0 and int(respuesta) <= 35:
            break
        else: 
            input("Error, presione enter para continuar")
    return int(respuesta)

def buscar_nombre_por_id(lista:list,id:int)->str:
    for personaje in lista:
        if personaje["ID"] == id:
            nombre = personaje["nombre"]
    return nombre

def buscar_poder_por_id(lista:list,id:int)->int:
    for personaje in lista:  #busco el poder de los personajes elegidos
        if personaje["ID"] == id:
            poder_de_pelea = personaje["poder_de_pelea"]
            poder_de_defensa = personaje["poder_de_defensa"]
            poder = calcular_promedio_ataque_defensa(poder_de_pelea, poder_de_defensa)
    return poder

def seleccionar_personaje_aleatorio(id_usuario:int):
    id_aleatorio = random.randint(1,35)
    if id_aleatorio == id_usuario:
            seleccionar_personaje_aleatorio(id_usuario)
    return id_aleatorio


def batallar(lista:list,id_usuario:int,id_maquina:int)->int: 

    poder_usuario = buscar_poder_por_id(lista, id_usuario)
    poder_maquina = buscar_poder_por_id(lista, id_maquina)
    if poder_usuario > poder_maquina:
        perdedor = id_maquina 
    else: 
        perdedor = id_usuario
        
    return perdedor

def seleccionar_personajes(lista:list):
    id_personaje_usuario = seleccionar_personaje_usuario(lista)
    id_personaje_maquina = seleccionar_personaje_aleatorio(id_personaje_usuario)

    return id_personaje_usuario,id_personaje_maquina

def jugar_batalla(lista:list):
    id_usuario,id_maquina = seleccionar_personajes(lista)
    id_perdedor = batallar(lista,id_usuario,id_maquina)
    resultado_batalla(lista,id_perdedor,id_usuario,id_maquina)

def resultado_batalla(lista:list, id_perdedor:int, id_usuario:int, id_maquina:int)->None:
    nombre_usuario = buscar_nombre_por_id(lista, id_usuario)
    nombre_maquina = buscar_nombre_por_id(lista, id_maquina)
    fecha = datetime.now().strftime("%d/%m/%Y")
    if id_perdedor == id_usuario:
        archivo = open("batallas.txt","a")
        archivo.write(f"{fecha} > {nombre_usuario} Perdio contra {nombre_maquina}\n")
        print("Has perdido la batalla")
        archivo.close()
    else:
        archivo = open("batallas.txt","a")
        print("Has ganado la batalla")
        archivo.write(f"{fecha} > {nombre_usuario} Gano contra {nombre_maquina}\n")
        archivo.close()

def validar_entero(numero:str)->bool:
    '''
    Brief: Valida si un string contiene digitos
    Parameters: 
    numero : str -> es el string a validar 
    return: retorna un valor booleano, True si es un digito y False si no
    '''
    return numero.isdigit()

def imprimir_menu()->None:
    print('''Elige una opcion: 
1: Traer datos desde archivo 
2: Mostrar cantidades por raza
3: Listar personaje por raza"
4: Listar personaje por habilidad
5: Jugar batalla
6: Guardar Json''')

def menu_principal(path:str):
    imprimir_menu()
    respuesta = input("Ingrese una opcion: ").upper()
    if validar_entero(respuesta) and int(respuesta) > 0 and int(respuesta) <= 8:
        match int(respuesta):
            case 1:
                mi_coleccion = parser_csv(path) 
                separar_mas_de_una_raza(mi_coleccion)
                menu_principal(path)
            case 2: 
                    mi_coleccion = parser_csv(path) 
                    separar_mas_de_una_raza(mi_coleccion)
                    lista_cantidad_por_raza = contar_tipos(mi_coleccion,"raza")
                    for i in lista_cantidad_por_raza:
                        cantidad = lista_cantidad_por_raza[i]
                        print(f"{i}: {cantidad}")
            case 3:
                    mi_coleccion = parser_csv(path)
                    separar_mas_de_una_raza(mi_coleccion)
                    listar_personajes_por_raza(mi_coleccion,"raza")
            case 4:
                    mi_coleccion = parser_csv(path)
                    separar_mas_de_una_raza(mi_coleccion)
                    listar_personajes_por_habilidad(mi_coleccion)
            case 5: 
                    mi_coleccion = parser_csv(path)
                    separar_mas_de_una_raza(mi_coleccion)
                    jugar_batalla(mi_coleccion)
            
    else: 
            system("cls")
            print("\n---------ERROR, INGRESE NUEVAMENTE LA OPCION---------\n")

"6"
def guardar_json(lista:list):
    respuesta = input("Ingrese una habilidad: ").upper()
    encontro_habilidad = False 
    for personaje in lista:
        habilidades = personaje["habilidades"]
        if type(habilidades) == list:
            for habilidad in habilidades:
                habilidad = habilidad.strip()
                if re.search(f"^{respuesta}$", habilidad.upper()):
                    encontro_habilidad = True
                    poder_pelea = personaje["poder_de_pelea"]
                    poder_defensa = personaje["poder_de_defensa"]
                    nombre = personaje["nombre"]
                    raza = personaje["raza"]
                    promedio = calcular_promedio_ataque_defensa(poder_pelea,poder_defensa)
                    print(f"NOMBRE: {nombre}\tRAZA: {raza}\tPROMEDIO ATQ/DEF: {promedio}")
                    print("--------------------------------------------------------------")

menu_principal("DBZ.csv")
mi_coleccion = parser_csv("DBZ.csv")
separar_mas_de_una_raza(mi_coleccion)

guardar_json(mi_coleccion)



