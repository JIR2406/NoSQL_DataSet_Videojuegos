from pymongo import MongoClient

# Reconectar a SQLite para crear documentos
conn = sqlite3.connect('videojuegos.db')
cursor = conn.cursor()
cursor.execute("SELECT Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales FROM datos")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Crear lista de diccionarios
documents = []
for row in rows:
    doc = dict(zip(columns, row))
    # Si Year está vacío o nulo, poner None, sino int
    if doc['Year'] is not None:
        try:
            doc['Year'] = int(doc['Year'])
        except:
            doc['Year'] = None
    documents.append(doc)

conn.close()

# Conectar MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['videojuegos_db']
collection = db['videojuegos']

# Insertar documentos en MongoDB
result = collection.insert_many(documents)
print(f"Documentos insertados: {len(result.inserted_ids)}")
