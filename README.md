# Proyecto-final- 

Definimos proyecto: 
1- Planificador de Tareas Educativas
2- Plataforma de destino, aplicación de escritorio. 
3- La interfaz permite: agregar, mostrar y eliminar tareas con título, fecha límite y prioridad (Alta, Media, Baja).
4- Persistencia en DB.
5-Se maneja validación básica para fechas y prioridades.
6-Se ordenan las tareas por fecha y prioridad para experiencia de manejo.
7-Uso de calendario visual, indicando la prioridad por color(rojo, amarillo y verde).



# Requerimientos del sistema — Planificador de Tareas

Sistema operativo:
Windows 10 o superior (versión de 64 bits recomendada)
Espacio en disco:
100 MB libres para instalación y archivos de datos
Memoria RAM:
4 GB mínimo (8 GB recomendados)


# 1. Instrucciones de instalación y ejecución

# Instalación Versión Portable:

1. Descargá el archivo Proyecto-final--Prog-I/planificador /dist/Planificador_de_tareas.exe
2. Copialo en una carpeta de tu elección (por ejemplo, Escritorio o Documentos).
3. Si el sistema muestra un aviso de seguridad de Windows, elegí Más información, Ejecutar de todos modos.
4. (Opcional) Si se requiere Java o Python, asegúrate de que esté instalado antes de abrir el programa.
5. Hacé doble clic en el archivo para iniciar el Planificador de Tareas.

# Instalación versión desarrollador:

Descargar o clonar el repositorio desde GitHub:
git clone https://github.com/GracielaBerio/Proyecto-final--Prog-I.git
Ingresar a la carpeta con Tkinter.
Instalar la librería tkcalendar ejecutando en la terminal:
pip install tkcalendar

# Ejecución:

Abrir una terminal en la carpeta del proyecto y ejecutar el archivo principal con el comando:
python Planificador_de_tareas.py

El programa abrirá una ventana donde el usuario puede agregar, editar y eliminar tareas, ver las fechas límite en un calendario, filtrar por prioridad (Alta, Media, Baja), exportar e importar datos en formatos CSV y JSON, y recibir notificaciones de tareas próximas a vencer.

# 2. Descripción del diseño, hitos y decisiones de desarrollo

El proyecto fue diseñado como una aplicación de escritorio educativa para gestionar tareas.
Existen dos versiones: una sin interfaz gráfica (solo consola) y otra con interfaz visual construida con Tkinter.

Hitos principales del desarrollo:

Diseño de la base de datos SQLite, con una tabla llamada “tareas” que contiene los campos id, título, descripción, fecha límite y prioridad.
Implementación de las funciones básicas de alta, baja, modificación y listado de tareas (CRUD).
Incorporación de la interfaz gráfica con Tkinter y el uso del widget Treeview para visualizar las tareas en forma de tabla.
Integración del calendario mediante tkcalendar, lo que permite seleccionar y marcar fechas de manera visual.
Inclusión de funciones para exportar e importar datos en CSV y JSON.
Agregado de un sistema de notificaciones que alerta sobre tareas próximas a vencer.

Decisiones de desarrollo:

Se eligió SQLite como base de datos por ser simple, local y no requerir instalación adicional.
Tkinter se eligió por ser parte del propio Python y permitir construir interfaces limpias y funcionales.
Se optó por mantener los nombres y textos en español para favorecer la comprensión del código en contextos educativos.
El proyecto está estructurado de forma modular, separando la lógica de la interfaz gráfica y las operaciones con la base de datos.

# 3. Justificación del uso de las librerías elegidas

tkinter: se utiliza para construir la interfaz gráfica. Es parte de la biblioteca estándar de Python, lo que evita dependencias externas y facilita el aprendizaje.

tkcalendar: se utiliza para mostrar un calendario interactivo y facilitar la selección de fechas. Mejora la experiencia del usuario al visualizar tareas por colores según la prioridad.

sqlite3: se utiliza para la base de datos local. Es confiable, rápida y no requiere instalación.

csv y json: se usan para exportar e importar datos. Permiten guardar copias de las tareas y compartir información fácilmente.

ttk (de tkinter): se usa para mejorar el diseño visual y estilizar los elementos de la interfaz.

Estas librerías fueron elegidas por su facilidad de uso, compatibilidad con distintos sistemas operativos y su valor didáctico, ya que permiten comprender distintos aspectos del desarrollo de software: interfaz, datos y persistencia.

# 4. Fundamento didáctico: aprendizajes, desafíos y reflexiones

Aprendizajes:

Durante el desarrollo del proyecto se aplicaron conocimientos de programación estructurada, manejo de bases de datos, diseño de interfaces y pensamiento computacional.
Se comprendió la importancia del diseño modular, la validación de datos y la persistencia de información en aplicaciones reales.

Desafíos enfrentados:

Los principales desafíos fueron integrar correctamente el calendario tkcalendar, sincronizar la base de datos con la interfaz gráfica, mantener la aplicación estable, y lograr un diseño claro y agradable para el usuario.
También se trabajó en las validaciones de fechas, formatos y en la implementación del sistema de notificaciones.

Reflexiones del proceso:

El proyecto permitió unir conceptos teóricos con la práctica, desarrollando una aplicación funcional y útil.
A nivel educativo, promovió el trabajo autónomo, la resolución de problemas y la planificación de tareas.
También demostró que la programación puede ser una herramienta creativa para organizar y comunicar ideas visualmente.
En síntesis, el proceso fue una experiencia formativa que integró habilidades técnicas, expresivas y organizativas, consolidando aprendizajes tanto en el área de programación como en la de comunicación visual.
