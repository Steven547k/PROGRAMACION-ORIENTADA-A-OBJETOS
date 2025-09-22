"""
Gestor de Eventos con Tkinter y tkcalendar
- Ventana principal con Treeview (Fecha, Hora, Descripción)
- DatePicker usando tkcalendar.DateEntry
- Entradas para hora (Spinbox) y descripción (Entry)
- Botones: Agregar Evento, Eliminar Evento Seleccionado, Salir
- Confirmación al eliminar
- Organización en Frames y comentarios explicativos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

# -----------------------
# Clase principal: App
# -----------------------
class EventManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Eventos")
        self.geometry("800x450")
        self.resizable(False, False)

        # Establecemos un padding general para la ventana
        self["padx"] = 10
        self["pady"] = 10

        # Datos internos (lista para almacenar eventos si se necesita)
        # Cada evento será un dict: {"fecha": "YYYY-MM-DD", "hora": "HH:MM", "desc": "texto"}
        self.events = []

        # Llamada a los métodos que construyen la interfaz
        self._create_widgets()
        self._place_widgets()
        self._configure_treeview()

    # -----------------------
    # Construcción de widgets
    # -----------------------
    def _create_widgets(self):
        # Frames para organizar la interfaz
        self.frame_tree = ttk.Frame(self, padding=(5, 5))
        self.frame_inputs = ttk.Frame(self, padding=(5, 5))
        self.frame_actions = ttk.Frame(self.frame_inputs, padding=(5, 5))

        # Treeview para mostrar eventos
        self.tree = ttk.Treeview(self.frame_tree, columns=("fecha", "hora", "desc"), show="headings", height=15)
        # Scrollbars para el Treeview
        self.tree_scroll_y = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
        self.tree_scroll_x = ttk.Scrollbar(self.frame_tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)

        # Labels para los campos de entrada
        self.lbl_fecha = ttk.Label(self.frame_inputs, text="Fecha:")
        self.lbl_hora = ttk.Label(self.frame_inputs, text="Hora (HH:MM):")
        self.lbl_desc = ttk.Label(self.frame_inputs, text="Descripción:")

        # DateEntry (DatePicker) desde tkcalendar
        self.date_entry = DateEntry(self.frame_inputs, date_pattern="yyyy-mm-dd", width=12)

        # Spinbox para horas y minutos (0-23, 0-59)
        self.spin_hora = tk.Spinbox(self.frame_inputs, from_=0, to=23, width=3, format="%02.0f")
        self.spin_min = tk.Spinbox(self.frame_inputs, from_=0, to=59, width=3, format="%02.0f")

        # Entry para la descripción (se puede ampliar a Text si se desea)
        self.entry_desc = ttk.Entry(self.frame_inputs, width=40)

        # Botones de acción
        self.btn_add = ttk.Button(self.frame_actions, text="Agregar Evento", command=self.add_event)
        self.btn_delete = ttk.Button(self.frame_actions, text="Eliminar Evento Seleccionado", command=self.delete_selected_event)
        self.btn_exit = ttk.Button(self.frame_actions, text="Salir", command=self.on_exit)

        # Etiqueta informativa de ayuda (opcional)
        self.lbl_info = ttk.Label(self.frame_inputs, text="Seleccione fecha con el calendario. Horas en 24h.", foreground="gray")

    # -----------------------
    # Colocación de widgets
    # -----------------------
    def _place_widgets(self):
        # Layout: Tree a la izquierda, inputs y botones a la derecha
        self.frame_tree.pack(side="left", fill="both", expand=True)
        self.frame_inputs.pack(side="right", fill="y")

        # Treeview + scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_scroll_y.grid(row=0, column=1, sticky="ns")
        self.tree_scroll_x.grid(row=1, column=0, sticky="ew", columnspan=2)
        # Configuramos que el frame del tree use grid para expandir correctamente
        self.frame_tree.grid_rowconfigure(0, weight=1)
        self.frame_tree.grid_columnconfigure(0, weight=1)

        # En el frame_inputs colocamos etiquetas y campos con grid
        pad_y = 6
        self.lbl_fecha.grid(row=0, column=0, sticky="w", pady=(0, pad_y))
        self.date_entry.grid(row=0, column=1, sticky="w", pady=(0, pad_y))

        self.lbl_hora.grid(row=1, column=0, sticky="w", pady=(0, pad_y))
        # Colocamos hora y minuto juntos
        self.spin_hora.grid(row=1, column=1, sticky="w")
        ttk.Label(self.frame_inputs, text=":").grid(row=1, column=1, sticky="w", padx=(35,0))  # separador visual (ajustado con padding)
        self.spin_min.grid(row=1, column=1, sticky="w", padx=(42,0))

        self.lbl_desc.grid(row=2, column=0, sticky="nw", pady=(0, pad_y))
        self.entry_desc.grid(row=2, column=1, sticky="w", pady=(0, pad_y))

        self.lbl_info.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, pad_y))

        # Frame para botones (dentro del frame_inputs)
        self.frame_actions.grid(row=4, column=0, columnspan=2, sticky="we", pady=(10,0))
        # Distribuimos botones en el frame_actions
        self.btn_add.pack(side="top", fill="x", pady=(0,6))
        self.btn_delete.pack(side="top", fill="x", pady=(0,6))
        self.btn_exit.pack(side="top", fill="x")

    # -----------------------
    # Configuración del Treeview (columnas y encabezados)
    # -----------------------
    def _configure_treeview(self):
        # Encabezados
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("desc", text="Descripción")
        # Anchos de columnas
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("hora", width=70, anchor="center")
        self.tree.column("desc", width=420, anchor="w")

        # Insertar algunos eventos de ejemplo (opcional)
        # self._insert_event_to_view({"fecha": "2025-09-01", "hora": "09:00", "desc": "Reunión inicial"})

    # -----------------------
    # Funciones auxiliares
    # -----------------------
    def _validate_time(self, hour_str, min_str):
        """Valida y formatea horario. Devuelve 'HH:MM' o None si inválido."""
        try:
            h = int(hour_str)
            m = int(min_str)
            if not (0 <= h <= 23 and 0 <= m <= 59):
                return None
            return f"{h:02d}:{m:02d}"
        except ValueError:
            return None

    def _insert_event_to_view(self, event):
        """Inserta un evento en el Treeview y lo añade a la lista interna."""
        # Usamos la combinación fecha+hora+desc como identificador visible
        item_id = self.tree.insert("", "end", values=(event["fecha"], event["hora"], event["desc"]))
        # Guardamos una referencia simple (opcional)
        self.events.append({"id": item_id, **event})

    # -----------------------
    # Acciones de los botones
    # -----------------------
    def add_event(self):
        """Acción para agregar un nuevo evento desde los campos de entrada."""
        fecha = self.date_entry.get_date().strftime("%Y-%m-%d")  # devuelve date, formateamos YYYY-MM-DD
        hora = self.spin_hora.get()
        minuto = self.spin_min.get()
        hora_formateada = self._validate_time(hora, minuto)
        descripcion = self.entry_desc.get().strip()

        # Validaciones
        if hora_formateada is None:
            messagebox.showerror("Hora inválida", "Introduce una hora válida (HH: 0-23, MM: 0-59).")
            return
        if not descripcion:
            messagebox.showerror("Descripción vacía", "La descripción no puede estar vacía.")
            return

        # Construimos el evento y lo insertamos en la vista
        evento = {"fecha": fecha, "hora": hora_formateada, "desc": descripcion}
        self._insert_event_to_view(evento)

        # Limpiar la descripción y devolver foco al campo
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.focus_set()

    def delete_selected_event(self):
        """Elimina el evento seleccionado en Treeview (con confirmación)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ningún evento seleccionado", "Seleccione un evento para eliminar.")
            return

        # Pedimos confirmación (opcional)
        respuesta = messagebox.askyesno("Confirmar eliminación", "¿Deseas eliminar el evento seleccionado?")
        if not respuesta:
            return

        # Eliminamos todos los seleccionados (soporta multi-selección)
        for item in selected:
            # Borramos del Treeview
            self.tree.delete(item)
            # Borramos de la lista interna si existe
            for e in self.events:
                if e.get("id") == item:
                    self.events.remove(e)
                    break

    def on_exit(self):
        """Acción al pulsar Salir: confirmación antes de cerrar."""
        if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
            self.destroy()

# -----------------------
# Punto de entrada
# -----------------------
if __name__ == "__main__":
    app = EventManagerApp()
    app.mainloop()
