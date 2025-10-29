import sqlite3

def conectar():
    return sqlite3.connect("tareas.db")

def inicializar():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            prioridad TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def agregar_tarea(titulo, fecha, prioridad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tareas (titulo, fecha, prioridad) VALUES (?, ?, ?)", (titulo, fecha, prioridad))
    conn.commit()
    conn.close()

def obtener_tareas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, fecha, prioridad FROM tareas")
    tareas = [{"Título": t[0], "Fecha límite": t[1], "Prioridad": t[2]} for t in cursor.fetchall()]
    conn.close()
    return tareas

def listar_tareas_con_id():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, fecha, prioridad FROM tareas")
    tareas = cursor.fetchall()
    conn.close()
    return tareas

def editar_tarea(id, nuevo_titulo, nueva_fecha, nueva_prioridad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas
        SET titulo = ?, fecha = ?, prioridad = ?
        WHERE id = ?
    """, (nuevo_titulo, nueva_fecha, nueva_prioridad, id))
    conn.commit()
    conn.close()

def borrar_tarea(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
    conn.commit()
    conn.close()