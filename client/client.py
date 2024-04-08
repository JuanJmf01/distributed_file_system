import sys
import requests
from tkinter import filedialog
from tkinter import *
import os
from datetime import datetime
import base64
import json



def seleccionar_archivo():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo")
    root.destroy()  # Cerrar la ventana despues de seleccionar el archivo
    return root.filename

def dividir_archivo(nombre_archivo):
    # Leer el archivo seleccionada (en la ruta) para guardarla
    with open(nombre_archivo, 'rb') as file:
        archivo_bytes = file.read()

    # Calcular la longitud total del archivo
    longitud_total = len(archivo_bytes)

    # Calcular el índice de división
    indice_division = longitud_total // 2

    # Dividir el archivo en dos partes
    parte1 = archivo_bytes[:indice_division]
    parte2 = archivo_bytes[indice_division:]

    # Convertir las partes a representaciones de texto utilizando base64
    parte1_codificada = base64.b64encode(parte1).decode('utf-8')
    parte2_codificada = base64.b64encode(parte2).decode('utf-8')

    return parte1_codificada, parte2_codificada

def unir_archivos(parte1, parte2):
    # Decodificar las partes codificadas en base64 y unirlas
    archivo_unido = parte1 + parte2
    return archivo_unido

def guardar_mensaje():
    response = requests.post('http://44.218.148.6:80/opcionesDataNodes')
    if response.status_code == 200:
        # Acceder al contenido de la respuesta como una lista de Python
        lista_de_data_nodes = response.json()
        
        # Llamar a la función para seleccionar un archivo
        nombre_completo = seleccionar_archivo()
        # Obtener el nombre de archivo sin la ruta del directorio
        nombre_archivo = os.path.basename(nombre_completo)

        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_con_fecha_hora = nombre_archivo.split(".")[0] + "_" + fecha_hora_actual + "." + nombre_archivo.split(".")[-1]

        print("Nombre de archivo seleccionado con fecha y hora:", nombre_con_fecha_hora)

        # Leer el archivo seleccionado (en la ruta) para guardarla
        parte1, parte2 = dividir_archivo(nombre_completo)

        guardar_archivo = True

        parte1_size_kb = sys.getsizeof(parte1) / 1024
        parte2_size_kb = sys.getsizeof(parte2) / 1024

        print(f'Tamaño bloque 1: {parte1_size_kb} ; Tamaño bloque 2: {parte2_size_kb}')

        if(parte1_size_kb >= lista_de_data_nodes[0]['capacidadActual']):
            guardar_archivo = False
        if(parte2_size_kb >= lista_de_data_nodes[1]['capacidadActual']):
            guardar_archivo = False


        for indice, dataNode in enumerate(lista_de_data_nodes):
            if indice == 0 and guardar_archivo:
                response = requests.post(f'http://{dataNode["host"]}:{dataNode["port"]}/guardar', json={'archivo': {'nombre': nombre_con_fecha_hora, 'archivo': parte1, 'tamaño_archivo': parte1_size_kb}})
                if response.status_code == 200 :
                    print(response.text)
                    requests.post(f'http://44.218.148.6:80/guardar_ubicacion_archivo', json={'ubicacion': {'nombre': nombre_con_fecha_hora, 'posicion': 1, 'host': dataNode["host"], 'port': dataNode["port"]}})
                elif response.status_code == 400:
                    print(response.text)
            elif indice == 1 and guardar_archivo:
                response = requests.post(f'http://{dataNode["host"]}:{dataNode["port"]}/guardar', json={'archivo': {'nombre': nombre_con_fecha_hora, 'posicion': 2, 'archivo': parte2,  'tamaño_archivo': parte2_size_kb}})
                if response.status_code == 200:
                    print(response.text)
                    requests.post(f'http://44.218.148.6:80/guardar_ubicacion_archivo', json={'ubicacion': {'nombre': nombre_con_fecha_hora, 'posicion': 2, 'host': dataNode["host"], 'port': dataNode["port"]}})
                elif response.status_code == 400:
                    print(response.text)
            else:
                print('Lastimosamente no tenemos espacio suficiente en nuestros servidores para almacenar tu archivo')

    else:
        print("Error al guardar el mensaje en el DataNode.")

def recuperar_archivo():
    response = requests.get('http://44.218.148.6:80/recuperar_ubicacion_archivos')
    if response.status_code == 200:
        # Acceder al contenido de la respuesta como una lista de Python
        lista_ubicacion_archivos = json.loads(response.text)

        nombres_archivos = set()
        for archivo in lista_ubicacion_archivos:
            nombres_archivos.add(archivo['nombre'])
        
        lista_nombre_archivos = [{'nombre': nombre} for nombre in nombres_archivos]

        # Mostrar el menú enumerado de nombres de archivos
        print("\nSeleccione el archivo que desea recuperar:")
        for i, archivo in enumerate(lista_nombre_archivos, start=1):
            print(f"{i}. {archivo['nombre']}")

        # Pedir al usuario que seleccione un archivo
        seleccion = input("\nIngrese el número correspondiente al archivo que desea recuperar: ")
        
        try:
            indice_seleccion = int(seleccion)
            if 1 <= indice_seleccion <= len(lista_nombre_archivos):
                nombre_seleccionado = lista_nombre_archivos[indice_seleccion - 1]['nombre']
                print(f"Ha seleccionado el archivo: {nombre_seleccionado}")
                # Aquí puedes devolver el nombre seleccionado o realizar otras acciones
            else:
                print("Selección inválida.")
        except ValueError:
            print("Entrada no válida. Por favor ingrese un número.")

        # Guardar en una lista solo la ubicacion de los bloques del archivo correspondiente
        archivos_con_mismo_nombre = [archivo for archivo in lista_ubicacion_archivos if archivo['nombre'] == nombre_seleccionado]
        print(archivos_con_mismo_nombre)

        parte1_archivo = None
        parte2_archivo = None

        for archivo in archivos_con_mismo_nombre:
            if archivo['posicion'] == 1:
                response = requests.get(f'http://{archivo["host"]}:{archivo["port"]}/recuperar_archivo', json={'data_archivo': {'nombre_archivo': nombre_seleccionado}})
                parte1_archivo = response.content  # Extraer el contenido del archivo de la respuesta
            elif archivo['posicion'] == 2:
                response = requests.get(f'http://{archivo["host"]}:{archivo["port"]}/recuperar_archivo', json={'data_archivo': {'nombre_archivo': nombre_seleccionado}})
                parte2_archivo = response.content  # Extraer el contenido del archivo de la respuesta

        # Decodificar los bloques de base64
        parte1_decodificada = base64.b64decode(parte1_archivo)
        parte2_decodificada = base64.b64decode(parte2_archivo)

        # Concatenar los bloques para reconstruir el archivo completo
        archivo_completo = parte1_decodificada + parte2_decodificada

        nombre_archivo_completo = f'{nombre_seleccionado}'
        with open(nombre_archivo_completo, 'wb') as file:
            file.write(archivo_completo)

    else:
        print("Error al recuperar la ubicación de los archivos del servidor.")




def menu():
    while True:
        print("\nSeleccione una opción:")
        print("1. Guardar archivo")
        print("2. Recuperar archivo")
        print("3. Salir")

        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            guardar_mensaje()
        elif opcion == "2":
            recuperar_archivo()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Por favor, seleccione 1, 2 o 3.")

if __name__ == '__main__':
    menu()
