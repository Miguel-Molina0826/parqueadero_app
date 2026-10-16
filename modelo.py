"""
modelo.py
Módulo que define la estructura, datos y lógica de cobro para el Sistema de Gestión de Parqueadero.
"""

from datetime import datetime
import math


# Tarifas por defecto según el tipo de vehículo (COP / hora o fracción)
TARIFAS_POR_DEFECTO: dict[str, float] = {
    "Automóvil": 2000.0,
    "Motocicleta": 1500.0,
    "Camioneta": 2500.0,
}


class Vehiculo:
    """
    Representa un vehículo dentro del sistema de parqueadero.
    """

    def __init__(
        self,
        placa: str,
        tipo_vehiculo: str,
        propietario: str,
        hora_ingreso: datetime | str | None = None,
    ):
        """
        Inicializa una nueva instancia de la clase Vehiculo.

        :param placa: Placa identificadora del vehículo (ej. ABC-123).
        :param tipo_vehiculo: Categoría del vehículo (Automóvil, Motocicleta, Camioneta).
        :param propietario: Nombre completo del propietario o conductor.
        :param hora_ingreso: Objeto datetime con la hora de ingreso. Si es None, se asigna datetime.now().
                             Si es un string en formato '%Y-%m-%d %H:%M:%S', se parsea a datetime.
        """
        self.placa = placa.strip().upper()
        self.tipo_vehiculo = tipo_vehiculo.strip()
        self.propietario = propietario.strip().title()

        # Guardar estrictamente un objeto datetime
        if hora_ingreso is None:
            self.hora_ingreso: datetime = datetime.now()
        elif isinstance(hora_ingreso, datetime):
            self.hora_ingreso = hora_ingreso
        elif isinstance(hora_ingreso, str):
            try:
                self.hora_ingreso = datetime.strptime(hora_ingreso.strip(), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Si viene en otro formato o falla, asignar la hora actual
                self.hora_ingreso = datetime.now()
        else:
            self.hora_ingreso = datetime.now()

    def hora_ingreso_str(self, formato: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Retorna la hora de ingreso formateada como cadena de texto."""
        return self.hora_ingreso.strftime(formato)

    def calcular_cobro(
        self,
        tarifa_por_hora: float | None = None,
        hora_salida: datetime | None = None,
    ) -> dict:
        """
        Calcula la diferencia de tiempo entre la hora de ingreso y la hora de salida,
        aplicando la regla de cobro por hora o fracción (mínimo 1 hora).

        :param tarifa_por_hora: Tarifa configurable por hora. Si es None, se toma la tarifa por defecto del tipo.
        :param hora_salida: Momento de salida. Si es None, se toma datetime.now().
        :return: Diccionario con el desglose detallado del cobro.
        """
        if hora_salida is None:
            hora_salida = datetime.now()

        # Asegurar que la hora de salida no sea anterior a la de ingreso
        if hora_salida < self.hora_ingreso:
            hora_salida = self.hora_ingreso

        diferencia = hora_salida - self.hora_ingreso
        segundos_totales = max(0.0, diferencia.total_seconds())

        # Desglose de tiempo transcurrido
        horas_transcurridas = int(segundos_totales // 3600)
        minutos_restantes = int((segundos_totales % 3600) // 60)
        segundos_restantes = int(segundos_totales % 60)

        # Regla de cobro: mínimo 1 hora completa si son menos de 60 minutos,
        # o redondeo hacia arriba (hora o fracción).
        if segundos_totales <= 3600:
            horas_a_cobrar = 1
        else:
            horas_a_cobrar = math.ceil(segundos_totales / 3600)

        # Determinar la tarifa horaria a aplicar
        if tarifa_por_hora is not None and tarifa_por_hora > 0:
            tarifa_aplicada = float(tarifa_por_hora)
        else:
            tarifa_aplicada = TARIFAS_POR_DEFECTO.get(self.tipo_vehiculo, 2000.0)

        total_a_pagar = horas_a_cobrar * tarifa_aplicada

        tiempo_str = f"{horas_transcurridas}h {minutos_restantes}m {segundos_restantes}s"

        return {
            "placa": self.placa,
            "tipo_vehiculo": self.tipo_vehiculo,
            "propietario": self.propietario,
            "hora_ingreso": self.hora_ingreso,
            "hora_salida": hora_salida,
            "hora_ingreso_str": self.hora_ingreso.strftime("%Y-%m-%d %H:%M:%S"),
            "hora_salida_str": hora_salida.strftime("%Y-%m-%d %H:%M:%S"),
            "segundos_totales": segundos_totales,
            "tiempo_transcurrido_str": tiempo_str,
            "horas_transcurridas": horas_transcurridas,
            "minutos_restantes": minutos_restantes,
            "horas_cobradas": horas_a_cobrar,
            "tarifa_por_hora": tarifa_aplicada,
            "total_a_pagar": total_a_pagar,
        }

    def __repr__(self) -> str:
        return (
            f"Vehiculo(placa='{self.placa}', tipo='{self.tipo_vehiculo}', "
            f"propietario='{self.propietario}', hora_ingreso='{self.hora_ingreso_str()}')"
        )
