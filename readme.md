# Sistema de Gestión y Cobro de Parqueadero

Aplicación de escritorio moderna desarrollada en Python con **CustomTkinter** y **ttk.Treeview**, implementando un CRUD en memoria con **cálculo automático de cobro por tiempo transcurrido (hora o fracción)**.

## 📁 Estructura del Proyecto

```text
app_parqueadero/
│
├── modelo.py           # Clase Vehiculo con objeto datetime y método de cálculo de cobro
├── main.py             # Interfaz gráfica moderna con CTkMessagebox y gestión de cobro
├── requirements.txt    # Dependencias del proyecto (customtkinter, CTkMessagebox)
└── README.md           # Documentación y guía de uso
```

## 🚀 Requisitos e Instalación

1. Asegúrate de tener Python 3.10 o superior instalado.
2. Instalar dependencias en el entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 💻 Ejecución

Para iniciar la aplicación:

```powershell
.\.venv\Scripts\python.exe main.py
```

## ✨ Nuevas Funcionalidades de Cobro y CRUD

1. **Objeto `datetime` en `hora_ingreso`**:
   - Cada vehículo almacena directamente un objeto `datetime` al registrarse (`datetime.now()`).
2. **Cálculo de Cobro por Tiempo**:
   - Calcula con exactitud la diferencia entre la hora de ingreso y la hora de salida.
   - **Regla de cobro**:
     - Si pasan menos de 60 minutos, se cobra la tarifa mínima de 1 hora.
     - Si supera la hora, se cobra por cada hora o fracción adicional (`math.ceil`).
   - Tarifa por hora configurable desde la interfaz gráfica (por defecto $2,000 COP, adaptable por tipo de vehículo o valor personalizado).
3. **Botón "Registrar Salida / Cobrar" con Resumen Emergente**:
   - Al seleccionar cualquier vehículo de la tabla (o hacer doble clic sobre él), se calcula automáticamente el tiempo y monto.
   - Muestra un cuadro de diálogo emergente (`CTkMessagebox`) con el resumen de liquidación detallado (placa, tipo, horas cobradas, tarifa y total a pagar).
   - Solo tras la confirmación del usuario se procede a registrar la salida y eliminar el vehículo de la lista en memoria.
4. **Contador de Recaudos**:
   - Muestra en tiempo real el total de dinero recaudado en la sesión activa.
