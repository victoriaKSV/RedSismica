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
        """
        CORRECCIÓN: Verifica si este es el estado actual (sin fecha de fin)
        SEGÚN ANOTACIONES PDF: "Con el método esEstadoActual() en CambioEstado verificamos 
        si ese estado está vigente (osea si fechaHoraFin esta en None)"
        """
        resultado = self.fechaHoraFin is None
        print(f"-> CambioEstado: esEstadoActual() = {resultado} (fechaHoraFin: {self.fechaHoraFin})")
        return resultado

    def esAutoDetectado(self) -> bool:
        """
        CORRECCIÓN: Verifica si el estado es 'Auto-Detectado'
        SEGÚN DIAGRAMA: estadoActual:CambioEstado → actual:Estado: esAutoDetectado()
        """
        print(f"-> CambioEstado: Delegando esAutoDetectado() al Estado")
        resultado = self.actual.esAutoDetectado()
        print(f"-> CambioEstado: esAutoDetectado() = {resultado}")
        return resultado

    def esPendienteDeRevision(self) -> bool:
        """
        CORRECCIÓN: Verifica si el estado es 'Pendiente de Revisión'
        SEGÚN DIAGRAMA: estadoActual:CambioEstado → actual:Estado: esPendienteDeRevision()
        SEGÚN ANOTACIONES PDF: "CambioEstado delega a su Estado para que compare su nombreEstado"
        """
        print(f"-> CambioEstado: Delegando esPendienteDeRevision() al Estado")
        resultado = self.actual.esPendienteDeRevision()
        print(f"-> CambioEstado: esPendienteDeRevision() = {resultado}")
        
        # SEGÚN DIAGRAMA: si es PendienteDeRevision, verificar el ámbito
        if resultado:
            print(f"-> CambioEstado: Es PendienteDeRevision, verificando ámbito...")
            self.esDelAmbito()
        
        return resultado

    def esDelAmbito(self) -> bool:
        """
        CORRECCIÓN: Verifica si el cambio de estado es del ámbito correcto
        SEGÚN DIAGRAMA: estadoActual:CambioEstado → :Estado: esÁmbitoEventoSismico()
        SEGÚN ANOTACIONES PDF: "se consulta el ámbito desde la clase Estado con esÁmbitoEventoSismico()"
        """
        print("-> CambioEstado: esDelAmbito() - Delegando a Estado")
        resultado = self.actual.esAmbitoEventoSismico()
        print(f"-> CambioEstado: esDelAmbito() = {resultado}")
        return resultado

    def setFechHoraFin(self):
        """
        CORRECCIÓN: Establece la fecha y hora de fin del estado
        SEGÚN DIAGRAMA: seleccionado:EventoSismico: → estadoActual:CambioEstado: setFechHoraFin()
        """
        self.fechaHoraFin = datetime.now()
        print(f"-> CambioEstado: setFechHoraFin() establecida a {self.fechaHoraFin}")

    def getNombreEstado(self) -> str:
        """Obtiene el nombre del estado actual"""
        return self.actual.nombre