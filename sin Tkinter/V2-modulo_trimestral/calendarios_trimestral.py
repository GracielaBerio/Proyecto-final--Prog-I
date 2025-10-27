import re

# Lista de tareas con fecha en formato AAAA-MM-DD
tareas = [
    {"Título": "Revisar propuesta", "Fecha límite": "2025-10-03", "Prioridad": "Media"},
    {"Título": "Ejercicios de grafos", "Fecha límite": "2025-10-15", "Prioridad": "Alta"},
    {"Título": "Informe institucional", "Fecha límite": "2025-10-22", "Prioridad": "Baja"},
    {"Título": "Evaluación final", "Fecha límite": "2025-11-10", "Prioridad": "Alta"},
    {"Título": "Reunión pedagógica", "Fecha límite": "2025-12-05", "Prioridad": "Media"},
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
def dia_semana_primero(mes, año):
    if mes < 3:
        mes += 12
        año -= 1
    k = año % 100
    j = año // 100
    h = (1 + 13*(mes+1)//5 + k + k//4 + j//4 + 5*j) % 7
    return (h + 5) % 7  # Ajuste para que 0 = lunes

# Extrae los días del mes que tienen tareas registradas
def dias_con_tareas(mes, año):
    dias = {}
    for tarea in tareas:
        a, m, d = map(int, tarea["Fecha límite"].split("-"))
        if a == año and m == mes:
            dias[d] = tarea["Prioridad"]
    return dias

# Mide el ancho visible de una línea (sin códigos ANSI)
def ancho_visible(texto):
    return len(re.sub(r'\033\[[0-9;]*m', '', texto))

# Muestra las tareas registradas en el mes y año indicados, con colores
def mostrar_tareas_del_mes(mes, año):
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
            color = colores.get(prioridad, "\033[40m")
            print(f" {color}- Día {d}: {tarea['Título']}, prioridad {prioridad}\033[0m")

# Construye un calendario mensual como lista de líneas con recuadro
def construir_calendario_en_lineas(mes, año, nombre_meses, dias_semana, colores):
    primer_dia = dia_semana_primero(mes, año)
    total_dias = dias_del_mes(mes, año)
    marcados = dias_con_tareas(mes, año)

    encabezado = f"{nombre_meses[mes-1]} {año}".center(20)
    lineas = [encabezado, " ".join(dias_semana)]
    dia_actual = 1
    columna = primer_dia
    fila = "    " * columna

    while dia_actual <= total_dias:
        while columna < 7 and dia_actual <= total_dias:
            if dia_actual in marcados:
                prioridad = marcados[dia_actual]
                color = colores.get(prioridad, "\033[40m")
                fila += f"{color}{dia_actual:>2}*\033[0m "
            else:
                fila += f"{dia_actual:>3} "
            dia_actual += 1
            columna += 1
        lineas.append(fila.rstrip())
        fila = ""
        columna = 0

    ancho = max(ancho_visible(l) for l in lineas)
    borde_sup = f"╔{'═' * ancho}╗"
    borde_inf = f"╚{'═' * ancho}╝"
    cuerpo = [f"║{l.ljust(ancho)}║" for l in lineas]
    return [borde_sup] + cuerpo + [borde_inf]

# Muestra tres calendarios mensuales en paralelo con recuadro
def mostrar_calendarios_trimestre(mes_inicial, año):
    nombre_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    colores = {"Alta": "\033[41m", "Media": "\033[43m", "Baja": "\033[42m"}

    calendarios = []
    for i in range(3):
        mes = (mes_inicial + i - 1) % 12 + 1
        año_actual = año + ((mes_inicial + i - 1) // 12)
        calendario = construir_calendario_en_lineas(mes, año_actual, nombre_meses, dias_semana, colores)
        calendarios.append(calendario)

    # Unir las líneas horizontalmente
    for filas in zip(*calendarios):
        print("   ".join(filas))

    # Mostrar tareas por mes
    for i in range(3):
        mes = (mes_inicial + i - 1) % 12 + 1
        año_actual = año + ((mes_inicial + i - 1) // 12)
        print(f"\n Tareas en {nombre_meses[mes-1]} {año_actual}:")
        mostrar_tareas_del_mes(mes, año_actual)

# Ejemplo de uso
mostrar_calendarios_trimestre(10, 2025)

