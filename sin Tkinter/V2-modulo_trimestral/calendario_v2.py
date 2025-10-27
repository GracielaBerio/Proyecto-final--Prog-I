# Lista de tareas con fecha en formato AAAA-MM-DD
tareas = [
    {"Título": "Revisar propuesta", "Fecha límite": "2025-10-03","Prioridad":"Media"},
    {"Título": "Ejercicios de grafos", "Fecha límite": "2025-10-15","Prioridad":"Alta"},
    {"Título": "Informe institucional", "Fecha límite": "2025-10-22","Prioridad":"Baja"},
]

# Verifica si un año es bisiesto
def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

# Devuelve la cantidad de días que tiene un mes determinado
def dias_del_mes(mes, año):
    if mes == 2:
        return 29 if es_bisiesto(año) else 28
    elif mes in [4, 6, 9, 11]:
        return 30
    else:
        return 31

# Calcula el día de la semana del 1° del mes usando el algoritmo de Zeller
# Devuelve un número entre 0 (lunes) y 6 (domingo)
def dia_semana_primero(mes, año):
    if mes < 3:
        mes += 12
        año -= 1
    k = año % 100      # Últimos dos dígitos del año
    j = año // 100     # Siglo
    h = (1 + 13*(mes+1)//5 + k + k//4 + j//4 + 5*j) % 7
    return (h + 5) % 7  # Ajuste para que 0 = lunes

# Extrae los días del mes que tienen tareas registradas

#def dias_con_tareas(mes, año):
#    dias = set()
#    for tarea in tareas:
#        fecha = tarea["Fecha límite"]
#        a, m, d = map(int, fecha.split("-"))
#        if a == año and m == mes:
#            dias.add(d)
#    return dias
# convertimos a diccionario para poder almacenar la prioridad

def dias_con_tareas(mes, año):
    dias = {}
    for tarea in tareas:
        fecha = tarea["Fecha límite"]
        a, m, d = map(int, fecha.split("-"))
        if a == año and m == mes:
            dias[d] = tarea["Prioridad"]
    return dias




# Imprime el calendario mensual en consola, marcando los días con tareas
def mostrar_calendario(mes, año):
    nombre_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    # Encabezado con nombre del mes y año
    print(f"\n{nombre_meses[mes-1]} {año}".center(28))
    print(" ".join(dias_semana))

    primer_dia = dia_semana_primero(mes, año)      # Día de la semana del 1°
    total_dias = dias_del_mes(mes, año)            # Total de días del mes
    marcados = dias_con_tareas(mes, año)           # Días con tareas

    # Espacios en blanco antes del primer día
    print("    " * primer_dia, end="")

    dia_actual = 1
    columna = primer_dia
    while dia_actual <= total_dias:
        # Si el día tiene tarea, se marca con asterisco
      #      if dia_actual in marcados:
      #      print(f"\033[41m{dia_actual:>2}*\033[40m", end=" ")

        if dia_actual in marcados:
            prioridad = marcados[dia_actual]
            color = {"Alta": "\033[41m", "Media": "\033[43m", "Baja": "\033[42m"}.get(prioridad, "\033[40m")
            print(f"{color}{dia_actual:>2}*\033[0m", end=" ")


        else:
            print(f"{dia_actual:>3} ", end="")
        columna += 1
        if columna == 7:
            print()     # Salto de línea al final de la semana
            columna = 0
        dia_actual += 1
    print("\n")
    
    mostrar_tareas_del_mes(mes, año)

    # Muestra las tareas registradas en ese mes
    # print(" Tareas registradas:")
    # for tarea in tareas:
    #    a, m, d = map(int, tarea["Fecha límite"].split("-"))
    #    if a == año and m == mes:
    #        print(f" - Día {d}: {tarea['Título']}, prioridad {tarea['Prioridad']}")


def mostrar_tareas_del_mes(mes, año):
    """
    Muestra las tareas registradas en el mes y año indicados,
    coloreadas según su prioridad.
    """
    colores = {
        "Alta": "\033[41m",   # Rojo fondo
        "Media": "\033[43m",  # Amarillo fondo
        "Baja": "\033[42m"    # Verde fondo
    }

    print(" Tareas registradas:")
    for tarea in tareas:
        a, m, d = map(int, tarea["Fecha límite"].split("-"))
        if a == año and m == mes:
            prioridad = tarea["Prioridad"]
            color = colores.get(prioridad, "\033[40m")  # Fondo negro por defecto
            print(f" {color}- Día {d}: {tarea['Título']}, prioridad {prioridad}\033[0m")

# Ejemplo de uso: octubre 2025
mostrar_calendario(10, 2025)
