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

## 📁 Estructura del Proyecto

```text
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
