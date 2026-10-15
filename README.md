# Sistema de Gestión de Parqueadero

Aplicación de escritorio moderna desarrollada en Python con **CustomTkinter** y **ttk.Treeview**, implementando un CRUD en memoria para la administración de vehículos en un parqueadero.

## 📁 Estructura del Proyecto

```text
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
