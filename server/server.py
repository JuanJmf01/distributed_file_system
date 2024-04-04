from flask import Flask, request, jsonify
import json


app = Flask(__name__)

data_nodes = []
direccion_archivos_guardados = []

@app.route('/register', methods=['POST'])
def register_data_node():
    data = request.json
    host = data.get('host')
    port = data.get('port')

    # Verificar si el DataNode ya está registrado
    for node in data_nodes:
        if node['host'] == host and node['port'] == port:
            print("El DataNode ya está registrado.")
            return jsonify({'message': 'DataNode ya registrado'}), 200

    # Si el DataNode no está registrado, agregarlo a la lista
    data_nodes.append({'host': host, 'port': port})

    print("Lista de DataNodes registrados:")
    for node in data_nodes:
        print(node)

    return jsonify({'message': 'DataNode registrado correctamente'}), 200

if __name__ == '__main__':
    # Especifica el HOST y PORT deseado
    host = '127.0.0.1'  # Por ejemplo
    port = 5000  # Por ejemplo

    @app.route('/opcionesDataNodes', methods=['POST'])
    def buscar_dataNodes_disponibles():
        # Devolver la lista de DataNodes como respuesta
        return jsonify(data_nodes)
    
    @app.route('/guardar_ubicacion_archivo', methods=['POST'])
    def guardar_ubicacion_archivo():
        ubicacion_archivo = request.json.get('ubicacion')
        nombre = ubicacion_archivo['nombre'] 
        posicion = ubicacion_archivo['posicion'] 
        host = ubicacion_archivo['host'] 
        port = ubicacion_archivo['port'] 

        direccion_archivos_guardados.append({"nombre": nombre, "posicion": posicion, "host": host, "port": port})

        return jsonify({'message': 'Ubicación del archivo guardada correctamente'}), 200

    

    @app.route('/recuperar_ubicacion_archivos', methods=['GET'])
    def devolver_ubicacion_archivos():
        # Convertir la lista a formato JSON
        ubicacion_json = json.dumps(direccion_archivos_guardados)
        
        # Devolver la lista como parte de la respuesta HTTP
        return ubicacion_json, 200

    

    # Ejecuta la aplicación Flask con el HOST y PORT especificado
    app.run(debug=True, host=host, port=port)
