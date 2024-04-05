# Definir el tamaño fijo del arreglo
tamaño_fijo = 10

# Crear una lista con el tamaño fijo inicializada con valores nulos
archivos = [None] * tamaño_fijo

# Valor que quieres insertar
valor_insertar = "archivo1"

print(archivos)

# Buscar la primera posición que tenga el valor None e insertar el valor en esa posición
for i in range(len(archivos)):
    if archivos[i] is None:
        archivos[i] = valor_insertar
        break

# Mostrar el resultado
print(archivos)
