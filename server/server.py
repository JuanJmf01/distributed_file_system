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
    capacidad = data.get('capacidad')

    # Verificar si el DataNode ya esta registrado
    for node in data_nodes:
        if node['host'] == host and node['port'] == port:
            return jsonify({'message': 'DataNode ya registrado'}), 200

    # Si el DataNode no está registrado, agregarlo a la lista
    data_nodes.append({'host': host, 'port': port, 'capacidadActual': capacidad})

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
        # Filtrar los data nodes con capacidad mayor a cero
        data_nodes_con_capacidad = [nodo for nodo in data_nodes if nodo['capacidadActual'] > 0]

        if len(data_nodes_con_capacidad) >= 2:
            # Ordenar la lista de data nodes por capacidad actual en orden descendente
            data_nodes_ordenados = sorted(data_nodes_con_capacidad, key=lambda x: x['capacidadActual'], reverse=True)
            
            # Seleccionar los dos primeros data nodes con la mayor capacidad
            data_nodes_top = data_nodes_ordenados[:2]
            
            # Devolver los dos data nodes seleccionados como respuesta
            return jsonify({"mensaje": "exito", "data_nodes": data_nodes_top})
        elif len(data_nodes_con_capacidad) == 1:
            # Si solo hay un nodo con capacidad mayor a cero, se puede enviar un mensaje especial
            return jsonify({"mensaje": "Solo hay un nodo con capacidad mayor a cero. No es posible almacenar el archivo."})
        else:
            # Si no hay nodos con capacidad mayor a cero, enviar un mensaje especial
            return jsonify({"mensaje": "No hay capacidad disponible para almacenar el archivo."})

    
    @app.route('/guardar_ubicacion_archivo', methods=['POST'])
    def guardar_ubicacion_archivo():
        ubicacion_archivo = request.json.get('ubicacion')
        nombre = ubicacion_archivo['nombre'] 
        posicion = ubicacion_archivo['posicion'] 
        host = ubicacion_archivo['host'] 
        port = ubicacion_archivo['port'] 

        direccion_archivos_guardados.append({"nombre": nombre, "posicion": posicion, "host": host, "port": port})
        for nodo in data_nodes:
            if nodo['host'] == host and nodo['port'] == port:
                # Restar la capacidad del nodo ya que se inserto un nuevo bloque de archivo
                nodo['capacidadActual'] = nodo['capacidadActual'] -1 
                print("Lista de DataNodes ahora:")
                for node in data_nodes:
                    print(node)
                break
        


        return jsonify({'message': 'Ubicación del archivo guardada correctamente'}), 200

    

    @app.route('/recuperar_ubicacion_archivos', methods=['GET'])
    def devolver_ubicacion_archivos():
        # Convertir la lista a formato JSON
        ubicacion_json = json.dumps(direccion_archivos_guardados)
        
        # Devolver la lista como parte de la respuesta HTTP
        return ubicacion_json, 200

    

    # Ejecuta la aplicación Flask con el HOST y PORT especificado
    app.run(debug=True, host=host, port=port)
