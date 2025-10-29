import calendarios_trimestral
import db_tareas
import os
import msvcrt
from datetime import datetime

# Inicializar base de datos
db_tareas.inicializar()



#  Exportar tareas a texto plano
def exportar_tareas():
    os.system('cls')
    tareas = db_tareas.listar_tareas_con_id()
    nombre_archivo = "tareas_exportadas.txt"

    if not tareas:
        print(" No hay tareas para exportar.")
    else:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(" Tareas exportadas\n\n")
            for t in tareas:
                archivo.write(f"ID: {t[0]}\n")
                archivo.write(f"Título: {t[1]}\n")
                archivo.write(f"Fecha límite: {t[2]}\n")
                archivo.write(f"Prioridad: {t[3]}\n")
                archivo.write("-" * 30 + "\n")
        print(f"\n Tareas exportadas a '{nombre_archivo}'")

        try:
            os.startfile(nombre_archivo)
        except:
            print(" No se pudo abrir el archivo automáticamente.")

        respuesta = input("\n¿Deseás imprimir el archivo? (s/n): ").strip().lower()
        if respuesta == 's':
            try:
                os.startfile(nombre_archivo, "print")
                print(" Enviando a impresión...")
            except:
                print(" No se pudo imprimir el archivo.")
    input("\nPresiona cualquier tecla para continuar...")


#  Normalizar prioridad con validación
def normalizar_prioridad(texto):
    texto = texto.strip().lower()
    if texto in ["alta", "a"]:
        return "Alta"
    elif texto in ["media", "m"]:
        return "Media"
    elif texto in ["baja", "b"]:
        return "Baja"
    else:
        return None

#  Validar fecha
def validar_fecha(fecha_texto):
    try:
        datetime.strptime(fecha_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False

#  Agregar tarea
def agregar_plan():
    os.system('cls')
    print("Agregar nueva tarea:")
    titulo = input("Título: ")

    while True:
        fecha = input("Fecha límite (AAAA-MM-DD) [Enter para usar la actual]: ").strip()
        if not fecha:
            fecha = datetime.now().strftime("%Y-%m-%d")
            break
        if validar_fecha(fecha):
            break
        print(" Fecha inválida. Usa el formato AAAA-MM-DD.")

    while True:
        prioridad_input = input("Prioridad (Alta, Media, Baja): ")
        prioridad = normalizar_prioridad(prioridad_input)
        if prioridad:
            break
        print(" Prioridad no válida. Usa Alta, Media o Baja.")

    db_tareas.agregar_tarea(titulo, fecha, prioridad)
    print("\n Tarea agregada con éxito.")
    input("\nPresiona cualquier tecla para continuar...")

#  Editar tarea
def editar_plan():
    os.system('cls')
    print("Editar tarea existente:\n")
    tareas = db_tareas.listar_tareas_con_id()
    for t in tareas:
        print(f"[{t[0]}] {t[1]} - {t[2]} ({t[3]})")

    try:
        id = int(input("\nID de la tarea a editar: "))
        tarea_actual = next((t for t in tareas if t[0] == id), None)

        if not tarea_actual:
            print("\n No se encontró una tarea con ese ID.")
        else:
            print("\nDeja el campo vacío para conservar el valor actual.")
            nuevo_titulo = input(f"Título [{tarea_actual[1]}]: ").strip() or tarea_actual[1]

            while True:
                nueva_fecha = input(f"Fecha límite [{tarea_actual[2]}]: ").strip()
                if not nueva_fecha:
                    nueva_fecha = tarea_actual[2]
                    break
                if validar_fecha(nueva_fecha):
                    break
                print(" Fecha inválida. Usa el formato AAAA-MM-DD.")

            while True:
                prioridad_input = input(f"Prioridad [{tarea_actual[3]}]: ").strip()
                if not prioridad_input:
                    nueva_prioridad = tarea_actual[3]
                    break
                nueva_prioridad = normalizar_prioridad(prioridad_input)
                if nueva_prioridad:
                    break
                print(" Prioridad no válida. Usa Alta, Media o Baja.")

            db_tareas.editar_tarea(id, nuevo_titulo, nueva_fecha, nueva_prioridad)
            print("\n Tarea actualizada con éxito.")
    except:
        print("\n Entrada inválida o error al editar.")
    input("\nPresiona cualquier tecla para continuar...")

#  Borrar tarea
def borrar_plan():
    os.system('cls')
    print("Borrar tarea:\n")
    tareas = db_tareas.listar_tareas_con_id()
    for t in tareas:
        print(f"[{t[0]}] {t[1]} - {t[2]} ({t[3]})")

    try:
        id = int(input("\nID de la tarea a borrar: "))
        confirmacion = input("¿Estás seguro? (s/n): ").lower()
        if confirmacion == 's':
            db_tareas.borrar_tarea(id)
            print("\n Tarea eliminada.")
        else:
            print("\nOperación cancelada.")
    except:
        print("\n Entrada inválida o error al borrar.")
    input("\nPresiona cualquier tecla para continuar...")

#  Imprimir tareas
def imprimir_plan():
    os.system('cls')
    print("Listado de tareas:\n")
    tareas = db_tareas.listar_tareas_con_id()
    for t in tareas:
        print(f"[{t[0]}] {t[1]} - {t[2]} ({t[3]})")
    input("\nPresiona cualquier tecla para continuar...")

#  Salir
def salir():
    print("Saliendo del programa. ¡Hasta pronto!")
    input("\nPresiona cualquier tecla para salir...")
    exit()

#  Menú principal
def crear_menu(fila, columna, opciones, funciones, orientacion='V'):
    seleccion = 0
    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    def mostrar_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\033[44m  Calendario actual: {mes_actual:02d}/{año_actual} \033[0m\n")
        tareas = db_tareas.obtener_tareas()
        calendarios_trimestral.mostrar_calendarios_trimestre(mes_actual, año_actual, tareas)
        print("\n" * fila)

        if orientacion.upper() == 'V':
            for idx, opcion in enumerate(opciones):
                texto = opcion.upper() if idx == seleccion else opcion.lower()
                ancho = len(texto) + 2
                bloque = [
                    " " * columna + f"┌{'─'*ancho}┐" if idx == seleccion else " " * columna + " " * (ancho + 2),
                    " " * columna + f"│ {texto} │" if idx == seleccion else " " * columna + f"  {texto}",
                    " " * columna + f"└{'─'*ancho}┘" if idx == seleccion else " " * columna + " " * (ancho + 2)
                ]
                print("\n".join(bloque))
        else:
            bloques = [[], [], []]
            for idx, opcion in enumerate(opciones):
                texto = opcion.upper() if idx == seleccion else opcion.lower()
                ancho = len(texto) + 1
                if idx == seleccion:
                    bloques[0].append(f"┌{'─'*ancho}┐")
                    bloques[1].append(f"│\033[41m {texto}\033[40m│")
                    bloques[2].append(f"└{'─'*ancho}┘")
                else:
                    espacio = len(texto) + 4
                    bloques[0].append(" " * espacio)
                    bloques[1].append(f"  {texto}  ")
                    bloques[2].append(" " * espacio)
            for linea in bloques:
                print(" " * columna + "    ".join(linea))

    while True:
        mostrar_menu()
        tecla = msvcrt.getch()

        if tecla in [b'\xe0', b'\x00']:
            flecha = msvcrt.getch()
            if orientacion.upper() == 'V':
                if flecha == b'H':
                    seleccion = (seleccion - 1) % len(opciones)
                elif flecha == b'P':
                    seleccion = (seleccion + 1) % len(opciones)
            else:
                if flecha == b'K':
                    seleccion = (seleccion - 1) % len(opciones)
                elif flecha == b'M':
                    seleccion = (seleccion + 1) % len(opciones)

            if flecha == b'G':
                mes_actual = 12 if mes_actual == 1 else mes_actual - 1
            elif flecha == b'O':
                mes_actual = 1 if mes_actual == 12 else mes_actual + 1
            elif flecha == b'I':
                año_actual -= 1
            elif flecha == b'Q':
                año_actual += 1

        elif tecla == b'\r':
            os.system('cls' if os.name == 'nt' else 'clear')
            funciones[seleccion]()
            if opciones[seleccion].lower().strip() == "salir":
                break

# Opciones del menú
opciones = ["Agregar ", "Editar ", "Borrar ", "Imprimir ", "Exportar ", "Salir "]
funciones = [agregar_plan, editar_plan, borrar_plan, imprimir_plan, exportar_tareas, salir]

# Ejecutar el menú
crear_menu(fila=10, columna=1, opciones=opciones, funciones=funciones, orientacion='H')