"""
main.py
Interfaz gráfica moderna para el Sistema de Gestión de Parqueadero.
Desarrollada con CustomTkinter y ttk.Treeview.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from modelo import Vehiculo


# Configuración estética global de CustomTkinter
ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")


class SistemaParqueaderoApp(ctk.CTk):
    """
    Ventana principal de la aplicación de gestión de parqueadero.
    """

    def __init__(self):
        super().__init__()

        # Configuración de ventana
        self.title("Sistema de Gestión de Parqueadero")
        self.geometry("1050, 650")
        self.minsize(900, 580)

        # Base de datos en memoria (Lista de instancias de Vehiculo)
        self.vehiculos: list[Vehiculo] = []

        # Estructura principal
        self._configurar_estilos_treeview()
        self._crear_interfaz()

        # Cargar datos iniciales de prueba para demostración (opcional pero muy útil)
        self._cargar_datos_demo()
        self.actualizar_tabla()

    def _configurar_estilos_treeview(self):
        """Configura el estilo ttk para armonizar con la paleta oscura de CustomTkinter."""
        style = ttk.Style()
        style.theme_use("clam")

        # Configuración del cuerpo de la tabla
        style.configure(
            "Parqueadero.Treeview",
            background="#242424",
            foreground="#EAEAEA",
            rowheight=32,
            fieldbackground="#242424",
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.map(
            "Parqueadero.Treeview",
            background=[("selected", "#1F6AA5")],
            foreground=[("selected", "#FFFFFF")],
        )

        # Configuración del encabezado
        style.configure(
            "Parqueadero.Treeview.Heading",
            background="#181818",
            foreground="#3B8ED0",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 8),
        )
        style.map(
            "Parqueadero.Treeview.Heading",
            background=[("active", "#202020")],
            foreground=[("active", "#60A5FA")],
        )

    def _crear_interfaz(self):
        """Construye todos los elementos de la interfaz de usuario."""
        # Contenedor superior (Header)
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#181818", height=70)
        header_frame.pack(fill="x", side="top")

        titulo = ctk.CTkLabel(
            header_frame,
            text="🚗 SISTEMA DE GESTIÓN DE PARQUEADERO",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#3B8ED0",
        )
        titulo.pack(side="left", padx=25, pady=18)

        subtitulo = ctk.CTkLabel(
            header_frame,
            text="Control de Ingresos y Salidas en Tiempo Real",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF",
        )
        subtitulo.pack(side="left", padx=5, pady=20)

        # Contenedor principal (dos columnas: Izquierda Formulario, Derecha Tabla)
        cuerpo_frame = ctk.CTkFrame(self, fg_color="transparent")
        cuerpo_frame.pack(fill="both", expand=True, padx=20, pady=15)
        cuerpo_frame.grid_columnconfigure(0, weight=0)  # Panel izquierdo fijo/flexible
        cuerpo_frame.grid_columnconfigure(1, weight=1)  # Panel derecho expandible
        cuerpo_frame.grid_rowconfigure(0, weight=1)

        # ------------------- PANEL IZQUIERDO: FORMULARIO Y ACCIONES -------------------
        form_card = ctk.CTkFrame(cuerpo_frame, width=340, corner_radius=12)
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        form_card.grid_propagate(False)

        # Título del formulario
        form_title = ctk.CTkLabel(
            form_card,
            text="Registrar Vehículo",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
        )
        form_title.pack(anchor="w", padx=20, pady=(20, 15))

        # Campo: Placa
        lbl_placa = ctk.CTkLabel(form_card, text="Placa del Vehículo *", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_placa.pack(anchor="w", padx=20, pady=(5, 2))
        self.entry_placa = ctk.CTkEntry(
            form_card,
            placeholder_text="Ej: ABC-123 o XYZ789",
            height=35,
            font=ctk.CTkFont(size=13),
        )
        self.entry_placa.pack(fill="x", padx=20, pady=(0, 10))

        # Campo: Propietario
        lbl_propietario = ctk.CTkLabel(form_card, text="Nombre del Propietario *", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_propietario.pack(anchor="w", padx=20, pady=(5, 2))
        self.entry_propietario = ctk.CTkEntry(
            form_card,
            placeholder_text="Ej: Carlos Mendoza",
            height=35,
            font=ctk.CTkFont(size=13),
        )
        self.entry_propietario.pack(fill="x", padx=20, pady=(0, 10))

        # Campo: Tipo de Vehículo (ComboBox)
        lbl_tipo = ctk.CTkLabel(form_card, text="Tipo de Vehículo *", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_tipo.pack(anchor="w", padx=20, pady=(5, 2))
        self.combo_tipo = ctk.CTkComboBox(
            form_card,
            values=["Automóvil", "Motocicleta", "Camioneta"],
            height=35,
            state="readonly",
            font=ctk.CTkFont(size=13),
        )
        self.combo_tipo.set("Automóvil")
        self.combo_tipo.pack(fill="x", padx=20, pady=(0, 20))

        # Botón Registrar
        btn_registrar = ctk.CTkButton(
            form_card,
            text="➕ Registrar Ingreso",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10B981",
            hover_color="#059669",
            height=40,
            command=self.registrar_vehiculo,
        )
        btn_registrar.pack(fill="x", padx=20, pady=(0, 10))

        # Botón Limpiar Campos
        btn_limpiar = ctk.CTkButton(
            form_card,
            text="🧹 Limpiar Formulario",
            font=ctk.CTkFont(size=12),
            fg_color="#374151",
            hover_color="#4B5563",
            height=32,
            command=self.limpiar_formulario,
        )
        btn_limpiar.pack(fill="x", padx=20, pady=(0, 15))

        # Separador decorativo
        separador = ctk.CTkFrame(form_card, height=2, fg_color="#333333")
        separador.pack(fill="x", padx=20, pady=(5, 15))

        # Sección de Salida / Eliminación
        lbl_acciones = ctk.CTkLabel(
            form_card,
            text="Gestión de Salida",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#EF4444",
        )
        lbl_acciones.pack(anchor="w", padx=20, pady=(0, 5))

        lbl_desc_salida = ctk.CTkLabel(
            form_card,
            text="Selecciona un registro en la tabla y presiona el botón para dar salida.",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF",
            wraplength=290,
            justify="left",
        )
        lbl_desc_salida.pack(anchor="w", padx=20, pady=(0, 10))

        btn_dar_salida = ctk.CTkButton(
            form_card,
            text="🚪 Dar Salida (Eliminar)",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            height=38,
            command=self.dar_salida_vehiculo,
        )
        btn_dar_salida.pack(fill="x", padx=20, pady=(0, 15))

        # Tarjeta de resumen de ocupación
        self.lbl_resumen = ctk.CTkLabel(
            form_card,
            text="Total: 0 | Autos: 0 | Motos: 0 | Camionetas: 0",
            font=ctk.CTkFont(size=11),
            text_color="#93C5FD",
        )
        self.lbl_resumen.pack(side="bottom", pady=15)

        # ------------------- PANEL DERECHO: TABLA (TREEVIEW) -------------------
        tabla_card = ctk.CTkFrame(cuerpo_frame, corner_radius=12)
        tabla_card.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        tabla_card.grid_columnconfigure(0, weight=1)
        tabla_card.grid_rowconfigure(1, weight=1)

        # Encabezado del panel de tabla (con buscador)
        tabla_header = ctk.CTkFrame(tabla_card, fg_color="transparent")
        tabla_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))
        tabla_header.grid_columnconfigure(0, weight=1)

        lbl_titulo_tabla = ctk.CTkLabel(
            tabla_header,
            text="Vehículos Estacionados",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
        )
        lbl_titulo_tabla.grid(row=0, column=0, sticky="w")

        # Campo de búsqueda en vivo
        self.entry_buscar = ctk.CTkEntry(
            tabla_header,
            placeholder_text="🔍 Buscar por placa o propietario...",
            width=260,
            height=32,
        )
        self.entry_buscar.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.entry_buscar.bind("<KeyRelease>", lambda event: self.actualizar_tabla())

        # Contenedor del Treeview con Scrollbar
        tree_container = ctk.CTkFrame(tabla_card, fg_color="#242424", corner_radius=8)
        tree_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)

        # Definición de Columnas
        columnas = ("placa", "tipo", "propietario", "hora")
        self.tree = ttk.Treeview(
            tree_container,
            columns=columnas,
            show="headings",
            style="Parqueadero.Treeview",
            selectmode="browse",
        )

        self.tree.heading("placa", text="Placa")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("propietario", text="Propietario")
        self.tree.heading("hora", text="Hora de Ingreso")

        self.tree.column("placa", width=110, anchor="center")
        self.tree.column("tipo", width=120, anchor="center")
        self.tree.column("propietario", width=220, anchor="w")
        self.tree.column("hora", width=180, anchor="center")

        # Scrollbar vertical moderno
        scrollbar = ctk.CTkScrollbar(tree_container, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=5)

        # Evento de doble clic para dar salida rápida
        self.tree.bind("<Double-1>", lambda event: self.dar_salida_vehiculo())

    def _cargar_datos_demo(self):
        """Carga un par de registros iniciales para verificar la visualización."""
        self.vehiculos.append(Vehiculo("ABC-123", "Automóvil", "María Gómez", "2026-10-15 08:30:15"))
        self.vehiculos.append(Vehiculo("XYZ-789", "Motocicleta", "Juan Pérez", "2026-10-15 09:15:42"))
        self.vehiculos.append(Vehiculo("KTM-456", "Camioneta", "Andrea Rojas", "2026-10-15 10:05:00"))

    # ------------------- OPERACIONES CRUD EN MEMORIA -------------------

    def registrar_vehiculo(self):
        """
        CREAR: Valida los campos ingresados y agrega un nuevo Vehículo a la lista en memoria.
        La hora de ingreso se captura de forma automática en el constructor de Vehiculo.
        """
        placa = self.entry_placa.get().strip().upper()
        propietario = self.entry_propietario.get().strip()
        tipo = self.combo_tipo.get().strip()

        # Validación 1: Campos vacíos
        if not placa or not propietario or not tipo:
            messagebox.showwarning(
                "Campos requeridos",
                "Por favor complete todos los campos obligatorios (Placa, Propietario y Tipo).",
            )
            return

        # Validación 2: Placa duplicada (un vehículo con la misma placa ya está dentro)
        if any(v.placa == placa for v in self.vehiculos):
            messagebox.showerror(
                "Vehículo ya registrado",
                f"El vehículo con placa '{placa}' ya se encuentra registrado en el parqueadero.",
            )
            return

        # Creación del objeto Vehiculo (la hora actual se asigna automáticamente)
        nuevo_vehiculo = Vehiculo(placa=placa, tipo_vehiculo=tipo, propietario=propietario)
        self.vehiculos.append(nuevo_vehiculo)

        # Actualización de interfaz
        self.actualizar_tabla()
        self.limpiar_formulario()

        messagebox.showinfo(
            "Registro Exitoso",
            f"Vehículo {nuevo_vehiculo.placa} ({nuevo_vehiculo.tipo_vehiculo}) ingresado exitosamente a las {nuevo_vehiculo.hora_ingreso}.",
        )

    def actualizar_tabla(self):
        """
        LEER: Limpia y repuebla el Treeview con los datos actuales de la lista en memoria.
        Soporta filtrado mediante el cuadro de búsqueda.
        """
        # Limpiar filas existentes en la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtro = self.entry_buscar.get().strip().lower()

        total = 0
        autos = 0
        motos = 0
        camionetas = 0

        for v in self.vehiculos:
            total += 1
            if v.tipo_vehiculo == "Automóvil":
                autos += 1
            elif v.tipo_vehiculo == "Motocicleta":
                motos += 1
            elif v.tipo_vehiculo == "Camioneta":
                camionetas += 1

            # Filtrar si hay texto en el buscador
            if filtro:
                coincide = (
                    filtro in v.placa.lower()
                    or filtro in v.propietario.lower()
                    or filtro in v.tipo_vehiculo.lower()
                )
                if not coincide:
                    continue

            # Insertar fila en el Treeview
            self.tree.insert(
                "",
                "end",
                values=(v.placa, v.tipo_vehiculo, v.propietario, v.hora_ingreso),
            )

        # Actualizar tarjeta de resumen
        self.lbl_resumen.configure(
            text=f"Total: {total} | Autos: {autos} | Motos: {motos} | Camionetas: {camionetas}"
        )

    def dar_salida_vehiculo(self):
        """
        ELIMINAR: Permite dar salida a un vehículo seleccionado en la tabla,
        eliminándolo de la lista en memoria y refrescando la vista.
        """
        seleccion = self.tree.selection()

        if not seleccion:
            # Si no hay selección en tabla, verificar si se colocó una placa en el campo de entrada
            placa_input = self.entry_placa.get().strip().upper()
            if placa_input:
                vehiculo_encontrado = next((v for v in self.vehiculos if v.placa == placa_input), None)
                if vehiculo_encontrado:
                    self._confirmar_y_eliminar(vehiculo_encontrado)
                    return

            messagebox.showwarning(
                "Selección requerida",
                "Por favor selecciona un vehículo de la tabla (o escribe su placa) para registrar la salida.",
            )
            return

        item_id = seleccion[0]
        valores = self.tree.item(item_id, "values")
        placa_seleccionada = valores[0]

        vehiculo = next((v for v in self.vehiculos if v.placa == placa_seleccionada), None)
        if vehiculo:
            self._confirmar_y_eliminar(vehiculo)

    def _confirmar_y_eliminar(self, vehiculo: Vehiculo):
        """Muestra diálogo de confirmación y elimina el vehículo de la memoria."""
        confirmacion = messagebox.askyesno(
            "Confirmar Salida",
            f"¿Desea registrar la salida del vehículo?\n\n"
            f"• Placa: {vehiculo.placa}\n"
            f"• Tipo: {vehiculo.tipo_vehiculo}\n"
            f"• Propietario: {vehiculo.propietario}\n"
            f"• Ingreso: {vehiculo.hora_ingreso}",
        )

        if confirmacion:
            self.vehiculos.remove(vehiculo)
            self.actualizar_tabla()
            messagebox.showinfo(
                "Salida Exitosa",
                f"Se ha registrado la salida del vehículo con placa '{vehiculo.placa}'.",
            )

    def limpiar_formulario(self):
        """Limpia los campos del formulario de registro."""
        self.entry_placa.delete(0, "end")
        self.entry_propietario.delete(0, "end")
        self.combo_tipo.set("Automóvil")
        self.entry_placa.focus()


if __name__ == "__main__":
    app = SistemaParqueaderoApp()
    app.mainloop()
