"""
modelo.py
Módulo que define la estructura y datos de los vehículos para el Sistema de Gestión de Parqueadero.
"""

from datetime import datetime


class Vehiculo:
    """
    Representa un vehículo dentro del sistema de parqueadero.
    """

    def __init__(self, placa: str, tipo_vehiculo: str, propietario: str, hora_ingreso: str | None = None):
        """
        Inicializa una nueva instancia de la clase Vehiculo.

        :param placa: Placa identificadora del vehículo (ej. ABC-123).
        :param tipo_vehiculo: Categoría del vehículo (Automóvil, Motocicleta, Camioneta).
        :param propietario: Nombre completo del propietario o conductor.
        :param hora_ingreso: Fecha y hora de ingreso. Si no se proporciona, se asigna la actual.
        """
        self.placa = placa.strip().upper()
        self.tipo_vehiculo = tipo_vehiculo.strip()
        self.propietario = propietario.strip().title()
        self.hora_ingreso = hora_ingreso or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self) -> str:
        return (
            f"Vehiculo(placa='{self.placa}', tipo='{self.tipo_vehiculo}', "
            f"propietario='{self.propietario}', hora_ingreso='{self.hora_ingreso}')"
        )
