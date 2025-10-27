import calendarios_trimestral
import os
import msvcrt  # Solo funciona en Windows

# Funciones asociadas a cada opción del menú
def agregar_plan():
    print("Función para agregar tareas (pendiente de implementación).")
    input("\nPresiona cualquier tecla para continuar...")

def editar_plan():
    print("Función para editar tareas (pendiente de implementación).")
    input("\nPresiona cualquier tecla para continuar...")

def borrar_plan():
    print("Función para borrar tareas (pendiente de implementación).")
    input("\nPresiona cualquier tecla para continuar...")

def imprimir_plan():
    print("Función para imprimir o exportar tareas (pendiente de implementación).")
    input("\nPresiona cualquier tecla para continuar...")

def salir():
    print("Saliendo del programa. ¡Hasta pronto!")
    input("\nPresiona cualquier tecla para salir...")
    exit()

# Función principal que crea y gestiona el menú
def crear_menu(fila, columna, opciones, funciones, orientacion='V'):
    seleccion = 0
    mes_actual = 11
    año_actual = 2025

    def mostrar_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"📅 Calendario actual: {mes_actual:02d}/{año_actual}\n")
        calendarios_trimestral.mostrar_calendarios_trimestre(mes_actual, año_actual)
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

            # Movimiento en menú
            if orientacion.upper() == 'V':
                if flecha == b'H':  # Flecha arriba
                    seleccion = (seleccion - 1) % len(opciones)
                elif flecha == b'P':  # Flecha abajo
                    seleccion = (seleccion + 1) % len(opciones)
            else:
                if flecha == b'K':  # Flecha izquierda
                    seleccion = (seleccion - 1) % len(opciones)
                elif flecha == b'M':  # Flecha derecha
                    seleccion = (seleccion + 1) % len(opciones)

            # Modificación de mes y año
            if flecha == b'G':  # Inicio (Home)
                mes_actual = 12 if mes_actual == 1 else mes_actual - 1
            elif flecha == b'O':  # Fin (End)
                mes_actual = 1 if mes_actual == 12 else mes_actual + 1
            elif flecha == b'I':  # Re Pág (Page Up)
                año_actual -= 1
            elif flecha == b'Q':  # Av Pág (Page Down)
                año_actual += 1

        elif tecla == b'\r':  # Enter
            os.system('cls' if os.name == 'nt' else 'clear')
            funciones[seleccion]()
            if opciones[seleccion].lower().strip() == "salir":
                break

# Opciones del menú y funciones asociadas
opciones = ["Agregar ", "Editar ", "Borrar ", "Imprimir ", "Salir "]
funciones = [agregar_plan, editar_plan, borrar_plan, imprimir_plan, salir]

# Ejecutar el menú
crear_menu(fila=2, columna=10, opciones=opciones, funciones=funciones, orientacion='H')