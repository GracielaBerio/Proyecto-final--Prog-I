import re

def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

def dias_del_mes(mes, año):
    if mes == 2:
        return 29 if es_bisiesto(año) else 28
    elif mes in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def dia_semana_primero(mes, año):
    if mes < 3:
        mes += 12
        año -= 1
    k = año % 100
    j = año // 100
    h = (1 + 13*(mes+1)//5 + k + k//4 + j//4 + 5*j) % 7
    return (h + 5) % 7

def dias_con_tareas(mes, año, tareas):
    dias = {}
    for tarea in tareas:
        a, m, d = map(int, tarea["Fecha límite"].split("-"))
        if a == año and m == mes:
            dias[d] = tarea["Prioridad"]
    return dias

def mostrar_tareas_del_mes(mes, año, tareas):
    colores = {
        "Alta": "\033[41m",
        "Media": "\033[43m",
        "Baja": "\033[42m"
    }
    print(" Tareas registradas:")
    for tarea in tareas:
        a, m, d = map(int, tarea["Fecha límite"].split("-"))
        if a == año and m == mes:
            prioridad = tarea["Prioridad"]
            color = colores.get(prioridad, "\033[40m")
            print(f" {color}- Día {d}: {tarea['Título']}, prioridad {prioridad}\033[0m")

def ancho_visible(texto):
    return len(re.sub(r'\033\[[0-9;]*m', '', texto))

def construir_calendario_en_lineas(mes, año, nombre_meses, dias_semana, colores, tareas):
    primer_dia = dia_semana_primero(mes, año)
    total_dias = dias_del_mes(mes, año)
    marcados = dias_con_tareas(mes, año, tareas)

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

    #  Forzar que haya 8 líneas de contenido
    while len(lineas) < 8:
        lineas.append("")

    ancho = max(ancho_visible(linea) for linea in lineas)
    cuerpo = [f"║{linea}{' ' * (ancho - ancho_visible(linea))}║" for linea in lineas]
    borde_sup = f"╔{'═' * ancho}╗"
    borde_inf = f"╚{'═' * ancho}╝"
    return [borde_sup] + cuerpo + [borde_inf]

def mostrar_calendarios_trimestre(mes_inicial, año, tareas):
    nombre_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    colores = {"Alta": "\033[41m", "Media": "\033[43m", "Baja": "\033[42m"}

    calendarios = []
    for i in range(3):
        mes = (mes_inicial + i - 1) % 12 + 1
        año_actual = año + ((mes_inicial + i - 1) // 12)
        calendario = construir_calendario_en_lineas(mes, año_actual, nombre_meses, dias_semana, colores, tareas)
        calendarios.append(calendario)

    for filas in zip(*calendarios):
        print("   ".join(filas))

    for i in range(3):
        mes = (mes_inicial + i - 1) % 12 + 1
        año_actual = año + ((mes_inicial + i - 1) // 12)
        # print(f"\n Tareas en {nombre_meses[mes-1]} {año_actual}:")
        mostrar_tareas_del_mes(mes, año_actual, tareas)