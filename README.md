<<<<<<< HEAD
# Sistema de Gestión de Parqueadero

Aplicación de escritorio moderna desarrollada en Python con **CustomTkinter** y **ttk.Treeview**, implementando un CRUD en memoria para la administración de vehículos en un parqueadero.
=======
# Sistema de Gestión de Parqueadero (JavaFX + Maven)

Aplicación de escritorio moderna desarrollada en **JavaFX 17** y **Maven**, diseñada bajo el patrón de arquitectura **MVC (Modelo - Vista - Controlador)** para la gestión y control de acceso de vehículos en un parqueadero. El almacenamiento y manipulación de datos se gestiona en memoria utilizando un `ArrayList<Vehiculo>`.

---

## 📸 Características Principales

- **Gestión CRUD Completa en Memoria (`ArrayList<Vehiculo>`)**:
  - **Crear (Registrar)**: Ingreso de nuevos vehículos con validación de campos obligatorios y prevención de placas duplicadas.
  - **Leer (Listar)**: Visualización en tiempo real de todos los vehículos activos dentro de una `TableView`.
  - **Actualizar**: Modificación de propietario, tipo de vehículo y hora de ingreso al seleccionar una fila.
  - **Eliminar (Salida)**: Registro de salida de vehículos con ventana modal de confirmación.
- **Búsqueda y Filtrado en Tiempo Real**: Buscador integrado que filtra automáticamente por placa, propietario o tipo de vehículo conforme se escribe.
- **Diseño UI/UX Profesional**:
  - Formulario lateral estructurado con tarjetas visuales (`card-panel`).
  - Botones con código de color intuitivo (Verde: Guardar, Ámbar: Editar, Rojo: Salida, Gris: Limpiar).
  - Hoja de estilos personalizada (`styles.css`) con paleta moderna *Slate & Indigo*.
  - Contador dinámico de vehículos registrados en el parqueadero.

---
>>>>>>> 41cb4a790d75ce0c5d58c0017ed3a19427da559a

## 📁 Estructura del Proyecto

```text
<<<<<<< HEAD
app_parqueadero/
│
├── modelo.py           # Clase Vehiculo con atributos y constructor
├── main.py             # Interfaz gráfica moderna y lógica del CRUD
├── requirements.txt    # Dependencias del proyecto (customtkinter)
└── README.md           # Documentación y guía de uso
```

## 🚀 Requisitos e Instalación

1. Asegúrate de tener Python 3.10 o superior instalado.
2. Si deseas instalar las dependencias manualmente en tu entorno virtual:

```bash
pip install -r requirements.txt
```

## 💻 Ejecución

Para iniciar la aplicación, ejecuta:

```bash
python main.py
```

O utilizando el entorno virtual del proyecto:

```powershell
.\.venv\Scripts\python.exe main.py
```

## ✨ Funcionalidades Principales

* **CREAR (Registrar)**:
  * Formulario con validación de campos obligatorios.
  * Selector desplegable (ComboBox) para **Automóvil**, **Motocicleta** y **Camioneta**.
  * Captura automática de la fecha y hora exacta de ingreso.
  * Validación contra placas duplicadas activas.
* **LEER (Listar)**:
  * Tabla moderna (`ttk.Treeview`) adaptada al estilo oscuro de CustomTkinter.
  * Buscador en tiempo real por placa o nombre de propietario.
  * Contador con resumen de vehículos totales y desglose por tipo.
* **ELIMINAR (Dar salida)**:
  * Salida seleccionando directamente cualquier fila de la tabla o ingresando la placa.
  * También admite doble clic en cualquier registro para tramitar la salida rápida.
  * Diálogo de confirmación antes de eliminar el registro de la memoria.
=======
app.parqueadero/
├── pom.xml
├── README.md
└── src/
    ├── main/
    │   ├── java/
    │   │   └── app/
    │   │       └── parqueadero/
    │   │           ├── controller/
    │   │           │   └── ParqueaderoController.java
    │   │           ├── model/
    │   │           │   └── Vehiculo.java
    │   │           └── Main.java
    │   └── resources/
    │       └── app/
    │           └── parqueadero/
    │               ├── parqueadero-view.fxml
    │               └── styles.css
    └── test/
```

---

## 🛠️ Tecnologías y Requisitos

- **Java Development Kit (JDK)**: Versión 17 o superior.
- **JavaFX**: Versión 17.0.2 (controles y FXML).
- **Apache Maven**: Versión 3.8+ (o el Maven integrado en IntelliJ IDEA).

---

## 🚀 Comandos Maven para Compilar y Ejecutar

### 1. Compilar el proyecto
Descarga las dependencias necesarias y compila el código fuente:
```bash
mvn clean compile
```

### 2. Ejecutar la aplicación
Inicia la interfaz gráfica mediante el plugin oficial de JavaFX:
```bash
mvn javafx:run
```

### 3. Empaquetar la aplicación
Genera el artefacto JAR en la carpeta `target/`:
```bash
mvn clean package
```

---

## 💻 Ejecución desde IntelliJ IDEA

1. Abre la carpeta del proyecto `app.parqueadero` en **IntelliJ IDEA**.
2. Espera a que Maven sincronice las dependencias del archivo `pom.xml`.
3. Navega a `src/main/java/app/parqueadero/Main.java`.
4. Haz clic derecho sobre el archivo o presiona el botón verde de **Run** (`Shift + F10`) para iniciar la aplicación.

---

## 📋 Descripción de los Archivos Clave

| Archivo | Rol | Descripción |
| :--- | :--- | :--- |
| `Vehiculo.java` | **Modelo** | Entidad con los atributos `placa`, `tipoVehiculo`, `propietario` y `horaIngreso`, constructores, getters y setters. |
| `ParqueaderoController.java` | **Controlador** | Administra el `ArrayList<Vehiculo>` en memoria, la lógica CRUD, validaciones y la sincronización con la `TableView`. |
| `Main.java` | **Lanzador** | Clase principal que extiende de `Application`, carga la vista FXML y aplica la hoja de estilos CSS. |
| `parqueadero-view.fxml` | **Vista** | Diseño declarativo en XML con cabecera, formulario lateral, botones de acción y tabla central. |
| `styles.css` | **Estilos** | Hoja de estilos con diseño contemporáneo, efectos hover y focus para todos los controles. |
>>>>>>> 41cb4a790d75ce0c5d58c0017ed3a19427da559a
