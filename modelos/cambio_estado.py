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
        """Método de clase para crear un nuevo cambio de estado"""
        print(f"-> CambioEstado: Creando nueva instancia (vía método de clase) para el estado '{estado.nombre}'")
        return cls(estado)

    def esEstadoActual(self) -> bool:
        """Verifica si este es el estado actual (sin fecha de fin)"""
        resultado = self.fechaHoraFin is None
        print(f"-> CambioEstado: esEstadoActual() = {resultado}")
        return resultado

    def esPendienteDeRevision(self) -> bool:
        """Verifica si el estado es 'Pendiente de Revisión'"""
        resultado = self.actual.esPendienteDeRevision()
        print(f"-> CambioEstado: esPendienteDeRevision() = {resultado}")
        
        # verificar si es del ambito
        if resultado:
            self.esDelAmbito()
        
        return resultado

    def esDelAmbito(self) -> bool:
        """Verifica si el cambio de estado es del ámbito correcto"""
        print("-> CambioEstado: Verificando esDelAmbito()")
        resultado = self.actual.esAmbitoEventoSismico()
        print(f"-> CambioEstado: esDelAmbito() = {resultado}")
        return resultado

    def esAutoDetectado(self) -> bool:
        """Verifica si el estado es 'Auto-Detectado'"""
        resultado = self.actual.esAutoDetectado()
        print(f"-> CambioEstado: esAutoDetectado() = {resultado}")
        return resultado

    def setFechHoraFin(self):
        """Establece la fecha y hora de fin del estado"""
        self.fechaHoraFin = datetime.now()
        print(f"-> CambioEstado: Establecida FechaHoraFin a {self.fechaHoraFin}")

    def getNombreEstado(self) -> str:
        """Obtiene el nombre del estado actual"""
        return self.actual.nombre