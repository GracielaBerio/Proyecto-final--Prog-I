import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import Planificador_de_tareas as app
from datetime import datetime
import pytest

# ---------- FIXTURE GLOBAL ----------
@pytest.fixture(scope="function", autouse=True)
def preparar_bd_temporal(tmp_path):
    test_db = tmp_path / "tareas_test.db"
    app.DB_NOMBRE = str(test_db)
    app.iniciar_bd()
    yield

# ---------- BASE DE DATOS ----------
def test_agregar_y_obtener_tarea():
    app.agregar_tarea("Prueba", "Descripción", "2025-11-01", "Alta")
    tareas = app.obtener_tareas()
    assert len(tareas) == 1
    assert tareas[0][1] == "Prueba"
    assert tareas[0][4] == "Alta"

def test_actualizar_tarea():
    app.agregar_tarea("Original", "Desc", "2025-11-01", "Media")
    id_tarea = app.obtener_tareas()[0][0]
    app.actualizar_tarea(id_tarea, "Modificada", "Nueva desc", "2025-11-02", "Baja")
    tarea = app.obtener_tareas()[0]
    assert tarea[1] == "Modificada"
    assert tarea[4] == "Baja"

def test_eliminar_tarea():
    app.agregar_tarea("Eliminar", "", "2025-11-01", "Alta")
    id_tarea = app.obtener_tareas()[0][0]
    app.eliminar_tarea(id_tarea)
    assert app.obtener_tareas() == []

# ---------- UTILIDADES ----------
def test_parsear_fecha_valida():
    fecha = app.parsear_fecha_segura("2025-11-01")
    assert isinstance(fecha, datetime)

def test_parsear_fecha_invalida():
    assert app.parsear_fecha_segura("fecha-mal") is None

# ---------- FILTROS Y ORDEN ----------
def test_filtrar_por_prioridad():
    app.agregar_tarea("Alta", "", "2025-11-01", "Alta")
    app.agregar_tarea("Baja", "", "2025-11-01", "Baja")
    tareas_alta = app.obtener_tareas(filtro_prioridad="Alta")
    assert all(t[4] == "Alta" for t in tareas_alta)

def test_busqueda_por_titulo():
    app.agregar_tarea("Buscarme", "Texto", "2025-11-01", "Media")
    resultados = app.obtener_tareas(busqueda="Buscarme")
    assert len(resultados) == 1
    assert resultados[0][1] == "Buscarme"

def test_ordenamiento_inverso():
    app.agregar_tarea("Primero", "", "2025-11-01", "Alta")
    app.agregar_tarea("Segundo", "", "2025-11-02", "Alta")
    tareas = app.obtener_tareas(orden="fecha_limite")
    tareas_invertidas = list(reversed(tareas))
    assert tareas_invertidas[0][1] == "Segundo"

# ---------- EXPORTACIÓN / IMPORTACIÓN ----------
def test_exportar_importar_csv(tmp_path):
    app.agregar_tarea("CSV", "Test", "2025-11-01", "Media")
    archivo = tmp_path / "tareas.csv"
    app.exportar_csv(str(archivo))
    app.eliminar_tarea(app.obtener_tareas()[0][0])
    app.importar_csv(str(archivo))
    tareas = app.obtener_tareas()
    assert len(tareas) == 1
    assert tareas[0][1] == "CSV"

def test_exportar_importar_json(tmp_path):
    app.agregar_tarea("JSON", "Test", "2025-11-01", "Baja")
    archivo = tmp_path / "tareas.json"
    app.exportar_json(str(archivo))
    app.eliminar_tarea(app.obtener_tareas()[0][0])
    app.importar_json(str(archivo))
    tareas = app.obtener_tareas()
    assert len(tareas) == 1
    assert tareas[0][1] == "JSON"