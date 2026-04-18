import sqlite3
import pandas as pd

# 1. Crear conexión y base de datos física
conn = sqlite3.connect('database/datos_ventas.db')

# 2. Datos de ejemplo
datos = {
    'dia': ['Lunes', 'Martes', 'Miercoles', 'Lunes', 'Martes', 'Miercoles', 'Lunes', 'Martes', 'Miercoles'],
    'fruta': ['Manzana', 'Manzana', 'Manzana', 'Pera', 'Pera', 'Pera', 'Uva', 'Uva', 'Uva'],
    'cantidad': [5, 7, 3, 2, 4, 8, 3, 6, 8]
}

df_ejemplo = pd.DataFrame(datos)

# 3. Guardar el DataFrame en una tabla SQL
df_ejemplo.to_sql('ventas_frutas', conn, if_exists='replace', index=False)

conn.close()
print("Base de datos 'datos_ventas.db' creada con éxito.")