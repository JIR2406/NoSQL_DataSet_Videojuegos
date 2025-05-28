import pandas as pd
import xml.etree.ElementTree as ET

# Leer el archivo CSV
df = pd.read_csv('vgsales.csv')

# Crear el elemento raíz
root = ET.Element('vgsales')

# Convertir cada fila en un elemento XML
for _, row in df.iterrows():
    game = ET.SubElement(root, 'game')
    for col in df.columns:
        child = ET.SubElement(game, col)
        child.text = str(row[col])

# Crear el árbol y escribirlo a un archivo XML
tree = ET.ElementTree(root)
tree.write('vgsales.xml', encoding='utf-8', xml_declaration=True)

print("Archivo XML generado correctamente.")
