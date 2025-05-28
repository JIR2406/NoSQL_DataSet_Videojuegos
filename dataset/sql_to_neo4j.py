from py2neo import Graph, Node, Relationship
import sqlite3

# Conectar a Neo4j (ajusta usuario y contraseña)
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

# Conectar a SQLite
conn = sqlite3.connect('videojuegos.db')
cursor = conn.cursor()
cursor.execute("""
SELECT Rank, Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales FROM datos
""")
rows = cursor.fetchall()

for row in rows:
    rank, name, platform, year, genre, publisher, na_sales, eu_sales, jp_sales, other_sales, global_sales = row

    # Validar y asignar valores por defecto si es necesario
    platform = platform if platform and platform.strip() else "Desconocido"
    genre = genre if genre and genre.strip() else "Desconocido"
    publisher = publisher if publisher and publisher.strip() else "Desconocido"

    # Crear o fusionar nodos principales
    p_node = Node("Plataforma", nombre=platform)
    g_node = Node("Genero", nombre=genre)
    pub_node = Node("Publisher", nombre=publisher)

    graph.merge(p_node, "Plataforma", "nombre")
    graph.merge(g_node, "Genero", "nombre")
    graph.merge(pub_node, "Publisher", "nombre")

    # Crear nodo videojuego
    vj_node = Node("Videojuego", 
                   name=name,
                   rank=rank,
                   year=year if year else None,
                   global_sales=global_sales)
    graph.create(vj_node)

    # Crear relaciones
    graph.create(Relationship(vj_node, "LANZADO_EN", p_node))
    graph.create(Relationship(vj_node, "TIENE_GENERO", g_node))
    graph.create(Relationship(vj_node, "PUBLICADO_POR", pub_node))

    # Crear nodos región y relaciones ventas si ventas > 0
    regions = [("NA", na_sales), ("EU", eu_sales), ("JP", jp_sales), ("Other", other_sales)]
    for region_name, sales in regions:
        if sales and sales > 0:
            r_node = Node("Region", nombre=region_name)
            graph.merge(r_node, "Region", "nombre")
            rel = Relationship(vj_node, "VENTAS_EN", r_node, cantidad=sales)
            graph.create(rel)

conn.close()
print("Migración a Neo4j completada.")
