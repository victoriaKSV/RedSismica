# modelos/cambio_estado.py

from datetime import datetime
from .estado import Estado

class CambioEstado:
    def __init__(self, estado: Estado):
        self.fechaHoraInicio = datetime.now()
        self.fechaHoraFin = None
        self.actual = estado
        print(f"-> Creada instancia de CambioEstado para el estado '{estado.nombre}'")

    @classmethod
    def crearCambioEstado(cls, estado: Estado):
        print(f"-> CambioEstado: Creando nueva instancia (vía método de clase) para el estado '{estado.nombre}'")
        return cls(estado)

    def esEstadoActual(self) -> bool:
        return self.fechaHoraFin is None

    def esPendienteDeRevision(self) -> bool:
        return self.actual.esPendienteDeRevision()

    def esAutoDetectado(self) -> bool:
        return self.actual.esAutoDetectado()

    def setFechHoraFin(self):
        self.fechaHoraFin = datetime.now()
        print(f"-> CambioEstado: Establecida FechaHoraFin a {self.fechaHoraFin}")