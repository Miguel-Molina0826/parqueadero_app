"""
main.py
Interfaz gráfica moderna para el Sistema de Gestión de Parqueadero.
Desarrollada con CustomTkinter, ttk.Treeview y cálculo de cobro por tiempo.
"""

from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from modelo import Vehiculo, TARIFAS_POR_DEFECTO

# Intentar importar CTkMessagebox con respaldo a tkinter.messagebox
try:
    from CTkMessagebox import CTkMessagebox
except ImportError:
    CTkMessagebox = None


# Configuración estética global de CustomTkinter
ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")


class SistemaParqueaderoApp(ctk.CTk):
    """
    Ventana principal de la aplicación de gestión de parqueadero y cobro por tiempo.
    """

    def __init__(self):
        super().__init__()

        # Configuración de ventana
        self.title("Sistema de Gestión de Parqueadero y Cobro")
        self.geometry("1100, 680")
        self.minsize(950, 600)

        # Base de datos en memoria y acumulador de recaudos en la sesión
        self.vehiculos: list[Vehiculo] = []
        self.total_recaudado: float = 0.0

        # Estructura principal
        self._configurar_estilos_treeview()
        self._crear_interfaz()

        # Cargar datos iniciales de prueba para demostración inmediata
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
            text="🚗 SISTEMA DE GESTIÓN Y COBRO DE PARQUEADERO",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#3B8ED0",
        )
        titulo.pack(side="left", padx=25, pady=18)

        subtitulo = ctk.CTkLabel(
            header_frame,
            text="Liquidación por Hora o Fracción en Tiempo Real",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#9CA3AF",
        )
        subtitulo.pack(side="left", padx=5, pady=20)

        # Contenedor principal (dos columnas: Izquierda Formulario y Cobro, Derecha Tabla)
        cuerpo_frame = ctk.CTkFrame(self, fg_color="transparent")
        cuerpo_frame.pack(fill="both", expand=True, padx=20, pady=15)
        cuerpo_frame.grid_columnconfigure(0, weight=0)  # Panel izquierdo
        cuerpo_frame.grid_columnconfigure(1, weight=1)  # Panel derecho expandible
        cuerpo_frame.grid_rowconfigure(0, weight=1)

        # ------------------- PANEL IZQUIERDO: FORMULARIO Y ACCIONES -------------------
        form_card = ctk.CTkFrame(cuerpo_frame, width=350, corner_radius=12)
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        form_card.grid_propagate(False)

        # Título del formulario
        form_title = ctk.CTkLabel(
            form_card,
            text="Registrar Ingreso",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        )
        form_title.pack(anchor="w", padx=20, pady=(15, 10))

        # Campo: Placa
        lbl_placa = ctk.CTkLabel(form_card, text="Placa del Vehículo *", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_placa.pack(anchor="w", padx=20, pady=(2, 2))
        self.entry_placa = ctk.CTkEntry(
            form_card,
            placeholder_text="Ej: ABC-123 o XYZ789",
            height=32,
            font=ctk.CTkFont(size=13),
        )
        self.entry_placa.pack(fill="x", padx=20, pady=(0, 8))

        # Campo: Propietario
        lbl_propietario = ctk.CTkLabel(form_card, text="Nombre del Propietario *", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_propietario.pack(anchor="w", padx=20, pady=(2, 2))
        self.entry_propietario = ctk.CTkEntry(
            form_card,
            placeholder_text="Ej: Carlos Mendoza",
            height=32,
            font=ctk.CTkFont(size=13),
        )
        self.entry_propietario.pack(fill="x", padx=20, pady=(0, 8))

        # Fila de Tipo de Vehículo y Tarifa Horaria Configurable
        lbl_tipo = ctk.CTkLabel(form_card, text="Tipo de Vehículo *", font=ctk.CTkFont(size=12, weight="bold"))
        lbl_tipo.pack(anchor="w", padx=20, pady=(2, 2))
        self.combo_tipo = ctk.CTkComboBox(
            form_card,
            values=["Automóvil", "Motocicleta", "Camioneta"],
            height=32,
            state="readonly",
            font=ctk.CTkFont(size=13),
            command=self._al_cambiar_tipo_vehiculo,
        )
        self.combo_tipo.set("Automóvil")
        self.combo_tipo.pack(fill="x", padx=20, pady=(0, 8))

        # Campo: Tarifa por Hora (Configurable)
        lbl_tarifa = ctk.CTkLabel(
            form_card,
            text="Tarifa por Hora o Fracción ($ COP) *",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        lbl_tarifa.pack(anchor="w", padx=20, pady=(2, 2))
        self.entry_tarifa = ctk.CTkEntry(
            form_card,
            placeholder_text="2000",
            height=32,
            font=ctk.CTkFont(size=13),
        )
        self.entry_tarifa.insert(0, "2000")
        self.entry_tarifa.pack(fill="x", padx=20, pady=(0, 12))

        # Botón Registrar Ingreso
        btn_registrar = ctk.CTkButton(
            form_card,
            text="➕ Registrar Ingreso",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#10B981",
            hover_color="#059669",
            height=36,
            command=self.registrar_vehiculo,
        )
        btn_registrar.pack(fill="x", padx=20, pady=(0, 6))

        # Botón Limpiar Campos
        btn_limpiar = ctk.CTkButton(
            form_card,
            text="🧹 Limpiar Formulario",
            font=ctk.CTkFont(size=12),
            fg_color="#374151",
            hover_color="#4B5563",
            height=28,
            command=self.limpiar_formulario,
        )
        btn_limpiar.pack(fill="x", padx=20, pady=(0, 10))

        # Separador decorativo
        separador = ctk.CTkFrame(form_card, height=2, fg_color="#333333")
        separador.pack(fill="x", padx=20, pady=(4, 10))

        # ------------------- SECCIÓN DE LIQUIDACIÓN Y SALIDA -------------------
        lbl_cobro_titulo = ctk.CTkLabel(
            form_card,
            text="Liquidación y Salida",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#F59E0B",
        )
        lbl_cobro_titulo.pack(anchor="w", padx=20, pady=(0, 4))

        lbl_desc_cobro = ctk.CTkLabel(
            form_card,
            text="Selecciona un vehículo en la tabla y haz clic en el botón para calcular el tiempo transcurrido y monto a cobrar.",
            font=ctk.CTkFont(size=11),
            text_color="#9CA3AF",
            wraplength=300,
            justify="left",
        )
        lbl_desc_cobro.pack(anchor="w", padx=20, pady=(0, 10))

        # Botón principal de Cobro y Salida
        self.btn_cobrar = ctk.CTkButton(
            form_card,
            text="💰 Registrar Salida / Cobrar",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#D97706",
            hover_color="#B45309",
            height=42,
            command=self.registrar_salida_y_cobrar,
        )
        self.btn_cobrar.pack(fill="x", padx=20, pady=(0, 10))

        # Tarjeta de resumen de ocupación y recaudos
        self.lbl_resumen = ctk.CTkLabel(
            form_card,
            text="Total: 0 | Autos: 0 | Motos: 0 | Camionetas: 0",
            font=ctk.CTkFont(size=11),
            text_color="#93C5FD",
            justify="center",
        )
        self.lbl_resumen.pack(side="bottom", pady=(0, 6))

        self.lbl_total_recaudado = ctk.CTkLabel(
            form_card,
            text="💵 Recaudado en sesión: $0 COP",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#34D399",
            justify="center",
        )
        self.lbl_total_recaudado.pack(side="bottom", pady=(0, 2))

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
            text="Vehículos en Parqueadero",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        )
        lbl_titulo_tabla.grid(row=0, column=0, sticky="w")

        # Campo de búsqueda en vivo
        self.entry_buscar = ctk.CTkEntry(
            tabla_header,
            placeholder_text="🔍 Buscar por placa o propietario...",
            width=270,
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

        # Evento de doble clic sobre la tabla para cobro y salida directa
        self.tree.bind("<Double-1>", lambda event: self.registrar_salida_y_cobrar())

    def _al_cambiar_tipo_vehiculo(self, tipo_seleccionado: str):
        """Actualiza sugerencia de tarifa por hora según el tipo de vehículo elegido."""
        tarifa_sugerida = TARIFAS_POR_DEFECTO.get(tipo_seleccionado, 2000.0)
        self.entry_tarifa.delete(0, "end")
        self.entry_tarifa.insert(0, str(int(tarifa_sugerida)))

    def _cargar_datos_demo(self):
        """
        Carga vehículos iniciales con horas de ingreso pasadas (objetos datetime reales)
        para permitir probar inmediatamente el cálculo de cobro por tiempo.
        """
        ahora = datetime.now()
        # Automóvil con 2 horas y 15 minutos transcurridos
        self.vehiculos.append(
            Vehiculo("ABC-123", "Automóvil", "María Gómez", ahora - timedelta(hours=2, minutes=15))
        )
        # Motocicleta con 40 minutos transcurridos (aplica tarifa mínima de 1 hora)
        self.vehiculos.append(
            Vehiculo("XYZ-789", "Motocicleta", "Juan Pérez", ahora - timedelta(minutes=40))
        )
        # Camioneta con 1 hora y 10 minutos transcurridos (aplica hora o fracción: 2 horas)
        self.vehiculos.append(
            Vehiculo("KTM-456", "Camioneta", "Andrea Rojas", ahora - timedelta(hours=1, minutes=10))
        )

    def _obtener_tarifa_configurada(self) -> float:
        """Lee y valida la tarifa por hora ingresada por el usuario."""
        texto_tarifa = self.entry_tarifa.get().strip()
        try:
            tarifa = float(texto_tarifa)
            if tarifa <= 0:
                return 2000.0
            return tarifa
        except ValueError:
            return 2000.0

    # ------------------- OPERACIONES CRUD Y COBRO EN MEMORIA -------------------

    def registrar_vehiculo(self):
        """
        CREAR: Valida los campos ingresados y agrega un nuevo Vehículo a la lista en memoria.
        La hora de ingreso se captura automáticamente como objeto datetime.now().
        """
        placa = self.entry_placa.get().strip().upper()
        propietario = self.entry_propietario.get().strip()
        tipo = self.combo_tipo.get().strip()

        # Validación 1: Campos vacíos
        if not placa or not propietario or not tipo:
            self._mostrar_alerta(
                "Campos requeridos",
                "Por favor complete todos los campos obligatorios (Placa, Propietario y Tipo).",
                icono="warning",
            )
            return

        # Validación 2: Placa duplicada activa en parqueadero
        if any(v.placa == placa for v in self.vehiculos):
            self._mostrar_alerta(
                "Vehículo ya registrado",
                f"El vehículo con placa '{placa}' ya se encuentra dentro del parqueadero.",
                icono="cancel",
            )
            return

        # Creación del objeto Vehiculo (hora_ingreso toma datetime.now())
        nuevo_vehiculo = Vehiculo(placa=placa, tipo_vehiculo=tipo, propietario=propietario)
        self.vehiculos.append(nuevo_vehiculo)

        # Actualización de interfaz
        self.actualizar_tabla()
        self.limpiar_formulario()

        self._mostrar_alerta(
            "Ingreso Registrado",
            f"Vehículo: {nuevo_vehiculo.placa} ({nuevo_vehiculo.tipo_vehiculo})\n"
            f"Propietario: {nuevo_vehiculo.propietario}\n"
            f"Hora de Ingreso: {nuevo_vehiculo.hora_ingreso_str()}",
            icono="check",
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

            # Insertar fila en el Treeview con la hora formateada
            self.tree.insert(
                "",
                "end",
                values=(v.placa, v.tipo_vehiculo, v.propietario, v.hora_ingreso_str()),
            )

        # Actualizar tarjeta de resumen
        self.lbl_resumen.configure(
            text=f"Total: {total} | Autos: {autos} | Motos: {motos} | Camionetas: {camionetas}"
        )
        self.lbl_total_recaudado.configure(
            text=f"💵 Recaudado en sesión: ${self.total_recaudado:,.0f} COP"
        )

    def registrar_salida_y_cobrar(self):
        """
        ELIMINAR / COBRO: Selecciona un vehículo de la tabla (o busca por placa),
        calcula la diferencia de tiempo entre el ingreso y el momento actual,
        calcula el total a pagar según la tarifa horaria configurable (hora o fracción con mínimo 1 hora),
        muestra un mensaje emergente de resumen de cobro y solicita confirmación antes de retirarlo.
        """
        seleccion = self.tree.selection()
        vehiculo_a_cobrar: Vehiculo | None = None

        if seleccion:
            item_id = seleccion[0]
            valores = self.tree.item(item_id, "values")
            placa_seleccionada = valores[0]
            vehiculo_a_cobrar = next((v for v in self.vehiculos if v.placa == placa_seleccionada), None)
        else:
            # Si no hay fila seleccionada, intentar con la placa ingresada en el campo de texto
            placa_input = self.entry_placa.get().strip().upper()
            if placa_input:
                vehiculo_a_cobrar = next((v for v in self.vehiculos if v.placa == placa_input), None)

        if not vehiculo_a_cobrar:
            self._mostrar_alerta(
                "Selección Requerida",
                "Por favor selecciona un vehículo de la tabla para calcular el cobro y dar salida.",
                icono="warning",
            )
            return

        # Obtener tarifa por hora configurada
        tarifa_hora = self._obtener_tarifa_configurada()

        # Calcular liquidación en el modelo
        liquidacion = vehiculo_a_cobrar.calcular_cobro(tarifa_por_hora=tarifa_hora)

        # Formato de mensaje resumen de cobro
        mensaje_resumen = (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"       RESUMEN DE LIQUIDACIÓN Y COBRO\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚗 Placa: {liquidacion['placa']}\n"
            f"📋 Tipo: {liquidacion['tipo_vehiculo']}\n"
            f"👤 Propietario: {liquidacion['propietario']}\n\n"
            f"📥 Hora de Ingreso:  {liquidacion['hora_ingreso_str']}\n"
            f"📤 Hora de Salida:   {liquidacion['hora_salida_str']}\n"
            f"⏱️ Tiempo Estacionado: {liquidacion['tiempo_transcurrido_str']}\n\n"
            f"⏳ Horas a Cobrar:   {liquidacion['horas_cobradas']} hora(s) (hora o fracción)\n"
            f"💵 Tarifa Aplicada:   ${liquidacion['tarifa_por_hora']:,.0f} COP / hora\n"
            f"──────────────────────────────────\n"
            f"💰 TOTAL A PAGAR:    ${liquidacion['total_a_pagar']:,.0f} COP\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"¿Desea confirmar el pago y registrar la salida del vehículo?"
        )

        # Mostrar mensaje emergente de confirmación (usando CTkMessagebox si está disponible)
        confirmado = self._mostrar_confirmacion("Confirmar Cobro y Salida", mensaje_resumen)

        if confirmado:
            # Retirar de la lista en memoria
            self.vehiculos.remove(vehiculo_a_cobrar)
            self.total_recaudado += liquidacion["total_a_pagar"]
            self.actualizar_tabla()

            self._mostrar_alerta(
                "Salida Exitosa",
                f"Vehículo con placa {liquidacion['placa']} ha salido del parqueadero.\n\n"
                f"Pago recibido: ${liquidacion['total_a_pagar']:,.0f} COP",
                icono="check",
            )

    def _mostrar_alerta(self, titulo: str, mensaje: str, icono: str = "info"):
        """Muestra una alerta usando CTkMessagebox con fallback a messagebox."""
        if CTkMessagebox:
            # Mapeo de iconos para CTkMessagebox: "check", "cancel", "info", "warning"
            CTkMessagebox(title=titulo, message=mensaje, icon=icono)
        else:
            if icono == "warning":
                messagebox.showwarning(titulo, mensaje)
            elif icono == "cancel":
                messagebox.showerror(titulo, mensaje)
            else:
                messagebox.showinfo(titulo, mensaje)

    def _mostrar_confirmacion(self, titulo: str, mensaje: str) -> bool:
        """Muestra diálogo modal de confirmación y retorna True si el usuario acepta."""
        if CTkMessagebox:
            msg = CTkMessagebox(
                title=titulo,
                message=mensaje,
                icon="question",
                option_1="Cancelar",
                option_2="Confirmar Salida",
            )
            return msg.get() == "Confirmar Salida"
        else:
            return messagebox.askyesno(titulo, mensaje)

    def limpiar_formulario(self):
        """Limpia los campos del formulario de registro."""
        self.entry_placa.delete(0, "end")
        self.entry_propietario.delete(0, "end")
        self.combo_tipo.set("Automóvil")
        self._al_cambiar_tipo_vehiculo("Automóvil")
        self.entry_placa.focus()


if __name__ == "__main__":
    app = SistemaParqueaderoApp()
    app.mainloop()
