'''
Planificador de tareas - versión 10
Interfaz completa (basada en v5), textos y columnas en español.
Requisitos: tkcalendar (opcional). Instalar: pip install tkcalendar
Base de datos: tareas.db con columnas:
    id, titulo, descripcion, fecha_limite, prioridad
'''
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import platform

# Intentar importar DateEntry y Calendar desde tkcalendar (opcional)
try:
    from tkcalendar import DateEntry, Calendar
except ImportError:
    DateEntry = None
    Calendar = None

DB_NOMBRE = 'tareas.db'

# ------------------- FUNCIONES DE BD -------------------
def iniciar_bd():
    conn = sqlite3.connect(DB_NOMBRE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tareas (
                 id INTEGER PRIMARY KEY,
                 titulo TEXT NOT NULL,
                 descripcion TEXT,
                 fecha_limite TEXT,
                 prioridad TEXT)""")
    conn.commit()
    conn.close()

def obtener_tareas(busqueda="", filtro_prioridad=None, orden="fecha_limite"):
    conn = sqlite3.connect(DB_NOMBRE)
    c = conn.cursor()
    columnas_validas = ["id", "titulo", "descripcion", "fecha_limite", "prioridad"]
    if orden not in columnas_validas:
        orden = "fecha_limite"
    query = "SELECT * FROM tareas WHERE 1=1"
    params = []
    if busqueda:
        query += " AND (titulo LIKE ? OR descripcion LIKE ?)"
        params.extend([f"%{busqueda}%", f"%{busqueda}%"])
    if filtro_prioridad:
        query += " AND prioridad=?"
        params.append(filtro_prioridad)
    query += f" ORDER BY {orden}"
    c.execute(query, params)
    tareas = c.fetchall()
    conn.close()
    return tareas

def agregar_tarea(titulo, descripcion, fecha_limite, prioridad):
    conn = sqlite3.connect(DB_NOMBRE)
    c = conn.cursor()
    c.execute("INSERT INTO tareas (titulo, descripcion, fecha_limite, prioridad) VALUES (?, ?, ?, ?)",
              (titulo, descripcion, fecha_limite, prioridad))
    conn.commit()
    conn.close()

def actualizar_tarea(id_tarea, titulo, descripcion, fecha_limite, prioridad):
    conn = sqlite3.connect(DB_NOMBRE)
    c = conn.cursor()
    c.execute('UPDATE tareas SET titulo=?, descripcion=?, fecha_limite=?, prioridad=? WHERE id=?',
              (titulo, descripcion, fecha_limite, prioridad, id_tarea))
    conn.commit()
    conn.close()

def eliminar_tarea(id_tarea):
    conn = sqlite3.connect(DB_NOMBRE)
    c = conn.cursor()
    c.execute("DELETE FROM tareas WHERE id=?", (id_tarea,))
    conn.commit()
    conn.close()

# ------------------- UTILIDADES -------------------
def parsear_fecha_segura(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None

def mostrar_globo(root, mensaje, duracion=4000):
    try:
        win = tk.Toplevel(root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        root.update_idletasks()
        rx = root.winfo_rootx()
        ry = root.winfo_rooty()
        rw = root.winfo_width()
        rh = root.winfo_height()
        x = rx + rw - 260
        y = ry + rh - 110
        win.geometry(f"240x80+{x}+{y}")
        frame = ttk.Frame(win, borderwidth=1, relief="solid", padding=8)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text="Notificación", font=("Segoe UI", 9, "bold")).pack(anchor='w')
        ttk.Label(frame, text=mensaje, wraplength=220).pack(anchor='w', pady=(4,0))
        if platform.system() == "Windows":
            try:
                win.attributes("-alpha", 0.98)
            except Exception:
                pass
        win.after(duracion, win.destroy)
    except Exception:
        messagebox.showinfo("Notificación", mensaje)

# ------------------- CLASE PRINCIPAL (INTERFAZ) -------------------
class AplicacionTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador de Tareas")
        self.var_busqueda = tk.StringVar()
        self.var_prioridad = tk.StringVar(value="")
        self._orden_actual = "fecha_limite"
        self._orden_inverso = False
        self.crear_estilo()
        self.crear_widgets()
        iniciar_bd()
        self.refrescar_tareas()
        self.verificar_proximas()

    def crear_estilo(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure("Treeview", rowheight=26, font=('Segoe UI', 10))
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))
        style.map("TButton",
                  foreground=[('active', '!disabled', 'black')],
                  background=[('active', '!disabled', '#e6e6e6')])
        style.configure("Alta.Treeview", background="#ffebeb")

    def crear_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=8)

        cal_frame = ttk.Frame(main_frame)
        cal_frame.pack(side='left', fill='y', padx=(0,8))

        if Calendar:
            try:
                self.calendario = Calendar(cal_frame, date_pattern='yyyy-mm-dd', selectmode='day', locale='es_ES', firstweekday='monday')
            except Exception:
                self.calendario = Calendar(cal_frame, date_pattern='yyyy-mm-dd', selectmode='day')
            self.calendario.pack(padx=4, pady=4)
            from datetime import datetime as _dt
            self.calendario.selection_set(_dt.now().date())
            self.calendario.bind("<<CalendarSelected>>", self.al_seleccionar_fecha)
        else:
            lbl = ttk.Label(cal_frame, text="tkcalendar no está instalado.\nInstala: pip install tkcalendar")
            lbl.pack(padx=8, pady=8)
            self.calendario = None

        cbtn_frame = ttk.Frame(cal_frame)
        cbtn_frame.pack(pady=(6,0), padx=4)
        ttk.Button(cbtn_frame, text="Mostrar todas", command=self.mostrar_todas).pack(side='left', padx=4)
        ttk.Button(cbtn_frame, text="Actualizar calendario", command=self.marcar_tareas_en_calendario).pack(side='left', padx=4)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='left', fill='both', expand=True)

        top_frame = ttk.Frame(right_frame)
        top_frame.pack(fill='x')

        ttk.Label(top_frame, text="Buscar:").pack(side='left')
        entrada_busqueda = ttk.Entry(top_frame, textvariable=self.var_busqueda, width=30)
        entrada_busqueda.pack(side='left', padx=6)
        entrada_busqueda.bind("<KeyRelease>", lambda e: self.refrescar_tareas())

        ttk.Label(top_frame, text="Prioridad:").pack(side='left', padx=(8,0))
        combo_prioridad = ttk.Combobox(top_frame, values=["", "Alta", "Media", "Baja"], textvariable=self.var_prioridad, width=8, state="readonly")
        combo_prioridad.pack(side='left', padx=(6,0))
        combo_prioridad.bind("<<ComboboxSelected>>", lambda e: self.refrescar_tareas())

        cols = ("ID", "Titulo", "Descripcion", "FechaLimite", "Prioridad")
        self.tree = ttk.Treeview(right_frame, columns=cols, show='headings', selectmode='browse')
        self.tree.heading("ID", text="ID", command=lambda: self.al_hacer_click_encabezado("id"))
        self.tree.heading("Titulo", text="Título", command=lambda: self.al_hacer_click_encabezado("titulo"))
        self.tree.heading("Descripcion", text="Descripción", command=lambda: self.al_hacer_click_encabezado("descripcion"))
        self.tree.heading("FechaLimite", text="Fecha límite", command=lambda: self.al_hacer_click_encabezado("fecha_limite"))
        self.tree.heading("Prioridad", text="Prioridad", command=lambda: self.al_hacer_click_encabezado("prioridad"))

        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Titulo", width=220, anchor='w')
        self.tree.column("Descripcion", width=320, anchor='w')
        self.tree.column("FechaLimite", width=110, anchor='center')
        self.tree.column("Prioridad", width=90, anchor='center')

        self.tree.tag_configure("Alta", background="#ffebeb")
        self.tree.tag_configure("Media", background="#fff7e6")
        self.tree.tag_configure("Baja", background="#ecffec")

        self.tree.pack(fill='both', expand=True, padx=(0,0), pady=8)

        btns = ttk.Frame(right_frame)
        btns.pack(fill='x', pady=(0,6))

        ttk.Button(btns, text="Agregar", command=self.dialogo_agregar).pack(side='left', padx=4)
        ttk.Button(btns, text="Editar", command=self.dialogo_editar).pack(side='left', padx=4)
        ttk.Button(btns, text="Eliminar", command=self.eliminar_seleccionado).pack(side='left', padx=4)
        ttk.Button(btns, text="Salir", command=self.root.destroy).pack(side='right', padx=4)

    def al_hacer_click_encabezado(self, columna):
        if self._orden_actual == columna:
            self._orden_inverso = not self._orden_inverso
        else:
            self._orden_actual = columna
            self._orden_inverso = False
        self.refrescar_tareas()

    def refrescar_tareas(self, fecha_filtro=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        busqueda = self.var_busqueda.get().strip()
        prio = self.var_prioridad.get() if self.var_prioridad.get() else None
        tareas = obtener_tareas(busqueda=busqueda, filtro_prioridad=prio, orden=self._orden_actual)
        if self._orden_inverso:
            tareas = list(reversed(tareas))

        for t in tareas:
            if fecha_filtro:
                if (t[3] or "") != fecha_filtro:
                    continue
            tag = t[4] if t[4] in ("Alta", "Media", "Baja") else ""
            self.tree.insert("", "end", iid=t[0], values=t, tags=(tag,))

        self.marcar_tareas_en_calendario()

    def dialogo_agregar(self):
        DialogoAgregarEditar(self, self.refrescar_tareas)

    def dialogo_editar(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona una tarea para editar")
            return
        tarea = next((t for t in obtener_tareas() if str(t[0]) == str(seleccionado)), None)
        if tarea:
            DialogoAgregarEditar(self, self.refrescar_tareas, id_tarea=seleccionado, datos_tarea=tarea)

    def eliminar_seleccionado(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona una tarea para eliminar")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar la tarea seleccionada?"):
            eliminar_tarea(seleccionado)
            self.refrescar_tareas()

    def verificar_proximas(self):
        ahora = datetime.now()
        proximas = []
        for t in obtener_tareas():
            fecha = parsear_fecha_segura(t[3])
            if fecha:
                dias = (fecha - ahora).days
                if 0 <= dias <= 3:
                    proximas.append((t, dias))
        if proximas:
            lines = [f"{task[0][1]} - {task[0][3]} (en {days} días)" for task, days in [(ut, dl) for (ut, dl) in proximas]]
            msg = "\n".join(lines)
            mostrar_globo(self.root, f"Tienes tareas próximas:\n{msg}", duracion=6000)
        self.root.after(3600000, self.verificar_proximas)

    # ------------------ CALENDARIO ------------------
    def marcar_tareas_en_calendario(self):
        if not self.calendario:
            return
        try:
            self.calendario.calevent_remove('all')
        except Exception:
            pass

        colores = {
            "Alta": "#ff4d4d",
            "Media": "#ffe066",
            "Baja": "#66ff99"
        }

        for t in obtener_tareas():
            fecha = t[3]
            pr = t[4]
            if fecha and pr in colores:
                try:
                    dt = datetime.strptime(fecha, "%Y-%m-%d")
                    self.calendario.calevent_create(dt, t[1], pr)
                except Exception:
                    continue

        for pr, col in colores.items():
            try:
                self.calendario.tag_config(pr, background=col, foreground="black")
            except Exception:
                pass

    def al_seleccionar_fecha(self, event):
        if not self.calendario:
            return
        fecha_sel = self.calendario.get_date()
        self.refrescar_tareas(fecha_filtro=fecha_sel)

    def mostrar_todas(self):
        self.refrescar_tareas(fecha_filtro=None)

# ------------------- DIALOGO AGREGAR / EDITAR -------------------
class DialogoAgregarEditar:
    def __init__(self, app, callback_refrescar, id_tarea=None, datos_tarea=None):
        self.app = app
        self.id_tarea = id_tarea
        self.callback_refrescar = callback_refrescar
        self.ventana = tk.Toplevel()
        self.ventana.title("Editar Tarea" if id_tarea else "Agregar Tarea")
        self.ventana.grab_set()
        self.ventana.resizable(False, False)

        ttk.Label(self.ventana, text="Título:").grid(row=0, column=0, padx=8, pady=6, sticky='e')
        self.entrada_titulo = ttk.Entry(self.ventana, width=42)
        self.entrada_titulo.grid(row=0, column=1, padx=8, pady=6, sticky='w')

        ttk.Label(self.ventana, text="Descripción:").grid(row=1, column=0, padx=8, pady=6, sticky='e')
        self.entrada_desc = ttk.Entry(self.ventana, width=42)
        self.entrada_desc.grid(row=1, column=1, padx=8, pady=6, sticky='w')

        ttk.Label(self.ventana, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, padx=8, pady=6, sticky='e')
        if DateEntry:
            self.entrada_fecha = DateEntry(self.ventana, date_pattern='yyyy-mm-dd', width=18)
            self.entrada_fecha.grid(row=2, column=1, padx=8, pady=6, sticky='w')
        else:
            self.entrada_fecha = ttk.Entry(self.ventana, width=20)
            self.entrada_fecha.grid(row=2, column=1, padx=8, pady=6, sticky='w')

        ttk.Label(self.ventana, text="Prioridad:").grid(row=3, column=0, padx=8, pady=6, sticky='e')
        self.var_prior = tk.StringVar()
        self.combo_prior = ttk.Combobox(self.ventana, textvariable=self.var_prior, values=["Alta", "Media", "Baja"], state="readonly", width=16)
        self.combo_prior.grid(row=3, column=1, padx=8, pady=6, sticky='w')

        btn_frame = ttk.Frame(self.ventana)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(8,10))

        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side='left', padx=6)
        ttk.Button(btn_frame, text="Cancelar", command=self.ventana.destroy).pack(side='left', padx=6)

        if datos_tarea:
            self.entrada_titulo.insert(0, datos_tarea[1])
            self.entrada_desc.insert(0, datos_tarea[2] or "")
            if DateEntry:
                try:
                    self.entrada_fecha.set_date(datos_tarea[3])
                except Exception:
                    self.entrada_fecha.delete(0, 'end')
                    self.entrada_fecha.insert(0, datos_tarea[3] or "")
            else:
                self.entrada_fecha.insert(0, datos_tarea[3] or "")
            self.var_prior.set(datos_tarea[4] or "")

    def guardar(self):
        titulo = self.entrada_titulo.get().strip()
        descripcion = self.entrada_desc.get().strip()
        if DateEntry:
            try:
                fecha_lim = self.entrada_fecha.get_date().strftime("%Y-%m-%d")
            except Exception:
                fecha_lim = self.entrada_fecha.get().strip()
        else:
            fecha_lim = self.entrada_fecha.get().strip()

        prioridad = self.var_prior.get().strip()

        if not titulo:
            messagebox.showerror("Error", "El título es obligatorio")
            return
        if fecha_lim:
            try:
                datetime.strptime(fecha_lim, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida, usa YYYY-MM-DD")
                return
        if prioridad not in ("Alta", "Media", "Baja"):
            messagebox.showerror("Error", "Prioridad inválida")
            return

        if self.id_tarea:
            actualizar_tarea(self.id_tarea, titulo, descripcion, fecha_lim, prioridad)
        else:
            agregar_tarea(titulo, descripcion, fecha_lim, prioridad)

        # refrescar lista y calendario
        self.app.refrescar_tareas()
        self.ventana.destroy()

# ------------------- EJECUTAR APLICACIÓN -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTareas(root)
    root.geometry("1000x620")
    root.mainloop()
