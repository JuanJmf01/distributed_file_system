import sys
import requests
from flask import Flask, request
import base64

def registrar_con_servidor(host, port, capacidad):
    server_url = 'http://127.0.0.1:5000/register'
    data = {
        'host': host,
        'port': port,
        'capacidad': capacidad
    }
    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("DataNode registrado correctamente en el servidor.")
        else:
            print("Error al registrar DataNode en el servidor.")
    except requests.exceptions.RequestException as e:
        print("Error al conectar con el servidor:", e)

if __name__ == '__main__':
    host = '127.0.0.1'
    
    # Obtener el puerto de la línea de comandos
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000

    capacidad = 4
    archivos = [None] * capacidad
    
    registrar_con_servidor(host, port, capacidad)

    app = Flask(__name__)


    @app.route('/guardar', methods=['POST'])
    def guardar_archivo():
        estructura_archivo = request.json.get('archivo')
        
        # Decodificar la representación de texto a bytes utilizando base64
        archivo_codificado = estructura_archivo['archivo']
        archivo_bytes = base64.b64decode(archivo_codificado.encode('utf-8'))

        for i in range(len(archivos)):
            if archivos[i] is None:
                archivos[i] = {'nombre': estructura_archivo['nombre'], 'archivo': archivo_bytes}
                print(f'\nArchivo {estructura_archivo['nombre']} guardado exitosamente')

                break
                
        return f'Archivo guardado correctamente en el DataNode. Host: {host}, Puerto: {port}', 200

    @app.route('/recuperar', methods=['GET'])
    def recuperar_mensaje():
        posicion = request.json.get('posicion')
        if archivos:
            mensaje_recuperado = archivos[posicion]
            return mensaje_recuperado, 200
        else:
            return 'No hay mensajes almacenados en el DataNode.', 404

    app.run(debug=True, host=host, port=port)
